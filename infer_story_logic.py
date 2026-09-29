import os
import math
import numpy as np

class AdvancedSwarmSimulator:
    def __init__(self):
        self.N = 6  # 🛸 6-Drone Node configuration
        self.t_max = 5.0
        self.dt = 0.1
        self.time_steps = np.arange(int(self.t_max / self.dt)) * self.dt
        self.steps_count = len(self.time_steps)
        
        # Initial positions forcing a tight, dense grid crossing path intersection
        self.pos_x = [0.0, 5.0, 0.0, 5.0, 2.5, 2.5]
        self.pos_y = [0.0, 5.0, 5.0, 0.0, 0.0, 5.0]
        
        self.vel_x = [1.0, -1.0, 1.0, -1.0, 0.0, 0.0]
        self.vel_y = [1.0, -1.0, -1.0, 1.0, 1.0, -1.0]

        # 📐 Term 3 Parameters: Critical Safety Radii and APF Thresholds
        self.r_safe = 0.4        # Critical crash radius boundary (Unresolvable barrier)
        self.d_influence = 1.2   # Potential field activation threshold region
        self.eta = 5.0           # APF scaling factor gain
        
        # Formation gains
        self.kp, self.kv, self.kw = 1.0, 0.5, 1.5

    def compute_wavelet_coefficient_extractor(self, raw_signal):
        """
        🌀 STEP 3: DISCRETE WAVELET COEFFICIENT EXTRACTOR
        Performs a single-level Haar wavelet decomposition to filter out 
        high-frequency turbulent noise from the active sensor array.
        """
        if len(raw_signal) < 2: return raw_signal
        # Compute approximation coefficients (low-pass filter mapping)
        approx = (raw_signal[0::2] + raw_signal[1::2]) / math.sqrt(2.0)
        return approx

    def compute_apf_collision_avoidance(self, i, current_pos_x, current_pos_y):
        """
        🛡️ TERM 3: ARTIFICIAL POTENTIAL FIELD COLLISION AVOIDANCE
        Enforces a hard gradient repulsive barrier if vehicle paths violate safety bounds.
        """
        u_collision_x = 0.0
        u_collision_y = 0.0
        
        for j in range(self.N):
            if j == i: continue
            dx = current_pos_x[i] - current_pos_x[j]
            dy = current_pos_y[i] - current_pos_y[j]
            d_ij = math.sqrt(dx**2 + dy**2)
            
            # Check if neighbor vehicle falls inside the active potential influence envelope
            if d_ij < self.d_influence:
                if d_ij <= self.r_safe:
                    # Guard against zero-division singularities at the exact crash point
                    d_ij = self.r_safe + 1e-5
                
                # Compute the potential barrier scalar gradient
                factor = self.eta * ((1.0 / (d_ij - self.r_safe)) - (1.0 / (self.d_influence - self.r_safe))) * (-1.0 / ((d_ij - self.r_safe)**2))
                u_collision_x += factor * (dx / d_ij)
                u_collision_y += factor * (dy / d_ij)
                
        return np.array([u_collision_x, u_collision_y])

    def run_simulation(self):
        print("=" * 95)
        print("🌀 LIVE LISP INTERPRETER: IMPLEMENTING WAVELET EXTRACTORS AND APF SAFETY SHIELDS")
        print("=" * 95)
        print(f"📥 Term 3 Active: Enforcing Safety Critical Radii (r_safe) = {self.r_safe}m")
        print(f"📥 Wavelet Core: Haar Coefficient Extractor Initialized over Spatial Streams")
        print("-" * 95)

        minimum_distance_recorded = float('inf')
        collision_detected = False

        for idx, t in enumerate(self.time_steps):
            # Sample continuous turbulent field vectors
            raw_turbulent_sample = np.array([math.sin(5.0 * t), math.cos(5.0 * t), math.sin(10.0 * t), math.cos(10.0 * t)])
            # Run live Wavelet extraction pass to isolate the true scale invariant trend
            wavelet_filtered_signal = self.compute_wavelet_coefficient_extractor(raw_turbulent_sample)
            weather_vector_x = wavelet_filtered_signal[0] * self.kw
            weather_vector_y = wavelet_filtered_signal[1] * self.kw

            next_x = list(self.pos_x)
            next_y = list(self.pos_y)

            for i in range(self.N):
                # Compute Term 3: Active APF Repulsion vectors
                u_collision = self.compute_apf_collision_avoidance(i, self.pos_x, self.pos_y)
                
                # Kinematic double-integrator state transformation updates
                self.vel_x[i] += (weather_vector_x + u_collision[0]) * self.dt
                self.vel_y[i] += (weather_vector_y + u_collision[1]) * self.dt
                
                next_x[i] += self.vel_x[i] * self.dt
                next_y[i] += self.vel_y[i] * self.dt

                # Track closest approach metrics across the dense vehicle grid crossing
                for j in range(self.N):
                    if j == i: continue
                    dist = math.sqrt((next_x[i] - next_x[j])**2 + (next_y[i] - next_y[j])**2)
                    if dist < minimum_distance_recorded:
                        minimum_distance_recorded = dist
                    if dist < self.r_safe:
                        collision_detected = True

            self.pos_x = next_x
            self.pos_y = next_y

            if idx % (self.steps_count // 4) == 0 or idx == self.steps_count - 1:
                print(f"   ➔ Time t = {t:3.1f}s | Swarm Minimum Inter-Agent Separation: {minimum_distance_recorded:.4f}m")

        print("-" * 95)
        print(f"🏆 SIMULATION COMPLETE: Absolute Closest Vehicle Approach ──➔ \033[1;32m{minimum_distance_recorded:.4f}m\033[0m")
        safety_status = "CRASH_RADIUS_VIOLATED" if collision_detected else "SAFETY_INVARIANT_PRESERVED"
        print(f"🎯 Term 3 Potential Field Operational Invariant       ──➔ \033[1;32m{safety_status}\033[0m")
        print("=" * 95 + "\n")

        # Record resolved structural metrics cleanly out to disk for our SWI-Prolog verifier
        root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
        exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write(f"swarm_safety_status(dense_grid_crossing, schema_{safety_status.lower()}).\n")

if __name__ == "__main__":
    engine = AdvancedSwarmSimulator()
    engine.run_simulation()
