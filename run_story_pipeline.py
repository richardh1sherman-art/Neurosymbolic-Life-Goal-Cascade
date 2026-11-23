import os
import json
import pickle
import re

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class DeepTimeTravelPipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.json_stories_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/stories_raw/timetravel_examples.json"
        self.json_patterns_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/stories_raw/fallacy_patterns.json"
        
        # Ingest the newly deepened tree structures
        with open(os.path.join(self.model_dir, "level3_story.pkl"), "rb") as f: self.t3 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "rb") as f: self.t5 = pickle.load(f)

    def extract_contextual_features(self, premise, counterfactual, story_id, pattern_map):
        combined = (premise + " " + counterfactual).lower()
        has_fallacy = "True" if story_id in pattern_map else "False"
        
        # Categorical feature array mapping to tree equality nodes
        features = {
            "has_contingent_fault": "True" if ("severed" in combined or "cancelled" in combined or "wrong" in combined or "ugliest" in combined) else "False",
            "operates_on_graph": "True" if ("route" in combined or "network" in combined or "airport" in combined or "city" in combined or "phone" in combined) else "False",
            "primary_modality_blocked": "True" if ("severed" in combined or "cancelled" in combined or "wrong" in combined) else "False",
            "local_partial_inversion_supported": "True" if ("friend" in combined or "alternative" in combined or "secondary" in combined) else "False",
            "has_logical_fallacy": has_fallacy,
            "has_fallacy_pattern": has_fallacy
        }
        return features

    def evaluate_node(self, node, feature_vector):
        if node is None: return "unknown"
        if node.is_leaf:
            val = node.classification
            return val[0] if isinstance(val, list) else val
        
        # Execute the absolute equality test against the feature value
        current_val = feature_vector.get(node.split_feature, "False")
        if str(current_val) == str(node.split_value):
            return self.evaluate_node(node.tb, feature_vector)
        return self.evaluate_node(node.fb, feature_vector)

    def execute_deep_cascade(self):
        print("=" * 95)
        print("🌊 RUNNING DEEP COMPREHENSIVE PIPELINE OVER FRESHLY TRAINED GEOMETRIES")
        print("=" * 95)
        
        with open(self.json_stories_path, "r", encoding="utf-8") as f: stories = json.load(f)
        with open(self.json_patterns_path, "r", encoding="utf-8") as f: patterns = json.load(f)

        pattern_map = {p["applied_story_context"]: p for p in patterns}
        t3_facts, t5_facts = [], []

        for story in stories:
            s_id = story["story_id"]
            features = self.extract_contextual_features(story["premise"], story["counterfactual"], s_id, pattern_map)
            
            # Evaluate using the newly trained deep equality nodes
            p3 = self.evaluate_node(self.t3, features)
            p5 = self.evaluate_node(self.t5, features)
            
            short_id = f"s_{s_id.split('-')[0]}"
            print(f"📥 Transpiling Story ID [{short_id}]:")
            print(f"   ➔ Tier 3 Situation Inferred ──➔ **{p3}**")
            print(f"   ➔ Tier 5 Strategy Inferred  ──➔ **{p5}**")

            # Handle the specific graph minor edge contraction output
            if p5 == "graph_minor_edge_contraction_healing":
                fact = f"contracted_nodes(failed_link_{short_id}, secondary_failover_vertex)."
                t5_facts.append(fact)
                print(f"   🎯 [METRIC EXTANT]: Fusing structural contraction ──➔ {fact}")
                
            t3_facts.append(f"pos(situation_context({short_id}, {p3})).")
            t5_facts.append(f"pos(synthesized_strategy({short_id}, {p5})).")
            print()

        # Serialize progressive output records straight to disk files
        with open(os.path.join(self.root_dir, "situation_rehearsal/exs.pl"), "w", encoding="utf-8") as f:
            f.write("%% Deep Integrated Tier 3 Context Facts\n")
            for fact in t3_facts: f.write(f"{fact}\n")
            
        with open(os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl"), "w", encoding="utf-8") as f:
            f.write("%% Deep Integrated Tier 5 Strategy Facts\n")
            for fact in t5_facts: f.write(f"{fact}\n")

        print("-" * 95)
        print("💾 [SERIALIZATION COMPLETE]: Deep multi-tier constraints safely frozen to world workspaces.")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = DeepTimeTravelPipeline()
    pipeline.execute_deep_cascade()