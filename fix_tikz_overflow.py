import os

TEX_PATH = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/scale_invariant_hierarchy.tex"
with open(TEX_PATH, "r") as f:
    tex = f.read()

start_idx = tex.index("\\begin{figure*}[!t]")
end_idx = tex.index("\\end{figure*}") + len("\\end{figure*}")

new_tikz = r"""\begin{figure*}[!t]
\centering
\begin{tikzpicture}[
    node distance=0.85cm and 0.9cm,
    box/.style={rectangle, draw=black!80, thick, rounded corners=3pt, align=center, inner sep=5pt, font=\scriptsize},
    l3/.style={box, fill=blue!10, text width=14.2cm},
    l2/.style={box, fill=green!10, text width=6.5cm},
    l1/.style={box, fill=orange!12, text width=6.5cm},
    arr/.style={-{Stealth[length=2.2mm]}, thick}
]
\node[l3] (fleet) {\textbf{Layer 3: Supervisory / Fleet Tier ($\tau_3 = 5\text{ s}$)} --- RG Critical Margin $\Delta P_{\text{crit}} > 0$, $\min (J_{\text{cost}} + \mu J_{\text{disrupt}})$\\[2pt]Compact Attainable Ellipsoid $\mathcal{R}_3(t)$ \& Nekrashevych Discrete-Event Automaton Tree $g(xw) = y\,h(w)$};

\node[l2, below=0.85cm of fleet.south west, anchor=north west] (sq1) {\textbf{Layer 2: Squadron / Area 1 ($\tau_2 = 0.5\text{ s}$)}\\[2pt]Quotient Metric $\bar{M}_2 = \Pi_{\mathcal{G}_1} M_1 \Pi_{\mathcal{G}_1}^\top$ \;|\; Tube $\mathcal{R}_2(t)$};
\node[l2, below=0.85cm of fleet.south east, anchor=north east] (sq2) {\textbf{Layer 2: Squadron / Area 2 ($\tau_2 = 0.5\text{ s}$)}\\[2pt]Quotient Metric $\bar{M}_2 = \Pi_{\mathcal{G}_1} M_1 \Pi_{\mathcal{G}_1}^\top$ \;|\; Tube $\mathcal{R}_2(t)$};

\node[l1, below=0.85cm of sq1] (dr1) {\textbf{Layer 1: Augmented Drone / Device Cluster ($\tau_1 = 10\text{ ms}$)}\\[2pt]$\tilde{x}_{1,i} = [x_{1,i};\, z_{\text{int},i}]$ absorbs $\mathbf{P}_1 \to \tilde{\mathbf{C}}_1$ \;|\; Compact $\mathcal{R}_1(t)$};
\node[l1, below=0.85cm of sq2] (dr2) {\textbf{Layer 1: Augmented Drone / Device Cluster ($\tau_1 = 10\text{ ms}$)}\\[2pt]$\tilde{x}_{1,i} = [x_{1,i};\, z_{\text{int},i}]$ absorbs $\mathbf{P}_1 \to \tilde{\mathbf{C}}_1$ \;|\; Compact $\mathcal{R}_1(t)$};

\draw[arr] (dr1.north) -- node[right, font=\scriptsize] {Reynolds $\Pi_{\mathcal{G}_1}$ \& Schur $\mathcal{R}_2 \subseteq \mathcal{R}_1$} (sq1.south);
\draw[arr] (dr2.north) -- node[right, font=\scriptsize] {Reynolds $\Pi_{\mathcal{G}_1}$ \& Schur $\mathcal{R}_2 \subseteq \mathcal{R}_1$} (sq2.south);
\draw[arr] (sq1.north) -- node[right, font=\scriptsize] {Stroboscopic $\Phi_{T_2}$ ($\epsilon_2 < \epsilon_2^*$)} (fleet.south -| sq1.north);
\draw[arr] (sq2.north) -- node[right, font=\scriptsize] {Stroboscopic $\Phi_{T_2}$ ($\epsilon_2 < \epsilon_2^*$)} (fleet.south -| sq2.north);
\end{tikzpicture}
\caption{Scale-invariant three-tier contraction hierarchy illustrated on a 3-tier Autonomous Drone Swarm (\texttt{Drone -> Squadron -> Fleet}) and isomorphic multi-area grid. State augmentation converts external coupling $\mathbf{P}_1$ into internal cohesion $\tilde{\mathbf{C}}_1$, while Reynolds projection, stroboscopic lifting, and Schur-complement inclusion propagate compactness upward.}
\label{fig:scale_invariant_arch}
\end{figure*}"""

updated = tex[:start_idx] + new_tikz + tex[end_idx:]
with open(TEX_PATH, "w") as f:
    f.write(updated)
print("Fixed TikZ box text widths cleanly.")
