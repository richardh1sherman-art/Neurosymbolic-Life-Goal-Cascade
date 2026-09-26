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

class ScienceInvariantsTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Relevant features representing the physical states and informed decisions
        self.science_training_data = [
            {"id": "case_1", "spring_stiffness": "soft", "initial_stretch": "unstretched", "tolerance": "liberal", "target": "increase_structural_stiffness"},
            {"id": "case_2", "spring_stiffness": "soft", "initial_stretch": "unstretched", "tolerance": "stringent", "target": "system_stable_maintain_policy"},
            {"id": "case_3", "spring_stiffness": "stiff", "initial_stretch": "stretched", "tolerance": "liberal", "target": "system_stable_maintain_policy"},
            {"id": "case_4", "spring_stiffness": "stiff", "initial_stretch": "stretched", "tolerance": "stringent", "target": "system_stable_maintain_policy"}
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

    def run_training(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: COMPILING DECISION TREE #12 (SCIENTIFIC ALGEBRA INVARIANTS)")
        print("=" * 95)
        
        features_list = ["spring_stiffness", "initial_stretch", "tolerance"]
        t12_root = self.build_tree(self.science_training_data, features_list)
        
        with open(os.path.join(self.model_dir, "level12_science_invariants.pkl"), "wb") as f:
            pickle.dump(t12_root, f)
            
        print("🌲 [GEOMETRY LAYOUT: DECISION TREE #12 (STABILITY CONTROL POLICIES)]")
        print("-" * 95)
        self.dump_tree(t12_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [INFORMED DECISION LEAF] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [STABILITY FEATURE ANALYSIS]: Is system property ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    trainer = ScienceInvariantsTrainer()
    trainer.run_training()
