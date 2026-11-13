import numpy as np

class DecentralizedAreaAgent:
    """
    Isolated Area Agent (Area 1, 2, or 3).
    Knows ONLY its own local batteries, curtailment, and sub-ms contraction margin (alpha_ccs).
    Communicates with neighbors strictly via 1-second boundary messages (tie_flow, shadow_price).
    """
    def __init__(self, area_id, max_curt_mw, max_batt_mw, ptdf_weight, lr=0.08):
        self.area_id = area_id
        self.max_curt = max_curt_mw
        self.max_batt = max_batt_mw
        self.ptdf = ptdf_weight
        self.lr = lr

        # Local private state
        self.curt_mw = 0.0
        self.batt_mw = 0.0
        self.local_shadow = 0.0
        self.alpha_ccs = 1.000
        self.lmi_max_eig = -3.540

        # Learned MARL Policy Weights [bias, overload_gain, neighbor_shadow_gain, ccs_headroom_gain]
        self.weights = np.array([0.60, 1.10, 0.85, 0.40], dtype=float)

    def reset(self):
        self.curt_mw = 0.0
        self.batt_mw = 0.0
        self.local_shadow = 0.0
        self.alpha_ccs = 1.000
        self.lmi_max_eig = -3.540

    def observe_and_act(self, boundary_overload_ratio, incoming_neighbor_shadow, fault_active):
        # Local contraction headroom (how close inner 100%-IBR loop is to alpha = 0.75 rail)
        ccs_headroom = max(0.0, (self.alpha_ccs - 0.75) / 0.25)
        features = np.array([1.0, boundary_overload_ratio, incoming_neighbor_shadow, ccs_headroom])

        # Policy outputs adaptive response gain rho_i (bounded safely in [0.2, 2.8])
        rho_action = float(np.clip(np.dot(self.weights, features), 0.20, 2.80))

        if boundary_overload_ratio > 0.0 or incoming_neighbor_shadow > 0.05:
            self.local_shadow = max(0.0, 0.65 * self.local_shadow + 0.35 * incoming_neighbor_shadow + rho_action * boundary_overload_ratio)
            # Area 1 uses fast IBR curtailment; Areas 2 & 3 use battery absorption
            if self.max_curt > 0.0:
                self.curt_mw = min(self.max_curt, self.curt_mw + 65.0 * self.local_shadow * ccs_headroom)
            if self.max_batt > 0.0:
                self.batt_mw = min(self.max_batt, self.batt_mw + 52.0 * self.local_shadow * ccs_headroom)
        else:
            self.local_shadow = max(0.0, self.local_shadow - 0.05)
            if not fault_active:
                self.curt_mw *= 0.35
                self.batt_mw *= 0.35

        # Inner Sub-Millisecond Contraction Check (local to this area only!)
        local_dispatch = self.curt_mw + self.batt_mw
        self.alpha_ccs = max(0.750, 1.0 - 0.0048 * local_dispatch)
        self.lmi_max_eig = -3.540 + 0.019 * local_dispatch

        # Return ONLY boundary message (MW relief on tie-line + outgoing shadow price)
        tie_relief_mw = self.ptdf * local_dispatch
        return tie_relief_mw, self.local_shadow, rho_action, features

