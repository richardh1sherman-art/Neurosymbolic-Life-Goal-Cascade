import numpy as np

# Parameters
lam = 0.5       # contraction rate
gamma = 1.5     # H-infinity gain
dt = 0.05
t = np.arange(0, 15, dt)
R = np.zeros_like(t)

# Initial condition
R[0] = 0.1

# Define time-varying noise/disturbance norm ||w(t)||
# Let's create a scenario where noise peaks, then drops, then peaks again
w_norm = np.zeros_like(t)
for i, ti in enumerate(t):
    if 2.0 <= ti < 5.0:
        w_norm[i] = 1.0  # Heavy cloud passing / noise spike
    elif 5.0 <= ti < 9.0:
        w_norm[i] = 0.1  # Calm operation
    elif 9.0 <= ti < 12.0:
        w_norm[i] = 0.8  # Second volatile front
    else:
        w_norm[i] = 0.0  # Fully stable grid

# Euler forward simulation of dot(R) = -lam * R + gamma * w_norm
for i in range(len(t) - 1):
    R_dot = -lam * R[i] + gamma * w_norm[i]
    R[i+1] = R[i] + R_dot * dt

# Print select data points to ensure accuracy and use for description
indices = [0, int(2.0/dt), int(5.0/dt), int(9.0/dt), int(12.0/dt), len(t)-1]
for idx in indices:
    print(f"t={t[idx]:.1f}, w_norm={w_norm[idx]:.1f}, R={R[idx]:.4f}")
