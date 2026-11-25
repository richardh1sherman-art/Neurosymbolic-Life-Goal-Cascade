p = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/sim_caltech_ev_network_traffic.py"
code = open(p).read()

old_block = """        excess_kw = p_raw_kw - feeder_ceiling_kw
        if excess_kw > 0.0:
            avail_dis_kw = min(p_bat_cap, max(0.0, (soc - 0.15) * e_bat_max / dt_hr))
            p_b = -min(excess_kw, avail_dis_kw)  # Negative = discharging into feeder
            rem_excess = excess_kw + p_b
            throttle_ratio = max(0.62, (p_raw_kw - rem_excess) / max(p_raw_kw, 1.0))
        else:
            # Recharge battery during off-peak valleys below 320 kW
            headroom_kw = max(0.0, 320.0 - p_raw_kw)
            avail_chg_kw = min(p_bat_cap * 0.65, max(0.0, (0.90 - soc) * e_bat_max / dt_hr))
            p_b = min(headroom_kw, avail_chg_kw)
            throttle_ratio = 1.0"""

new_block = """        # Smooth linear SoC droop taper between 28% and 15% SoC + 25 kW/min slew limiter
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
            throttle_ratio = 1.0"""

assert old_block in code, "Target block not found"
open(p, "w").write(code.replace(old_block, new_block, 1))
print("Patched SoC droop taper + slew limiter cleanly.")
