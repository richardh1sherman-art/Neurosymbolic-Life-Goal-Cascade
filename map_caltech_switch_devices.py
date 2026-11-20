import os
import glob
import json
import csv
from collections import defaultdict, deque

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOPO_DIR = os.path.join(BASE_DIR, "digital-twin-dataset/sample_dataset/topology")
JSON_PATH = os.path.join(TOPO_DIR, "network_files/circuit3/2023-08-01T00h00m00.000000s.json")
TS_DIR = os.path.join(TOPO_DIR, "parameter_timeseries")

def extract_buses(val):
    out = list()
    if isinstance(val, str):
        out.append(val)
    elif isinstance(val, list):
        for el in val:
            out.extend(extract_buses(el))
    elif isinstance(val, dict):
        for k in ("bus", "fbus", "tbus", "name"):
            if k in val and isinstance(val[k], str):
                out.append(val[k])
                break
    return out

def inspect_step1_files():
    print("=" * 105)
    print("STEP 1: INSPECTING EXISTING BOTTOM-UP EVENT & COTANGENT LIFTING MODULES")
    print("=" * 105)
    for fname in ("BridgeObserver.py", "CoTangent_Lifting.py", "CoTangent_Lifting_V1.py"):
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r") as f:
                lines = [ln.strip() for ln in f if ln.strip().startswith(("class ", "def "))]
            print(f" -> {fname:<24} : {lines}")

def map_caltech_discrete_events():
    print("\n" + "=" * 105)
    print("STEP 2: MAPPING NAMED OFFLINE DEVICES TO CALTECH DISCRETE SWITCH EVENTS")
    print("=" * 105)

    with open(JSON_PATH, "r") as f:
        net = json.load(f)

    adj = defaultdict(list)
    edge_cats = ("Line", "Transformer", "Switch", "SwitchMultiPosition", "CB", "Fuse", "VFI")
    for cat in edge_cats:
        for item in net.get(cat, list()):
            fb = item.get("fbus")
            tb = item.get("tbus")
            nm = item.get("name")
            if fb and tb:
                for u_b in extract_buses(fb):
                    for v_b in extract_buses(tb):
                        adj[u_b].append((v_b, nm, cat))
                        adj[v_b].append((u_b, nm, cat))

    inv_sources = defaultdict(list)
    for pv in net.get("PV", list()):
        inv_name = pv.get("inverter")
        cap = pv.get("nameplate_capacity", dict()).get("value", "?")
        inv_sources[inv_name].append(f"PV:{pv.get('name')}({cap}kW)")
    for fc in net.get("FuelCell", list()):
        cap = fc.get("nameplate_capacity", dict()).get("value", "?")
        invs = fc.get("inverter", list())
        if isinstance(invs, str):
            invs = [invs]
        for inv_name in invs:
            inv_sources[inv_name].append(f"FuelCell:{fc.get('name')}({cap}kW)")

    bus_devices = defaultdict(list)
    for inv in net.get("Inverter", list()):
        b = inv.get("bus")
        nm = inv.get("name")
        src_tag = "+".join(inv_sources.get(nm, list()))
        label = f"Inverter:{nm}[{src_tag}]" if src_tag else f"Inverter:{nm}"
        if b:
            bus_devices[b].append(label)

    for cat in ("Generator", "Load", "GridPower"):
        for item in net.get(cat, list()):
            b = item.get("bus")
            if b:
                bus_devices[b].append(f"{cat}:{item.get('name')}")

    sub_buses = {gp.get("bus") for gp in net.get("GridPower", list()) if gp.get("bus")}
    switch_map = dict()
    for item in net.get("CB", list()) + net.get("SwitchMultiPosition", list()):
        switch_map[item.get("name")] = item

    out_csv = os.path.join(BASE_DIR, "caltech_named_discrete_events.csv")
    enriched_rows = list()

    print(f"{'Switch/CB':<12} | {'From -> To Bus':<24} | {'Events':<6} | {'Named Offline Devices When Opened'}")
    print("-" * 105)

    for path in sorted(glob.glob(os.path.join(TS_DIR, "*.csv"))):
        fname = os.path.basename(path)
        parts = fname.split("-")
        dev_name = "-".join(parts[:2]) if fname.startswith("swmp") else parts.pop(0)

        with open(path, "r") as cf:
            rows = list(csv.reader(cf))

        sw = switch_map.get(dev_name)
        fb_list = extract_buses(sw.get("fbus")) if sw else list()
        tb_list = extract_buses(sw.get("tbus")) if sw else list()
        fb_str = fb_list.pop(0) if fb_list else "unknown"
        tb_str = ",".join(tb_list) if tb_list else "unknown"

        offline_devs = list()
        if sw:
            for side_bus in extract_buses(sw.get("fbus")) + extract_buses(sw.get("tbus")):
                vis = {side_bus}
                q = deque([side_bus])
                reaches_grid = side_bus in sub_buses
                while q:
                    u = q.popleft()
                    for v, edge_nm, _ in adj[u]:
                        if edge_nm == dev_name or v in vis:
                            continue
                        vis.add(v)
                        if v in sub_buses:
                            reaches_grid = True
                        q.append(v)
                if not reaches_grid:
                    for b in sorted(vis):
                        for d_lbl in bus_devices[b]:
                            if d_lbl not in offline_devs:
                                offline_devs.append(d_lbl)

        offline_str = "; ".join(offline_devs) if offline_devs else "Loop/Tie Reconfiguration (No Islanded Devices)"
        num_events = max(0, len(rows) - 1)
        print(f"{dev_name:<12} | {f'{fb_str} -> {tb_str}':<24} | {num_events:<6d} | {offline_str}")

        for r in rows[1:]:
            ts = r.pop(0) if r else ""
            status = r.pop(0) if r else ""
            enriched_rows.append([dev_name, ts, status, fb_str, tb_str, offline_str])

    with open(out_csv, "w", newline="") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["switch_name", "timestamp", "status", "fbus", "tbus", "offline_devices"])
        writer.writerows(enriched_rows)

    print("-" * 105)
    print(f" -> Saved {len(enriched_rows)} named discrete-event records to: caltech_named_discrete_events.csv")
    print("=" * 105)

if __name__ == "__main__":
    inspect_step1_files()
    map_caltech_discrete_events()
