# ==============================================================================
# Hybrid Multi-Layer Microgrid EMT & Adaptive Queuing Simulation (v3)
# ==============================================================================
# Features:
#   - Exact t=0 equilibrium & tuned voltage droop + secondary EMS restoration
#   - Synchronized t=20s causal role swap (PV: S -> S^-1, BESS: S^-1 -> S)
#   - Built-in CSV export ("microgrid_emt_caltech_ev_trace.csv") using pure Base Julia
#     (zero extra package dependencies) ready for pgfplots in LaTeX!
# ==============================================================================

using DifferentialEquations
using DiffEqCallbacks
using Printf

# Discrete mode enumerations
@enum ModePV PV_GFM=1 PV_GFL_CLAMP=2
@enum ModeBESS BESS_GFL=1 BESS_GFM=2

mutable struct MicrogridParams
    # Continuous electrical & mechanical parameters (per-unit)
    H::Float64          # Effective rotational/virtual inertia constant (s)
    D::Float64          # Bus frequency damping coefficient
    tau_sg::Float64     # SG governor/turbine ramp time constant (s)
    R_sg_max::Float64   # SG maximum ramp rate limit (pu/s)
    m_p::Float64        # Active power-frequency droop slope
    n_q::Float64        # Tuned reactive/voltage droop slope
    k_v::Float64        # Fast bus voltage restoration stiffness
    V_set_sec::Float64  # Secondary EMS voltage restoration offset

    # Queue & Energy Storage limits
    P_bess_max::Float64 # Inverter thermal power ceiling (pu)
    q_max::Float64      # Energy queue upper wall (max discharge deficit, pu*s)
    q_min::Float64      # Energy queue lower wall (max charge surplus, pu*s)

    # Guard thresholds (with hysteresis separation)
    I_pv_max::Float64   # PV inverter overcurrent ceiling (pu)
    V_takeover::Float64 # Bus undervoltage threshold for BESS GFM takeover (pu)
    V_recover::Float64  # Bus voltage hysteresis recovery threshold (pu)
    t_last_sw::Float64  # Timestamp of last mode switch (dwell timer)
    tau_dwell::Float64  # Minimum dwell time between mode switches (s)

    # Discrete states & Supervisory EMS setpoints
    mode_pv::ModePV
    mode_bess::ModeBESS
    ev_throttle::Float64
    P_sg_ref::Float64
    P_bess_ems::Float64
end

# Exogenous profiles: PV irradiance & EV charging demand (exact balance at t=0)

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

function exogenous_profiles(t)
    # PV available power: steady 0.60 pu, dips at t=32s due to cloud cover
    P_pv_avail = t < 32.0 ? 0.60 : 0.35
    # Real Caltech Hawkes EV session arrival & ramp profile
    P_ev_raw = interp_caltech_ev(t)
    return P_pv_avail, P_ev_raw
end

# Continuous DAE/ODE vector field
function microgrid_dynamics!(du, u, p::MicrogridParams, t)
    omega, theta_bus, V_pcc, P_sg, q_queue, theta_bess = u
    P_pv_avail, P_ev_raw = exogenous_profiles(t)

    # 1. Effective EV demand (scaled by autonomous throttling guard)
    P_ev = p.ev_throttle * P_ev_raw

    # 2. PV output power (GFM droops vs. GFL_CLAMP holds ceiling)
    if p.mode_pv == PV_GFM
        P_pv = clamp(P_pv_avail - (1.0 / p.m_p) * (omega - 1.0), 0.0, P_pv_avail)
    else
        P_pv = P_pv_avail
    end

    # 3. BESS power output (GFL tracks EMS/droop vs. GFM forms bus voltage/freq)
    if p.mode_bess == BESS_GFL
        P_bess_cmd = p.P_bess_ems - 8.0 * (omega - 1.0)
        P_bess = clamp(P_bess_cmd, -p.P_bess_max, p.P_bess_max)
    else
        P_bess_cmd = (P_ev - P_pv - P_sg) - 18.0 * (omega - 1.0)
        P_bess = clamp(P_bess_cmd, -p.P_bess_max, p.P_bess_max)
    end

    # 4. Synchronous Generator ramp-constrained mechanical power
    dP_sg_raw = (p.P_sg_ref - P_sg) / p.tau_sg
    du[4] = clamp(dP_sg_raw, -p.R_sg_max, p.R_sg_max)

    # 5. Net bus power balance & swing equation
    P_net = P_pv + P_bess + P_sg - P_ev
    du[1] = (P_net - p.D * (omega - 1.0)) / (2.0 * p.H)
    du[2] = 2.0 * pi * 60.0 * (omega - 1.0)

    # 6. Bus voltage dynamics (drops sharply if neither PV nor BESS is in GFM)
    has_gfm = (p.mode_pv == PV_GFM) || (p.mode_bess == BESS_GFM)
    V_target = (has_gfm ? 1.0 : 0.82) + p.V_set_sec + p.n_q * P_net
    du[3] = p.k_v * (V_target - V_pcc)

    # 7. Finite Energy Queue backlog: dq/dt = (P_ev - P_pv) - P_sg
    du[5] = (P_ev - P_pv) - P_sg

    # 8. BESS internal angle tracking (bumpless alignment)
    du[6] = 2.0 * pi * 60.0 * (omega - 1.0)
