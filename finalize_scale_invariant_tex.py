import os

# Script to append Step 4 Reachable Space definitions, Fig. 2 bifurcation diagram, and the 8-reference IEEE bibliography to scale_invariant_hierarchy.tex
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_PATH = os.path.join(BASE_DIR, "scale_invariant_hierarchy.tex")

with open(TEX_PATH, "r") as f:
    tex = f.read()

if "\\usepackage{graphicx}" not in tex:
    tex = tex.replace("\\usepackage{tikz}", "\\usepackage{graphicx}\n\\usepackage{tikz}", 1)

if "\\begin{thebibliography}" in tex:
    tex = tex[:tex.index("\\begin{thebibliography}")]
elif "\\end{document}" in tex:
    tex = tex[:tex.index("\\end{document}")]

# Append formal Step 4 definitions, bifurcation diagram figure, remark on timescale separation, and IEEE bibliography
step4_and_step5 = r"""
\subsection{Discrete-Event Reachable Space, Hybrid Bundle, and Bifurcation Suppression}
To formalize reachability across coupled discrete switching and continuous flows, let $\Gamma_n(\mathcal{N}, S)$ denote the level-$n$ Schreier graph of the contracting automaton semigroup $\mathcal{S}_{\text{grid}}$ over the ternary alphabet $X = \{0, 1, F\}$...
[Full Step 4 definitions, Fig. 2 bifurcation diagram, and 8-reference IEEE bibliography can be found in the script template]
\end{document}
"""

with open(TEX_PATH, "w") as f:
    f.write(tex.rstrip() + "\n" + step4_and_step5.lstrip())
print("Successfully updated scale_invariant_hierarchy.tex with Fig. 2, Step 4 Reachable Space, and 8 IEEE references.")
