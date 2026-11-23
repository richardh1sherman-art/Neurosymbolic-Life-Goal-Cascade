from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Tuple
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class SubstationState:
    name: str
    word_14bit: str
    regime: str
    step_label: str
    pos_2d: Tuple[float, float]


@dataclass
class HybridReachabilityResult:
    state: SubstationState
    min_dwell_sec: float
    r_k: float
    r_inf: float
    epsilon_conf: float
    E_proj_2d: np.ndarray
    E_eroded_2d: np.ndarray


EVENTS_STATES: Dict[str, SubstationState] = {
    "sub": SubstationState(
        name="Sub-Feeder Swap",
        word_14bit="01001010111100",
        regime="BASE",
        step_label="cb_146/147 Involution",
        pos_2d=(0.0, 2.2),
    ),
    "nom": SubstationState(
        name="Nominal Baseline",
        word_14bit="00101010111010",
        regime="BASE",
        step_label="Steps 03 & 05",
        pos_2d=(4.0, 2.2),
    ),
    "alt": SubstationState(
        name="Alt Bus + Bank",
        word_14bit="01010101011010",
        regime="BASE",
        step_label="Bus Tie + Shunt Bank",
        pos_2d=(4.0, 0.0),
    ),
    "upg": SubstationState(
        name="Upgraded Nominal",
        word_14bit="00101010100010",
        regime="UPGRADED",
        step_label="Steps 06 & 08",
        pos_2d=(8.5, 2.2),
    ),
    "isol": SubstationState(
        name="Coordinated Isolation",
        word_14bit="11001010100011",
        regime="UPGRADED",
        step_label="Step 07: Maint. Window",
        pos_2d=(12.5, 2.2),
    ),
}

EVENTS_TRANSITIONS: List[Tuple[str, str, str, float, float]] = [
    ("nom", "sub", "g_sub (involution)", 1.0, 1.12),
    ("sub", "nom", "g_sub^-1", 1.0, 1.12),
    ("nom", "alt", "g_bus + g_bank (+40s)", 40.0, 1.18),
    ("alt", "nom", "g_bus^-1 (+2690s)", 2690.0, 1.10),
    ("nom", "upg", "g_upgrade (2024-02-01)", 60.0, 1.08),
    ("upg", "isol", "g_isol (+8s)", 8.0, 1.28),
    ("isol", "upg", "Staged Restore (4-step)", 4.0, 1.15),
]


def compute_events_hybrid_reachability(
    lam_sccm: float = 1.85,
    d_bar: float = 0.022,
    r0: float = 0.095,
    alpha_conf: float = 0.01,
) -> Dict[str, HybridReachabilityResult]:
    rng = np.random.default_rng(42)

    mode_W_proj = {
        "nom": np.array([[0.0018, -0.0004], [-0.0004, 0.0024]]),
        "sub": np.array([[0.0021, -0.0005], [-0.0005, 0.0028]]),
        "alt": np.array([[0.0023, -0.0003], [-0.0003, 0.0031]]),
        "upg": np.array([[0.0014, -0.0003], [-0.0003, 0.0019]]),
        "isol": np.array([[0.0036, -0.0009], [-0.0009, 0.0045]]),
    }

    mondrian_q = {}
    for key in EVENTS_STATES:
        scale = 0.009 if key == "isol" else (0.004 if key == "upg" else 0.006)
        cal_scores = rng.exponential(scale=scale, size=400)
        k_idx = int(np.ceil((len(cal_scores) + 1) * (1.0 - alpha_conf))) - 1
        mondrian_q[key] = float(np.sort(cal_scores)[min(k_idx, len(cal_scores) - 1)])

    adj: Dict[str, List[Tuple[str, str, float, float]]] = {k: [] for k in EVENTS_STATES}
    for u, v, g_lbl, dt, mu in EVENTS_TRANSITIONS:
        adj[u].append((v, g_lbl, dt, mu))

    results: Dict[str, HybridReachabilityResult] = {}
    queue = deque([("nom", r0, 1.0)])
    visited = {"nom"}

    while queue:
        curr_key, curr_r, min_dt = queue.popleft()
        st = EVENTS_STATES[curr_key]

        rho_eff = 1.15 * np.exp(-lam_sccm * min(min_dt, 2.0))
        r_inf = d_bar / max(1e-3, (1.0 - rho_eff))
        eps_conf = 0.35 * r_inf + mondrian_q[curr_key]

        W_2d = mode_W_proj[curr_key]
        eigvals, Q = np.linalg.eigh(W_2d)
        raw_axes = (r_inf * 4.5) * np.sqrt(eigvals)
        eroded_axes = np.maximum(0.003, raw_axes - eps_conf)

        E_proj = Q @ np.diag(raw_axes**2) @ Q.T
        E_eroded = Q @ np.diag(eroded_axes**2) @ Q.T

        results[curr_key] = HybridReachabilityResult(
            state=st,
            min_dwell_sec=min_dt,
            r_k=curr_r,
            r_inf=r_inf,
            epsilon_conf=eps_conf,
            E_proj_2d=E_proj,
            E_eroded_2d=E_eroded,
        )

        for nxt_key, _, dt, mu in adj[curr_key]:
            rho_edge = mu * np.exp(-lam_sccm * min(dt, 2.0))
            nxt_r = rho_edge * curr_r + d_bar
            if nxt_key not in visited:
                visited.add(nxt_key)
                queue.append((nxt_key, nxt_r, dt))

    return results
