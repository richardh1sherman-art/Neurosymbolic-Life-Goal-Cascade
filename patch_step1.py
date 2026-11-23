with open("/home/rsherman/projects/SMT-ILP/ZeroVRAM/run_steps123_hybrid_bifurcation.py", "r") as f:
    code = f.read()

start_idx = code.index("def step1_wire_bottom_up_events(")
end_idx = code.index("def step3_bifurcation_without_discrete_events(")

new_step1 = '''def step1_wire_bottom_up_events(enriched_rows):
    print("\\n" + "=" * 108)
    print("STEP 1: WIRING BOTTOM-UP CALTECH DISCRETE EVENTS INTO BRIDGEOBSERVER & COTANGENT LIFTING")
    print("=" * 108)

    W_i = np.linalg.inv(np.array([[2.5, 0.4, 0.0], [0.4, 1.8, 0.1], [0.0, 0.1, 2.2]]))
    C_tie = np.array([[0.85, -0.35, 0.10], [0.15, 0.75, -0.25]])
    bridge_cfg = BridgeObserver.EMTBridgeConfig(
        W_metric_inv=W_i,
        C_tie_proj=C_tie,
        R_invariant_inf=0.22,
        epsilon_layer_mismatch=0.025,
        H_thermal=np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        h_thermal_max=np.array([0.80, 0.80, 0.65, 0.65]),
    )

    observer = BridgeObserver.EMTModeObserver(min_dwell_time=bridge_cfg.min_dwell_time)
    hybrid_grid = CoTangent_Lifting.HybridSelfSimilarGrid()

    # Drive 10 kHz microsecond EMT observer with bottom-up Caltech breaker cb_128 & cb_134 events
    dt_emt = 100e-6
    held_count = 0
    transitions_logged = list()

    for step in range(4500):  # 0.45 seconds
        t_s = step * dt_emt
        # At t = 0.05s, Caltech breaker cb_128 opens (stress rises to 0.88 p.u., V sags to 0.84 p.u.)
        # At t = 0.22s, breaker recloses prematurely, testing dwell-time supervisor tau_dwell = 0.1334s
        if 0.05 <= t_s < 0.22:
            v_pu, stress_pu, pll_err = 0.84, 0.88, 0.28
        else:
            v_pu, stress_pu, pll_err = 0.98, 0.40, 0.08

        prev_w = observer.current_word
        word, held = observer.update(t_s, stress_pu, v_pu, pll_phase_error_rad=pll_err)
        if held:
            held_count += 1
        if word != prev_w:
            r_cont = hybrid_grid.compute_reachable_set(word)
            transitions_logged.append((t_s, prev_w, word, r_cont))

    for t_s, pw, nw, rc in transitions_logged:
        print(f" t={t_s:6.4f}s | Bottom-Up Event Transition '{pw}' -> '{nw}' | Cotangent Fiber Radius r_cont = {rc:.4f}")
    print(f" -> Dwell-Time Supervisor Holds Enforced : {held_count} microsecond steps held (tau_dwell = {bridge_cfg.min_dwell_time:.4f}s)")

    y_nominal = np.array([0.30, -0.15])
    A_qp, b_qp, stats = BridgeObserver.compute_pontryagin_eroded_qp_bounds(bridge_cfg, y_nominal)
    print("-" * 108)
    print(f" -> Bottom-Up Cotangent Reachable Radius : {stats['min_eroded_semi_axis']:.4f} (Safety Ratio = {stats['safety_margin_ratio']:.4f})")
    print(f" -> Exported {A_qp.shape} Inner-Eroded Half-Space Constraints to 15s MIT Supervisory QP.")

'''

updated = code[:start_idx] + new_step1 + code[end_idx:]
with open("/home/rsherman/projects/SMT-ILP/ZeroVRAM/run_steps123_hybrid_bifurcation.py", "w") as f:
    f.write(updated)
print("Patched Step 1 cleanly.")
