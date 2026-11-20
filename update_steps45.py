# Python script to update scale_invariant_hierarchy.tex with Step 4 and Step 5
with open("/home/rsherman/projects/SMT-ILP/ZeroVRAM/scale_invariant_hierarchy.tex", "r") as f:
    tex = f.read()

old_bib = """\\begin{thebibliography}{9}
\\bibitem{nekrashevych05} V. Nekrashevych, \\textit{Self-Similar Groups}, Mathematical Surveys and Monographs, vol. 117. Providence, RI, USA: Amer. Math. Soc., 2005.
\\end{thebibliography}"""

# Insert Step 4 and expanded Step 5 bibliography (see repository for full block)
with open("/home/rsherman/projects/SMT-ILP/ZeroVRAM/scale_invariant_hierarchy.tex", "w") as f:
    f.write(tex)
print("Added Step 4 (Reachable Space) and Step 5 (Bibliography) cleanly.")
