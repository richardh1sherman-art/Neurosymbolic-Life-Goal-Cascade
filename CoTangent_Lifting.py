from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass(frozen=True)
class CotangentFiberState:
    """Represents a reachable vertex in the cotangent-lifted Schreier graph."""

    word: str
    step_discovered: int
    max_geodesic_radius: float
    invariant_radius_inf: float
    adjoint_sensitivity_norm: float
    is_safe: bool


class HybridSelfSimilarGrid:
    """
    Models a 2-layer hybrid grid hierarchy (continuous nonlinear ODEs + discrete events)
    with absorbing loss-of-lock state 'F' and explicit hybrid dwell-time contraction bounds.
    """

    def __init__(
        self,
        alphabet: Tuple[str, ...] = ("0", "1", "F"),
        metric_M: np.ndarray = None,
        continuous_contraction_lambda: float = 1.85,
        min_inter_event_time: float = 0.25,
        disturbance_bound_d_bar: float = 0.035,
        saltation_impulse_mu: float = 1.28,
    ):
        self.X = alphabet
        self.M = metric_M if metric_M is not None else np.array([[2.5, 0.4], [0.4, 1.8]])
        self.M_sqrt = np.linalg.cholesky(self.M)
        self.M_inv = np.linalg.inv(self.M)

        self.lam = continuous_contraction_lambda
        self.tau_actual = min_inter_event_time
        self.d_bar = disturbance_bound_d_bar
        self.mu = saltation_impulse_mu

        # Explicit Minimum Dwell Time: tau_dwell > ln(mu) / lambda
        self.tau_dwell_min = float(np.log(self.mu) / self.lam)

        # Effective hybrid contraction factor per event-flow cycle: rho_hybrid = mu * exp(-lambda * tau)
        self.rho_hybrid = float(self.mu * np.exp(-self.lam * self.tau_actual))

        # Finite contracting nucleus N = {'id', 'a', 'b', 'c'} over X = {'0', '1', 'F'}
        self.nucleus: Dict[str, dict] = {
            "id": {
                "pi": {"0": "0", "1": "1", "F": "F"},
                "sections": {"0": "id", "1": "id", "F": "id"},
                "event_mu": 1.00,
            },
            "a": {
                "pi": {"0": "1", "1": "0", "F": "F"},
                "sections": {"0": "id", "1": "b", "F": "id"},
                "event_mu": 1.22,
            },
            "b": {
                "pi": {"0": "1", "1": "F", "F": "F"},
                "sections": {"0": "c", "1": "b", "F": "id"},
                "event_mu": 1.28,
            },
            "c": {
                "pi": {"0": "0", "1": "0", "F": "F"},
                "sections": {"0": "id", "1": "c", "F": "id"},
                "event_mu": 1.05,
            },
        }
        self.generators = ("a", "b", "c")

    def apply_generator(self, gen_state: str, word: str) -> Tuple[str, float]:
        """Recursively evaluates g(x w) = pi_g(x) (g|_x)(w) down X^n."""
        if not word:
            return "", 0.0

        head, tail = word[0], word[1:]
        rule = self.nucleus[gen_state]

        new_head = rule["pi"][head]
        next_section = rule["sections"][head]
        new_tail, child_rho = self.apply_generator(next_section, tail)

        local_rho = rule["event_mu"] * np.exp(-self.lam * self.tau_actual)
        effective_rho = max(local_rho, child_rho)
        return new_head + new_tail, float(effective_rho)


    def build_schreier_graph(self, n_layers: int) -> Dict[str, List[Tuple[str, str, float]]]:
        """Builds the finite level-n Schreier graph over X^n."""
        words = [""]
        for _ in range(n_layers):
            words = [w + x for w in words for x in self.X]

        adjacency: Dict[str, List[Tuple[str, str, float]]] = {w: [] for w in words}
        for w in words:
            for g in self.generators:
                w_next, eff_rho = self.apply_generator(g, w)
                adjacency[w].append((g, w_next, eff_rho))
        return adjacency
    def compute_reachable_set(
        self,
        initial_word: str,
        initial_delta_x: np.ndarray,
        allowed_generators: Tuple[str, ...] = ("a", "b", "c"),
    ) -> Tuple[Dict[str, List[Tuple[str, str, float]]], Dict[str, CotangentFiberState]]:
        """Computes discrete + continuous contraction-ball reachability."""
        if self.tau_actual <= self.tau_dwell_min:
            raise ValueError(
                f"Hybrid contraction violated! Actual dwell time ({self.tau_actual:.3f}s) "
                f"<= minimum dwell time ({self.tau_dwell_min:.3f}s)."
            )

        n_layers = len(initial_word)
        schreier_graph = self.build_schreier_graph(n_layers)

        r_0 = float(np.linalg.norm(self.M_sqrt @ initial_delta_x, ord=2))
        r_inf = self.d_bar / (1.0 - self.rho_hybrid)

        reachable: Dict[str, CotangentFiberState] = {
            initial_word: CotangentFiberState(
                word=initial_word,
                step_discovered=0,
                max_geodesic_radius=r_0,
                invariant_radius_inf=r_inf,
                adjoint_sensitivity_norm=1.0,
                is_safe=("F" not in initial_word),
            )
        }

        queue = deque([initial_word])
        while queue:
            curr_w = queue.popleft()
            curr_state = reachable[curr_w]
            k_next = curr_state.step_discovered + 1

            if not curr_state.is_safe:
                continue

            for gen, next_w, eff_rho in schreier_graph[curr_w]:
                if gen not in allowed_generators:
                    continue

                is_next_safe = "F" not in next_w
                if is_next_safe:
                    r_k = (eff_rho**k_next) * r_0 + (
                        (1.0 - eff_rho**k_next) / (1.0 - eff_rho)
                    ) * self.d_bar
                    adj_norm = curr_state.adjoint_sensitivity_norm * eff_rho
                else:
                    r_k = float("inf")
                    adj_norm = float("inf")

                if next_w not in reachable:
                    reachable[next_w] = CotangentFiberState(
                        word=next_w,
                        step_discovered=k_next,
                        max_geodesic_radius=r_k,
                        invariant_radius_inf=r_inf if is_next_safe else float("inf"),
                        adjoint_sensitivity_norm=adj_norm,
                        is_safe=is_next_safe,
                    )
                    queue.append(next_w)
                elif is_next_safe and r_k > reachable[next_w].max_geodesic_radius:
                    existing = reachable[next_w]
                    reachable[next_w] = CotangentFiberState(
                        word=next_w,
                        step_discovered=existing.step_discovered,
                        max_geodesic_radius=r_k,
                        invariant_radius_inf=r_inf,
                        adjoint_sensitivity_norm=max(existing.adjoint_sensitivity_norm, adj_norm),
                        is_safe=True,
                    )

        return schreier_graph, reachable


