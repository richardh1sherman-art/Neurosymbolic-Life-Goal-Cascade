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

class AnalogyOntologyTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Complex analogy profiles incorporating your spiritual parthood metrics
        self.analogy_training_data = [
            {
                "analogy_id": "m_to_k", 
                "transmission_failure": "True", "mitigation_vector": "True", "awareness_lapse": "True", "connection_vector": "True", 
                "has_permission_q": "True", "boundary_asymmetry": "False",
                "target": "valid_structural_analogy"
            },
            {
                "analogy_id": "m_to_k_breach", 
                "transmission_failure": "True", "mitigation_vector": "True", "awareness_lapse": "True", "connection_vector": "True", 
                "has_permission_q": "False", "boundary_asymmetry": "False",
                "target": "pragmatic_contract_violation"
            },
            # 🚨 NEW VARIANT: Spiritual Analogy Map
            {
                "analogy_id": "judith_to_prodigal",
                "fundamental_crisis": "True", "visceral_depletion": "True", "external_deliverance": "True", 
                "informational_beacon": "True", "awareness_vector": "True", "initial_abundance": "True", 
                "structural_descent": "True", "boundary_asymmetry": "True", "has_permission_q": "True",
                "target": "partial_spiritual_homomorphism"
            }
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
        if len(set(targets)) == 1: return WorldLevelNode(is_leaf=True, classification=str(targets))
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 5:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return WorldLevelNode(is_leaf=True, classification=str(max(counts, key=counts.get)))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "False") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "False") != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_training(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: COMPILING ANALOGICAL FORESTS OVER SPIRITUAL DOMAINS")
        print("=" * 95)
        
        features_list = [
            "transmission_failure", "mitigation_vector", "has_permission_q", "boundary_asymmetry",
            "fundamental_crisis", "visceral_depletion", "external_deliverance", "informational_beacon",
            "awareness_vector", "initial_abundance", "structural_descent"
        ]
        t7_root = self.build_tree(self.analogy_training_data, features_list)
        
        with open(os.path.join(self.model_dir, "level7_analogy_inferencing.pkl"), "wb") as f:
            pickle.dump(t7_root, f)
            
        print("🌲 [DUMPING LEVEL 3 HOMOMORPHISM SELECTIONS]")
        print("   └── Tree #7 (Spiritual & Structural Analogy Core Restructured Successfully)")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    # Also initialize dummy Tree #6 wrapper file to keep inference unpickler from crashing
    model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
    with open(os.path.join(model_dir, "level6_parthood_ontology.pkl"), "wb") as f:
        pickle.dump(WorldLevelNode(is_leaf=True, classification="system_rescue_schema"), f)

    trainer = AnalogyOntologyTrainer()
    trainer.run_training()
