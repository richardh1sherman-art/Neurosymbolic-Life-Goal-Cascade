import numpy as np


def numerical_jacobian(func, x, eps=1e-6):
    """Computes df/dx via central finite differences."""
    x = np.asarray(x, dtype=float)
    f0 = np.asarray(func(x), dtype=float)
    J = np.zeros((f0.size, x.size))
    for i in range(x.size):
        dx = np.zeros_like(x)
        dx[i] = eps
        f_plus = np.asarray(func(x + dx), dtype=float)
        f_minus = np.asarray(func(x - dx), dtype=float)
        J[:, i] = (f_plus - f_minus) / (2.0 * eps)
    return J


class ExtendedSaltedKalmanRPEM:
    """
    Method #1: Extended Salted Kalman Filter (ESKF) + Recursive PEM (RPEM)
    for hybrid continuous/discrete-event nonlinear electrical systems.
    """

    def __init__(
        self,
        x0,
        P0,
        theta0,
        P_theta0,
        f_modes,
        h_modes,
        guard_fn,
        reset_fn,
        Qc,
        R,
        dt,
        Q_jump=None,
        lam=0.99,
        blanking_steps=5,
        nis_threshold=15.0,
    ):
        self.x = np.array(x0, dtype=float)
        self.P = np.array(P0, dtype=float)
        self.theta = np.array(theta0, dtype=float)
        self.P_theta = np.array(P_theta0, dtype=float)

        self.f_modes = f_modes
        self.h_modes = h_modes
        self.guard_fn = guard_fn
        self.reset_fn = reset_fn

        self.Qc = np.array(Qc, dtype=float)
        self.R = np.array(R, dtype=float)
        self.dt = float(dt)
        self.Q_jump = (
            np.zeros_like(self.P)
            if Q_jump is None
            else np.array(Q_jump, dtype=float)
        )

        self.lam = float(lam)
        self.blanking_steps = int(blanking_steps)
        self.nis_threshold = float(nis_threshold)

        self.n = self.x.size
        self.p = self.theta.size
        self.W = np.zeros((self.n, self.p))
        self.mode = 1
        self.blanking_counter = 0

    def rk4_step(self, f, x, u, theta, dt):
        """4th-order Runge-Kutta integration step."""
        k1 = f(x, u, theta)
        k2 = f(x + 0.5 * dt * k1, u, theta)
        k3 = f(x + 0.5 * dt * k2, u, theta)
        k4 = f(x + dt * k3, u, theta)
        return x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def predict(self, u):
        """Step 2: Continuous-time state and covariance propagation."""
        f = self.f_modes[self.mode]
        x_pred = self.rk4_step(f, self.x, u, self.theta, self.dt)

        A_k = numerical_jacobian(lambda x_: f(x_, u, self.theta), self.x)
        F_k = np.eye(self.n) + A_k * self.dt
        Qd = self.Qc * self.dt

        P_pred = F_k @ self.P @ F_k.T + Qd
        self.x = x_pred
        self.P = P_pred
        return F_k

    def detect_jump(self, y, u, external_trigger=False):
        """Detects discrete switching via explicit trigger or NIS spike."""
        if external_trigger:
            return True

        h = self.h_modes[self.mode]
        e = y - h(self.x, u, self.theta)
        H = numerical_jacobian(lambda x_: h(x_, u, self.theta), self.x)
        S = H @ self.P @ H.T + self.R
        nis = float(e.T @ np.linalg.solve(S, e))
        return nis > self.nis_threshold

    def apply_saltation(self, u, next_mode):
        """Step 3: Saltation Matrix covariance mapping across mode jump."""
        f_minus = self.f_modes[self.mode](self.x, u, self.theta)
        x_plus = self.reset_fn(self.x)
        f_plus = self.f_modes[next_mode](x_plus, u, self.theta)

        D_R = numerical_jacobian(self.reset_fn, self.x)
        grad_g_T = numerical_jacobian(
            lambda x_: np.atleast_1d(self.guard_fn(x_, u)), self.x
        )

        denom = float(np.squeeze(grad_g_T @ f_minus))
        if abs(denom) < 1e-9:
            denom = np.sign(denom) * 1e-9 if denom != 0 else 1e-9

        numerator = (f_plus - D_R @ f_minus).reshape(-1, 1) @ grad_g_T
        Xi = D_R + numerator / denom

        self.x = x_plus
        self.P = Xi @ self.P @ Xi.T + self.Q_jump
        self.mode = next_mode
        self.blanking_counter = self.blanking_steps
        return Xi

    def update(self, y, u, F_k):
        """Steps 4 & 5: EKF measurement update + Recursive PEM update."""
        f = self.f_modes[self.mode]
        h = self.h_modes[self.mode]

        # EKF Measurement Update
        y_pred = h(self.x, u, self.theta)
        e_k = y - y_pred

        H_k = numerical_jacobian(lambda x_: h(x_, u, self.theta), self.x)
        S_k = H_k @ self.P @ H_k.T + self.R
        K_k = self.P @ H_k.T @ np.linalg.inv(S_k)

        self.x = self.x + K_k @ e_k
        I_KH = np.eye(self.n) - K_k @ H_k
        self.P = I_KH @ self.P @ I_KH.T + K_k @ self.R @ K_k.T

        # Recursive PEM Parameter Update
        df_dtheta = numerical_jacobian(lambda th_: f(self.x, u, th_), self.theta)
        dh_dtheta = numerical_jacobian(lambda th_: h(self.x, u, th_), self.theta)
        Psi_k = H_k @ self.W + dh_dtheta

        if self.blanking_counter > 0:
            self.blanking_counter -= 1
        else:
            denom_theta = self.lam * S_k + Psi_k @ self.P_theta @ Psi_k.T
            L_k = self.P_theta @ Psi_k.T @ np.linalg.inv(denom_theta)
            self.theta = self.theta + L_k @ e_k
            self.P_theta = (np.eye(self.p) - L_k @ Psi_k) @ self.P_theta / self.lam

        self.W = F_k @ I_KH @ self.W + (
            df_dtheta * self.dt - F_k @ K_k @ dh_dtheta
        )
        return self.x.copy(), self.theta.copy(), e_k

    def step(self, y, u, external_jump_flag=False, candidate_next_mode=None):
        """Full single-sample observer step."""
        F_k = self.predict(u)
        jumped = self.detect_jump(y, u, external_trigger=external_jump_flag)

        Xi = None
        if jumped:
            next_mode = (
                candidate_next_mode
                if candidate_next_mode is not None
                else (2 if self.mode == 1 else 1)
            )
            Xi = self.apply_saltation(u, next_mode)

        x_est, theta_est, residual = self.update(y, u, F_k)
        return {
            "x": x_est,
            "theta": theta_est,
            "mode": self.mode,
            "jumped": jumped,
            "saltation_matrix": Xi,
            "residual": residual,
        }
