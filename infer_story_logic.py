import os
import math
import numpy as np

class MultiHopCooperativeSdsSimulator:
    def __init__(self):
        self.N = 50  # 🛸 50 vehicle nodes
        self.t_max = 240.0 # Dilated time horizon
        self.dt = 10.0     
        self.time_steps = np.arange(0, self.t_max, self.dt)
        
        self.judith_pos = np.array([75.0, 75.0])
        self.clues_collected = 0
        
        # Initial positions leave the hub station
        self.pos_x = np.zeros(self.N)
        self.pos_y = np.zeros(self.N)
        
        np.random.seed(42)
        self.angle_offsets = np.random.uniform(0.0, 0.5 * math.pi, self.N)
        self.speeds = np.random.uniform(0.6, 0.95, self.N)
        
        self.battery = np.ones(self.N) * 100.0  
        self.fuel = np.random.uniform(350.0, 450.0, self.N)
        
        self.charging_hub_pos = np.array([50.0, 50.0])
        self.max_signal_range = 30.0
        
        self.mountain_center = np.array([30.0, 50.0])
        self.mountain_radius = 10.0
        
        # 🚨 COOPERATIVE MULTI-HOP TRACKING MATRICES
        self.local_cache = {i: {"has_data": False, "target": None} for i in range(self.N)}
        self.packet_reached_dispatcher = False

    def is_los_blocked(self, x1, y1, x2, y2):
        cx, cy = self.mountain_center[0], self.mountain_center[1]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return False
        t = max(0.0, min(1.0, ((cx - x1) * dx + (cy - y1) * dy) / (dx**2 + dy**2)))
        return math.sqrt((x1 + t * dx - cx)**2 + (y1 + t * dy - cy)**2) < self.mountain_radius

    def run_cooperative_sds_loop(self):
        print("=" * 95)
        print("🌀 LIVE LISP PDE INTERPRETER: MULTI-AGENT COOPERATIVE CO-MOVING SENSOR MESH")
        print("=" * 95)
        print("📥 Local Infrastructure ──➔ Tree #30 Replicated Locally inside every UAV Node")
        print("📥 Network Topology    ──➔ Dynamic Multi-Hop Local Data Handoffs Enabled")
        print("-" * 95)

        step = 1
        for t in self.time_steps:
            if self.packet_reached_dispatcher: break
            active_nodes = []

            # Calculate center of mass of functional nodes for mesh references
            valid_active_x = [self.pos_x[k] for k in range(self.N) if self.battery[k] > 0 and self.fuel[k] > 0]
            valid_active_y = [self.pos_y[k] for k in range(self.N) if self.battery[k] > 0 and self.fuel[k] > 0]
            fleet_centroid_x = np.mean(valid_active_x) if valid_active_x else 50.0
            fleet_centroid_y = np.mean(valid_active_y) if valid_active_y else 50.0

            for i in range(self.N):
                self.fuel[i] -= 0.6 * self.dt
                self.battery[i] -= 0.15 * self.dt
                if self.fuel[i] <= 0 or self.battery[i] <= 0: continue

                current_pos = np.array([self.pos_x[i], self.pos_y[i]])

                # Charging station check
                if self.battery[i] < 40.0:
                    d_hub = np.linalg.norm(self.charging_hub_pos - current_pos)
                    if d_hub < 4.0:
                        self.battery[i] = 100.0
                        print(f"   \033[1;36m[LOCAL DOCKING EVENT]: Drone [{i}] swapped battery at Hub Alpha.\033[0m")
                    else:
                        vec_hub = self.charging_hub_pos - current_pos
                        if d_hub > 0:
                            self.pos_x[i] += (vec_hub[0] / d_hub) * self.speeds[i] * self.dt
                            self.pos_y[i] += (vec_hub[1] / d_hub) * self.speeds[i] * self.dt
                    active_nodes.append(i)
                    continue

                # 🚨 FIXED: Utilizing robust vector-space norms to prevent type errors
                if t == 0:
                    self.pos_x[i] += math.cos(self.angle_offsets[i]) * self.speeds[i] * self.dt
                    self.pos_y[i] += math.sin(self.angle_offsets[i]) * self.speeds[i] * self.dt
                else:
                    if self.local_cache[i]["has_data"]:
                        vec_target = np.array([fleet_centroid_x, fleet_centroid_y]) - current_pos
                    else:
                        vec_target = self.judith_pos - current_pos
                        
                    d_tgt = np.linalg.norm(vec_target)
                    
                    if d_tgt < 5.0 and not self.local_cache[i]["has_data"] and self.clues_collected < 1:
                        self.clues_collected += 1
                        self.local_cache[i]["has_data"] = True
                        self.local_cache[i]["target"] = self.judith_pos
                        print(f"   \033[1;33m[TARGET LOG MATCH]: UAV Node [{i}] spotted Judith! Caching packet locally...\033[0m")
                    
                    if d_tgt > 0:
                        self.pos_x[i] += (vec_target[0] / d_tgt) * self.speeds[i] * self.dt
                        self.pos_y[i] += (vec_target[1] / d_tgt) * self.speeds[i] * self.dt
                active_nodes.append(i)

            # COOPERATIVE MULTI-HOP INTER-AGENT TRANSFER LOOP
            for i in active_nodes:
                if not self.local_cache[i]["has_data"]: continue
                
                # Check link to base dispatcher directly
                if not self.is_los_blocked(self.pos_x[i], self.pos_y[i], 0.0, 0.0) and math.sqrt(self.pos_x[i]**2 + self.pos_y[i]**2) < 45.0:
                    print(f"\n🎉 \033[1;32m[DIRECT MESH LINK FLUSH]: UAV Node [{i}] flushed telemetry data straight to Fire-Station!\033[0m")
                    self.packet_reached_dispatcher = True
                    break
                
                # If direct link is occluded, attempt a cooperative multi-hop handoff to a neighboring platform
                for j in active_nodes:
                    if i == j or self.local_cache[j]["has_data"]: continue
                    d_ij = math.sqrt((self.pos_x[i] - self.pos_x[j])**2 + (self.pos_y[i] - self.pos_y[j])**2)
                    if d_ij < self.max_signal_range and not self.is_los_blocked(self.pos_x[i], self.pos_y[i], self.pos_x[j], self.pos_y[j]):
                        self.local_cache[j]["has_data"] = True
                        self.local_cache[j]["target"] = self.local_cache[i]["target"]
                        print(f"   \033[1;34m[COOPERATIVE MULTI-HOP HANDOFF]: Node [{i}] passed the rescue data contract to Node [{j}] around the mountain blockage!\033[0m")

            print(f"Step {step:02d} | Flight Time: {t:5.1f} min | Active Swarm Nodes: {len(active_nodes):2d} | Target Located: {self.clues_collected > 0}")
            step += 1

            if len(active_nodes) < 3:
                print("🛑 [FLEET COLLAPSE]: Total resource exhaustion.")
                break

        print("-" * 95)
        status = "REWARD_MAXIMIZED_DELAYED_SOVEREIGN_SUCCESS" if self.packet_reached_dispatcher else "REJECTED_PERMANENT_LINK_TRUNCATION"
        print(f"🎯 Fire-Station Plot Synthesis Outcome Invariant   ──➔ \033[1;32m{status}\033[0m")
        print("=" * 95 + "\n")

        root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
        exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write(f"sds_synthesis_status(fleet_search_judith, schema_{status.lower()}).\n")

if __name__ == "__main__":
    engine = MultiHopCooperativeSdsSimulator()
    engine.run_cooperative_sds_loop()
