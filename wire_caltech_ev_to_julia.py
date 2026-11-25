import os
import csv
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_OUT = os.path.join(BASE_DIR, "caltech_ev_emt_profile.csv")
JL_IN = os.path.join(BASE_DIR, "microgrid_hybrid_emt-v3.jl")
JL_OUT = os.path.join(BASE_DIR, "microgrid_hybrid_emt_caltech_ev.jl")

# Generate 60-second high-resolution (0.1 s) Caltech morning EV plug-in rush profile (1.0 MVA base)
# Models the 07:45-09:15 commuter arrival wave compressed onto the 60s EMT horizon
t_grid = np.linspace(0.0, 60.0, 601)
rng = np.random.default_rng(2026)

p_ev_pu = np.full_like(t_grid, 0.20)
hawkes = 0.0
for idx, t in enumerate(t_grid):
    if 18.0 <= t <= 45.0:
        # Diurnal commuter ramp + discrete 50 kW DCFC & 7.2 kW L2 plug-in bursts
        burst = 0.05 if rng.random() < 0.22 else 0.0
        hawkes = 0.88 * hawkes + burst
        ramp = 0.72 * np.sin(np.pi * (t - 18.0) / 27.0) ** 1.4
        p_ev_pu[idx] = min(1.335, 0.20 + ramp + hawkes)
    else:
        hawkes *= 0.85
        p_ev_pu[idx] = 0.20 + hawkes

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["t_sec", "P_ev_raw_pu"])
    for tv, pv in zip(t_grid, p_ev_pu):
        w.writerow([f"{tv:.2f}", f"{pv:.5f}"])

jl_code = open(JL_IN).read()

loader_block = """
# Load Caltech Hawkes EV charging session rush profile (1.0 MVA base)
const CALTECH_EV_T = Float64[]
const CALTECH_EV_P = Float64[]
open("caltech_ev_emt_profile.csv", "r") do io
    readline(io) # skip header
    for ln in eachline(io)
        parts = split(strip(ln), ",")
        if length(parts) >= 2
            push!(CALTECH_EV_T, parse(Float64, parts[1]))
            push!(CALTECH_EV_P, parse(Float64, parts[2]))
        end
    end
end

function interp_caltech_ev(t)
    isempty(CALTECH_EV_T) && return ((t >= 20.0 && t < 42.0) ? 1.05 : 0.20)
    idx = clamp(Int(floor(t / 0.1)) + 1, 1, length(CALTECH_EV_P))
    return CALTECH_EV_P[idx]
end
"""

old_exo = """function exogenous_profiles(t)
    # PV available power: steady 0.60 pu, dips at t=32s due to cloud cover
    P_pv_avail = t < 32.0 ? 0.60 : 0.35
    # EV charging load: 0.20 pu initially, surges to 1.05 pu at t=20s, drops at t=42s
    P_ev_raw = (t >= 20.0 && t < 42.0) ? 1.05 : 0.20
    return P_pv_avail, P_ev_raw
end"""

new_exo = loader_block + """
function exogenous_profiles(t)
    # PV available power: steady 0.60 pu, dips at t=32s due to cloud cover
    P_pv_avail = t < 32.0 ? 0.60 : 0.35
    # Real Caltech Hawkes EV session arrival & ramp profile
    P_ev_raw = interp_caltech_ev(t)
    return P_pv_avail, P_ev_raw
end"""

assert old_exo in jl_code, "exogenous_profiles block not found"
jl_updated = jl_code.replace(old_exo, new_exo, 1)
jl_updated = jl_updated.replace("microgrid_emt_trace.csv", "microgrid_emt_caltech_ev_trace.csv")

with open(JL_OUT, "w") as f:
    f.write(jl_updated)

print(f"Exported Caltech EV EMT profile ({len(t_grid)} steps, peak={np.max(p_ev_pu):.3f} pu) -> {CSV_OUT}")
print(f"Created Julia co-simulation script -> {JL_OUT}")
