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
        
        # 📋 Combined matrix restoring both multi-sentence tracks and character profiles safely
        self.parthood_training_data = [
            {"story_id": "st1_timeline", "stagnate": "True", "diligent": "True", "rejection": "True", "withdraw": "True", "target": "quits_job"},
            {"story_id": "sb_timeline_pos", "difficulty": "True", "effort": "True", "reward": "True", "target": "keeps_job"},
            {"story_id": "st2_timeline_neg", "grief": "True", "engagement": "True", "success": "False", "target": "no_mate"},
            {"story_id": "john_reversal", "planned_trajectory": "True", "edge_deletion": "True", "node_contraction": "True", "target": "graph_minor_recovery"},
            
            # Character Parthood Profiling Matrices
            {"story_id": "judith_character", "syntax": "rescue", "abstract_type": "information_flow", "region": "mt_ateh", "target": "system_rescue_schema"},
            {"story_id": "moses_character", "syntax": "saves_people", "abstract_type": "leader_lifecycle", "region": "egypt", "target": "sovereign_liberation_schema"},
            {"story_id": "david_character", "syntax": "unifies_kingdom", "abstract_type": "leader_lifecycle", "region": "jerusalem", "target": "sovereign_monarchy_schema"},
            {"story_id": "paul_character", "syntax": "establishes_church", "abstract_type": "apostle_lifecycle", "region": "damascus_road", "target": "ecclesiastical_apostolic_schema"},
            {"story_id": "joseph_character", "syntax": "preserves_lineage", "abstract_type": "ruler_lifecycle", "region": "egypt", "target": "sovereign_providence_schema"},
            {"story_id": "gideon_character", "syntax": "routes_oppressor", "abstract_type": "judge_lifecycle", "region": "midian_camp", "target": "judge_routing_schema"},
            {"story_id": "peter_character", "syntax": "shepherds_flock", "abstract_type": "pillar_lifecycle", "region": "sea_of_galilee", "target": "ecclesiastical_pastoral_schema"}
        ]

        # 📋 Independent Analogy Training Set
        self.analogy_training_data = [
            {"analogy_id": "m_to_k", "transmission_failure": "True", "mitigation_vector": "True", "awareness_lapse": "True", "connection_vector": "True", "has_permission_q": "True", "target": "valid_structural_analogy"},
            {"analogy_id": "m_to_k_breach", "transmission_failure": "True", "mitigation_vector": "True", "awareness_lapse": "True", "connection_vector": "True", "has_permission_q": "False", "target": "pragmatic_contract_violation"}
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
        if len(set(targets)) == 1: return WorldLevelNode(is_leaf=True, classification=str(targets[0]))
        
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
        print("🚀 CUSTOM AI PIPELINE: COMPILING DECOUPLED FOREST PARTHOOD & ANALOGY REPRESENTATIONS")
        print("=" * 95)
        
        # Train Tree #6 (Parthood Ontology)
        f6_list = ["stagnate", "difficulty", "planned_trajectory", "syntax", "abstract_type", "region"]
        t6_root = self.build_tree(self.parthood_training_data, f6_list)
        with open(os.path.join(self.model_dir, "level6_parthood_ontology.pkl"), "wb") as f:
            pickle.dump(t6_root, f)
            
        # Train Tree #7 (Analogies Core)
        f7_list = ["transmission_failure", "mitigation_vector", "has_permission_q"]
        t7_root = self.build_tree(self.analogy_training_data, f7_list)
        with open(os.path.join(self.model_dir, "level7_analogy_inferencing.pkl"), "wb") as f:
            pickle.dump(t7_root, f)
            
        print("🌲 [DUMPING LEVEL 3 COMPACT SITUATIONAL FORESTS SELECTIONS]")
        print("   ├── Tree #6 (Parthood Schema Loaded Successfully)")
        print("   └── Tree #7 (Analogy Inference Engine Loaded Successfully)")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    trainer = ForestOntologyTrainer()
    trainer.run_training()
