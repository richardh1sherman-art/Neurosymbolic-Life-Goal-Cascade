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
        
        # 📋 FIXED: Added rigid string quotes around 'moses' to eliminate the variable leak
        self.parthood_training_data = [
            {"subject": "judith", "syntax": "rescue", "abstract_type": "information_flow", "region": "mt_ateh", "target": "system_rescue_schema"},
            {"subject": "moses", "syntax": "saves_people", "abstract_type": "leader_lifecycle", "region": "egypt", "target": "sovereign_liberation_schema"},
            {"subject": "david", "syntax": "unifies_kingdom", "abstract_type": "leader_lifecycle", "region": "jerusalem", "target": "sovereign_monarchy_schema"},
            {"subject": "paul", "syntax": "establishes_church", "abstract_type": "apostle_lifecycle", "region": "damascus_road", "target": "ecclesiastical_apostolic_schema"},
            {"subject": "joseph", "syntax": "preserves_lineage", "abstract_type": "ruler_lifecycle", "region": "egypt", "target": "sovereign_providence_schema"},
            {"subject": "gideon", "syntax": "routes_oppressor", "abstract_type": "judge_lifecycle", "region": "midian_camp", "target": "judge_routing_schema"},
            {"subject": "peter", "syntax": "shepherds_flock", "abstract_type": "pillar_lifecycle", "region": "sea_of_galilee", "target": "ecclesiastical_pastoral_schema"}
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
            return WorldLevelNode(is_leaf=True, classification=str(targets))
        
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
        print("🚀 CUSTOM AI PIPELINE: RETRAINING NEW DECISION TREE #6 (PARTHOOD RELATIONAL MATRIX)")
        print("=" * 95)
        
        features_list = ["syntax", "abstract_type", "region"]
        t6_root = self.build_tree(self.parthood_training_data, features_list)
        
        with open(os.path.join(self.model_dir, "level6_parthood_ontology.pkl"), "wb") as f:
            pickle.dump(t6_root, f)
            
        print("🌲 [DUMPING LEVEL 3 PARTHOOD 'part_of' DECISION TREE GEOMETRY]")
        print("-" * 95)
        self.dump_tree(t6_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [TERMINAL REPRESENTATION LEAF] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [RELATIONAL LOOKUP]: Checks if parthood category ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    trainer = ForestOntologyTrainer()
    trainer.run_training()