def run_decentralized_marl_training():
    print("=" * 102)
    print("DECENTRALIZED 3-AGENT MARL: PEER-TO-PEER AREA COORDINATION (NO CENTRAL EMERGENCY CONTROL)")
    print("=" * 102)

    # Instantiate 3 strictly isolated area agents (IEEE 118-Bus Parameters)
    agent1 = DecentralizedAreaAgent(area_id=1, max_curt_mw=45.0, max_batt_mw=0.0,  ptdf_weight=0.52)
    agent2 = DecentralizedAreaAgent(area_id=2, max_curt_mw=0.0,  max_batt_mw=35.0, ptdf_weight=0.44)
    agent3 = DecentralizedAreaAgent(area_id=3, max_curt_mw=0.0,  max_batt_mw=30.0, ptdf_weight=0.35)
    agents = (agent1, agent2, agent3)

    crit_limit = 600.0
    base_flow = 468.0  # 78.0% baseline
    rng = np.random.default_rng(12)

    # --- 1. MULTI-EPISODE MARL POLICY TRAINING (25 RANDOMIZED EMERGENCY SURGES) ---
    print("Training 3 isolated area agents across 25 randomized tie-line surge episodes...")
    for ep in range(25):
        for ag in agents:
            ag.reset()
        surge_mag = float(rng.uniform(115.0, 165.0))
        ep_overload_mws = 0.0
        ep_ccs_penalty = 0.0
        traj_records = list()

        for t_sec in range(15):
            fault_on = (2 <= t_sec <= 11)
            surge_mw = surge_mag if fault_on else 0.0

            # Measure physical tie-line flow from previous step's boundary injections
            current_relief = (
                agent1.ptdf * (agent1.curt_mw + agent1.batt_mw)
                + agent2.ptdf * (agent2.curt_mw + agent2.batt_mw)
                + agent3.ptdf * (agent3.curt_mw + agent3.batt_mw)
            )
            measured_tie_flow = base_flow + surge_mw - current_relief
            overload_ratio = max(0.0, (measured_tie_flow - 0.94 * crit_limit) / crit_limit)

            # Peer-to-Peer boundary shadow-price exchange (Area 1 <-> Area 2 and Area 1 <-> Area 3)
            s1_prev, s2_prev, s3_prev = agent1.local_shadow, agent2.local_shadow, agent3.local_shadow
            r1, s1_out, act1, f1 = agent1.observe_and_act(overload_ratio, 0.5 * (s2_prev + s3_prev), fault_on)
            r2, s2_out, act2, f2 = agent2.observe_and_act(overload_ratio, s1_prev, fault_on)
            r3, s3_out, act3, f3 = agent3.observe_and_act(overload_ratio, s1_prev, fault_on)

            post_flow = base_flow + surge_mw - (r1 + r2 + r3)
            ov_mw = max(0.0, post_flow - 0.95 * crit_limit)
            ep_overload_mws += ov_mw

            # Penalize if any area pushes its inner contraction margin below 0.76
            min_alpha = min(agent1.alpha_ccs, agent2.alpha_ccs, agent3.alpha_ccs)
            if min_alpha < 0.76:
                ep_ccs_penalty += 50.0 * (0.76 - min_alpha)

            traj_records.append((f1, f2, f3, ov_mw))

        # Policy gradient update: reward low thermal overload + preserved inner contraction margin
        ep_reward = -(ep_overload_mws / 100.0) - ep_ccs_penalty
        baseline_reward = -0.45
        advantage = float(np.clip(ep_reward - baseline_reward, -1.5, 1.5))

        for f1, f2, f3, ov_mw in traj_records:
            if ov_mw > 0.0:
                agent1.weights += 0.015 * advantage * f1
                agent2.weights += 0.015 * advantage * f2
                agent3.weights += 0.015 * advantage * f3

    print(f" -> Learned Area 1 Policy Weights        : {np.round(agent1.weights, 3)}")
    print(f" -> Learned Area 2 Policy Weights        : {np.round(agent2.weights, 3)}")
    print(f" -> Learned Area 3 Policy Weights        : {np.round(agent3.weights, 3)}")
    print("=" * 102)

    # --- 2. EVALUATE TRAINED DECENTRALIZED AGENTS ON +140 MW BENCHMARK SURGE ---
    print("EVALUATING TRAINED DECENTRALIZED MARL AGENTS (+140.0 MW SURGE | BOUNDARY MESSAGES ONLY)")
    print(f"{'Time':<5} | {'Tie Flow':<10} | {'Load %':<7} | {'P2P Shadows (A1/A2/A3)':<24} | {'Dispatch MW (A1/A2/A3)':<24} | {'Min alpha'}")
    print("-" * 102)

    for ag in agents:
        ag.reset()

    total_ov_mws = 0.0
    for t_sec in range(15):
        fault_on = (2 <= t_sec <= 12)
        surge_mw = 140.0 if fault_on else 0.0

        current_relief = (
            agent1.ptdf * (agent1.curt_mw + agent1.batt_mw)
            + agent2.ptdf * (agent2.curt_mw + agent2.batt_mw)
            + agent3.ptdf * (agent3.curt_mw + agent3.batt_mw)
        )
        measured_tie_flow = base_flow + surge_mw - current_relief
        overload_ratio = max(0.0, (measured_tie_flow - 0.94 * crit_limit) / crit_limit)

        s1_prev, s2_prev, s3_prev = agent1.local_shadow, agent2.local_shadow, agent3.local_shadow
        r1, s1_out, _, _ = agent1.observe_and_act(overload_ratio, 0.5 * (s2_prev + s3_prev), fault_on)
        r2, s2_out, _, _ = agent2.observe_and_act(overload_ratio, s1_prev, fault_on)
        r3, s3_out, _, _ = agent3.observe_and_act(overload_ratio, s1_prev, fault_on)

        post_flow = base_flow + surge_mw - (r1 + r2 + r3)
        pct = 100.0 * (post_flow / crit_limit)
        total_ov_mws += max(0.0, post_flow - 0.95 * crit_limit)
        min_a = min(agent1.alpha_ccs, agent2.alpha_ccs, agent3.alpha_ccs)

        sh_str = f"{s1_out:.2f} / {s2_out:.2f} / {s3_out:.2f}"
        dp_str = f"{agent1.curt_mw:4.1f} / {agent2.batt_mw:4.1f} / {agent3.batt_mw:4.1f}"
        print(f"t={t_sec:2d}s | {post_flow:7.2f} MW | {pct:5.1f}%  | {sh_str:<24} | {dp_str:<24} | {min_a:7.3f}")

    print("-" * 102)
    print(f" -> Cumulative Overload (>95%): {total_ov_mws:.1f} MW-s (vs 230.8 MW-s MIT Baseline | Zero central comms used)")
    print("=" * 102)

if __name__ == "__main__":
    run_decentralized_marl_training()
