TEX_PATH = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Documents/microgrid_smart_grid_tsg-v2.tex"
with open(TEX_PATH, "r") as f:
    tex = f.read()

tikz_caltech = r"""
\begin{figure*}[t]
\centering
\resizebox{0.94\textwidth}{!}{%
\begin{tikzpicture}[
    font=\sffamily\scriptsize,
    mbus/.style={draw=red!85!black, line width=1.8pt},
    ubus/.style={draw=black, line width=1.6pt},
    wire/.style={draw=black, line width=0.65pt},
    xfmr/.pic={
        \draw[wire, fill=white] (0, 0.13) circle (0.16);
        \draw[wire, fill=white] (0,-0.13) circle (0.16);
        \node[font=\tiny] at (0, 0.13) {$\triangle$};
        \node[font=\tiny] at (0,-0.13) {$\mathrm{Y}$};
    },
    tie/.pic={
        \draw[wire] (-0.22,0) -- (-0.09,0) arc[start angle=180, end angle=0, radius=0.09] -- (0.22,0);
    }
]
% Voltage tier left labels
\fill[gray!35] (-0.75, 4.75) rectangle (-0.25, 6.15);
\node[rotate=90, font=\sffamily\bfseries\scriptsize] at (-0.50, 5.45) {16.5 kV};
\fill[gray!45] (-0.75, 2.05) rectangle (-0.25, 4.65);
\node[rotate=90, font=\sffamily\bfseries\scriptsize] at (-0.50, 3.35) {2.4 kV};
\fill[gray!35] (-0.75,-0.55) rectangle (-0.25, 1.95);
\node[rotate=90, font=\sffamily\bfseries\scriptsize] at (-0.50, 0.70) {480 V};

% Shaded A Side & B Side regions
\fill[orange!18] (-0.15, 4.75) rectangle (5.35, 6.15);
\fill[orange!14] (-0.15, 2.05) rectangle (5.35, 4.65);
\fill[orange!18] (-0.15,-0.55) rectangle (5.35, 1.95);
\node[font=\sffamily\bfseries\small, anchor=west] at (0.05, 5.85) {A Side};

\fill[teal!14] (6.15, 4.75) rectangle (8.75, 6.15);
\fill[teal!12] (6.15, 2.05) rectangle (14.45, 4.65);
\fill[teal!14] (6.15,-0.55) rectangle (14.45, 1.95);
\node[font=\sffamily\bfseries\small, anchor=west] at (6.30, 5.85) {B Side};

% Legend (Top Right)
\pic at (9.35, 5.85) {tie}; \node[anchor=west] at (9.65, 5.85) {Tie breaker};
\draw[ubus] (9.12, 5.42) -- (9.62, 5.42); \node[anchor=west] at (9.68, 5.42) {Bus (unmeasured)};
\pic[scale=0.72] at (12.15, 5.85) {xfmr}; \node[anchor=west] at (12.40, 5.85) {Transformer};
\draw[mbus] (11.92, 5.42) -- (12.42, 5.42); \node[anchor=west] at (12.48, 5.42) {Bus (measured)};

% ================= A SIDE =================
\draw[mbus] (2.95, 5.75) -- (3.75, 5.75) node[midway, above=1pt] {1033};
\draw[wire] (3.35, 5.75) -- (3.35, 5.42);
\pic at (3.35, 5.13) {xfmr};
\draw[wire] (3.35, 4.84) -- (3.35, 4.25);

\draw[mbus] (2.45, 4.25) -- (4.35, 4.25);
\node[above=1pt] at (2.35, 4.25) {1034};

% A Side 2.4 kV branches
\draw[wire] (2.85, 4.25) -- (2.85, 3.75) -- (2.05, 3.75) -- (2.05, 3.30);
\draw[ubus] (0.45, 3.30) -- (3.85, 3.30);
\node[above=1pt] at (0.55, 3.30) {1081};

\draw[wire] (4.05, 4.25) -- (4.05, 3.75) -- (4.75, 3.75) -- (4.75, 3.30);
\draw[ubus] (4.35, 3.30) -- (5.15, 3.30) node[midway, above=1pt] {1117};

% A Side 5 feeder columns
\foreach \x/\ubus/\mbusname/\ylow in {
    0.70/1068/1069/-0.25,
    1.55/1105/1106/0.02,
    2.40/1093/1097/0.29,
    3.45//1082/0.56,
    4.75//1118/0.83
}{
    \draw[wire] (\x, 3.30) -- (\x, 2.52);
    \ifx\ubus\empty\else
        \draw[ubus] (\x-0.32, 2.75) -- (\x+0.32, 2.75);
        \node[above=1pt] at (\x-0.08, 2.75) {\ubus};
    \fi
    \pic at (\x, 2.23) {xfmr};
    \draw[wire] (\x, 1.94) -- (\x, \ylow);
    \draw[mbus] (\x-0.38, \ylow) -- (\x+0.38, \ylow);
    \node[above=1pt] at (\x-0.25, \ylow) {\mbusname};
}

% ================= B SIDE =================
\draw[mbus] (7.55, 5.75) -- (8.35, 5.75) node[midway, above=1pt] {1035};
\draw[wire] (7.95, 5.75) -- (7.95, 5.42);
\pic at (7.95, 5.13) {xfmr};
\draw[wire] (7.95, 4.84) -- (7.95, 4.25);

\draw[mbus] (6.95, 4.25) -- (11.35, 4.25);
\node[above=1pt] at (11.35, 4.25) {1036};

% B Side 2.4 kV branches
\draw[wire] (7.30, 4.25) -- (7.30, 3.75) -- (6.65, 3.75) -- (6.65, 3.30);
\draw[ubus] (6.25, 3.30) -- (7.05, 3.30) node[midway, above=1pt] {1123};

\draw[wire] (8.55, 4.25) -- (8.55, 3.75) -- (9.25, 3.75) -- (9.25, 3.30);
\draw[ubus] (7.50, 3.30) -- (10.95, 3.30);
\node[above=1pt] at (10.85, 3.30) {1087};

\draw[wire] (9.75, 4.25) -- (9.75, 3.75) -- (11.95, 3.75) -- (11.95, 3.30);
\draw[ubus] (11.55, 3.30) -- (12.35, 3.30) node[midway, above=1pt] {1168};

\draw[wire] (10.95, 4.25) -- (10.95, 3.92) -- (13.45, 3.92) -- (13.45, 3.30);
\draw[ubus] (13.05, 3.30) -- (13.85, 3.30) node[midway, above=1pt] {1159};

% B Side 5 main feeder columns
\foreach \x/\ubus/\mbusname/\ylow in {
    6.65//1124/0.83,
    7.85//1088/0.56,
    8.90/1096/1100/0.29,
    9.75/1111/1112/0.02,
    10.60/1074/1075/-0.25
}{
    \draw[wire] (\x, 3.30) -- (\x, 2.52);
    \ifx\ubus\empty\else
        \draw[ubus] (\x-0.32, 2.75) -- (\x+0.32, 2.75);
        \node[above=1pt] at (\x+0.05, 2.75) {\ubus};
    \fi
    \pic at (\x, 2.23) {xfmr};
    \draw[wire] (\x, 1.94) -- (\x, \ylow);
    \draw[mbus] (\x-0.38, \ylow) -- (\x+0.38, \ylow);
    \node[above=1pt] at (\x+0.28, \ylow) {\mbusname};
}

% B Side DER feeders: Fuel Cells (1183) & PVs + EV Chargers (1175)
\draw[wire] (11.95, 3.30) -- (11.95, 2.52);
\pic at (11.95, 2.23) {xfmr};
\draw[wire] (11.95, 1.94) -- (11.95, 0.83);
\draw[mbus] (11.55, 0.83) -- (12.35, 0.83) node[right=1pt, above=1pt] {1183};
\draw[wire] (11.95, 0.83) -- (11.95, 0.42);
\node[draw=black, fill=white, rounded corners=1.5pt, align=center, font=\sffamily\scriptsize, inner sep=2.5pt] at (11.95, 0.05) {Fuel\\Cells};

\draw[wire] (13.45, 3.30) -- (13.45, 2.52);
\pic at (13.45, 2.23) {xfmr};
\draw[wire] (13.45, 1.94) -- (13.45, 0.83);
\draw[mbus] (12.85, 0.83) -- (14.15, 0.83) node[right=1pt, above=1pt] {1175};
\draw[wire] (13.10, 0.83) -- (13.10, 0.42);
\draw[wire] (13.85, 0.83) -- (13.85, 0.42);
\node[draw=black, fill=white, rounded corners=1.5pt, align=center, font=\sffamily\scriptsize, inner sep=2.5pt] at (13.05, 0.12) {PVs};
\node[draw=black, fill=white, rounded corners=1.5pt, align=center, font=\sffamily\scriptsize, inner sep=2.5pt] at (13.90, 0.05) {EV\\Chargers};

% ================= 6 TIE BREAKERS =================
\draw[wire] (4.35, 4.25) -- (5.53, 4.25); \pic at (5.75, 4.25) {tie}; \draw[wire] (5.97, 4.25) -- (6.95, 4.25);
\foreach \xa/\xb/\yrow in {
    5.13/6.27/0.83,
    3.83/7.47/0.56,
    2.78/8.52/0.29,
    1.93/9.37/0.02,
    1.08/10.22/-0.25
}{
    \draw[wire] (\xa, \yrow) -- (5.53, \yrow);
    \pic at (5.75, \yrow) {tie};
    \draw[wire] (5.97, \yrow) -- (\xb, \yrow);
}
\end{tikzpicture}%
}
\caption{Caltech SoCal 28-Bus Circuit~3 distribution testbed architecture showing the $16.5\,\mathrm{kV}$, $2.4\,\mathrm{kV}$, and $480\,\mathrm{V}$ tiers across A~Side and B~Side, measured (red) vs.\ unmeasured (black) buses, six normally-open tie breakers, Fuel Cells (Bus~1183), and PVs + EV Chargers (Bus~1175).}
\label{fig:caltech_circuit3_tikz}
\end{figure*}
"""

if "fig:caltech_circuit3_tikz" not in tex:
    target = r"\begin{table}[t]"
    assert target in tex, "Table anchor not found"
    tex = tex.replace(target, tikz_caltech + "\n" + target, 1)
    tex = tex.replace(
        "Caltech SoCal 28-Bus Digital Twin",
        "Caltech SoCal 28-Bus Digital Twin (Fig.~\\ref{fig:caltech_circuit3_tikz})",
        1
    )

with open(TEX_PATH, "w") as f:
    f.write(tex)
print("Successfully inserted native vector TikZ Caltech schematic into microgrid_smart_grid_tsg-v2.tex.")
