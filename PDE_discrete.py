import numpy as np
import matplotlib
matplotlib.use('Agg')  # Prevents GUI crash on the headless DGX
import matplotlib.pyplot as plt
from scipy.special import gamma

# 1. Simulation Parameters
t_max = 10.0          # Total simulation time
dt = 0.05             # Time step size
N = int(t_max / dt)   # Total number of steps
time_steps = np.arange(N) * dt

beta = 0.7            # Fractal boundary order (0 < beta < 1)
A = 1.0               # Control amplitude scaling factor

# 2. Compute Grünwald-Letnikov Binomial Memory Weights
weights = np.zeros(N)
weights[0] = 1.0
for k in range(1, N):
    weights[k] = weights[k-1] * (1.0 - (beta + 1.0) / k)

# 3. Generate the Scale-Invariant Control Trajectory
# According to our fractional matching, the boundary temperature must scale as:
u_boundary_target = A * gamma(2.0 - beta) * time_steps

# 4. Compute the Fractional Response to verify the control loop matches the target
# We track what the fractional derivative evaluates to at each step using the memory window
fractional_derivative_response = np.zeros(N)
for n in range(1, N):
    # Perform a discrete convolution of the historical states with the GL weights
    history = u_boundary_target[:n+1]
    flipped_weights = weights[:n+1][::-1]
    fractional_derivative_response[n] = np.sum(history * flipped_weights) / (dt**beta)

# 5. Plotting the Control Action and System Memory Response
plt.figure(figsize=(10, 5))

# Plot the continuous temperature profile being injected at x=0
plt.subplot(1, 2, 1)
plt.plot(time_steps, u_boundary_target, 'b-', label=r'$u(0, t)$ Control Input')
plt.title("Discrete-Time Boundary Control Input")
plt.xlabel("Time (t)")
plt.ylabel("Temperature Surface Value")
plt.grid(True)
plt.legend()

# Plot the verified fractional flux response, matching the theoretical target power-law: A * t^(1-beta)
plt.subplot(1, 2, 2)
plt.plot(time_steps[1:], fractional_derivative_response[1:], 'r--', label=r'Measured $\mathcal{D}_t^\beta u$')
plt.plot(time_steps[1:], A * (time_steps[1:]**(1.0 - beta)), 'k:', alpha=0.7, label=r'Theoretical Target $A t^{1-\beta}$')
plt.title(f"Fractal Memory Flux Balance (Order $\\beta$ = {beta})")
plt.xlabel("Time (t)")
plt.ylabel("Flux Response")
plt.grid(True)
plt.legend()

plt.tight_layout()
#plt.show()
plt.savefig('fractal_control_results.png')
plt.tight_layout()
plt.savefig('fractal_control_results.png', dpi=300)
print("Simulation complete. Image saved to disk.")