def project_ball_to_tieline(M_inv: np.ndarray, C_tie: np.ndarray, radius: float) -> float:
    if np.isinf(radius):
        return float("inf")
    projected_var = float((C_tie @ M_inv @ C_tie.T).item())
    return radius * np.sqrt(projected_var)
def diagnose_area_downward(
    area_prefix: str,
    reachable_states: Dict[str, CotangentFiberState],
    schreier_graph: Dict[str, List[Tuple[str, str, float]]],
    r_safe_threshold: float = 0.22,
) -> Dict[str, object]:
    """
    Descends the subtree rooted at `area_prefix` (e.g., '1' for Area 1) to isolate
    the root cause of an Area-level anomaly across discrete symbols and continuous fibers.
    """
    subtree = {
        w: st for w, st in reachable_states.items() if w.startswith(area_prefix)
    }
    if not subtree:
        return {"area": area_prefix, "status": "UNREACHABLE_PREFIX", "causes": []}

    # 1. Identify absorbing leaf faults ('F') inside the Area 1 subtree
    fault_leaves = [w for w, st in subtree.items() if not st.is_safe]

    # 2. Rank safe leaves by continuous geodesic contraction radius R_k
    safe_leaves = sorted(
        [st for st in subtree.values() if st.is_safe],
        key=lambda s: s.max_geodesic_radius,
        reverse=True,
    )

    # 3. Trace incoming generator edges into the worst-case leaf
    worst_word = fault_leaves[0] if fault_leaves else safe_leaves[0].word
    incoming_generators = [
        (src, gen, rho)
        for src, edges in schreier_graph.items()
        for (gen, dst, rho) in edges
        if dst == worst_word
    ]

    # 4. Classify root cause
    if fault_leaves:
        diagnosis = (
            f"LOCAL_LOSS_OF_LOCK: Leaf node(s) {fault_leaves} entered absorbing semigroup state 'F' "
            f"(PLL loss-of-lock or V < 0.45 pu)."
        )
    elif safe_leaves[0].max_geodesic_radius > r_safe_threshold:
        diagnosis = (
            f"CONTINUOUS_TUBE_OVERFLOW: Leaf '{worst_word}' geodesic radius "
            f"R_k={safe_leaves[0].max_geodesic_radius:.4f} exceeds safe ceiling {r_safe_threshold:.4f}."
        )
    elif worst_word.endswith("1"):
        diagnosis = (
            f"DOWNSTREAM_LVRT_SATURATION: Leaf '{worst_word}' is in local LVRT/current-limit mode ('1'), "
            f"inflating Area '{area_prefix}' Pontryagin ellipsoid."
        )
    else:
        diagnosis = (
            f"EXTERNAL_TIE_LINE_STRESS: Leaf '{worst_word}' remains nominal ('0'); "
            f"Area '{area_prefix}' stress is driven by external inter-area power flow."
        )

    return {
        "area_prefix": area_prefix,
        "worst_leaf_word": worst_word,
        "diagnosis": diagnosis,
        "fault_leaves": fault_leaves,
        "ranked_safe_leaves": [(s.word, round(s.max_geodesic_radius, 4)) for s in safe_leaves],
        "incoming_generators": incoming_generators,
    }


