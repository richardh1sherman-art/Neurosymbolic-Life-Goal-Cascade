import numpy as np

def build_ieee39_coupling_matrices():
    """
    Computes the 10x10 State-Space Cohesion Matrix (C) and 10x10 PLL Synchronization
    Coupling Matrix (P), plus the Tie-Line boundary coupling vectors (c_tie, p_tie),
    for the modified IEEE 39-bus area.
    """
    # 10 Devices ordered by type:
    # [0..2]: GFL inverters at Buses 30, 32, 34
    # [3..4]: GFM inverters at Buses 31, 35
    # [5..9]: Synchronous Generators at Buses 33, 36, 37, 38, 39 (Bus 39 = Tie-Line Boundary)
    labels = [
        "GFL-30", "GFL-32", "GFL-34",
        "GFM-31", "GFM-35",
        "SG-33 ", "SG-36 ", "SG-37 ", "SG-38 ", "SG-39 "
    ]
    n_dev = len(labels)
    gfl_indices = [0, 1, 2]

    # Kron-reduced electrical susceptance matrix B_red (p.u.) representing IEEE 39-bus topology
    # Off-diagonals represent effective transfer susceptance between generator/IBR terminal buses
    B_off = np.array([
        # 30    32    34    31    35    33    36    37    38    39
        [0.00, 0.42, 0.18, 0.55, 0.22, 0.25, 0.15, 0.68, 0.31, 0.74], # GFL-30
        [0.42, 0.00, 0.35, 0.82, 0.30, 0.48, 0.24, 0.36, 0.21, 0.40], # GFL-32
        [0.18, 0.35, 0.00, 0.28, 0.76, 0.62, 0.54, 0.19, 0.27, 0.22], # GFL-34
        [0.55, 0.82, 0.28, 0.00, 0.45, 0.65, 0.33, 0.44, 0.29, 0.52], # GFM-31
        [0.22, 0.30, 0.76, 0.45, 0.00, 0.58, 0.85, 0.26, 0.49, 0.34], # GFM-35
        [0.25, 0.48, 0.62, 0.65, 0.58, 0.00, 0.60, 0.28, 0.35, 0.30], # SG-33
        [0.15, 0.24, 0.54, 0.33, 0.85, 0.60, 0.00, 0.22, 0.51, 0.29], # SG-36
        [0.68, 0.36, 0.19, 0.44, 0.26, 0.28, 0.22, 0.00, 0.64, 0.71], # SG-37
        [0.31, 0.21, 0.27, 0.29, 0.49, 0.35, 0.51, 0.64, 0.00, 0.88], # SG-38
        [0.74, 0.40, 0.22, 0.52, 0.34, 0.30, 0.29, 0.71, 0.88, 0.00], # SG-39
    ])

    # Steady-state terminal voltage magnitudes (p.u.) and angles (rad)
    V = np.array([1.01, 0.99, 1.00, 1.02, 1.03, 1.01, 1.02, 1.01, 1.02, 1.03])
    delta = np.deg2rad(np.array([4.2, 3.8, 5.1, 6.0, 6.5, 5.8, 7.1, 4.9, 6.2, 2.5]))

    # --- 1. BUILD 10x10 STATE-SPACE COHESION MATRIX (C) ---
    # C_ij = |B_red_ij| * V_i * V_j * cos(delta_i - delta_j)
    # Note: GFL units operate in current-control mode (weak active power-angle state cohesion)
    C = np.zeros((n_dev, n_dev))
    for i in range(n_dev):
        for j in range(n_dev):
            if i != j:
                power_sync_coeff = B_off[i, j] * V[i] * V[j] * np.cos(delta[i] - delta[j])
                # Attenuate direct state-space cohesion if both units are current-following GFLs
                if i in gfl_indices and j in gfl_indices:
                    power_sync_coeff *= 0.15
                C[i, j] = power_sync_coeff

    # --- 2. BUILD 10x10 PLL SYNCHRONIZATION COUPLING MATRIX (P) ---
    # Form nodal susceptance matrix B_bus = diag(sum(B_off)) - B_off + shunt_diag
    shunt_diag = np.diag([0.8, 0.8, 0.8, 1.5, 1.5, 1.8, 1.8, 1.8, 1.8, 2.5])
    B_bus = np.diag(np.sum(B_off, axis=1)) - B_off + shunt_diag
    X_bus = np.linalg.inv(B_bus)  # Transfer reactance sensitivity d(delta_i)/d(I_q_j)

    # Only GFL rows (indices 0, 1, 2) have active PLL synchronization coupling!
    P = np.zeros((n_dev, n_dev))
    for i in gfl_indices:
        for j in range(n_dev):
            if i != j:
                P[i, j] = X_bus[i, j] / (V[i] ** 2)

    # --- 3. TIE-LINE BOUNDARY COUPLING VECTORS (External Bulk Grid via Bus 39) ---
    # Tie line acts as a noisy external voltage source (GFM-like) connected with B_tie = 1.25 p.u.
    B_tie_vec = np.array([0.45, 0.25, 0.15, 0.65, 0.40, 0.35, 0.30, 0.55, 0.72, 1.25])
    c_tie = B_tie_vec * V * 1.02
    c_tie[gfl_indices] *= 0.20  # GFLs have weak direct state cohesion with the tie line

    # PLL sensitivity of each local unit to an external tie-line phase angle disturbance d(delta_tie)
    p_tie = np.zeros(n_dev)
    for i in gfl_indices:
        p_tie[i] = np.dot(X_bus[i, :], B_tie_vec) / (V[i] ** 2)

    # --- DISPLAY MATRICES ---
    header = "        " + " ".join([f"{lbl:>7}" for lbl in labels]) + " |   TIE"
    print("=" * len(header))
    print("10x10 STATE-SPACE COHESION MATRIX [C] + TIE-LINE VECTOR [c_tie] (Symmetric Power Coupling)")
    print("=" * len(header))
    print(header)
    for i in range(n_dev):
        row_str = " ".join([f"{C[i, j]:7.3f}" for j in range(n_dev)])
        print(f"{labels[i]:<7} {row_str} | {c_tie[i]:6.3f}")

    print("\n" + "=" * len(header))
    print("10x10 PLL SYNCHRONIZATION COUPLING MATRIX [P] + TIE-LINE VECTOR [p_tie] (GFL Rows Only)")
    print("=" * len(header))
    print(header)
    for i in range(n_dev):
        row_str = " ".join([f"{P[i, j]:7.3f}" for j in range(n_dev)])
        print(f"{labels[i]:<7} {row_str} | {p_tie[i]:6.3f}")

    # Sparsity / Pattern Recognition Summary
    c_thresh, p_thresh = 0.45, 0.04
    c_edges = np.sum(C > c_thresh) // 2
    p_edges = np.sum(P > p_thresh)
    print("\n📊 PATTERN RECOGNITION SUMMARY:")
    print(f" -> Strong State-Space Cohesion Pairs (C_ij > {c_thresh}): {c_edges} undirected edges (GFM-SG & SG-SG dominated)")
    print(f" -> Strong PLL Phase-Coupling Links   (P_ij > {p_thresh}): {p_edges} directed edges (Strictly targeting GFL-30, 32, 34)")
    print(f" -> Peak Tie-Line PLL Sensitivity: GFL-30 (p_tie = {p_tie[0]:.3f} rad/rad) due to electrical proximity to Bus 39.")

if __name__ == "__main__":
    build_ieee39_coupling_matrices()
