import numpy as np
from eskf_rpem import ExtendedSaltedKalmanRPEM


def f_online(x, u, theta):
    delta, omega, V = x
    P_ref, V_ref = u
    B_eff = theta[0]
    ddelta = omega
    domega = (P_ref - B_eff * V * np.sin(delta) - 0.5 * omega) / 0.1
    dV = (V_ref - V - 0.05 * B_eff * (1.0 - np.cos(delta))) / 0.02
    return np.array([ddelta, domega, dV])


def f_offline(x, u, theta):
    delta, omega, V = x
    P_ref, V_ref = u
    B_eff = theta[0]
    ddelta = omega
    domega = (P_ref - 0.6 * B_eff * V * np.sin(delta) - 0.5 * omega) / 0.1
    dV = (V_ref - V - 0.08 * B_eff * (1.0 - np.cos(delta))) / 0.02
    return np.array([ddelta, domega, dV])


def h_online(x, u, theta):
    delta, _, V = x
    B_eff = theta[0]
    return np.array([V, B_eff * V * np.sin(delta)])


def h_offline(x, u, theta):
    delta, _, V = x
    B_eff = theta[0]
    return np.array([V, 0.6 * B_eff * V * np.sin(delta)])


def guard_fn(x, u):
    # Scalar guard surface g(x, u) = V_mag - 0.92
    return x[2] - 0.92


def reset_fn(x_minus):
    return x_minus.copy()


def main():
    dt = 1.0 / 120.0

    observer = ExtendedSaltedKalmanRPEM(
        x0=[0.2, 0.0, 1.0],
        P0=np.diag([1e-3, 1e-3, 1e-3]),
        theta0=[4.5],
        P_theta0=np.array([[0.1]]),
        f_modes={1: f_online, 2: f_offline},
        h_modes={1: h_online, 2: h_offline},
        guard_fn=guard_fn,
        reset_fn=reset_fn,
        Qc=np.diag([1e-5, 1e-4, 1e-5]),
        R=np.diag([1e-4, 1e-4]),
        dt=dt,
        Q_jump=np.diag([1e-4, 1e-3, 1e-4]),
        lam=0.985,
        blanking_steps=8,
        nis_threshold=30.0,
    )

    rng = np.random.default_rng(42)
    x_true = np.array([0.2, 0.0, 1.0])
    theta_true = np.array([5.0])
    u_cmd = np.array([0.95, 1.0])

    for k in range(300):
        true_mode = 1 if k < 150 else 2
        f_true = f_online if true_mode == 1 else f_offline
        h_true = h_online if true_mode == 1 else h_offline

        x_true = observer.rk4_step(f_true, x_true, u_cmd, theta_true, dt)
        y_meas = h_true(x_true, u_cmd, theta_true) + rng.normal(0, 0.01, size=2)

        dv_dt_trigger = (k == 150)
        out = observer.step(y_meas, u_cmd, external_jump_flag=dv_dt_trigger)

        if k in (149, 150, 151, 299):
            x_str = np.round(out["x"], 4)
            th_val = float(out["theta"][0])
            print(
                f"k={k:3d} | Mode={out['mode']} | Jumped={str(out['jumped']):5s} | "
                f"x_est={x_str} | theta_est={th_val:.4f} (true=5.0)"
            )


if __name__ == "__main__":
    main()
