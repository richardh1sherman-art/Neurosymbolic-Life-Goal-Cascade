import numpy as np
import scipy.linalg as la

def frozen_offline_decision_tree(theta_phys_hat, theta_nn_hat, lmi_max_eig):
    """
    Represents a static, offline-trained utility Decision Tree classifier.
    Because its split thresholds cannot be updated online, it relies on the
    real-time PEM-MHE parameter estimates and LMI residual to classify mode shifts.
    """
    if lmi_max_eig > -0.02 or theta_nn_hat > 0.35:
        return "ALARM: GFL-MODE FALLBACK (CRITICAL)"
    elif theta_phys_hat < 0.72 and theta_nn_hat > 0.18:
        return "WARN : GFM CURRENT-LIMIT DRIFT"
    else:
        return "OK   : NOMINAL GFM VOLTAGE-FORMING"

def run_gfm_to_gfl_detection_test():
    print("=" * 84)
    print("ONLINE GFM-TO-GFL MODE-SHIFT DETECTION TEST (BUS 31 | PEM-MHE + OFF-DIAGONAL LMI)")
    print("=" * 84)

    # 1. Baseline Coupled Area Matrices (4-state reduced representation: GFL-30, GFM-31, GFM-35, SG-39)
    # States per device: [delta_i, omega_i / I_q_i] -> 8 states total
    A_nom = np.array([
        [-3.5,  1.2,  0.05, 0.00,  0.04, 0.00,  0.05, 0.00], # GFL-30 (PLL coupled)
        [-2.0, -4.5,  0.00, 0.00,  0.00, 0.00,  0.00, 0.00],
        [ 0.00, 0.00, -1.8, 1.00,  0.16, 0.00,  0.19, 0.00], # GFM-31 (Initially zero PLL row)
        [ 0.20, 0.00, -1.5, -2.8,  0.17, 0.00,  0.19, 0.00],
        [ 0.00, 0.00,  0.16, 0.00, -1.8, 1.00,  0.13, 0.00], # GFM-35
        [ 0.08, 0.00,  0.17, 0.00, -1.5, -2.8,  0.13, 0.00],
        [ 0.00, 0.00,  0.19, 0.00,  0.13, 0.00, -0.9, 1.00], # SG-39
        [ 0.27, 0.00,  0.19, 0.00,  0.13, 0.00, -1.2, -1.6]
    ])
    B_nom = np.kron(np.eye(4), np.array([[0.0], [1.4]]))
    lam = 0.35
    A_shifted = A_nom + lam * np.eye(8)

    # Synthesize baseline off-diagonal contraction metric W_base
    M_base = la.solve_continuous_are(A_shifted, B_nom, np.eye(8) * 2.0, np.eye(4) * 0.5)
    W_base = la.inv(M_base)
    K_base = -la.inv(np.eye(4) * 0.5) @ B_nom.T @ M_base
    Y_base = K_base @ W_base

    # 2. Simulate 400 ms transient where GFM-31 degrades into GFL mode between t=0.10s and t=0.25s
    dt = 0.001
    steps = 400
    theta_hat = np.array([0.8500, 0.0400])  # [theta_phys (voltage stiffness), theta_nn (PLL coupling residual)]
    rng = np.random.default_rng(42)

    print(f"{'Time (s)':<9} | {'True Shift mu':<13} | {'Est th_phys':<11} | {'Est th_nn':<10} | {'LMI Max Eig':<12} | {'Offline Tree Output'}")
    print("-" * 84)

    warn_time = None
    alarm_time = None

    for step in range(steps):
        t = step * dt
        # Smooth ramp of GFM-31 current-limit saturation -> GFL PLL fallback
        if t < 0.10:
            mu = 0.0
        elif t < 0.25:
            mu = (t - 0.10) / 0.15
        else:
            mu = 1.0

        # True underlying physical parameters at Bus 31
        theta_phys_true = 0.85 - 0.45 * mu   # Drops from 0.85 to 0.40 as voltage stiffness is lost
        theta_nn_true = 0.04 + 0.48 * mu     # Rises from 0.04 to 0.52 as PLL phase coupling turns on

        # Online PEM-MHE recursive parameter update (with small measurement noise)
        meas_noise = rng.normal(0.0, 0.004, size=2)
        theta_meas = np.array([theta_phys_true, theta_nn_true]) + meas_noise
        learning_gain = 0.12
        theta_hat = theta_hat + learning_gain * (theta_meas - theta_hat)

        # Perturb A_area using online estimated mode shift at GFM-31 (rows 2 & 3)
        mu_hat = np.clip((theta_hat[1] - 0.04) / 0.48, 0.0, 1.2)
        A_live = A_shifted.copy()
        # GFM-31 loses voltage-forming damping and gains GFL PLL phase coupling from GFL-30 & SG-39
        A_live[2, 2] += 1.45 * mu_hat
        A_live[2, 0] += 0.22 * mu_hat
        A_live[2, 6] += 0.28 * mu_hat

        # Evaluate Off-Diagonal Contraction LMI Residual Psi_11
        Psi_11_live = A_live @ W_base + W_base @ A_live.T + B_nom @ Y_base + Y_base.T @ B_nom.T
        max_eig = np.max(np.linalg.eigvalsh(Psi_11_live))

        # Query Frozen Offline Decision Tree
        status = frozen_offline_decision_tree(theta_hat[0], theta_hat[1], max_eig)
        if "WARN" in status and warn_time is None:
            warn_time = t
        if "ALARM" in status and alarm_time is None:
            alarm_time = t

        if step % 35 == 0 or step == steps - 1:
            print(f"{t:7.3f} s | {mu:11.2f}   | {theta_hat[0]:11.4f} | {theta_hat[1]:10.4f} | {max_eig:12.6f} | {status}")

    print("-" * 84)
    print(f" -> Mode Shift Initiated at t = 0.100 s")
    print(f" -> Early Drift Warning Triggered at t = {warn_time:.3f} s (+{(warn_time - 0.10)*1000:.1f} ms latency)")
    print(f" -> Critical GFL-Fallback Alarm at   t = {alarm_time:.3f} s (+{(alarm_time - 0.10)*1000:.1f} ms latency)")
    print("=" * 84)

if __name__ == "__main__":
    run_gfm_to_gfl_detection_test()
