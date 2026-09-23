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

class TriangulatedForestTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Fully specified training matrices to ensure clean isolation
        self.graph_training_data = [
            {"id": "judith_network", "topology": "cycle", "logic_property": "planar", "target": "cyclic_flow_schema"},
            {"id": "kitchen_fire_network", "topology": "cycle", "logic_property": "planar", "target": "cyclic_flow_schema"},
            {"id": "john_transit_network", "topology": "path", "logic_property": "bounded_tree_width", "target": "linear_routing_schema"},
            {"id": "job_loss_short", "topology": "none", "logic_property": "unknown", "target": "static_atomic_schema"},
            {"id": "moses_expanded_lifecycle", "topology": "cyclic_mesh", "logic_property": "dynamic_growth", "target": "expanding_sovereign_manifold"},
            {"id": "david_expanded_lifecycle", "topology": "cyclic_mesh", "logic_property": "dynamic_growth", "target": "expanding_sovereign_manifold"},
            {"id": "paul_expanded_lifecycle", "topology": "cyclic_mesh", "logic_property": "dynamic_growth", "target": "expanding_sovereign_manifold"}
        ]
        
        self.fallacy_training_data = [
            {"id": "john_tree_hugger", "pattern": "attacking_individual", "authority_error": "False", "target": "ad_hominem"},
            {"id": "louise_campaign", "pattern": "attacking_individual", "authority_error": "False", "target": "ad_hominem"},
            {"id": "bible_circularity", "pattern": "circular_loop", "authority_error": "False", "target": "circular_reasoning"},
            {"id": "friend_sneeze_corona", "pattern": "unknown", "authority_error": "True", "target": "irrelevant_authority"}
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
        if len(set(targets)) == 1: 
            return WorldLevelNode(is_leaf=True, classification=str(list(set(targets))[0]))
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 6:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return WorldLevelNode(is_leaf=True, classification=str(max(counts, key=counts.get)))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "unknown") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "unknown") != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_training(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: COMPILING & DUMPING EVERY TREE REPRESENTATION CORE")
        print("=" * 95)
        
        # Train and Dump Tree #8 (Graph Topologies)
        t8_root = self.build_tree(self.graph_training_data, ["topology", "logic_property"])
        with open(os.path.join(self.model_dir, "level8_graph_topologies.pkl"), "wb") as f:
            pickle.dump(t8_root, f)
        print("🌲 [GEOMETRY LAYOUT: DECISION TREE #8 (GRAPH STRUCTURE TAXONOMY)]")
        self.dump_tree(t8_root)
        print("-" * 95)
            
        # Train and Dump Tree #9 (Fallacy Classifications)
        t9_root = self.build_tree(self.fallacy_training_data, ["pattern", "authority_error"])
        with open(os.path.join(self.model_dir, "level9_fallacy_patterns.pkl"), "wb") as f:
            pickle.dump(t9_root, f)
        print("🌲 [GEOMETRY LAYOUT: DECISION TREE #9 (FALLACY PATTERN SCHEMAS)]")
        self.dump_tree(t9_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [TERMINAL LEAF NODE] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [SPLIT MATRIX CHECK]: Does field ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    trainer = TriangulatedForestTrainer()
    trainer.run_training()
