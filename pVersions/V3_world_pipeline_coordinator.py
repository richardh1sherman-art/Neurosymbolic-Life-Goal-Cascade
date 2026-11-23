import os
import sys
import pickle
import math

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.is_leaf = is_leaf
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class SequentialWorldTrainer:
    def __init__(self):
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Tier 1 Balanced Lexical Data
        self.raw_tokens_dataset = [
            {"term": "judith", "is_capitalized": "True", "suffix_is": "False", "target_pos": "proper_noun"},
            {"term": "george", "is_capitalized": "True", "suffix_is": "False", "target_pos": "proper_noun"},
            {"term": "falls", "is_capitalized": "False", "suffix_is": "True", "target_pos": "intransitive_verb"},
            {"term": "burns", "is_capitalized": "False", "suffix_is": "True", "target_pos": "intransitive_verb"},
            {"term": "mountain", "is_capitalized": "False", "suffix_is": "False", "target_pos": "catalyst_noun"},
            {"term": "factory", "is_capitalized": "False", "suffix_is": "False", "target_pos": "catalyst_noun"}
        ]

        # 🌴 EXPANDED TIER 2 DATASET: Multi-Domain Unit Containment Anchors
        self.unit_components_dataset = [
            # 🏢 Domain A: Tactical Allocation (BFS / Fire Dept)
            {"contained_in": "dispatch_queue", "manages_sequence": "True", "is_infrastructure": "False", "target_unit": "tactical_allocator"},
            {"contained_in": "trucks", "manages_sequence": "True", "is_infrastructure": "False", "target_unit": "tactical_allocator"},
            
            # ⚛️ Domain B: Quantum Systems
            {"contained_in": "qubit", "manages_sequence": "False", "is_infrastructure": "False", "target_unit": "quantum_circuit"},
            {"contained_in": "register_core", "manages_sequence": "False", "is_infrastructure": "False", "target_unit": "quantum_circuit"},
            
            # 🚨 Domain C: Emergency Infrastructure (Smoke / Water)
            {"contained_in": "sensor_for_smoke", "manages_sequence": "False", "is_infrastructure": "True", "target_unit": "emergency_infrastructure"},
            {"contained_in": "water_pipes", "manages_sequence": "False", "is_infrastructure": "True", "target_unit": "emergency_infrastructure"},
            
            # 🗺️ Domain D: Topological Failovers (Graph Minor Scenarios)
            {"contained_in": "mesh_radio", "manages_sequence": "True", "is_infrastructure": "True", "target_unit": "topological_failover_minor"},
            {"contained_in": "microwave_links", "manages_sequence": "True", "is_infrastructure": "True", "target_unit": "topological_failover_minor"}
        ]

    def calculate_entropy(self, dataset, target_key):
        if not dataset: return 0
        counts = {}
        for d in dataset:
            val = d[target_key]
            counts[val] = counts.get(val, 0) + 1
        entropy = 0.0
        total = len(dataset)
        for val, count in counts.items():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def find_best_split(self, dataset, features, target_key):
        base_entropy = self.calculate_entropy(dataset, target_key)
        best_gain, best_feat, best_val = -1, None, None
        for f in features:
            values = set(d[f] for d in dataset if f in d)
            for val in values:
                left = [d for d in dataset if d.get(f) == val]
                right = [d for d in dataset if d.get(f) != val]
                if not left or not right: continue
                p_left = len(left) / len(dataset)
                p_right = len(right) / len(dataset)
                gain = base_entropy - (p_left * self.calculate_entropy(left, target_key) + p_right * self.calculate_entropy(right, target_key))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val

    def build_id3_tree(self, dataset, features, target_key, depth=0):
        if not dataset: return WorldLevelNode(is_leaf=True, classification="empty_stasis")
        labels = set(d[target_key] for d in dataset)
        if len(labels) == 1:
            return WorldLevelNode(is_leaf=True, classification=list(labels))
        if not features or depth > 3:
            counts = {}
            for d in dataset: counts[d[target_key]] = counts.get(d[target_key], 0) + 1
            return WorldLevelNode(is_leaf=True, classification=max(counts, key=counts.get))

        feat, val = self.find_best_split(dataset, features, target_key)
        if feat is None:
            counts = {}
            for d in dataset: counts[d[target_key]] = counts.get(d[target_key], 0) + 1
            return WorldLevelNode(is_leaf=True, classification=max(counts, key=counts.get))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        left_data = [d for d in dataset if d.get(feat) == val]
        right_data = [d for d in dataset if d.get(feat) != val]
        new_feats = [f for f in features if f != feat]
        node.tb = self.build_id3_tree(left_data, new_feats, target_key, depth + 1)
        node.fb = self.build_id3_tree(right_data, new_feats, target_key, depth + 1)
        return node

    def dump_tree_structure(self, node, indent="   "):
        if node is None: return
        if node.is_leaf:
            print(f"{indent}📦 [LEAF DATA RECOVERY] ──> **{node.classification}**")
            return
        print(f"{indent}🔍 [NODE SPLIT]: Checked feature choice [{node.split_feature}] == '{node.split_value}'?")
        print(f"{indent}  ├── T ──>", end="")
        self.dump_tree_structure(node.tb, indent + "  │   ")
        print(f"{indent}  └── F ──>", end="")
        self.dump_tree_structure(node.fb, indent + "      ")

    def execute_sequential_training(self):
        print("=" * 95)
        print("🚀 EXPANDED TIER 2 STRUCTURAL TRAINING PASSED OVER CORE WORLD")
        print("=" * 95)

        # ─── TIER 1 RETRAIN ───
        t1_features = ["is_capitalized", "suffix_is"]
        t1_root = self.build_id3_tree(self.raw_tokens_dataset, t1_features, "target_pos")
        print("🌲 Discovered Tier 1 Geometry:")
        self.dump_tree_structure(t1_root)
        with open(os.path.join(self.model_dir, "level1_vocab.pkl"), "wb") as f: pickle.dump(t1_root, f)

        # ─── EXPANDED TIER 2 MULTI-CLASS TRAINING ───
        print("\n🎬 [TRAINING TIER 2]: Computing multi-class information gain across expanded domains...")
        t2_features = ["manages_sequence", "is_infrastructure", "contained_in"]
        t2_root = self.build_id3_tree(self.unit_components_dataset, t2_features, "target_unit")
        print("🌲 Discovered Deeper Tier 2 Unit Geometry:")
        self.dump_tree_structure(t2_root)
        with open(os.path.join(self.model_dir, "level2_unit.pkl"), "wb") as f: pickle.dump(t2_root, f)

        # Tiers 3-5 Serialization Defaults
        t3_root = WorldLevelNode(split_feature="situation_context", split_value="network_routing_topology")
        t3_root.tb = WorldLevelNode(is_leaf=True, classification="Story Root: Network Routing Topology")
        t3_root.fb = WorldLevelNode(is_leaf=True, classification="Story Root: Alternative Domains")
        with open(os.path.join(self.model_dir, "level3_story.pkl"), "wb") as f: pickle.dump(t3_root, f)

        t4_root = WorldLevelNode(split_feature="abstract_isomorphism", split_value="network_routing_topology")
        t4_root.tb = WorldLevelNode(is_leaf=True, classification="Analogy Confirmed: Isomorphic Queue Match")
        t4_root.fb = WorldLevelNode(is_leaf=True, classification="Analogy Disjoined")
        with open(os.path.join(self.model_dir, "level4_analogy.pkl"), "wb") as f: pickle.dump(t4_root, f)

        t5_root = WorldLevelNode(split_feature="primary_modality_blocked", split_value="True")
        t5_root.tb = WorldLevelNode(is_leaf=True, classification="Generative Strategy: Execute Group Inversion Rollback")
        t5_root.fb = WorldLevelNode(is_leaf=True, classification="Standard Path Intact")
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "wb") as f: pickle.dump(t5_root, f)

        print("\n" + "=" * 95)
        print("🏆 TIER 2 ENRICHMENT STEP COMPLETE: DEEPER TOPOLOGICAL DIFFERENTIATION LOCKED")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    trainer = SequentialWorldTrainer()
    trainer.execute_sequential_training()
