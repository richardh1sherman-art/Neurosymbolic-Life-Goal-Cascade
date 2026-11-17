using PowerSystems
using PowerSimulationsDynamics
using DifferentialEquations
using DelimitedFiles
using LinearAlgebra

const PSID_VERSION = pkgversion(PowerSimulationsDynamics)

function integrate_10device_ibr_emt(p_surge_pu::Float64, u_mit_relief_pu::Float64, sccm_active::Bool)
    n_dev = 10
    gfm_mask = [true, true, true, true, true, true, true, false, false, false]
    b_tie = [0.45, 0.25, 0.15, 0.65, 0.40, 0.35, 0.30, 0.55, 0.72, 1.25]

    function ibr_emt_rhs!(du, u, p, t)
        jitter_rad = 0.2618 * sin(2.0 * pi * 4.5 * t) * exp(-0.18 * t)
        for i in 1:n_dev
            delta_i = u[2*i - 1]
            curr_i  = u[2*i]
            net_forcing = max(0.0, p_surge_pu - u_mit_relief_pu) * (b_tie[i] / 1.25)

            if sccm_active
                alpha_gfl = gfm_mask[i] ? 1.0 : 0.74
                u_sccm_d = -4.2 * delta_i - 1.8 * (curr_i - 0.92)
                u_sccm_i = -8.5 * (curr_i - 0.92) - 2.4 * delta_i
            else
                alpha_gfl = 1.0
                u_sccm_d = 0.0
                u_sccm_i = 0.0
            end

            if gfm_mask[i]
                du[2*i - 1] = -3.8 * delta_i + 1.4 * (0.92 - curr_i) + 0.42 * net_forcing + u_sccm_d
                du[2*i]     = -6.5 * (curr_i - 0.92) + 2.85 * sin(delta_i + 0.15 * jitter_rad) + 0.34 * net_forcing + u_sccm_i
            else
                du[2*i - 1] = -5.2 * delta_i + 1.65 * jitter_rad * alpha_gfl + 0.35 * net_forcing + u_sccm_d
                du[2*i]     = -9.0 * (curr_i - 0.88 * alpha_gfl) + 2.10 * sin(delta_i) + 0.28 * net_forcing * alpha_gfl + u_sccm_i
            end
        end
    end

    u0 = zeros(Float64, 2 * n_dev)
    for i in 1:n_dev
        u0[2*i - 1] = 0.015 * i / n_dev
        u0[2*i]     = gfm_mask[i] ? 0.92 : 0.88
    end

    prob = ODEProblem(ibr_emt_rhs!, u0, (0.0, 15.0))
    sol = solve(prob, Rodas5P(), reltol=1e-6, abstol=1e-6, saveat=0.002)

    i_max_pu = 0.0
    v_min_pu = 1.05
    df_max_hz = 0.0

    for idx in eachindex(sol.t)
        state_vec = sol.u[idx]
        for i in 1:n_dev
            d_val = state_vec[2*i - 1]
            c_val = state_vec[2*i]
            i_max_pu = max(i_max_pu, c_val)
            v_bus = 1.00 - 0.065 * max(0.0, c_val - 0.92) - 0.025 * abs(d_val)
            v_min_pu = min(v_min_pu, v_bus)
            df_hz = abs(d_val) * (60.0 / (2.0 * pi)) * 0.12
            df_max_hz = max(df_max_hz, df_hz)
        end
    end

    return i_max_pu, v_min_pu, df_max_hz
end

function main()
    in_path  = popfirst!(ARGS)
    out_path = popfirst!(ARGS)
    vals = vec(readdlm(in_path, ',', Float64))
    p_surge_pu    = popfirst!(vals)
    u_mit_base_pu = popfirst!(vals)
    u_mit_sccm_pu = popfirst!(vals)

    i_base, v_base, df_base = integrate_10device_ibr_emt(p_surge_pu, u_mit_base_pu, false)
    i_sccm, v_sccm, df_sccm = integrate_10device_ibr_emt(p_surge_pu, u_mit_sccm_pu, true)

    open(out_path, "w") do io
        writedlm(io, [i_base v_base df_base i_sccm v_sccm df_sccm], ',')
    end
end

main()
