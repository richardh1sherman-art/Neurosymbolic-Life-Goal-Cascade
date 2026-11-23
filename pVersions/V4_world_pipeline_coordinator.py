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

        # 📋 Tier 2 Multi-Class Unit Containment Anchors
        self.unit_components_dataset = [
            {"contained_in": "dispatch_queue", "manages_sequence": "True", "is_infrastructure": "False", "target_unit": "tactical_allocator"},
            {"contained_in": "trucks", "manages_sequence": "True", "is_infrastructure": "False", "target_unit": "tactical_allocator"},
            {"contained_in": "qubit", "manages_sequence": "False", "is_infrastructure": "False", "target_unit": "quantum_circuit"},
            {"contained_in": "register_core", "manages_sequence": "False", "is_infrastructure": "False", "target_unit": "quantum_circuit"},
            {"contained_in": "sensor_for_smoke", "manages_sequence": "False", "is_infrastructure": "True", "target_unit": "emergency_infrastructure"},
            {"contained_in": "water_pipes", "manages_sequence": "False", "is_infrastructure": "True", "target_unit": "emergency_infrastructure"},
            {"contained_in": "mesh_radio", "manages_sequence": "True", "is_infrastructure": "True", "target_unit": "topological_failover_minor"},
            {"contained_in": "microwave_links", "manages_sequence": "True", "is_infrastructure": "True", "target_unit": "topological_failover_minor"}
        ]

        # 🌴 NEW TIER 3 DATASET: Macro Situational Story Contexts
        self.situation_stories_dataset = [
            # 🕸️ network_routing_topology
            {"story_id": "story_14_bfs", "operates_on_graph": "True", "has_contingent_fault": "False", "target_situation": "network_routing_topology"},
            {"story_id": "story_15_fire_dept", "operates_on_graph": "True", "has_contingent_fault": "False", "target_situation": "network_routing_topology"},
            
            # ⚛️ advanced_quantum_algebra
            {"story_id": "story_05_quantum", "operates_on_graph": "False", "has_contingent_fault": "False", "target_situation": "advanced_quantum_algebra"},
            
            # 🚨 active_fault_remediation
            {"story_id": "story_17_disaster", "operates_on_graph": "True", "has_contingent_fault": "True", "target_situation": "active_fault_remediation"},
            {"story_id": "story_19_circuit", "operates_on_graph": "True", "has_contingent_fault": "True", "target_situation": "active_fault_remediation"},
            
            # 📉 asymmetric_cost_override
            {"story_id": "story_20_cab", "operates_on_graph": "False", "has_contingent_fault": "True", "target_situation": "asymmetric_cost_override"}
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
        print("🚀 SEQUENTIAL MULTI-TIER GROUNDING SUITE: TRAILING TIER 3 NATIVELY")
        print("=" * 95)

        # ─── TIER 1 ───
        t1_features = ["is_capitalized", "suffix_is"]
        t1_root = self.build_id3_tree(self.raw_tokens_dataset, t1_features, "target_pos")
        print("🌲 Discovered Tier 1 Geometry:")
        self.dump_tree_structure(t1_root)
        with open(os.path.join(self.model_dir, "level1_vocab.pkl"), "wb") as f: pickle.dump(t1_root, f)

        # ─── TIER 2 ───
        t2_features = ["manages_sequence", "is_infrastructure", "contained_in"]
        t2_root = self.build_id3_tree(self.unit_components_dataset, t2_features, "target_unit")
        print("\n🌲 Discovered Tier 2 Geometry:")
        self.dump_tree_structure(t2_root)
        with open(os.path.join(self.model_dir, "level2_unit.pkl"), "wb") as f: pickle.dump(t2_root, f)

        # ─── 👑 NEW TIER 3 SITUATIONAL SCHEMA TRAINING ───
        print("\n🎬 [TRAINING TIER 3]: Computing information gain across macro domain schemas...")
        t3_features = ["operates_on_graph", "has_contingent_fault"]
        t3_root = self.build_id3_tree(self.situation_stories_dataset, t3_features, "target_situation")
        print("🌲 Discovered Deeper Tier 3 Situational Geometry:")
        self.dump_tree_structure(t3_root)
        with open(os.path.join(self.model_dir, "level3_story.pkl"), "wb") as f: pickle.dump(t3_root, f)

        # Tiers 4-5 Serialization Defaults
        t4_root = WorldLevelNode(split_feature="abstract_isomorphism", split_value="network_routing_topology")
        t4_root.tb = WorldLevelNode(is_leaf=True, classification="Analogy Confirmed: Isomorphic Queue Match")
        t4_root.fb = WorldLevelNode(is_leaf=True, classification="Analogy Disjoined")
        with open(os.path.join(self.model_dir, "level4_analogy.pkl"), "wb") as f: pickle.dump(t4_root, f)

        t5_root = WorldLevelNode(split_feature="primary_modality_blocked", split_value="True")
        t5_root.tb = WorldLevelNode(is_leaf=True, classification="Generative Strategy: Execute Group Inversion Rollback")
        t5_root.fb = WorldLevelNode(is_leaf=True, classification="Standard Path Intact")
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "wb") as f: pickle.dump(t5_root, f)

        print("\n" + "=" * 95)
        print("🏆 TIER 3 CONTEXT INTEGRATION EXECUTED SUCCESSFULLY")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    trainer = SequentialWorldTrainer()
    trainer.execute_sequential_training()
