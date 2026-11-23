import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOPO_TEX = os.path.join(BASE_DIR, "TopologyCaltech.tex")
MAIN_TEX = os.path.join(BASE_DIR, "scale_invariant_hierarchy.tex")
JSON_PATH = os.path.join(
    BASE_DIR,
    "digital-twin-dataset/sample_dataset/topology/network_files/circuit3/2023-08-01T00h00m00.000000s.json"
)

def merge_caltech_topology():
    with open(TOPO_TEX, "r") as f:
        topo_raw = f.read()

    with open(MAIN_TEX, "r") as f:
        main_raw = f.read()

    with open(JSON_PATH, "r") as f:
        net = json.load(f)

    # Check which named entities from Caltech JSON are not yet mentioned in TopologyCaltech.tex
    missing_by_cat = dict()
    categories = ("GridPower", "Inverter", "PV", "FuelCell", "Generator", "CB", "SwitchMultiPosition", "Load")
    for cat in categories:
        items = net.get(cat, list())
        missing = list()
        for it in items:
            nm = str(it.get("name", ""))
            if nm and nm not in topo_raw and nm.replace("_", "\\_") not in topo_raw:
                bus_info = it.get("bus") or it.get("fbus") or ""
                missing.append(f"{nm} ({bus_info})" if bus_info else nm)
        if missing:
            missing_by_cat[cat] = missing

    print("=" * 96)
    print("CALTECH NAMED ENTITY AUDIT (CHECKING FOR MISSING DEVICE NAMES)")
    print("=" * 96)
    if missing_by_cat:
        for cat, m_list in missing_by_cat.items():
            print(f" -> Missing {cat:<19} ({len(m_list):2d}) : {', '.join(m_list[:8])}{' ...' if len(m_list) > 8 else ''}")
    else:
        print(" -> All named entities in Caltech Circuit 3 are already present in TopologyCaltech.tex!")

    # Extract body of TopologyCaltech.tex between \begin{document} and \end{document}
    body = topo_raw
    if "\\begin{document}" in body:
        body = body.split("\\begin{document}", 1).pop(1)
    if "\\end{document}" in body:
        body = body.split("\\end{document}", 1).pop(0)

    # Remove standalone \maketitle or \title if present in the sub-document
    body = re.sub(r"\\(maketitle|title\{.*?\}|author\{.*?\})", "", body, flags=re.DOTALL).strip()

    # Build supplemental table of any omitted named devices so every physical component is indexed
    supp_tex = ""
    if missing_by_cat:
        rows_tex = list()
        for cat, m_list in missing_by_cat.items():
            escaped_items = ", ".join(x.replace("_", "\\_") for x in m_list)
            rows_tex.append(f"\\textbf{{{cat}}} ({len(m_list)}) & \\texttt{{{escaped_items}}} \\\\")
        supp_tex = (
            "\n\\subsection{Complete Inventory of Named Circuit Components}\n"
            "To ensure full traceability between symbolic automaton transitions and physical hardware, "
            "Table~\\ref{tab:caltech_named_inventory} indexes all additional named components in Caltech Circuit~3:\n"
            "\\begin{table}[!t]\n\\centering\n"
            "\\caption{Complete Named Device Inventory in Caltech SoCal 28-Bus Circuit~3}\n"
            "\\label{tab:caltech_named_inventory}\n\\scriptsize\n"
            "\\begin{tabularx}{\\columnwidth}{@{}lX@{}}\n\\toprule\n"
            "\\textbf{Component Class} & \\textbf{Named Physical Entities (Bus Location)} \\\\\n\\midrule\n"
            + "\n".join(rows_tex) +
            "\n\\bottomrule\n\\end{tabularx}\n\\end{table}\n"
        )

    merged_block = (
        "\n% ==========================================================================\n"
        "% MERGED FROM TopologyCaltech.tex\n"
        "% ==========================================================================\n"
        + body + "\n" + supp_tex + "\n"
    )

    # Insert merged Caltech topology section right before \begin{thebibliography} or \end{document}
    if "\\begin{thebibliography}" in main_raw:
        idx = main_raw.index("\\begin{thebibliography}")
        updated_main = main_raw[:idx] + merged_block + main_raw[idx:]
    else:
        idx = main_raw.index("\\end{document}")
        updated_main = main_raw[:idx] + merged_block + main_raw[idx:]

    with open(MAIN_TEX, "w") as f:
        f.write(updated_main)

    print("-" * 96)
    print(" -> Successfully merged TopologyCaltech.tex + complete device name inventory into scale_invariant_hierarchy.tex")
    print("=" * 96)

if __name__ == "__main__":
    merge_caltech_topology()
