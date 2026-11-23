# At top of BridgeObserver.py:
from CoTangent_Lifting import diagnose_area_downward
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import numpy as np

from DES_Supervisor import SupervisoryController


@dataclass
class EMTBridgeConfig:
    """Parameters linking the microsecond EMT loop, SCCM metric, and 15s QP."""

    W_metric_inv: np.ndarray  # Dual SCCM metric W_i = M_i^{-1} (n_i x n_i)
    C_tie_proj: np.ndarray  # Tie-line boundary projection matrix C_i (d_i x n_i)
    R_invariant_inf: float  # Invariant geodesic radius R_inf from Schreier graph
    epsilon_layer_mismatch: float  # Inter-layer tracking mismatch bound epsilon_i
    H_thermal: np.ndarray  # Physical tie-line linear limit matrix (m_lin x d_i)
    h_thermal_max: np.ndarray  # Physical tie-line upper limits (m_lin,)
    min_dwell_time: float = 0.1334  # tau_dwell = ln(mu) / lambda (s)


class EMTModeObserver:
    """
    Converts continuous microsecond EMT waveforms into discrete Schreier symbols
    ('0', '1', 'F') and filters controllable transitions through the Ramadge-Wonham
    SupervisoryController so dwell-time bounds (dt > tau_dwell) are strictly enforced.
    """

    def __init__(
        self,
        v_enter_lvrt: float = 0.88,
        v_exit_lvrt: float = 0.92,
        pll_loss_of_lock_rad: float = np.pi / 2.0,
        min_dwell_time: float = 0.1334,
        supervisor: Optional[SupervisoryController] = None,
    ):
        self.v_enter = v_enter_lvrt
        self.v_exit = v_exit_lvrt
        self.pll_limit = pll_loss_of_lock_rad
        self.min_dwell = min_dwell_time

        self.supervisor = supervisor or SupervisoryController(
            continuous_lambda=1.85,
            worst_case_mu=1.28,
        )
        self.supervisor.tau_dwell_min = min_dwell_time

        self.current_word: str = "00"
        self.last_event_time: float = -1e9
        self.event_log: list = []
        self.held_transitions: list = []

    @staticmethod
    def _infer_generator(curr_word: str, candidate_word: str) -> str:
        """Maps a discrete word change to its self-similar group/semigroup generator."""
        if "F" in candidate_word:
            return "b"  # Uncontrollable physical fault into absorbing 'F'
        if candidate_word == "00" and curr_word != "00":
            return "c"  # Irreversible semigroup synchronizing reset to nominal '00'
        return "a"      # Reversible self-similar group mode transition

    def update(
        self,
        t_sec: float,
        area_tieline_stress_pu: float,
        inverter_bus_voltage_pu: float,
        pll_phase_error_rad: float,
        proposed_breaker_states: Optional[Dict[str, str]] = None,
    ) -> Tuple[str, bool]:
        """
        Evaluates threshold crossings at each EMT step and applies SupervisoryController.
        Returns (enforced_2layer_word, transition_was_held_by_supervisor).
        """
        l1_curr, l2_curr = self.current_word[0], self.current_word[1]

        # 1. Determine candidate symbolic word from continuous EMT waveforms
        if abs(pll_phase_error_rad) >= self.pll_limit or inverter_bus_voltage_pu < 0.45:
            candidate_word = "FF"
        else:
            if l1_curr == "0" and area_tieline_stress_pu > 0.85:
                l1_next = "1"
            elif l1_curr == "1" and area_tieline_stress_pu < 0.78:
                l1_next = "0"
            else:
                l1_next = l1_curr

            if l2_curr == "0" and inverter_bus_voltage_pu < self.v_enter:
                l2_next = "1"
            elif l2_curr == "1" and inverter_bus_voltage_pu > self.v_exit:
                l2_next = "0"
            else:
                l2_next = l2_curr

            candidate_word = l1_next + l2_next

        if candidate_word == self.current_word:
            return self.current_word, False

        gen = self._infer_generator(self.current_word, candidate_word)

        # 2. Uncontrollable physical fault ('b' -> 'FF') cannot be blocked by supervisor
        if gen == "b":
            dt_since_last = t_sec - self.last_event_time
            self.event_log.append((t_sec, self.current_word, candidate_word, dt_since_last, "UNCONTROLLABLE_FAULT"))
            self.current_word = candidate_word
            self.last_event_time = t_sec
            self.supervisor.last_switch_time = t_sec
            return self.current_word, False

        # 3. Filter controllable transitions ('a', 'c') through SupervisoryController
        decision = self.supervisor.filter_command(
            t_sec=t_sec,
            current_word=self.current_word,
            proposed_gen=gen,
            next_word=candidate_word,
            next_breaker_states=proposed_breaker_states,
        )

        if not decision.command_accepted:
            self.held_transitions.append((t_sec, self.current_word, candidate_word, decision.reason))
            return self.current_word, True

        dt_since_last = t_sec - self.last_event_time
        self.event_log.append((t_sec, self.current_word, decision.enforced_word, dt_since_last, f"SUPERVISED({gen})"))
        self.current_word = decision.enforced_word
        self.last_event_time = t_sec
        return self.current_word, False
        # Inside EMTModeObserver class in BridgeObserver.py:
    def check_area_alarm_and_diagnose(
        self,
        reachable_states: dict,
        schreier_graph: dict,
        r_safe_threshold: float = 0.22,
    ) -> Optional[dict]:
        """Triggers downward subtree root-cause analysis whenever Area 1 is non-nominal."""
        if self.current_word.startswith(("1", "F")):
            return diagnose_area_downward(
                area_prefix=self.current_word,
                reachable_states=reachable_states,
                schreier_graph=schreier_graph,
                r_safe_threshold=r_safe_threshold,
            )
        return None

