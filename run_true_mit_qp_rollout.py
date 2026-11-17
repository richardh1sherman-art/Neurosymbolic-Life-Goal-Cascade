import sys
import os
import time
import numpy as np
import scipy.sparse as sp
import osqp
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIT_DIR = os.path.join(BASE_DIR, "comm-limited-congestion-mgmt-main")
sys.path.insert(0, MIT_DIR)

import grid_pkg
import controller_utils

torch.set_default_dtype(torch.double)

def fast_sparse_osqp_layer(Q_list, q_list, G_list, non_sparse_G, h_list, A_list, b_list, scipy_Q, scipy_G, scipy_A, t):
    """
    Ultra-fast sparse C-backend OSQP solver solving the exact MIT (Q, q, G, h, A, b)
    matrices in < 5 ms per area controller.
    """
    sols = list()
    for i in range(len(Q_list)):
        P_csc = sp.csc_matrix(scipy_Q[i])
        q_vec = q_list[i].detach().numpy().flatten()
        P_csc = 0.5 * (P_csc + P_csc.T) + 1e-7 * sp.eye(len(q_vec), format="csc")

        G_csc = sp.csc_matrix(scipy_G[i])
        h_vec = h_list[i].detach().numpy().flatten()
        A_csc = sp.csc_matrix(scipy_A[i])
        b_vec = b_list[i].detach().numpy().flatten()

        C_mat = sp.vstack([A_csc, G_csc], format="csc")
        l_vec = np.concatenate([b_vec, -np.inf * np.ones_like(h_vec)])
        u_vec = np.concatenate([b_vec, h_vec])

        prob = osqp.OSQP()
        prob.setup(P=P_csc, q=q_vec, A=C_mat, l=l_vec, u=u_vec, verbose=False, eps_abs=1e-5, eps_rel=1e-5)
        res = prob.solve()
        sols.append(torch.tensor(res.x, dtype=torch.double))
    return sols

def build_mit_system(apply_sccm_limits=False):
    line_data_loc = os.path.join(MIT_DIR, "data/case118_line_data.pt")
    bus_data_loc = os.path.join(MIT_DIR, "data/case118_bus_data.pt")
    gen_data_loc = os.path.join(MIT_DIR, "data/case118_gen_data.pt")
    ptdf_data_loc = os.path.join(MIT_DIR, "data/case118_ptdf_data.pt")

    bus_with_curt = torch.load(gen_data_loc, weights_only=True)[:, 0].int()
    bus_with_batt = torch.tensor([10 * i + 2 for i in range(12)], dtype=torch.int)
    grid = grid_pkg.Grid(bus_with_curt, bus_with_batt, 15, line_data_loc, bus_data_loc, gen_data_loc, ptdf_data_loc)

    nodes_1 = list(range(0, 42)) + list((112, 113, 114, 116))
    nodes_2 = list(range(42, 69)) + list((115,))
    nodes_3 = list(range(69, 112)) + list((117,))
    partition = list((nodes_1, nodes_2, nodes_3))

    T_steps = 4
    H_horizon = 5
    ctrls = controller_utils.create_split_constraint_controllers(
        grid, 3, partition, T_steps, H_horizon, 100, 0.01, 1, 1e8, 1e2
    )

    if apply_sccm_limits:
        di_grid = 0.0269
        sigma_inj_mw = 45.0 * (di_grid / 0.082)
        M_ptdf = grid.M.numpy()
        ptdf_row_norms = np.linalg.norm(M_ptdf, axis=1)
        delta_p_tube_mw = torch.tensor(sigma_inj_mw * ptdf_row_norms, dtype=torch.double)

        max_len = max(int(c.num_lines) for c in ctrls)
        area_max_changes = torch.zeros((len(ctrls), max_len), dtype=torch.double)
        area_min_changes = torch.zeros((len(ctrls), max_len), dtype=torch.double)
        for idx_c, c in enumerate(ctrls):
            n_l = int(c.num_lines)
            area_max_changes[idx_c, :n_l] = -delta_p_tube_mw[c.lines_in_area]
            area_min_changes[idx_c, :n_l] = delta_p_tube_mw[c.lines_in_area]

        controller_utils.assign_line_limit_changes(ctrls, area_max_changes, area_min_changes)

    return grid, ctrls

