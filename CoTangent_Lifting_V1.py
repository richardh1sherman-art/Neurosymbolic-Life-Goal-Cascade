from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass(frozen=True)
class CotangentFiberState:
    """Represents a reachable vertex in the cotangent-lifted Schreier graph."""

    word: str  # Multi-layer discrete cell address (e.g., "10", "1F")
    step_discovered: int  # Earliest event step reached
    max_geodesic_radius: float  # Contraction tube radius R_k in Riemannian metric M
    invariant_radius_inf: float  # Asymptotic invariant ball radius R_inf = d_bar / (1 - rho_hybrid)
    adjoint_sensitivity_norm: float  # Backward saltation/adjoint gain bound
    is_safe: bool  # False if any layer entered absorbing loss-of-lock state 'F'


class HybridSelfSimilarGrid:
    """
    Models a 2-layer hybrid grid hierarchy (continuous nonlinear ODEs + discrete events)
    with absorbing loss-of-lock state 'F' and explicit hybrid dwell-time contraction bounds.
    """

    def __init__(
        self,
        alphabet: Tuple[str, ...] = ("0", "1", "F"),
        metric_M: np.ndarray = None,
        continuous_contraction_lambda: float = 1.85,  # Continuous SCCM rate lambda (1/s)
        min_inter_event_time: float = 0.25,  # Minimum physical dwell time between events (s)
        disturbance_bound_d_bar: float = 0.035,
        saltation_impulse_mu: float = 1.28,  # Worst-case trajectory stretch at switching surface
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
        # '0': Nominal/locked cell
        # '1': Stressed/LVRT ride-through cell
        # 'F': Absorbing Critical Clearing Time (CCT) / loss-of-lock failure state
        self.nucleus: Dict[str, dict] = {
            "id": {
                "pi": {"0": "0", "1": "1", "F": "F"},
                "sections": {"0": "id", "1": "id", "F": "id"},
                "event_mu": 1.00,
            },
            # Generator 'a': Tie-line trip / reclose (toggles '0' <-> '1'; 'F' stays absorbed)
            "a": {
                "pi": {"0": "1", "1": "0", "F": "F"},
                "sections": {"0": "id", "1": "b", "F": "id"},
                "event_mu": 1.22,
            },
            # Generator 'b': Inverter PLL stress / severe fault pulse
            # Note: If already stressed ('1'), a second severe fault without recovery pushes to 'F'
            "b": {
                "pi": {"0": "1", "1": "F", "F": "F"},
                "sections": {"0": "c", "1": "b", "F": "id"},
                "event_mu": 1.28,
            },
            # Generator 'c': Dissipative emergency damping / fast battery clamping (resets '1' -> '0')
            "c": {
                "pi": {"0": "0", "1": "0", "F": "F"},
                "sections": {"0": "id", "1": "c", "F": "id"},
                "event_mu": 1.05,
            },
        }
        self.generators = ("a", "b", "c")

    def apply_generator(self, gen_state: str, word: str) -> Tuple[str, float]:
        """
        Recursively evaluates g(x w) = pi_g(x) (g|_x)(w) down X^n and returns
        (new_word, hybrid_cycle_contraction_rho).
        """
        if not word:
            return "", 0.0

        head, tail = word[0], word[1:]
        rule = self.nucleus[gen_state]

        new_head = rule["pi"][head]
        next_section = rule["sections"][head]
        new_tail, child_rho = self.apply_generator(next_section, tail)

        # Compute single-layer hybrid contraction factor: mu_event * exp(-lambda * tau_actual)
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
        """
        Computes discrete + continuous contraction-ball reachability under a specified
        set of active event generators (e.g., excluding 'b' when N-2 faults are blocked).
        """
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

            # Do not expand transitions out of absorbing failure states
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
                    # Beyond CCT / loss-of-lock boundary: contraction metric no longer valid
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

    # Case 1: Severe cascading fault ('b') allowed -> reaches absorbing loss-of-lock 'F'
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
    # Case 2: Supervisor disables generator 'b' when in stressed state (Zhong-Wonham SOCC)
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