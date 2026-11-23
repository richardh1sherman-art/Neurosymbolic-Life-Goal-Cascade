from collections import deque
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
    upgraded with Alleaume et al.'s Two-Matrix Saltation Covariance Update (Xi_1, Xi_2)
    and Ring-Buffer Rollback for unknown jump times (delta_t > 0).
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
        rollback_steps=0,
        use_two_matrix_xi2=True,
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
        self.rollback_steps = int(rollback_steps)
        self.use_two_matrix_xi2 = bool(use_two_matrix_xi2)

        self.n = self.x.size
        self.p = self.theta.size
        self.W = np.zeros((self.n, self.p))
        self.mode = 1
        self.blanking_counter = 0
        self.history = deque(maxlen=max(6, self.rollback_steps + 2))

    def rk4_step(self, f, x, u, theta, dt):
        """4th-order Runge-Kutta integration step."""
        k1 = f(x, u, theta)
        k2 = f(x + 0.5 * dt * k1, u, theta)
        k3 = f(x + 0.5 * dt * k2, u, theta)
        k4 = f(x + dt * k3, u, theta)
        return x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def predict(self, u):
        """Continuous-time state and covariance propagation."""
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
            return True, 0.0

        h = self.h_modes[self.mode]
        e = y - h(self.x, u, self.theta)
        H = numerical_jacobian(lambda x_: h(x_, u, self.theta), self.x)
        S = H @ self.P @ H.T + self.R
        nis = float(e.T @ np.linalg.solve(S, e))
        return (nis > self.nis_threshold), nis

    def compute_saltation_matrices(self, x_ref, u, curr_mode, next_mode, lag_dt=0.0):
        """
        Computes:
          Xi_1: Classical plant-jump saltation matrix at switching guard g(x, u) = 0.
          Xi_2: Alleaume et al. output-derivative mismatch saltation matrix over detection lag lag_dt.
        """
        f_minus = self.f_modes[curr_mode](x_ref, u, self.theta)
        x_plus = self.reset_fn(x_ref)
        f_plus = self.f_modes[next_mode](x_plus, u, self.theta)

        D_R = numerical_jacobian(self.reset_fn, x_ref)
        grad_g_T = numerical_jacobian(
            lambda x_: np.atleast_1d(self.guard_fn(x_, u)), x_ref
        )

        denom = float(np.squeeze(grad_g_T @ f_minus))
        if abs(denom) < 1e-9:
            denom = np.sign(denom) * 1e-9 if denom != 0 else 1e-9

        Xi_1 = D_R + ((f_plus - D_R @ f_minus).reshape(-1, 1) @ grad_g_T) / denom

        if lag_dt > 0.0 and self.use_two_matrix_xi2:
            h_minus = self.h_modes[curr_mode](x_ref, u, self.theta)
            h_plus = self.h_modes[next_mode](x_plus, u, self.theta)
            H_k = numerical_jacobian(lambda x_: self.h_modes[next_mode](x_, u, self.theta), x_plus)
            S_k = H_k @ self.P @ H_k.T + self.R
            L_obs = (self.P @ H_k.T @ np.linalg.inv(S_k)) / max(self.dt, 1e-6)
            mismatch_vec = (f_plus - f_minus) - L_obs @ (h_plus - h_minus)
            Xi_2 = np.eye(self.n) + (mismatch_vec.reshape(-1, 1) @ grad_g_T) * (lag_dt / denom)
        else:
            Xi_2 = np.eye(self.n)

        return Xi_1, Xi_2, x_plus

    def apply_saltation(self, u, next_mode, lag_dt=0.0):
        """Applies single-matrix (lag_dt == 0) or two-matrix (lag_dt > 0) saltation covariance map."""
        Xi_1, Xi_2, x_plus = self.compute_saltation_matrices(self.x, u, self.mode, next_mode, lag_dt=lag_dt)
        Xi_tot = Xi_2 @ Xi_1
        self.x = x_plus
        self.P = Xi_tot @ self.P @ Xi_tot.T + (self.Q_jump if lag_dt == 0.0 else 0.25 * self.Q_jump)
        self.mode = next_mode
        self.blanking_counter = self.blanking_steps
        return Xi_1, Xi_2

    def update(self, y, u, F_k):
        """EKF measurement update + Recursive PEM parameter update."""
        f = self.f_modes[self.mode]
        h = self.h_modes[self.mode]

        y_pred = h(self.x, u, self.theta)
        e_k = y - y_pred

        H_k = numerical_jacobian(lambda x_: h(x_, u, self.theta), self.x)
        S_k = H_k @ self.P @ H_k.T + self.R
        K_k = self.P @ H_k.T @ np.linalg.inv(S_k)

        self.x = self.x + K_k @ e_k
        I_KH = np.eye(self.n) - K_k @ H_k
        self.P = I_KH @ self.P @ I_KH.T + K_k @ self.R @ K_k.T

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

        self.W = F_k @ I_KH @ self.W + (df_dtheta * self.dt - F_k @ K_k @ dh_dtheta)
        return self.x.copy(), self.theta.copy(), e_k

    def step(self, y, u, external_jump_flag=False):
        """Full predict -> jump-detect (with optional ring-buffer rollback or Xi_2) -> update cycle."""
        y = np.asarray(y, dtype=float)
        u = np.asarray(u, dtype=float)

        F_k = self.predict(u)
        jumped, nis = self.detect_jump(y, u, external_trigger=external_jump_flag)

        if jumped:
            next_mode = 2 if self.mode == 1 else 1
            # Option 2: Ring-Buffer Rollback (rewinds to true inflection step k - delta_k so lag_dt = 0)
            if (not external_jump_flag) and self.rollback_steps > 0 and len(self.history) >= self.rollback_steps:
                replay_items = [self.history.pop() for _ in range(self.rollback_steps)]
                replay_items.reverse()
                snap = replay_items.pop(0)
                self.x, self.P, self.theta, self.P_theta, self.W, self.mode = snap["state"]
                self.apply_saltation(snap["u"], next_mode, lag_dt=0.0)
                F_rep = self.predict(snap["u"])
                self.update(snap["y"], snap["u"], F_rep)
                for item in replay_items:
                    F_rep = self.predict(item["u"])
                    self.update(item["y"], item["u"], F_rep)
                F_k = self.predict(u)
            else:
                # Option 1: Two-Matrix Saltation Covariance Update (Xi_1 + Xi_2) for unknown jump lag
                lag_dt = 0.0 if external_jump_flag else (2.0 * self.dt)
                self.apply_saltation(u, next_mode, lag_dt=lag_dt)

        x_est, th_est, innov = self.update(y, u, F_k)
        self.history.append({
            "state": (self.x.copy(), self.P.copy(), self.theta.copy(), self.P_theta.copy(), self.W.copy(), self.mode),
            "y": y.copy(),
            "u": u.copy(),
        })
        return {
            "x": x_est,
            "theta": th_est,
            "mode": self.mode,
            "jumped": jumped,
            "nis": nis,
            "innovation": innov,
        }
