from dataclasses import dataclass
import numpy as np


@dataclass
class ConformalTubeCertificate:
    """Holds the calibrated conformal safety offset and empirical coverage stats."""

    quantile_offset_q: float
    target_coverage: float
    empirical_test_coverage: float
    calibration_samples: int


class LocalAreaNeuralSurrogate:
    """
    Lightweight ridge/MLP-style feature surrogate predicting worst-case tie-line
    excursion r_true(T) over [0, 15s] from (14-bit topology word, x_0, theta_hat).
    (Can be swapped with any PyTorch/ONNX MLP with zero changes to calibration.)
    """

    def __init__(self, reg_lambda: float = 1e-3):
        self.reg_lambda = reg_lambda
        self.weights: np.ndarray = None

    @staticmethod
    def _featurize(words_14bit: np.ndarray, x0: np.ndarray, theta_hat: np.ndarray) -> np.ndarray:
        """Builds nonlinear polynomial/interaction features from discrete bits + continuous states."""
        # words_14bit: (N, 14), x0: (N, n_x), theta_hat: (N, n_theta)
        base = np.hstack([words_14bit, x0, theta_hat])
        quad = base**2
        # Cross-interaction between key breaker bits and continuous state norm
        interactions = words_14bit[:, :4] * np.linalg.norm(x0, axis=1, keepdims=True)
        bias = np.ones((base.shape[0], 1))
        return np.hstack([bias, base, quad, interactions])

    def fit(self, words_14bit: np.ndarray, x0: np.ndarray, theta_hat: np.ndarray, r_true: np.ndarray):
        Phi = self._featurize(words_14bit, x0, theta_hat)
        eye = self.reg_lambda * np.eye(Phi.shape[1])
        eye[0, 0] = 0.0  # Do not regularize bias
        self.weights = np.linalg.solve(Phi.T @ Phi + eye, Phi.T @ r_true)

    def predict(self, words_14bit: np.ndarray, x0: np.ndarray, theta_hat: np.ndarray) -> np.ndarray:
        Phi = self._featurize(words_14bit, x0, theta_hat)
        return np.maximum(0.0, Phi @ self.weights)


def calibrate_split_conformal_tube(
    surrogate: LocalAreaNeuralSurrogate,
    cal_words: np.ndarray,
    cal_x0: np.ndarray,
    cal_theta: np.ndarray,
    cal_r_true: np.ndarray,
    alpha: float = 0.005,
) -> float:
    """
    Computes the exact finite-sample Split Conformal quantile q_{1-alpha}
    such that P(r_true <= r_pred + q_{1-alpha}) >= 1 - alpha.
    """
    M = len(cal_r_true)
    r_pred = surrogate.predict(cal_words, cal_x0, cal_theta)

    # One-sided nonconformity score: positive when NN under-predicts true EMT excursion
    scores = cal_r_true - r_pred

    # Exact finite-sample order statistic index: ceil((M + 1) * (1 - alpha))
    k_idx = int(np.ceil((M + 1) * (1.0 - alpha))) - 1
    k_idx = min(max(k_idx, 0), M - 1)

    sorted_scores = np.sort(scores)
    q_hat = float(sorted_scores[k_idx])
    return q_hat


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # Synthetic Caltech EMT rollout dataset for a single Area (1,500 rollouts)
    N_total = 1500
    raw_words = [
        "00101010111010",  # Nominal baseline
        "01001010111100",  # Sub-feeder swap
        "01010101011010",  # Alt bus + bank
        "00101010100010",  # Upgraded nominal
        "11001010100011",  # Coordinated isolation
    ]
    word_bank = np.array([[int(b) for b in w] for w in raw_words], dtype=float)

    words = word_bank[rng.integers(0, len(word_bank), size=N_total)]
    x0 = rng.normal(0.0, 0.12, size=(N_total, 3))
    theta_hat = rng.uniform(0.8, 1.2, size=(N_total, 2))

    # True worst-case EMT tie-line excursion over [0, 15s] (nonlinear + heavy-tailed switching spike)
    isolation_stress = 0.045 * words[:, 0] + 0.020 * words[:, 9]
    nonlinear_swing = 0.18 * np.sum(x0**2, axis=1) + 0.05 * np.linalg.norm(x0, axis=1) / theta_hat[:, 0]
    heavy_tail_noise = rng.exponential(scale=0.006, size=N_total)
    r_true = isolation_stress + nonlinear_swing + heavy_tail_noise

    # Split into Train (800), Calibration (400), and Held-Out Test (300)
    surrogate = LocalAreaNeuralSurrogate(reg_lambda=1e-3)
    surrogate.fit(words[:800], x0[:800], theta_hat[:800], r_true[:800])

    alpha_target = 0.01  # 99.0% guaranteed coverage
    q_hat = calibrate_split_conformal_tube(
        surrogate, words[800:1200], x0[800:1200], theta_hat[800:1200], r_true[800:1200], alpha=alpha_target
    )

    # Verify empirical coverage on unseen test rollouts
    test_preds = surrogate.predict(words[1200:], x0[1200:], theta_hat[1200:])
    certified_bounds = test_preds + q_hat
    empirical_cov = float(np.mean(r_true[1200:] <= certified_bounds))

    print("=== Distributed Area Conformal Reachable-Tube Calibration ===")
    print(f"  Target Coverage (1 - alpha):    {(1.0 - alpha_target) * 100:.2f}%")
    print(f"  Calibrated Safety Offset (q):   +{q_hat:.5f} pu")
    print(f"  Empirical Test Coverage:        {empirical_cov * 100:.2f}%")
    print(f"  Sample Certified Epsilon Bound: {certified_bounds[0]:.5f} pu (ready for Pontryagin erosion)")