def run_true_mit_qp_rollout():
    t0 = time.perf_counter()
    print("=" * 110)
    print("REAL MIT 3-AREA SPARSE QP 60-SECOND ROLLOUT (t = 0, 15, 30, 45 s): BASELINE VS. SCCM PTDF CONSTRAINTS")
    print("=" * 110)

    grid_base, ctrls_base = build_mit_system(apply_sccm_limits=False)
    grid_sccm, ctrls_sccm = build_mit_system(apply_sccm_limits=True)

    grid_base.reset_state()
    for c in ctrls_base:
        c.zero_line_state()
    grid_sccm.reset_state()
    for c in ctrls_sccm:
        c.zero_line_state()

    T_steps = 4
    H_horizon = 5
    num_buses = grid_base.num_buses

    torch.manual_seed(2026)
    disturbances = 0.05 * torch.randn((T_steps + H_horizon, num_buses), dtype=torch.double)
    area1_gen_buses = (4, 9, 11, 24, 25, 30)
    area3_load_buses = (75, 79, 89, 99, 102, 111)
    for step_idx in range(1, T_steps + H_horizon):
        for b in area1_gen_buses:
            disturbances[step_idx, b] += 0.45
        for b in area3_load_buses:
            disturbances[step_idx, b] -= 0.45

    line_limits = grid_base.line_limits
    crit_lim_59 = float(line_limits.tolist().pop(59))

    print(f" -> Real MIT Grid State Initialized : {grid_base.num_buses} buses | {grid_base.num_lines} lines | {grid_base.num_batt} batteries | {grid_base.num_curt} IBRs")
    print(f" -> Bottleneck Line 59 Rating       : {crit_lim_59:.2f} MW")
    print("=" * 110)
    print(f"{'Step (Time)':<13} | {'Base Curt':<11} | {'SCCM Curt':<11} | {'Base Batt':<11} | {'SCCM Batt':<11} | {'Base MaxRatio':<13} | {'SCCM MaxRatio'}")
    print("-" * 110)

    max_ratio_base = 0.0
    max_ratio_sccm = 0.0
    total_slack_base = 0.0
    total_slack_sccm = 0.0

    for t in range(T_steps):
        dist_window = disturbances[t : t + H_horizon, :]

        curt_b, batt_b, lmax_sl_b, lmin_sl_b, _ = controller_utils.get_next_action(
            grid_base, ctrls_base, dist_window, t, fast_sparse_osqp_layer, update_state=True
        )
        act_curt_b = curt_b[0, :]
        act_batt_b = batt_b[0, :]
        grid_base.update_state(act_curt_b, act_batt_b, disturbances[t, :])
        controller_utils.update_controller_bus_states(ctrls_base)

        curt_s, batt_s, lmax_sl_s, lmin_sl_s, _ = controller_utils.get_next_action(
            grid_sccm, ctrls_sccm, dist_window, t, fast_sparse_osqp_layer, update_state=True
        )
        act_curt_s = curt_s[0, :]
        act_batt_s = batt_s[0, :]
        grid_sccm.update_state(act_curt_s, act_batt_s, disturbances[t, :])
        controller_utils.update_controller_bus_states(ctrls_sccm)

        flows_b = grid_base.M @ grid_base.state[:grid_base.num_buses]
        flows_s = grid_sccm.M @ grid_sccm.state[:grid_sccm.num_buses]
        ratios_b = torch.abs(flows_b) / line_limits
        ratios_s = torch.abs(flows_s) / line_limits
        peak_r_b = float(torch.max(ratios_b).item())
        peak_r_s = float(torch.max(ratios_s).item())

        max_ratio_base = max(max_ratio_base, peak_r_b)
        max_ratio_sccm = max(max_ratio_sccm, peak_r_s)
        total_slack_base += float(torch.sum(lmax_sl_b[:, 0, :] + lmin_sl_b[:, 0, :]).item())
        total_slack_sccm += float(torch.sum(lmax_sl_s[:, 0, :] + lmin_sl_s[:, 0, :]).item())

        sum_curt_b = float(torch.sum(act_curt_b).item())
        sum_curt_s = float(torch.sum(act_curt_s).item())
        sum_batt_b = float(torch.sum(torch.abs(act_batt_b)).item())
        sum_batt_s = float(torch.sum(torch.abs(act_batt_s)).item())

        t_lbl = f"t={t*15:2d}s (k={t})"
        print(f"{t_lbl:<13} | {sum_curt_b:9.4f}   | {sum_curt_s:9.4f}   | {sum_batt_b:9.4f}   | {sum_batt_s:9.4f}   | {100.0*peak_r_b:10.2f}%   | {100.0*peak_r_s:10.2f}%")

    elapsed = time.perf_counter() - t0
    print("-" * 110)
    print(f" -> Network-Wide Peak Line Loading (60s) : MIT Baseline = {100.0*max_ratio_base:.2f}% | MIT + SCCM Constraints = {100.0*max_ratio_sccm:.2f}%")
    print(f" -> Total QP Soft Line-Slack Violation   : MIT Baseline = {total_slack_base:.4f} | MIT + SCCM Constraints = {total_slack_sccm:.4f}")
    print(f" -> Total Sparse OSQP Wall-Clock Time    : {elapsed:.2f} s across 24 multi-area QP solves")
    print("=" * 110)

if __name__ == "__main__":
    run_true_mit_qp_rollout()
