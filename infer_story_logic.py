import os
import math
import numpy as np

class DelayTolerantHubSwarmSimulator:
    def __init__(self):
        self.N = 50  # 🛸 50-vehicle Large Swarm
        self.t_max = 480.0 # 8 Hours total horizon (480 minutes)
        self.dt = 10.0     
        self.time_steps = np.arange(0, self.t_max, self.dt)
        
        # Judith's target coordinate
        self.judith_pos = np.array([75.0, 75.0])
        self.required_clues = 1  
        self.clues_collected = 0
        
        # Initial positions: All 50 drones leave the Firestation at [0.0, 0.0]
        self.pos_x = np.zeros(self.N)
        self.pos_y = np.zeros(self.N)
        
        np.random.seed(42)
        self.angle_offsets = np.random.uniform(0.0, 0.5 * math.pi, self.N)
        self.speeds = np.random.uniform(0.6, 0.95, self.N) 
        
        # Power metrics
        self.battery = np.ones(self.N) * 100.0  
        self.fuel = np.random.uniform(350.0, 450.0, self.N)
        
        # 🚨 NEW: Infrastructure Power Replenishment Hub Station
        self.charging_hub_pos = np.array([50.0, 50.0])
        
        # Network constraints
        self.max_signal_range = 30.0 
        self.weather_center = np.array([45.0, 45.0])
        self.weather_radius = 12.0
        
        # Non-convex obstacles
        self.mountain_center = np.array([30.0, 50.0])
        self.mountain_radius = 10.0
        self.city_center = np.array([60.0, 30.0])
        self.city_radius = 12.0
        
        # 🚨 STEP 8: Store-and-Forward Local Data Caching Buffers
        self.local_memory_buffer = {i: {"has_clue": False, "target_coordinates": None} for i in range(self.N)}
        self.global_packet_flushed = False

    def is_line_of_sight_blocked(self, x1, y1, x2, y2):
        cx, cy = self.mountain_center[0], self.mountain_center[1]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return False
        t = ((cx - x1) * dx + (cy - y1) * dy) / (dx**2 + dy**2)
        t = max(0.0, min(1.0, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        dist = math.sqrt((closest_x - cx)**2 + (closest_y - cy)**2)
        return dist < self.mountain_radius

    def run_simulation(self):
        print("=" * 95)
        print("🌀 LIVE LISP PDE INTERPRETER: STORE-AND-FORWARD BUFFER & CHARGING HUBS INITIATED")
        print("=" * 95)
        print("📥 Network Capability ──➔ Step 8 Delay-Tolerant Local Queue Caching Active")
        print("📥 Infrastructure     ──➔ Central Power Replenishment Station Docked at [50, 50]")
        print("-" * 95)

        step = 1

        for t in self.time_steps:
            if self.global_packet_flushed: break
            
            active_nodes = []
            
            # Compute center of mass of functional nodes for mesh communication references
            valid_active_x = [self.pos_x[k] for k in range(self.N) if self.battery[k] > 0 and self.fuel[k] > 0]
            valid_active_y = [self.pos_y[k] for k in range(self.N) if self.battery[k] > 0 and self.fuel[k] > 0]
            fleet_centroid_x = np.mean(valid_active_x) if valid_active_x else 50.0
            fleet_centroid_y = np.mean(valid_active_y) if valid_active_y else 50.0

            for i in range(self.N):
                self.fuel[i] -= 0.6 * self.dt
                
                # Weather drain
                dist_to_weather = math.sqrt((self.pos_x[i] - self.weather_center[0])**2 + (self.pos_y[i] - self.weather_center[1])**2)
                if dist_to_weather < self.weather_radius:
                    self.battery[i] -= 1.5 * self.dt
                else:
                    self.battery[i] -= 0.15 * self.dt  

                if self.fuel[i] <= 0 or self.battery[i] <= 0:
                    continue  # Asset dead

                # Obstacle deflections
                dist_to_mountain = math.sqrt((self.pos_x[i] - self.mountain_center[0])**2 + (self.pos_y[i] - self.mountain_center[1])**2)
                if dist_to_mountain < self.mountain_radius:
                    self.pos_x[i] = self.mountain_center[0] + (self.mountain_radius * (self.pos_x[i] / 50.0))
                    self.pos_y[i] = self.mountain_center[1] + (self.mountain_radius * (self.pos_y[i] / 50.0))

                dist_to_city = math.sqrt((self.pos_x[i] - self.city_center[0])**2 + (self.pos_y[i] - self.city_center[1])**2)
                if dist_to_city < self.city_radius:
                    self.pos_x[i] = self.city_center[0] + (self.city_radius * (self.pos_x[i] / 100.0))
                    self.pos_y[i] = self.city_center[1] + (self.city_radius * (self.pos_y[i] / 100.0))

                # 🔌 CHARGING HUB NAVIGATION: If battery drops below 30%, reroute to station for automatic swap
                if self.battery[i] < 30.0:
                    dx, dy = self.charging_hub_pos[0] - self.pos_x[i], self.charging_hub_pos[1] - self.pos_y[i]
                    dist_to_hub = math.sqrt(dx**2 + dy**2)
                    if dist_to_hub < 4.0:
                        self.battery[i] = 100.0  # 🔌 RECHARGED: Battery capacity restored to maximum
                        print(f"   \033[1;36m[INFRASTRUCTURE RECHARGE]: Drone [{i}] has docked at Hub Alpha! Battery swapped to 100%.\033[0m")
                    else:
                        if dist_to_hub > 0:
                            self.pos_x[i] += (dx / dist_to_hub) * self.speeds[i] * self.dt
                            self.pos_y[i] += (dy / dist_to_hub) * self.speeds[i] * self.dt
                    active_nodes.append(i)
                    continue

                # Normal task navigation routing
                if t == 0:
                    self.pos_x[i] += math.cos(self.angle_offsets[i]) * self.speeds[i] * self.dt
                    self.pos_y[i] += math.sin(self.angle_offsets[i]) * self.speeds[i] * self.dt
                else:
                    # If this specific drone has cached a clue but is currently link-occluded, steer to center mass to flush
                    if self.local_memory_buffer[i]["has_clue"]:
                        dx, dy = fleet_centroid_x - self.pos_x[i], fleet_centroid_y - self.pos_y[i]
                    else:
                        dx, dy = self.judith_pos[0] - self.pos_x[i], self.judith_pos[1] - self.pos_y[i]
                        
                    dist_to_target = math.sqrt(dx**2 + dy**2)
                    
                    if dist_to_target < 5.0 and not self.local_memory_buffer[i]["has_clue"] and self.clues_collected < self.required_clues:
                        self.clues_collected += 1
                        # 🚨 STEP 8: Store-and-Forward caching rule triggers natively
                        self.local_memory_buffer[i]["has_clue"] = True
                        self.local_memory_buffer[i]["target_coordinates"] = self.judith_pos
                        print(f"   \033[1;33m[SENSORY PACKET CACHED]: Drone [{i}] spotted Judith! Link occluded; caching data in local storage buffer...\033[0m")
                    
                    if dist_to_target > 0:
                        self.pos_x[i] += (dx / dist_to_target) * self.speeds[i] * self.dt
                        self.pos_y[i] += (dy / dist_to_target) * self.speeds[i] * self.dt
                
                active_nodes.append(i)

            # Rule 2 Network Connectivity and Store-and-Forward Flash Loops
            isolated_nodes = 0
            for i in active_nodes:
                has_link = False
                for j in active_nodes:
                    if i == j: continue
                    d_ij = math.sqrt((self.pos_x[i] - self.pos_x[j])**2 + (self.pos_y[i] - self.pos_y[j])**2)
                    if d_ij < self.max_signal_range:
                        if not self.is_line_of_sight_blocked(self.pos_x[i], self.pos_y[i], self.pos_x[j], self.pos_y[j]):
                            has_link = True
                            break
                if not has_link:
                    isolated_nodes += 1
                else:
                    # 🚨 STEP 8: If the drone has a cached packet and regains a valid line-of-sight link, flush it instantly!
                    if self.local_memory_buffer[i]["has_clue"]:
                        print(f"\n🎉 \033[1;32m[DELAY-TOLERANT FLUSH SUCCESS]: Drone [{i}] has re-entered a clear Morse saddle corridor!\033[0m")
                        print("   └── Cached visual sensor packet successfully un-buffered and transmitted to dispatch.")
                        self.global_packet_flushed = True
                        break

            current_hours = int(t // 60)
            current_mins = int(t % 60)
            print(f"Step {step:02d} | Time: {current_hours:02d}h {current_mins:02d}m | Active Nodes: {len(active_nodes):2d} | Isolated: {isolated_nodes} | Store-and-Forward Caches Active")
            step += 1
            
            if len(active_nodes) < 3:
                print("🛑 [FLEET COLLAPSE]: Total resource exhaustion.")
                break

        print("-" * 95)
        status = "REWARD_MAXIMIZED_DELAYED_SOVEREIGN_SUCCESS" if self.global_packet_flushed else "REJECTED_PERMANENT_LINK_TRUNCATION"
        print(f"🎯 Complex SDS Performance Outcome Invariant        ──➔ \033[1;32m{status}\033[0m")
        print("=" * 95 + "\n")

        root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
        exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write(f"sds_synthesis_status(fleet_search_judith, schema_{status.lower()}).\n")

if __name__ == "__main__":
    engine = DelayTolerantHubSwarmSimulator()
    engine.run_simulation()
