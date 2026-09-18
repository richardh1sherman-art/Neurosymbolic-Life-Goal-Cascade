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

class DynamicComprehensiveInference:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.dcg_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl"
        
        # 🚨 READ-ONLY INGESTION: Load the unified multi-class model directly from disk
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "rb") as f:
            self.t5 = pickle.load(f)

    def query_live_dcg_engine(self, raw_sentence):
        """👑 THE INTENSIONAL SYNTAX GATE: Extracts (Type, Concept, Sign) from Prolog."""
        sanitized = re.sub(r'[^a-zA-Z\s]', '', raw_sentence).lower().strip()
        if not sanitized: return "phrase", "unknown", "-"
        
        prolog_query = f"consult('{self.dcg_path}'), (parse_sentence('{sanitized}', Type, Name, Sign) -> format('~w,~w,~w', [Type, Name, Sign]) ; format('phrase,unknown,-', [])), halt."
        
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=3
            )
            output = result.stdout.strip()
            parts = output.split(',')
            if len(parts) == 3:
                return parts
            return ["phrase", "unknown", "-"]
        except Exception:
            return ["phrase", "unknown", "-"]

    def evaluate_tree_logic(self, node, feature_vector):
        if node is None: return "unknown"
        if node.is_leaf:
            if isinstance(node.classification, list):
                return node.classification[0]
            return node.classification
        
        val = feature_vector.get(node.split_feature, "False")
        # Direct check matching the root split geometry computed by the ID3 trainer
        if str(val) == str(node.split_value): 
            return self.evaluate_tree_logic(node.tb, feature_vector)
        return self.evaluate_tree_logic(node.fb, feature_vector)

    def run_comprehensive_cascade(self):
        print("=" * 95)
        print("🔮 INTENSIONAL INFERENCE SUITE: EXECUTING MULTI-DOMAIN RECURSIVE DCG CASCADE")
        print("=" * 95)
        
        # Full evaluation matrix passing all core, infrastructure, and sovereign life tracks
        universal_stories = [
            {"id": "pierre_story_s1", "text": "Pierre loved Halloween"},
            {"id": "pierre_story_s2", "text": "He decided to be a vampire"},
            {"id": "pierre_story_s2_prime", "text": "He decided to be a werewolf"},
            {"id": "alec_story_s2", "text": "Alec figured blocks develop her mind"},
            {"id": "alec_story_s2_prime", "text": "Alec couldnt afford new blocks"},
            {"id": "ana_story_s2", "text": "She took her baby to the studio and pierced ears"},
            {"id": "ana_story_s2_prime", "text": "She decided not to take her baby to get pierced ears"},
            {"id": "john_story_s1", "text": "John needed to determine startup roi"},
            {"id": "fiber_story_s2", "text": "the packets utilized the primary fiber link"},
            {"id": "fiber_story_s2_prime", "text": "an excavator severed the primary fiber link"},
            {"id": "display_story_s2", "text": "commuters monitored the central train arrival display"},
            {"id": "display_story_s2_prime", "text": "power surges corrupted the central train arrival display"},
            {"id": "moses_sovereign_flaw", "text": "Moses committed murder in Egypt"},
            {"id": "david_sovereign_flaw", "text": "David committed adultery with Bathsheba"},
            {"id": "paul_sovereign_flaw", "text": "Paul persecuted the early Church"}
        ]
        
        t5_facts = []

        for s in universal_stories:
            s_text = s["text"]
            stype, concept_name, sign = self.query_live_dcg_engine(s_text)
            
            # Translate the logical sign into the abstract attribute expected by the tree model
            is_neg = "True" if sign == "-" else "False"
            features = {
                "concept_class": concept_name,
                "is_positive_example": is_neg
            }
            
            inferred_action = self.evaluate_tree_logic(self.t5, features)
            
            print(f"📥 Sentence Ingested: \"{s_text}\"")
            print(f"   ├── Grounded Concept Name ──➔ '{concept_name}' (Sign: {sign})")
            print(f"   └── Inferred DT Classifier──➔ **{inferred_action}**\n")
            
            if inferred_action == "trigger_terminal_node_rewrite":
                t5_facts.append(f"execute_rewrite({s['id']}, {concept_name}).")
            else:
                t5_facts.append(f"semantic_match({s['id']}, {concept_name}).")

        # Freeze the generated facts sheet straight back to disk
        exs_path = os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Intensional Facts Driven by Pickled Multi-Domain Tree Layout\n")
            for fact in t5_facts: f.write(f"{fact}\n")
            
        print("-" * 95)
        print("💾 [FS UPDATE]: Dynamic multi-domain facts successfully frozen inside 'exs.pl'")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = DynamicComprehensiveInference()
    pipeline.run_comprehensive_cascade()
