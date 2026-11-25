import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(
    BASE_DIR,
    "digital-twin-dataset/sample_dataset/topology/network_files/circuit3/2023-08-01T00h00m00.000000s.json"
)
OUT_PNG = os.path.join(BASE_DIR, "Documents/caltech_ev_queue_ramps.png")


def load_caltech_load_buses():
    with open(JSON_PATH, "r") as f:
        net = json.load(f)
    loads = net.get("Load", list())
    load_names = [str(ld.get("name", f"load_{i}")) for i, ld in enumerate(loads)]
    return len(loads), load_names


def simulate_ev_session_queues():
    print("=" * 108)
    print("CALTECH 28-BUS PHYSICAL EV CHARGING SESSION QUEUES & ADAPTIVE BATTERY QUEUING SIMULATION")
    print("=" * 108)

    n_loads, load_names = load_caltech_load_buses()
    print(f" -> Anchored to {n_loads} real Caltech Circuit 3 Load nodes: {', '.join(load_names[:6])} ...")

    # Simulate 16-hour campus operating window (06:00 to 22:00) at 1-minute resolution (960 steps)
    dt_hr = 1.0 / 60.0
    n_steps = 960
    t_hrs = 6.0 + np.arange(n_steps) * dt_hr

    rng = np.random.default_rng(2026)

    # Diurnal + Hawkes self-exciting EV arrival rate (sessions / hour across 120 campus EVSE ports)
    # Morning commuter peak at 08:45, midday turnover peak at 13:00
    base_rate = (
        6.0
        + 42.0 * np.exp(-0.5 * ((t_hrs - 8.75) / 1.05) ** 2)
        + 24.0 * np.exp(-0.5 * ((t_hrs - 13.00) / 0.95) ** 2)
    )

    n_ports = 120
    port_rem_kwh = np.zeros(n_ports)
    port_max_kw = np.zeros(n_ports)
    wait_queue = list()  # FIFO queue of waiting EV sessions (req_kwh, max_kw)

    p_ev_uncoord = np.zeros(n_steps)
    p_ev_queued = np.zeros(n_steps)
    p_bat_kw = np.zeros(n_steps)
    soc_bat = np.zeros(n_steps)
    active_sessions = np.zeros(n_steps, dtype=int)
    waiting_sessions = np.zeros(n_steps, dtype=int)
    discrete_events = 0

    # Adaptive Battery Queuing Layer parameters (Caltech campus BESS: 600 kWh / 300 kW)
    e_bat_max = 600.0
    p_bat_cap = 300.0
    soc = 0.55
    feeder_ceiling_kw = 420.0  # Transformer thermal & contraction cell '00' threshold
    hawkes_boost = 0.0

    for k in range(n_steps):
        # Hawkes arrival intensity with cluster excitation
        lam_k = base_rate[k] + hawkes_boost
        n_arr = int(rng.poisson(lam_k * dt_hr))
        hawkes_boost = 0.82 * hawkes_boost + 1.8 * n_arr

        for _ in range(n_arr):
            is_dcfc = (rng.random() < 0.18)
            req_kwh = float(rng.uniform(28.0, 58.0) if is_dcfc else rng.uniform(12.0, 32.0))
            max_kw = 50.0 if is_dcfc else 7.2
            wait_queue.append((req_kwh, max_kw))
            discrete_events += 1

        # Assign queued EVs to free EVSE ports
        for p_idx in range(n_ports):
            if port_rem_kwh[p_idx] <= 1e-6 and wait_queue:
                rq, mk = wait_queue.pop(0)
                port_rem_kwh[p_idx] = rq
                port_max_kw[p_idx] = mk

        # Uncoordinated charging power (all active ports draw full nameplate power immediately)
        active_mask = port_rem_kwh > 1e-6
        active_sessions[k] = int(np.sum(active_mask))
        waiting_sessions[k] = len(wait_queue)
        p_raw_kw = float(np.sum(port_max_kw[active_mask]))
        p_ev_uncoord[k] = p_raw_kw

        # Adaptive Battery Queuing & Soft-Throttle Dispatch:
        # 1) Battery discharges to shave peaks above feeder_ceiling_kw and charges during lulls
        # 2) Queue rate-modulation scales EVSE draw smoothly when SoC approaches floor
        # Smooth linear SoC droop taper between 28% and 15% SoC + 25 kW/min slew limiter
        soc_taper = float(np.clip((soc - 0.15) / 0.13, 0.0, 1.0))
        prev_pb = p_bat_kw[k - 1] if k > 0 else 0.0
        excess_kw = p_raw_kw - feeder_ceiling_kw
        if excess_kw > 0.0:
            avail_dis_kw = min(p_bat_cap * soc_taper, max(0.0, (soc - 0.15) * e_bat_max / dt_hr))
            target_pb = -min(excess_kw, avail_dis_kw)
        else:
            headroom_kw = max(0.0, 320.0 - p_raw_kw)
            avail_chg_kw = min(p_bat_cap * 0.65, max(0.0, (0.90 - soc) * e_bat_max / dt_hr))
            target_pb = min(headroom_kw, avail_chg_kw)

        p_b = float(np.clip(target_pb, prev_pb - 25.0, prev_pb + 25.0))
        if excess_kw > 0.0:
            rem_excess = max(0.0, excess_kw + p_b)
            throttle_ratio = max(0.55, (p_raw_kw - rem_excess) / max(p_raw_kw, 1.0))
        else:
            throttle_ratio = 1.0

        p_bat_kw[k] = p_b
        soc = float(np.clip(soc + (p_b * dt_hr) / e_bat_max, 0.15, 0.90))
        soc_bat[k] = soc

        # Advance EV port energy states & count unplug discrete events
        delivered_kw = port_max_kw[active_mask] * throttle_ratio
        p_ev_queued[k] = float(np.sum(delivered_kw)) + p_b
        port_rem_kwh[active_mask] = np.maximum(0.0, port_rem_kwh[active_mask] - delivered_kw * dt_hr)
        newly_done = int(np.sum(active_mask & (port_rem_kwh <= 1e-6)))
        discrete_events += newly_done

    # Compute ramp & peak metrics
    ramp_uncoord = np.max(np.abs(np.diff(p_ev_uncoord))) / (dt_hr * 60.0)  # kW / min
    ramp_queued = np.max(np.abs(np.diff(p_ev_queued))) / (dt_hr * 60.0)    # kW / min
    peak_uncoord = float(np.max(p_ev_uncoord))
    peak_queued = float(np.max(p_ev_queued))
    peak_cut_pct = 100.0 * (peak_uncoord - peak_queued) / peak_uncoord
    ramp_cut_pct = 100.0 * (ramp_uncoord - ramp_queued) / ramp_uncoord

    print("-" * 108)
    print(f"Total Discrete EV Plug-In/Unplug Switching Events : {discrete_events}")
    print(f"Peak Active EVSE Ports / Max Waiting Queue        : {int(np.max(active_sessions))} active / {int(np.max(waiting_sessions))} queued")
    print(f"Uncoordinated EV Peak Feeder Load / Max Ramp      : {peak_uncoord:6.1f} kW  |  {ramp_uncoord:5.2f} kW/min")
    print(f"Adaptive Battery Queuing Peak Load / Max Ramp     : {peak_queued:6.1f} kW  |  {ramp_queued:5.2f} kW/min")
    print(f"Peak Demand Reduction / Ramp-Rate Reduction       : -{peak_cut_pct:4.1f}%     |  -{ramp_cut_pct:4.1f}%")
    print(f"Battery SoC Operating Range (Min -> Max)          : {100*np.min(soc_bat):4.1f}% -> {100*np.max(soc_bat):4.1f}%")
    print("-" * 108)

    # Save 3-panel publication figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7.6, 6.4), sharex=True)

    ax1.plot(t_hrs, active_sessions, color="#1f77b4", linewidth=2.0, label="Active Charging EVs (120 Ports)")
    ax1.plot(t_hrs, waiting_sessions, color="#d62728", linestyle="--", linewidth=1.8, label="Waiting Queue Backlog Q_EV(t)")
    ax1.set_ylabel("EV Sessions", fontsize=9.5)
    ax1.set_title("Caltech 28-Bus EV Charging Session Queues & Adaptive Battery Queuing Layer", fontsize=10.5, fontweight="bold")
    ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.legend(loc="upper right", fontsize=8.2)

    ax2.axhline(feeder_ceiling_kw, color="#ff7f0e", linestyle=":", linewidth=1.4, label="Contraction Cell '00' Ceiling (420 kW)")
    ax2.plot(t_hrs, p_ev_uncoord, color="#d62728", linewidth=1.8, alpha=0.85, label=f"Uncoordinated EV Load (Peak={peak_uncoord:.0f} kW)")
    ax2.plot(t_hrs, p_ev_queued, color="#2ca02c", linewidth=2.2, label=f"Adaptive Battery Queuing Net Load (Peak={peak_queued:.0f} kW)")
    ax2.set_ylabel("Net Feeder Power (kW)", fontsize=9.5)
    ax2.grid(True, linestyle="--", alpha=0.35)
    ax2.legend(loc="upper right", fontsize=8.2)

    ax3.plot(t_hrs, 100.0 * soc_bat, color="#9467bd", linewidth=2.0, label="Campus BESS State of Charge (%)")
    ax3.set_ylabel("Battery SoC (%)", fontsize=9.5)
    ax3.set_xlabel("Time of Day (Hours, Caltech SoCal 28-Bus Campus Microgrid)", fontsize=9.5)
    ax3.set_ylim(10.0, 95.0)
    ax3.grid(True, linestyle="--", alpha=0.35)
    ax3.legend(loc="lower right", fontsize=8.2)

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=300)
    print(f" -> Saved 3-panel EV queue & battery ramp figure to: {OUT_PNG}")
    print("=" * 108)


if __name__ == "__main__":
    simulate_ev_session_queues()
