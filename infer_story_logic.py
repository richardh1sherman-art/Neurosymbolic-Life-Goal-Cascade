import os
import json
import pickle
import subprocess
import re

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class ForestSituationInferencePipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.dcg_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl"
        
        # 🚨 READ-ONLY MODE: Load the exact multi-sentence forest model
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "rb") as f:
            self.t5 = pickle.load(f)

    def query_cross_tree_parthood(self, text_segment):
        """👑 THE SITUATIONAL DELEGATION HOOK: Queries the syntax rules for concept membership."""
        # Clean the input phrase to safe Prolog atom formats
        clean_text = text_segment.replace("'", "").strip().lower()
        if not clean_text: return "unknown"
        
        # Interrogates part_of(Text, situation_tree, Concept) via the compiler gate
        prolog_query = f"consult('{self.dcg_path}'), (part_of('{clean_text}', situation_tree, Concept) -> write(Concept) ; write('unknown')), halt."
        
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=3
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def evaluate_forest_logic(self, node, feature_vector):
        if node is None: return "unknown"
        if node.is_leaf:
            if isinstance(node.classification, list):
                return node.classification[0] if node.classification else "unknown"
            return node.classification
        
        val = feature_vector.get(node.split_feature, "False")
        if str(val) == str(node.split_value): 
            return self.evaluate_forest_logic(node.tb, feature_vector)
        return self.evaluate_forest_logic(node.fb, feature_vector)

    def run_forest_cascade(self):
        print("=" * 95)
        print("🔮 INTENSIONAL INFERENCE SUITE: PARSING CONSOLIDATED MULTI-SENTENCE COGNITIVE FOREST")
        print("=" * 95)
        
        # The multi-sentence situational arrays structured straight from your notes
        multi_sentence_stories = [
            {
                "id": "st1_timeline", 
                "narrative_units": ["without a raise", "kept working hard", "request for a raise is refused", "decided to withdraw his effort"]
            },
            {
                "id": "sb_timeline_pos", 
                "narrative_units": ["was overwhelmed at work", "tried hard and finished everything", "boss rewarded him"]
            },
            {
                "id": "st2_timeline_neg", 
                "narrative_units": ["painful breakup", "attend a party", "anniversary"]
            }
        ]
        
        t5_facts = []

        for story in multi_sentence_stories:
            print(f"📥 Processing Multi-Sentence Situation ID: [{story['id']}]")
            
            # Step 1: Accumulate features dynamically through the Tier 1 parthood lookup hooks
            detected_concepts = []
            features = {}
            
            # Baseline zero-initialization of our active ontology feature matrix keys
            all_ontology_features = ["stagnate", "diligent", "rejection", "withdraw", "difficulty", "effort", "reward", "grief", "engagement", "success"]
            for f in all_ontology_features: features[f] = "False"
            
            for unit in story["narrative_units"]:
                concept = self.query_cross_tree_parthood(unit)
                if concept != "unknown":
                    detected_concepts.append(concept)
                    features[concept] = "True"
            
            # Step 2: Route the gathered feature maps into your unpickled forest lattice
            inferred_schema = self.evaluate_forest_logic(self.t5, features)
            
            print(f"   ├── Extracted Ontology Units ──➔ {detected_concepts}")
            print(f"   └── Forest Schema Decision   ──➔ **{inferred_schema}**\n")
            
            # Step 3: Serialize resulting logic predicates cleanly to your background drive
            t5_facts.append(f"situation_classification({story['id']}, schema_{inferred_schema}).")

        exs_path = os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Intensional Facts Driven by Interlocking Forest Model\n")
            for fact in t5_facts: f.write(f"{fact}\n")
            
        print("-" * 95)
        print("💾 [FS UPDATE]: Situation-level concept facts safely written into 'grigorchuk_planning_space/exs.pl'")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = ForestSituationInferencePipeline()
    pipeline.run_forest_cascade()