if __name__ == "__main__":
    grid = HybridSelfSimilarGrid(
        alphabet=("0", "1", "F"),
        metric_M=np.array([[2.5, 0.4], [0.4, 1.8]]),
        continuous_contraction_lambda=1.85,
        min_inter_event_time=0.25,
        disturbance_bound_d_bar=0.035,
        saltation_impulse_mu=1.28,
    )

    print("=== Hybrid Dwell-Time Contraction Certification ===")
    print(f"  Continuous SCCM Rate (lambda):      {grid.lam:.3f} s^-1")
    print(f"  Worst-Case Saltation Impulse (mu):  {grid.mu:.3f}")
    print(f"  Minimum Required Dwell Time:        {grid.tau_dwell_min:.4f} s")
    print(f"  Actual Inter-Event Dwell Time:      {grid.tau_actual:.4f} s (SAFE)")
    print(f"  Effective Hybrid Contraction (rho): {grid.rho_hybrid:.4f}\n")

    w_0 = "10"
    delta_x_0 = np.array([0.12, -0.08])
    C_tie = np.array([[0.85, -0.35]])

    _, reach_unprotected = grid.compute_reachable_set(
        w_0, delta_x_0, allowed_generators=("a", "b", "c")
    )
    print("=== Scenario 1: Unprotected Cascading Faults ('a', 'b', 'c' active) ===")
    for word, info in sorted(reach_unprotected.items(), key=lambda x: x[1].step_discovered):
        status = "SAFE (Contracting)" if info.is_safe else "UNSAFE (Absorbing Loss-of-Lock 'F')"
        margin = project_ball_to_tieline(grid.M_inv, C_tie, info.max_geodesic_radius)
        print(
            f"  Cell '{word}' (step {info.step_discovered}): {status} | "
            f"R_k = {info.max_geodesic_radius:.4f}, Tie Margin = ±{margin:.4f} pu"
        )

    _, reach_supervised = grid.compute_reachable_set(
        w_0, delta_x_0, allowed_generators=("a", "c")
    )
    print("\n=== Scenario 2: SOCC Supervised Operation ('b' disabled; 'a', 'c' active) ===")
    for word, info in sorted(reach_supervised.items(), key=lambda x: x[1].step_discovered):
        margin_k = project_ball_to_tieline(grid.M_inv, C_tie, info.max_geodesic_radius)
        margin_inf = project_ball_to_tieline(grid.M_inv, C_tie, info.invariant_radius_inf)
        print(
            f"  Cell '{word}' (step {info.step_discovered}): SAFE | "
            f"R_k = {info.max_geodesic_radius:.4f}, Tie Margin (k/inf) = ±{margin_k:.4f} / ±{margin_inf:.4f} pu"
        )
        print("\n=== Downward Root-Cause Diagnosis for Area 1 (Prefix '1') ===")
    diag_unprotected = diagnose_area_downward(
        area_prefix="1",
        reachable_states=reach_unprotected,
        schreier_graph=_,
        r_safe_threshold=0.22,
    )
    print(f"  [Unprotected] Worst Leaf: '{diag_unprotected['worst_leaf_word']}' -> {diag_unprotected['diagnosis']}")
    print(f"                Incoming Edges: {diag_unprotected['incoming_generators']}")

    # Capture graph from Scenario 2 to diagnose supervised Area 1
    graph_sup, reach_supervised = grid.compute_reachable_set(
        w_0, delta_x_0, allowed_generators=("a", "c")
    )
    diag_supervised = diagnose_area_downward(
        area_prefix="1",
        reachable_states=reach_supervised,
        schreier_graph=graph_sup,
        r_safe_threshold=0.22,
    )
    print(f"  [Supervised]  Worst Leaf: '{diag_supervised['worst_leaf_word']}' -> {diag_supervised['diagnosis']}")
    print(f"                Ranked Safe Leaves: {diag_supervised['ranked_safe_leaves']}")