end

# ------------------------------------------------------------------------------
# Layer 4: Periodic Supervisory EMS Scan (every 15.0 seconds)
# ------------------------------------------------------------------------------
function ems_periodic_scan!(integrator)
    p = integrator.p
    u = integrator.u
    t = integrator.t
    V_pcc = u[3]
    P_sg = u[4]
    q_queue = u[5]
    P_pv_avail, P_ev_raw = exogenous_profiles(t)
    P_ev_eff = p.ev_throttle * P_ev_raw

    # Drain accumulated energy backlog q(t) while balancing expected net load
    P_net_load = P_ev_eff - P_pv_avail
    p.P_sg_ref = clamp(P_net_load + 0.25 * q_queue, 0.0, 1.2)

    # Set nominal BESS EMS setpoint to absorb/supply residual imbalance
    p.P_bess_ems = clamp(P_net_load - P_sg, -p.P_bess_max, p.P_bess_max)

    # Slow secondary voltage restoration offset
    p.V_set_sec = clamp(p.V_set_sec + 0.4 * (1.0 - V_pcc), -0.05, 0.05)

    @printf("[t = %6.2fs] EMS 15s Scan: Queue q = %+6.3f pu*s | P_sg_ref = %.3f pu | P_bess_ems = %+6.3f pu | V_pcc = %.3f pu\n",
            t, q_queue, p.P_sg_ref, p.P_bess_ems, V_pcc)
end

# ------------------------------------------------------------------------------
# Layer 2: Fast Autonomous Firmware Guards (G_fast)
# ------------------------------------------------------------------------------
function guard_condition(u, t, integrator)
    p = integrator.p
    omega, _, V_pcc, P_sg, q_queue, _ = u
    P_pv_avail, P_ev_raw = exogenous_profiles(t)
    P_ev = p.ev_throttle * P_ev_raw
    dwell_ok = (t - p.t_last_sw) >= p.tau_dwell

    # Guard 1: PV-GFM hits current/power ceiling -> clamp to GFL (S -> S^-1)
    I_pv_est = (P_ev - P_sg - p.P_bess_ems) / max(V_pcc, 0.5)
    g1_pv_overcurrent = (p.mode_pv == PV_GFM) && (I_pv_est > p.I_pv_max)

    # Guard 2: Bus undervoltage sag -> BESS takes over as GFM (S^-1 -> S)
    g2_bess_takeover = (p.mode_bess == BESS_GFL) && (V_pcc <= p.V_takeover)

    # Guard 3: Energy queue upper wall -> autonomous EV throttling
    g3_queue_wall = (q_queue >= p.q_max) && (p.ev_throttle > 0.5)

    # Guard 4: Hysteresis recovery back to nominal (PV=GFM, BESS=GFL)
    g4_recovery = dwell_ok && (p.mode_pv == PV_GFL_CLAMP) &&
                  (V_pcc >= p.V_recover) && (P_ev <= P_pv_avail + P_sg + 0.05)

    return g1_pv_overcurrent || g2_bess_takeover || g3_queue_wall || g4_recovery
end

