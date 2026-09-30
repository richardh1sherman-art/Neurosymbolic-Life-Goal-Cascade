import os
import math
import numpy as np

class FirestationHubSdsSwarmSimulator:
    def __init__(self):
        self.N = 50  # 🛸 50 vehicle nodes
        self.t_max = 30.0 # Extended flight path timeline: 30 minutes
        self.dt = 1.0     # Time-scale steps in minutes
        self.time_steps = np.arange(0, self.t_max, self.dt)
        self.steps_count = len(self.time_steps)
        
        # 📐 MASSIVE FIELD EXPANSION: Judith is lost 75 miles away in a ditch zone
        self.judith_pos = np.array([75.0, 75.0])
        self.required_clues = 3  
        self.clues_collected = 0
        
        # 🚨 LAUNCH INITIAL CONDITIONS: All 50 drones leave the Firestation at [0.0, 0.0]
        self.pos_x = np.zeros(self.N)
        self.pos_y = np.zeros(self.N)
        
        # Scale flight velocities so drones scatter and fan out across the 100-mile zone
        np.random.seed(42)
        self.angle_offsets = np.random.uniform(0.0, 2.0 * math.pi, self.N)
        self.speeds = np.random.uniform(12.0, 18.0, self.N) # Miles per minute capabilities
        
        # Resilient fuel capacities to support the long-range 100-mile exploration grid
        self.fuel = np.random.uniform(400.0, 500.0, self.N)
        self.power = np.random.uniform(400.0, 500.0, self.N)
        
        # Signal reach limits across the expanded 100-mile matrix
        self.max_signal_range = 25.0
        self.weather_center = np.array([40.0, 40.0])
        self.weather_radius = 15.0
        
        self.pending_broadcast = False
        self.locating_node_idx = -1

    def run_hidden_sds_planning(self):
        print("=" * 95)
        print("🌀 LIVE LISP PDE INTERPRETER: FIRESTATION HUB HETEROGENEOUS 100-MILE FIELD SEARCH")
        print("=" * 95)
        print("📥 Initial State ──➔ All 50 Drones Deploying Simultaneously from Firestation")
        print("📥 Search Field  ──➔ 100-Mile Continuous Spatial Grid Mesh Matrix")
        print("-" * 95)

        mission_complete = False
        step = 1

        for t in self.time_steps:
            if mission_complete: break
            
            active_nodes = []
            scan_registered_this_step = False
            
            # Compute real-time cluster center of mass for re-routing loops
            valid_active_x = [self.pos_x[k] for k in range(self.N) if self.fuel[k] > 0 and k != self.locating_node_idx]
            valid_active_y = [self.pos_y[k] for k in range(self.N) if self.fuel[k] > 0 and k != self.locating_node_idx]
            fleet_centroid_x = np.mean(valid_active_x) if valid_active_x else 50.0
            fleet_centroid_y = np.mean(valid_active_y) if valid_active_y else 50.0

            for i in range(self.N):
                # Consume fuels over long-range flight operations
                self.fuel[i] -= 8.0 * self.dt
                self.power[i] -= 5.0 * self.dt
                
                if self.fuel[i] <= 0 or self.power[i] <= 0:
                    continue  # Fuel depletion freezes the node
                
                # 🚨 FIXED: Reference absolute array indices to extract pure 0-dimensional scalar parameters
                dist_to_weather = math.sqrt((self.pos_x[i] - self.weather_center[0])**2 + (self.pos_y[i] - self.weather_center[1])**2)
                if dist_to_weather < self.weather_radius:
                    # Execute graph minor contraction: squeeze nodes outward along boundary edges
                    self.pos_x[i] = self.weather_center[0] + (self.weather_radius * (self.pos_x[i] / 100.0))
                    self.pos_y[i] = self.weather_center[1] + (self.weather_radius * (self.pos_y[i] / 100.0))
                
                # Active re-routing loop for the locating drone to restore link coherence
                if self.pending_broadcast and i == self.locating_node_idx:
                    dx, dy = fleet_centroid_x - self.pos_x[i], fleet_centroid_y - self.pos_y[i]
                    dist_to_base = math.sqrt(dx**2 + dy**2)
                    if dist_to_base > 0:
                        self.pos_x[i] += (dx / dist_to_base) * self.speeds[i] * self.dt
                        self.pos_y[i] += (dy / dist_to_base) * self.speeds[i] * self.dt
                    active_nodes.append(i)
                    continue

                # Exploration Fan-Out: Move vehicles along their randomized heading angles
                if t == 0:
                    # Initial scatter step from the firestation hub
                    self.pos_x[i] += math.cos(self.angle_offsets[i]) * self.speeds[i] * self.dt
                    self.pos_y[i] += math.sin(self.angle_offsets[i]) * self.speeds[i] * self.dt
                else:
                    # Guided tracking toward Judith's ravine coordinate field
                    dx, dy = self.judith_pos[0] - self.pos_x[i], self.judith_pos[1] - self.pos_y[i]
                    dist_to_target = math.sqrt(dx**2 + dy**2)
                    
                    if dist_to_target < 5.0 and not scan_registered_this_step and self.clues_collected < self.required_clues:
                        scan_registered_this_step = True
                        self.clues_collected += 1
                        print(f"   \033[1;33m[VISUAL SENSOR ALERT]: Drone [{i}] logged Pass {self.clues_collected}/{self.required_clues} over the ditch!\033[0m")
                        
                        if self.clues_collected >= self.required_clues:
                            print(f"   \033[1;34m[COGNITIVE ALERT]: Judith located at {t:.1f} min! Drone [{i}] isolated. Initiating return dash...\033[0m")
                            self.pending_broadcast = True
                            self.locating_node_idx = i
                    
                    if dist_to_target > 0:
                        self.pos_x[i] += (dx / dist_to_target) * self.speeds[i] * self.dt
                        self.pos_y[i] += (dy / dist_to_target) * self.speeds[i] * self.dt
                
                active_nodes.append(i)

            # Rule 2 Connectivity Verification Checks
            isolated_nodes = 0
            locating_node_isolated = False
            for i in active_nodes:
                has_link = False
                for j in active_nodes:
                    if i == j: continue
                    d_ij = math.sqrt((self.pos_x[i] - self.pos_x[j])**2 + (self.pos_y[i] - self.pos_y[j])**2)
                    if d_ij < self.max_signal_range:
                        has_link = True
                        break
                if not has_link:
                    isolated_nodes += 1
                    if i == self.locating_node_idx:
                        locating_node_isolated = True

            print(f"Step {step:02d} | Time t = {t:4.1f} min | Active Nodes: {len(active_nodes):2d} | Isolated: {isolated_nodes} | Pending Packet: {self.pending_broadcast}")
            step += 1
            
            # Check for link recovery success conditions
            if self.pending_broadcast:
                if not locating_node_isolated and isolated_nodes < 25:
                    print(f"\n🎉 \033[1;32m[DELAYED LINK COHERENCE FIXED]: Drone [{self.locating_node_idx}] re-connected at t = {t:.1f} min!\033[0m")
                    print("   └── 100-mile spatial data broadcast successful. Target coordinates locked globally.")
                    mission_complete = True
                    break

            if len(active_nodes) < 3:
                print("🛑 \033[1;31m[FLEET COLLAPSE]: Swarm depleted inside the 100-mile zone.\033[0m")
                break

        print("-" * 95)
        status = "REWARD_MAXIMIZED_DELAYED_SOVEREIGN_SUCCESS" if mission_complete else "REJECTED_PERMANENT_LINK_TRUNCATION"
        print(f"🎯 Mesarovic Performance Outcome Invariant          ──➔ \033[1;32m{status}\033[0m")
        print("=" * 95 + "\n")

        root_dir = "/home/rsherman/projects/SMT-ILP/Popper-main/examples"
        exs_path = os.path.join(root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write(f"sds_synthesis_status(fleet_search_judith, schema_{status.lower()}).\n")

if __name__ == "__main__":
    engine = FirestationHubSdsSwarmSimulator()
    engine.run_hidden_sds_planning()