def compute_sccm_control(
    x_i: np.ndarray,
    x_star: np.ndarray,
    u_star: np.ndarray,
    theta_hat_i: np.ndarray,
    W_i: np.ndarray,
    Y_gain_func,
) -> np.ndarray:
    """
    Evaluates the closed-form parameter-dependent SCCM controller inside the
    microsecond EMT loop: u_i = u_i* + Y_i(theta_hat) W_i^{-1} (x_i - x_i*).
    """
    delta_x = x_i - x_star
    K_i = Y_gain_func(theta_hat_i) @ np.linalg.inv(W_i)
    return u_star + K_i @ delta_x


def compute_pontryagin_eroded_qp_bounds(
    cfg: EMTBridgeConfig,
    y_nom: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
    """
    Computes the Pontryagin inner erosion (A_lower \\ominus B_epsilon) and extracts
    the tightest eigenvector-aligned inscribed polytope (A_safe @ y <= b_safe)
    for the 15-second upper-level MIT differentiable Quadratic Program.
    """
    d_i = cfg.C_tie_proj.shape[0]

    E_i = cfg.C_tie_proj @ cfg.W_metric_inv @ cfg.C_tie_proj.T
    eigvals, Q = np.linalg.eigh(E_i)

    raw_semi_axes = cfg.R_invariant_inf * np.sqrt(np.maximum(eigvals, 0.0))
    eroded_semi_axes = raw_semi_axes - cfg.epsilon_layer_mismatch

    if np.any(eroded_semi_axes <= 0.0):
        raise ValueError(
            f"Pontryagin eroded set is EMPTY! Inter-layer mismatch epsilon ({cfg.epsilon_layer_mismatch:.4f}) "
            f"exceeds minimum projected contraction semi-axis ({np.min(raw_semi_axes):.4f})."
        )

    half_widths = eroded_semi_axes / np.sqrt(d_i)
    A_ellipsoid = np.vstack([Q.T, -Q.T])
    b_ellipsoid = np.concatenate([Q.T @ y_nom + half_widths, -(Q.T @ y_nom) + half_widths])

    row_norms = np.linalg.norm(cfg.H_thermal, axis=1)
    b_thermal_eroded = cfg.h_thermal_max - cfg.epsilon_layer_mismatch * row_norms

    A_safe = np.vstack([cfg.H_thermal, A_ellipsoid])
    b_safe = np.concatenate([b_thermal_eroded, b_ellipsoid])

    diagnostics = {
        "min_raw_semi_axis": float(np.min(raw_semi_axes)),
        "min_eroded_semi_axis": float(np.min(eroded_semi_axes)),
        "safety_margin_ratio": float(np.min(eroded_semi_axes) / np.min(raw_semi_axes)),
    }
    return A_safe, b_safe, diagnostics


if __name__ == "__main__":
    W_i = np.linalg.inv(np.array([[2.5, 0.4, 0.0], [0.4, 1.8, 0.1], [0.0, 0.1, 2.2]]))
    C_tie = np.array([[0.85, -0.35, 0.10], [0.15, 0.75, -0.25]])

    bridge_cfg = EMTBridgeConfig(
        W_metric_inv=W_i,
        C_tie_proj=C_tie,
        R_invariant_inf=0.22,
        epsilon_layer_mismatch=0.025,
        H_thermal=np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]),
        h_thermal_max=np.array([0.80, 0.80, 0.65, 0.65]),
    )

    y_nominal = np.array([0.30, -0.15])
    A_safe, b_safe, stats = compute_pontryagin_eroded_qp_bounds(bridge_cfg, y_nominal)

    print("=== Pontryagin Inner-Eroded QP Constraints (Ready for 15s MIT Optimizer) ===")
    print(f"  Diagnostics: {stats}")
    for idx in range(A_safe.shape[0]):
        print(f"  Row {idx:02d}: {A_safe[idx]} @ y_tie <= {b_safe[idx]:.4f}")

    observer = EMTModeObserver(min_dwell_time=bridge_cfg.min_dwell_time)
    dt_emt = 100e-6  # 100 microsecond EMT step (10 kHz)
    print("\n=== Supervised Microsecond EMT Hybrid Mode Observer Trace ===")
    first_hold_printed = False
    for step in range(4000):  # 0.40 seconds total
        t = step * dt_emt
        v_pu = 0.84 if 0.05 <= t < 0.25 else 0.98
        stress_pu = 0.88 if 0.05 <= t < 0.22 else 0.40
        prev_word = observer.current_word
        word, held = observer.update(t, stress_pu, v_pu, pll_phase_error_rad=0.12)
        if held and not first_hold_printed:
            print(f"  t = {t:.4f} s: Supervisor HELD premature reset '{prev_word}' -> '00' (enforcing tau_dwell = {bridge_cfg.min_dwell_time:.4f}s)")
            first_hold_printed = True
    if word != prev_word:
        dt_actual = observer.event_log[-1][3]
        tag = observer.event_log[-1][4]
        print(f"  t = {t:.4f} s: Transition '{prev_word}' -> '{word}' | dt = {dt_actual:.4f}s | {tag}")
        if word.startswith(("1", "F")):
            print(f"    -> [ALARM] Area 1 non-nominal ('{word}'): invoking downward subtree diagnosis...")