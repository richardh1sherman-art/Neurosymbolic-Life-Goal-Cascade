TEX_PATH = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Documents/MasterTheory-copy.tex"
with open(TEX_PATH, "r") as f:
    tex = f.read()

for pkg in ("\\usepackage{graphicx}", "\\usepackage{booktabs}", "\\usepackage{tikz}"):
    if pkg not in tex:
        tex = tex.replace("\\begin{document}", pkg + "\n\\begin{document}", 1)
if "\\usetikzlibrary{arrows.meta,positioning,shapes.geometric}" not in tex:
    tex = tex.replace("\\usepackage{tikz}", "\\usepackage{tikz}\n\\usetikzlibrary{arrows.meta,positioning,shapes.geometric}", 1)

sec1_marker = "\\section{Hierarchical Power Grid Architecture and Operational Scope}"
sub1_heading = "\\subsection{Multi-Timescale Operational Scope and Supervisory Interface}"
if sec1_marker in tex and sub1_heading not in tex:
    tex = tex.replace(sec1_marker, sec1_marker + "\n" + sub1_heading, 1)

salt_eq = r"\Xi_{w \to w'}(x) = \frac{\partial \Delta}{\partial x} + \frac{\Big( f_{w'}(\Delta(x)) - \frac{\partial \Delta}{\partial x} f_w(x) \Big) \left( \frac{\partial g_{\mathrm{event}}}{\partial x} \right)^\top}{\left( \frac{\partial g_{\mathrm{event}}}{\partial x} \right)^\top f_w(x) + \frac{\partial g_{\mathrm{event}}}{\partial t}}"
salt_eq_alt = r"\Xi_{w \to w'}(x) = \frac{\partial \Delta}{\partial x} + \frac{\Big( f_{w'}(\Delta(x)) - \frac{\partial \Delta}{\partial x} f_w(x) \Big) \left( \frac{\partial g_{\mathrm{event}}}{\partial x} \right)^{\top}}{\left( \frac{\partial g_{\mathrm{event}}}{\partial x} \right)^{\top} f_w(x) + \frac{\partial g_{\mathrm{event}}}{\partial t}}"

if salt_eq in tex and "\\label{eq:saltation_jump}" not in tex:
    tex = tex.replace(salt_eq, salt_eq + " \\label{eq:saltation_jump}", 1)
if salt_eq_alt in tex:
    tex = tex.replace(salt_eq_alt, r"\Xi_{w \to w'}(x) \quad \text{(defined in \eqref{eq:saltation_jump})}", 1)

with open(TEX_PATH, "w") as f:
    f.write(tex)
print("Part 1 complete: packages, subsection 1.1, and deduplicated saltation equation updated.")
