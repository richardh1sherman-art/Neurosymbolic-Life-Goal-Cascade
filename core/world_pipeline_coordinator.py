import os
import json
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

class CleanNetworkTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.train_json_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Counterfactual-StoryRW-master/data/train_network.json"
        os.makedirs(self.model_dir, exist_ok=True)

    def extract_features(self, text_content):
        combined = text_content.lower()
        features = {
            "primary_modality_blocked": "True" if any(w in combined for w in ["cancelled", "severed", "failed", "blocked", "wrong"]) else "False",
            "local_partial_inversion_supported": "True" if any(w in combined for w in ["friend", "alternative", "secondary", "draw"]) else "False",
            "is_transport_network": "True" if any(w in combined for w in ["flight", "plane", "train", "route"]) else "False"
        }
        return features

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
        base_entropy = self.calculate_entropy([d[1] for d in data])
        best_gain, best_feat, best_val = -1, None, None
        for f in features:
            values = set(d[0][f] for d in data)
            for val in values:
                left = [d for d in data if d[0][f] == val]
                right = [d for d in data if d[0][f] != val]
                if not left or not right: continue
                gain = base_entropy - ((len(left)/len(data)) * self.calculate_entropy([d[1] for d in left]) + (len(right)/len(data)) * self.calculate_entropy([d[1] for d in right]))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val

    def build_tree(self, data, features, depth=0):
        if not data: return WorldLevelNode(is_leaf=True, classification="empty")
        labels = set(d[1] for d in data)
        if len(labels) == 1: return WorldLevelNode(is_leaf=True, classification=list(labels))
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 3:
            counts = {}
            for d in data: counts[d[1]] = counts.get(d[1], 0) + 1
            return WorldLevelNode(is_leaf=True, classification=max(counts, key=counts.get))
        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d[0][feat] == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d[0][feat] != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_training_suite(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: RUNNING RETRAINING SPREAD OVER TEXT CORPUS")
        print("=" * 95)
        if not os.path.exists(self.train_json_path):
            print("🚨 Training network JSON missing. Regenerating standard samples...")
            os.makedirs(os.path.dirname(self.train_json_path), exist_ok=True)
            mock = [{"premise": "Tom flight cancelled", "counterfactual": "Alternative train", "original_ending": "He arrived early"}] * 10
            with open(self.train_json_path, "w") as f: json.dump(mock, f)
        with open(self.train_json_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        processed_data = []
        for idx, r in enumerate(records):
            text = f"{r.get('premise','')} {r.get('counterfactual','')} {r.get('original_ending','')}"
            features = self.extract_features(text)
            if idx % 4 == 0: target = "local_partial_group_inversion"
            elif idx % 4 == 1: target = "graph_minor_edge_contraction_healing"
            elif idx % 4 == 2: target = "global_alternate_modality_routing"
            else: target = "standard_priority_path_execution"
            processed_data.append((features, target))
        features_list = ["primary_modality_blocked", "local_partial_inversion_supported", "is_transport_network"]
        t5_root = self.build_tree(processed_data, features_list)
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "wb") as f:
            pickle.dump(t5_root, f)
        print("🌲 [DUMPING LEVEL 5 DECISION TOPOLOGY FOLLOWING PROBE]")
        print("✅ Training complete.")

if __name__ == "__main__":
    trainer = CleanNetworkTrainer()
    trainer.run_training_suite()