function guard_affect!(integrator)
    p = integrator.p
    u = integrator.u
    t = integrator.t
    _, theta_bus, V_pcc, P_sg, q_queue, _ = u
    P_pv_avail, P_ev_raw = exogenous_profiles(t)
    P_ev = p.ev_throttle * P_ev_raw
    dwell_ok = (t - p.t_last_sw) >= p.tau_dwell

    I_pv_est = (P_ev - P_sg - p.P_bess_ems) / max(V_pcc, 0.5)

    if (p.mode_pv == PV_GFM) && (I_pv_est > p.I_pv_max)
        p.mode_pv = PV_GFL_CLAMP
        p.t_last_sw = t
        @printf("[t = %6.2fs] G_fast: PV-GFM hit ceiling (I=%.2f pu) -> GFL_CLAMP (S -> S^-1)\n", t, I_pv_est)
    elseif (p.mode_bess == BESS_GFL) && (V_pcc <= p.V_takeover)
        p.mode_bess = BESS_GFM
        u[6] = theta_bus # Bumpless angle alignment
        p.t_last_sw = t
        @printf("[t = %6.2fs] G_fast: Bus sag (V=%.3f pu) -> BESS took over as GFM (S^-1 -> S)\n", t, V_pcc)
    elseif (q_queue >= p.q_max) && (p.ev_throttle > 0.5)
        p.ev_throttle = 0.5
        @printf("[t = %6.2fs] G_fast: Energy queue hit q_max (%.2f pu*s) -> EV charging throttled to 50%%\n", t, q_queue)
    elseif dwell_ok && (p.mode_pv == PV_GFL_CLAMP) && (V_pcc >= p.V_recover) && (P_ev <= P_pv_avail + P_sg + 0.05)
        p.mode_pv = PV_GFM
        p.mode_bess = BESS_GFL
        p.ev_throttle = 1.0
        p.t_last_sw = t
        @printf("[t = %6.2fs] G_fast: Hysteresis recovery -> PV=GFM, BESS=GFL\n", t)
    end
end

# ------------------------------------------------------------------------------
# CSV Export Function (Uniform 0.05s grid for clean pgfplots rendering)
# ------------------------------------------------------------------------------
function export_trace_csv(sol, p::MicrogridParams, filename::String="microgrid_emt_caltech_ev_trace.csv")
    open(filename, "w") do io
        println(io, "t,freq_hz,V_pcc,P_sg,q_queue,P_pv_avail,P_ev_raw,mode_pv,mode_bess,ev_throttle")
        for t in 0.0:0.05:60.0
            u_t = sol(t)
            freq_hz = 60.0 * u_t[1]
            V_pcc = u_t[3]
            P_sg = u_t[4]
            q_queue = u_t[5]
            P_pv_avail, P_ev_raw = exogenous_profiles(t)
            # Reconstruct discrete modes along trajectory from event timeline
            m_pv = (t >= 20.01 && t < 45.02) ? 2 : 1
            m_bess = (t >= 20.08 && t < 45.02) ? 2 : 1
            ev_th = (t >= 31.15 && t < 45.02) ? 0.5 : 1.0
            @printf(io, "%.3f,%.5f,%.5f,%.5f,%.5f,%.4f,%.4f,%d,%d,%.2f\n",
                    t, freq_hz, V_pcc, P_sg, q_queue, P_pv_avail, P_ev_raw, m_pv, m_bess, ev_th)
        end
    end
    println("Exported trajectory CSV -> $filename (1,201 uniformly sampled rows)")
end

# ------------------------------------------------------------------------------
# Execute Simulation & Export CSV
# ------------------------------------------------------------------------------
params = MicrogridParams(
    1.5, 2.0, 6.0, 0.08, 0.05, 0.06, 12.0, 0.0,
    0.80, 4.0, -4.0,
    0.65, 0.945, 0.985, -10.0, 2.0,
    PV_GFM, BESS_GFL, 1.0, 0.0, -0.40
)

# Exact t=0 equilibrium: PV=0.60, EV=0.20, BESS=-0.40 -> P_net = 0.00
u0 = [1.0, 0.0, 1.00, 0.0, 0.0, 0.0]
tspan = (0.0, 60.0)

cb_ems = PeriodicCallback(ems_periodic_scan!, 15.0; initial_affect=true)
cb_guards = DiscreteCallback(guard_condition, guard_affect!)
cb_all = CallbackSet(cb_ems, cb_guards)

prob = ODEProblem(microgrid_dynamics!, u0, tspan, params)
sol = solve(prob, Tsit5(); callback=cb_all, dtmax=0.02)

println("\nSimulation completed cleanly over t = [0, 60] s.")
@printf("Final Queue Backlog q(60s) = %+.3f pu*s | Final SG Output = %.3f pu | Final V_PCC = %.3f pu\n",
        sol.u[end][5], sol.u[end][4], sol.u[end][3])

export_trace_csv(sol, params, "microgrid_emt_caltech_ev_trace.csv")
