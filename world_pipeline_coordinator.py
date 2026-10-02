import os
import pickle
import math

class EnhancedWorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None, context=None, reward_metric=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.context = context                # Intensional State Context field
        self.reward_metric = reward_metric    # Analytical Reward Invariant field
        self.tb = None                        
        self.fb = None                        

class EnhancedForestCoordinator:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Top-level categorical dispatch training signatures for Tree #0
        self.apex_dispatch_data = [
            {"id": "monkey_bananas", "system_type": "symbolic", "manifold": "discrete", "target": "route_to_tree_11_linguistic"},
            {"id": "parity_proofs", "system_type": "symbolic", "manifold": "algebraic", "target": "route_to_tree_11_algebra"},
            {"id": "algebra_stories", "system_type": "symbolic", "manifold": "discrete", "target": "route_to_tree_11_linguistic"},
            {"id": "inverted_pendulum", "system_type": "continuous", "manifold": "differential", "target": "route_to_tree_12_ode"},
            {"id": "fractional_pde", "system_type": "continuous", "manifold": "differential", "target": "route_to_tree_12_pde"},
            {"id": "pde_blowup", "system_type": "continuous", "manifold": "differential", "target": "route_to_tree_12_pde"},
            {"id": "wavelet_swarm", "system_type": "continuous", "manifold": "graph_dynamic", "target": "route_to_tree_12_swarm"},
            {"id": "dynamic_sds_swarm", "system_type": "continuous", "manifold": "graph_dynamic", "target": "route_to_tree_12_swarm"}
        ]

    def calculate_entropy(self, targets):
        if not targets: return 0
        counts = {}
        for t in targets: counts[t] = counts.get(t, 0) + 1
        entropy = 0.0
        for count in counts.values():
            p = count / len(targets)
            entropy -= p * math.log2(p)
        return entropy

    def find_best_split(self, data, features):
        base_entropy = self.calculate_entropy([d["target"] for d in data])
        best_gain, best_feat, best_val = -1, None, None
        for f in features:
            values = set(d.get(f, "unknown") for d in data)
            for val in values:
                left = [d for d in data if d.get(f, "unknown") == val]
                right = [d for d in data if d.get(f, "unknown") != val]
                if not left or not right: continue
                gain = base_entropy - ((len(left)/len(data)) * self.calculate_entropy([d["target"] for d in left]) + (len(right)/len(data)) * self.calculate_entropy([d["target"] for d in right]))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val

    def build_tree(self, data, features, depth=0):
        if not data: return EnhancedWorldLevelNode(is_leaf=True, classification="empty")
        targets = [d["target"] for d in data]
        if len(set(targets)) == 1: 
            return EnhancedWorldLevelNode(is_leaf=True, classification=str(list(set(targets))))
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 5:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return EnhancedWorldLevelNode(is_leaf=True, classification=str(max(counts, key=counts.get)))

        node = EnhancedWorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "unknown") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "unknown") != val], [f for f in features if f != feat], depth + 1)
        return node

    def build_custom_tree12_with_schema(self):
        """🔨 COMPILING TREE #12 TO INJECT THE INTENSIONAL LEAF SCHEMAS NATIVELY"""
        root = EnhancedWorldLevelNode(split_feature="wavelet", split_value="active")
        
        # --- LEFT BRANCH: Wavelet is Active (True) ---
        root.tb = EnhancedWorldLevelNode(split_feature="connectivity", split_value="connected_mesh")
        
        root.tb.tb = EnhancedWorldLevelNode(
            is_leaf=True,
            classification="system_stable_maintain_policy",
            context="Smooth multi-scale gradient filtering; tight local communication links",
            reward_metric="V' Reachable Space Maximized (0.6161 tracking error units)"
        )
        root.tb.fb = EnhancedWorldLevelNode(
            is_leaf=True,
            classification="activate_delayed_recovery_routing",
            context="Drones isolated on edge of 100-mile grid with pending discovery packets",
            reward_metric="Transactional link restoration path identified and verified open"
        )
        
        # --- RIGHT BRANCH: Wavelet is Inactive (False) ---
        root.fb = EnhancedWorldLevelNode(split_feature="connectivity", split_value="disconnected_minor")
        
        root.fb.tb = EnhancedWorldLevelNode(
            is_leaf=True,
            classification="trigger_graph_minor_contraction",
            context="High-frequency fractal chattering noise detected; network topology nearing saturation limits",
            reward_metric="Prevent structural network fragmentation into forbidden minor M_danger"
        )
        root.fb.fb = EnhancedWorldLevelNode(
            is_leaf=True,
            classification="activate_mission_abort_safety_halt",
            context="Task queue load permanently exceeds sustainable capacity (>140%) across active fleet nodes",
            reward_metric="Backward reachability tubes confirm Attainable Space Performance Subset V' is EMPTY"
        )
        
        with open(os.path.join(self.model_dir, "level12_science_invariants.pkl"), "wb") as f:
            pickle.dump(root, f)

    def run_coordination_pipeline(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: RETRAINING RECURSIVE TREE FORESTS WITH ENHANCED LEAF SCHEMAS")
        print("=" * 95)
        
        # Train Tree #0
        features_list = ["system_type", "manifold"]
        t0_root = self.build_tree(self.apex_dispatch_data, features_list)
        with open(os.path.join(self.model_dir, "level00_master_dispatcher.pkl"), "wb") as f:
            pickle.dump(t0_root, f)
            
        # Build upgraded Tree #12
        self.build_custom_tree12_with_schema()
        
        # Build placeholders for legacy branches to make sure the dump loop unrolls fully
        for t_idx in range(1, 12):
            stub_path = os.path.join(self.model_dir, f"level{t_idx:02d}_experiential_memory.pkl")
            if not os.path.exists(stub_path):
                stub_node = EnhancedWorldLevelNode(is_leaf=True, classification=f"legacy_tree_{t_idx}_active")
                with open(stub_path, "wb") as sf:
                    pickle.dump(stub_node, sf)

        # Output the comprehensive forest audit
        print("🌲 DUMPING HIGH-RESOLUTION GEOMETRY MATRIX FOR CHOSEN TARGET TREES:")
        print("-" * 95)
        # 🚨 FIXED: Explicitly defined list limits [0, 12] to eradicate the syntax drop
        for i in[0, 12]:
            file_name = "level00_master_dispatcher.pkl" if i == 0 else "level12_science_invariants.pkl"
            full_path = os.path.join(self.model_dir, file_name)
            with open(full_path, "rb") as mf:
                tree_root = pickle.load(mf)
            print(f"\n▶️ [EXPLORING STRUCTURE: DECISION TREE #{i}] ──➔ Source Asset: {file_name}")
            self.dump_tree(tree_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{node}📦 [ENHANCED CONTROL LEAF SCHEME]")
            if node.context:
                print(f"{node}  ├── 📝 State Context  ──➔ {node.context}")
            if node.reward_metric:
                print(f"{node}  ├── 🎯 Reward Metric  ──➔ {node.reward_metric}")
            print(f"{node}  └── ⚙️ Action Command ──➔ \033[1;32m**{node.classification}**\033[0m")
            return
        print(f"{node}🔍 [FEATURE LOGIC VERTEX]: Is system property ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{node}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{node}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    coordinator = EnhancedForestCoordinator()
    coordinator.run_coordination_pipeline()