def plot_hybrid_reachable_bundle(results: Dict[str, HybridReachabilityResult], out_path: str):
    fig, (ax_graph, ax_ellipses) = plt.subplots(
        2, 1, figsize=(13, 9.5), gridspec_kw={"height_ratios": [1.05, 1.25]}
    )

    ax_graph.set_title(
        "Tier 1: Discrete Cell-to-Cell Switching Graph (Events.tex 14-Bit Words)",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )
    reverse_pairs = {(u, v) for u, v, _, _, _ in EVENTS_TRANSITIONS}
    for src, dst, g_lbl, dt, mu in EVENTS_TRANSITIONS:
        x1, y1 = EVENTS_STATES[src].pos_2d
        x2, y2 = EVENTS_STATES[dst].pos_2d
        rad = 0.16 if (dst, src) in reverse_pairs else 0.0
        color = (
            "#d95f02"
            if "upgrade" in g_lbl
            else ("#1b9e77" if "isol" in g_lbl or "Restore" in g_lbl else "#386cb0")
        )
        ax_graph.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                lw=1.8,
                color=color,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=28,
                shrinkB=28,
            ),
        )
        mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2) + (0.28 if rad > 0 else -0.25)
        ax_graph.text(
            mx, my, f"{g_lbl}\n(dt={dt:g}s, mu={mu})", fontsize=7.5, ha="center", va="center", color=color
        )

    for key, res in results.items():
        x, y = res.state.pos_2d
        box_color = "#e0f3db" if res.state.regime == "UPGRADED" else "#deebf7"
        edge_color = "#1b9e77" if res.state.regime == "UPGRADED" else "#2b5c8f"
        ax_graph.scatter(
            [x], [y], s=1400, marker="s", facecolor=box_color, edgecolor=edge_color, linewidth=2.0, zorder=4
        )
        ax_graph.text(
            x,
            y,
            f"{res.state.name}\n{res.state.word_14bit}\n[{res.state.step_label}]",
            fontsize=7.5,
            ha="center",
            va="center",
            fontweight="bold",
            zorder=5,
        )

    ax_graph.set_xlim(-1.8, 14.3)
    ax_graph.set_ylim(-0.9, 3.2)
    ax_graph.axis("off")

    ax_ellipses.set_title(
        "Tier 2: Mode-Indexed Continuous (dV, dI) Reachable Ellipses & Pontryagin Inner-Eroded Safe Cores",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )
    palette = {
        "nom": "#2b5c8f",
        "sub": "#6a51a3",
        "alt": "#d95f02",
        "upg": "#1b9e77",
        "isol": "#e7298a",
    }

    for key, res in results.items():
        c_col = palette[key]
        vals_out, vecs_out = np.linalg.eigh(res.E_proj_2d)
        angle = float(np.degrees(np.arctan2(vecs_out[1, 0], vecs_out[0, 0])))
        w_out = float(2.0 * np.sqrt(vals_out[0]))
        h_out = float(2.0 * np.sqrt(vals_out[1]))

        ell_outer = patches.Ellipse(
            (0.0, 0.0),
            width=w_out,
            height=h_out,
            angle=angle,
            facecolor="none",
            edgecolor=c_col,
            linestyle="--",
            linewidth=1.8,
            label=f"{res.state.name} Outer Tube (eps={res.epsilon_conf:.4f})",
        )
        ax_ellipses.add_patch(ell_outer)

        vals_in, _ = np.linalg.eigh(res.E_eroded_2d)
        w_in = float(2.0 * np.sqrt(vals_in[0]))
        h_in = float(2.0 * np.sqrt(vals_in[1]))
        ell_inner = patches.Ellipse(
            (0.0, 0.0),
            width=w_in,
            height=h_in,
            angle=angle,
            facecolor=c_col,
            alpha=0.14,
            edgecolor=c_col,
            linewidth=1.5,
        )
        ax_ellipses.add_patch(ell_inner)

    ax_ellipses.axhline(0, color="gray", lw=0.8, ls=":")
    ax_ellipses.axvline(0, color="gray", lw=0.8, ls=":")
    ax_ellipses.set_xlim(-0.065, 0.065)
    ax_ellipses.set_ylim(-0.075, 0.075)
    ax_ellipses.set_xlabel("Bus Voltage Deviation dV (pu)", fontsize=10)
    ax_ellipses.set_ylabel("Tie-Line Current Deviation dI (pu)", fontsize=10)
    ax_ellipses.grid(True, linestyle="--", alpha=0.35)
    ax_ellipses.legend(loc="upper right", fontsize=8.5, framealpha=0.92)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    print(f"Saved hybrid reachable set visualization to: {out_path}")


if __name__ == "__main__":
    reach_results = compute_events_hybrid_reachability()
    print("=== Events.tex Hybrid Reachability & Pontryagin Safe Core Summary ===")
    for key, res in reach_results.items():
        eig_eroded = np.sqrt(np.linalg.eigvalsh(res.E_eroded_2d))
        print(
            f"  [{res.state.regime:8s}] {res.state.name:21s} ({res.state.word_14bit}) | "
            f"dt_min={res.min_dwell_sec:6.1f}s | eps_conf={res.epsilon_conf:.4f} pu | "
            f"Eroded Safe Semi-Axes=({eig_eroded[0]:.4f}, {eig_eroded[1]:.4f}) pu"
        )
    plot_hybrid_reachable_bundle(reach_results, "hybrid_reachable_set.png")
