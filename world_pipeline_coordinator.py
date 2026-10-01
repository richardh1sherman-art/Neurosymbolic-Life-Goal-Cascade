import os
import pickle
import math

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class GlobalForestCoordinator:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Top-level categorical dispatch training signatures for Tree #0
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
        if not data: return WorldLevelNode(is_leaf=True, classification="empty")
        targets = [d["target"] for d in data]
        if len(set(targets)) == 1: return WorldLevelNode(is_leaf=True, classification=str(list(set(targets))))
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 5:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return WorldLevelNode(is_leaf=True, classification=str(max(counts, key=counts.get)))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "unknown") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "unknown") != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_coordination_pipeline(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: COMPILING APEX TREE #0 (MASTER FUNCTOR DISPATCHER)")
        print("=" * 95)
        
        features_list = ["system_type", "manifold"]
        t0_root = self.build_tree(self.apex_dispatch_data, features_list)
        
        with open(os.path.join(self.model_dir, "level00_master_dispatcher.pkl"), "wb") as f:
            pickle.dump(t0_root, f)
            
        print("🌲 [APEX ROUTING GEOMETRY: DECISION TREE #0]")
        self.dump_tree(t0_root)
        print("=" * 95 + "\n")

        # 📋 Realizing simulated definitions for historical placeholder trees to populate the dump cleanly
        self.generate_legacy_trees_stubs()

        print("🌲 COMPREHENSIVE RECURSIVE FOREST CORES REGISTER DUMP (TREES 1 - 12):")
        print("-" * 95)
        for i in range(13):
            file_name = f"level{i:02d}_science_invariants.pkl" if i == 12 else (f"level00_master_dispatcher.pkl" if i == 0 else f"level{i:02d}_experiential_memory.pkl")
            full_path = os.path.join(self.model_dir, file_name)
            if os.path.exists(full_path):
                with open(full_path, "rb") as mf:
                    tree_root = pickle.load(mf)
                print(f"\n▶️ [DUMPING STRUCTURE: DECISION TREE #{i}] ──➔ Source Asset: {file_name}")
                self.dump_tree(tree_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [CLASSIFICATION LEAF] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [FEATURE CONDITION]: Checks if matrix attribute ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

    def generate_legacy_trees_stubs(self):
        """Ensures structural placeholders are mapped cleanly to the forest inventory file rows."""
        for t_idx in range(1, 11):
            stub_path = os.path.join(self.model_dir, f"level{t_idx:02d}_experiential_memory.pkl")
            if not os.path.exists(stub_path):
                stub_node = WorldLevelNode(is_leaf=True, classification=f"legacy_conceptual_space_tree_{t_idx}_active")
                with open(stub_path, "wb") as sf:
                    pickle.dump(stub_node, sf)

if __name__ == "__main__":
    coordinator = GlobalForestCoordinator()
    coordinator.run_coordination_pipeline()
