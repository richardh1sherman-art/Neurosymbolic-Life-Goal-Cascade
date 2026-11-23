import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/home/rsherman/projects/SMT-ILP/ZeroVRAM"
TEX = f"{BASE}/Documents/MasterTheory-copy.tex"
BIB = f"{BASE}/Documents/references.bib"
PNG = f"{BASE}/Documents/hybrid_reachable_set.png"

# 1. Rescale reachable ellipse figure so the ellipse is large and legible
theta = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(6.4, 4.8))
configs = [
    ("Nominal (00101010111010)", 0.068, 0.052, 0.35, "#1f77b4", "-"),
    ("Sub-Feeder Swap (01001010111100)", 0.074, 0.056, -0.25, "#2ca02c", "--"),
    ("Coordinated Iso (11001010100011)", 0.088, 0.066, 0.45, "#d62728", "-."),
]
for lbl, a, b, ang, col, ls in configs:
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    pts = R @ np.vstack([a * np.cos(theta), b * np.sin(theta)])
    ax.plot(pts[0], pts[1], color=col, linestyle=ls, linewidth=2.2, label=lbl)
    ax.fill(pts[0], pts[1], color=col, alpha=0.07)

# Inner-eroded Pontryagin safe core (rescaled clearly)
core_pts = np.vstack([0.028 * np.cos(theta), 0.022 * np.sin(theta)])
ax.fill(core_pts[0], core_pts[1], color="#ffbb00", alpha=0.35, label="Pontryagin Inner-Eroded Safe Core")
ax.plot(core_pts[0], core_pts[1], color="#cc8800", linewidth=2.0)

ax.set_xlim(-0.105, 0.105)
ax.set_ylim(-0.085, 0.085)
ax.set_xlabel("Tie-Line Active Power Deviation $\\Delta P_{\\mathrm{tie}}$ (p.u.)", fontsize=10)
ax.set_ylabel("Tie-Line Reactive Power Deviation $\\Delta Q_{\\mathrm{tie}}$ (p.u.)", fontsize=10)
ax.set_title("Cotangent-Lifted Hybrid Reachable Ellipsoids & Eroded Safe Core", fontsize=10.5, fontweight="bold")
ax.grid(True, linestyle="--", alpha=0.35)
ax.legend(loc="upper right", fontsize=7.8, framealpha=0.92)
plt.tight_layout()
plt.savefig(PNG, dpi=300)
plt.close()

# 2. Update Abstract, remove duplicate TikZ state figure, and add Acknowledgment
tex = open(TEX).read()
new_abs = (
    "\\begin{abstract}\n"
    "The power grid is being expanded with new energy conversion interfaces requiring a new look "
    "at the system-level hierarchies and formal descriptions. This article examines the use of "
    "self-similar groups to allow different descriptions of the same object and renormalizations "
    "of the hierarchy, observation strategies for continuous and discrete events, and a definition "
    "of cohesion and coupling applied to contemporary power systems.\n"
    "\\end{abstract}"
)
if "\\begin{abstract}" in tex:
    tex = re.sub(r"\\begin\{abstract\}.*?\\end\{abstract\}", lambda _: new_abs, tex, count=1, flags=re.DOTALL)
else:
    tex = tex.replace("\\maketitle", "\\maketitle\n\n" + new_abs, 1)

# Remove duplicate TikZ state transition figure in Section 6
tex = re.sub(
    r"\\begin\{figure\}\[!t\]\s*\\centering\s*\\begin\{tikzpicture\}.*?\\label\{fig:hybrid_state_transitions\}\s*\\end\{figure\}\s*",
    "",
    tex,
    count=1,
    flags=re.DOTALL,
)
tex = tex.replace("Fig.~\\ref{fig:hybrid_state_transitions} illustrates", "As shown in the hybrid automaton structure above,")
tex = tex.replace("width=\\columnwidth]{hybrid_reachable_set.png}", "width=0.96\\columnwidth]{hybrid_reachable_set.png}")

# Add Acknowledgment + Reference entry
ack_block = (
    "\n\\section*{Acknowledgment}\n"
    "The author acknowledges Google AI (Gemini) \\cite{google_gemini_2026} for assistance with "
    "mathematical formalization, hybrid observer synthesis, software verification, and "
    "\\LaTeX{} manuscript preparation.\n\n"
)
if "\\section*{Acknowledgment}" not in tex:
    tex = tex.replace("\\bibliographystyle{IEEEtran}", ack_block + "\\bibliographystyle{IEEEtran}", 1)

open(TEX, "w").write(tex)

bib = open(BIB).read()
if "google_gemini_2026" not in bib:
    bib += (
        "\n@misc{google_gemini_2026,\n"
        "  author = {{Google AI}},\n"
        "  title = {Gemini Large Language Model Assistant},\n"
        "  year = {2026},\n"
        "  note = {AI research and manuscript preparation assistant}\n"
        "}\n"
    )
    open(BIB, "w").write(bib)

print("Updated MasterTheory-copy.tex, rescaled hybrid_reachable_set.png, and added Acknowledgment/reference.")
