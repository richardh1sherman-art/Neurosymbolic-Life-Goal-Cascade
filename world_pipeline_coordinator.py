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

class ForestOntologyTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Expanded Training Exemplar profiles incorporating your full notes
        self.forest_training_data = [
            {"story_id": "ST1_pos", "stagnate": "True", "diligent": "True", "rejection": "True", "withdraw": "True", "target": "quits_job"},
            {"story_id": "ST1_neg", "stagnate": "True", "diligent": "True", "rejection": "False", "withdraw": "False", "target": "keeps_job"},
            {"story_id": "SB_pos", "difficulty": "True", "effort": "True", "reward": "True", "target": "keeps_job"},
            {"story_id": "SB_neg", "difficulty": "True", "effort": "False", "reward": "False", "target": "lost_job"},
            {"story_id": "ST2_pos", "grief": "True", "engagement": "True", "success": "True", "target": "mate"},
            {"story_id": "ST2_neg", "grief": "True", "engagement": "True", "success": "False", "target": "no_mate"},
            # John's Plan Reversal Exemplars
            {"story_id": "John_Plan", "planned_trajectory": "True", "edge_deletion": "False", "target": "complete_trip"},
            {"story_id": "John_Reversal", "planned_trajectory": "True", "edge_deletion": "True", "node_contraction": "True", "target": "graph_minor_recovery"},
            # Sovereign Immutable Histories
            {"story_id": "Moses_History", "decalogue_violation": "True", "scripture_authorship": "True", "target": "sovereign_success"},
            {"story_id": "David_History", "decalogue_violation": "True", "path_healing": "True", "scripture_authorship": "True", "target": "sovereign_success"}
        ]

    def print_exemplars(self):
        print("-" * 95)
        print("📋 INGESTED ONTOLOGY EXEMPLARS MATRIX (TIER 3 INPUTS):")
        print("-" * 95)
        for ex in self.forest_training_data:
            features = {k: v for k, v in ex.items() if k not in ["story_id", "target"]}
            print(f" 📥 Exemplar ID: [{ex['story_id']}] ──➔ Target: **{ex['target']}**")

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
            values = set(d.get(f, "False") for d in data)
            for val in values:
                left = [d for d in data if d.get(f, "False") == val]
                right = [d for d in data if d.get(f, "False") != val]
                if not left or not right: continue
                gain = base_entropy - ((len(left)/len(data)) * self.calculate_entropy([d["target"] for d in left]) + (len(right)/len(data)) * self.calculate_entropy([d["target"] for d in right]))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val

    def build_tree(self, data, features, depth=0):
        if not data: return WorldLevelNode(is_leaf=True, classification="empty")
        targets = [d["target"] for d in data]
        if len(set(targets)) == 1: return WorldLevelNode(is_leaf=True, classification=targets[0])
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 4:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return WorldLevelNode(is_leaf=True, classification=max(counts, key=counts.get))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "False") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "False") != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_forest_training(self):
        print("=" * 95)
        print("🚀 RETRAINING DECISION FOREST CORES ACROSS ONTOLOGY CONCEPTS")
        print("=" * 95)
        
        self.print_exemplars()
        
        features_list = ["stagnate", "diligent", "rejection", "withdraw", "difficulty", "effort", "reward", "grief", "engagement", "success", "planned_trajectory", "edge_deletion", "node_contraction", "decalogue_violation", "path_healing", "scripture_authorship"]
        t5_root = self.build_tree(self.forest_training_data, features_list)
        
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "wb") as f:
            pickle.dump(t5_root, f)
            
        print("-" * 95)
        print("🌲 [DUMPING LEVEL 3 SITUATIONAL SCHEMA DECISION TREE BRANCHES]")
        print("-" * 95)
        self.dump_tree(t5_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [TERMINAL ONTOLOGY LEAF NODE] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [CROSS-TREE LOOKUP]: Checks if story unit contains concept ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    trainer = ForestOntologyTrainer()
    trainer.run_forest_training()
