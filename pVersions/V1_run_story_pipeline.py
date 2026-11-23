import os
import json
import pickle
import re

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.is_leaf = is_leaf
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class TimeTravelJSONPipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.json_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/stories_raw/timetravel_examples.json"
        
        # Load the trained Zalta topological truth trees from disk
        with open(os.path.join(self.model_dir, "level1_vocab.pkl"), "rb") as f: self.t1 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level2_unit.pkl"), "rb") as f: self.t2 = pickle.load(f)

    def evaluate_node(self, node, feature_vector):
        if node is None: return "unmapped_stasis"
        if node.is_leaf:
            val = node.classification
            return val if not isinstance(val, list) else val[0]
        val = feature_vector.get(node.split_feature, "False")
        if str(val) == str(node.split_value):
            return self.evaluate_node(node.tb, feature_vector)
        return self.evaluate_node(node.fb, feature_vector)

    def execute_live_json_stream(self):
        print("=" * 95)
        print("🌊 TIMETRAVEL JSON PIPELINE: STREAMING COUNTERFACTUAL PARTHOOD TRAJECTORIES")
        print("=" * 95)
        
        if not os.path.exists(self.json_path):
            print(f"🚨 Error: Missing JSON dataset file at {self.json_path}")
            return

        with open(self.json_path, "r", encoding="utf-8") as f:
            stories = json.load(f)

        print(f"   🔍 Successfully loaded JSON array. Found {len(stories)} counterfactual records.")
        print("-" * 95)

        # Storage buffers for synchronized progressive appends
        t1_facts, t2_facts, t3_facts, t5_facts = [], [], [], []

        for idx, story in enumerate(stories):
            s_id = story["story_id"]
            premise = story["premise"]
            counterfactual = story["counterfactual"]
            
            print(f"📥 Processing Node: [{s_id}]")
            print(f"   🔹 Premise        : \"{premise}\"")
            print(f"   🔻 Counterfactual : \"{counterfactual}\"")

            # --- PROCESS WORLD A: THE ORIGINAL STAND (Positive Track) ---
            orig_words = re.findall(r"\b[a-zA-Z]+\b", premise)
            for w in orig_words:
                f1 = {"capitalized": "True" if w[0].isupper() else "False", "suffix": w[-2:]}
                p1_pos = self.evaluate_node(self.t1, f1)
                t1_facts.append(f"pos(token_type({w.lower()}, {p1_pos}, {s_id}_orig)).")

            f2_pos = {"has_proper_noun": "True", "contains_counterfactual_twist": "False"}
            p2_pos = self.evaluate_node(self.t2, f2_pos)
            t2_facts.append(f"pos(situation_part({s_id}_vocab, {p2_pos})).")
            t3_facts.append(f"pos(situation_truth({s_id}_orig, true_world_line)).")
            t5_facts.append(f"pos(synthesize_failover({s_id}_orig, standard_path)).")

            # --- PROCESS WORLD B: THE COUNTERFACTUAL TWIST (Negative Track) ---
            cf_words = re.findall(r"\b[a-zA-Z]+\b", counterfactual)
            for w in cf_words:
                f1 = {"capitalized": "True" if w[0].isupper() else "False", "suffix": w[-2:]}
                p1_neg = self.evaluate_node(self.t1, f1)
                t1_facts.append(f"neg(token_type({w.lower()}, {p1_neg}, {s_id}_cf)).")

            f2_neg = {"has_proper_noun": "True", "contains_counterfactual_twist": "True"}
            p2_neg = self.evaluate_node(self.t2, f2_neg)
            t2_facts.append(f"neg(situation_part({s_id}_vocab, {p2_neg})).")
            t3_facts.append(f"neg(situation_truth({s_id}_cf, encodes_counterfactual)).")
            t5_facts.append(f"neg(synthesize_failover({s_id}_cf, alternate_operator_override)).")
            
            print(f"   ➔ Real-time Inference Complete: Traversed Zalta lattices successfully.\n")

        # progressive append update to the respective world locations
        print("-" * 95)
        print("📝 [SERIALIZING TRANSPILED HORN CLAUSES TO PROGRESSIVE DISK]")
        
        paths = {
            "linguistic_tier1/exs.pl": t1_facts,
            "outing_support/exs.pl": t2_facts,
            "situation_rehearsal/exs.pl": t3_facts,
            "grigorchuk_planning_space/exs.pl": t5_facts
        }

        for rel_path, facts in paths.items():
            full_path = os.path.join(self.root_dir, rel_path)
            with open(full_path, "a", encoding="utf-8") as f:
                f.write(f"\n%% --- Progressive JSON TimeTravel Fact Streams ---\n")
                for fact in facts:
                    f.write(f"{fact}\n")
            print(f"   💾 Successfully appended {len(facts)} records inside -> Popper-main/examples/{rel_path}")
            
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = TimeTravelJSONPipeline()
    pipeline.execute_live_json_stream()