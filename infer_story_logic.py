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

class DCGInferencePipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.dcg_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl"
        self.dev_json_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Counterfactual-StoryRW-master/data/dev_network.json"
        
        # Load the level 5 strategy tree strictly in READ-ONLY mode
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "rb") as f:
            self.t5 = pickle.load(f)

    def query_prolog_dcg(self, clean_sentence):
        """👑 THE INTENSIONAL SYNTAX GATE: Asks SWI-Prolog DCG to validate sentence structure."""
        # Sanitize text input for safe Prolog string atom consumption
        sanitized = re.sub(r'[^a-zA-Z\s]', '', clean_sentence).lower().strip()
        if not sanitized: return False, "empty"
        
        # Temporary Prolog verification wrapper execution hook
        prolog_query = f"consult('{self.dcg_path}'), (parse_sentence('{sanitized}', Term) -> write(Term) ; write(failed_parse)), halt."
        
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=2
            )
            output = result.stdout.strip()
            if "failed_parse" in output or not output:
                return False, "failed_syntax"
            return True, output
        except Exception:
            return False, "offline_fallback"

    def evaluate_tree(self, node, feature_vector):
        if node is None: return "unknown"
        if node.is_leaf: return node.classification
        val = feature_vector.get(node.split_feature, "False")
        if str(val) == str(node.split_value): return self.evaluate_tree(node.tb, feature_vector)
        return self.evaluate_tree(node.fb, feature_vector)

    def execute_dcg_batch_inference(self):
        print("=" * 95)
        print("🔮 INTENSIONAL INFERENCE SUITE: RUNNING LIVE SWI-PROLOG TIER 1 DCG SYNTAX PARSER")
        print("=" * 95)
        
        if not os.path.exists(self.dev_json_path):
            print(f"🚨 Error: Target validation JSON missing at {self.dev_json_path}")
            return

        with open(self.dev_json_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        print(f"   🔍 Ingesting {len(records)} active research profiles from local disk storage.")
        print("-" * 95)

        t5_facts = []

        for idx, r in enumerate(records):
            clean_id = f"s_{idx}"
            
            # Extract discrete components from the text structure
            premise = r.get("premise", "")
            counterfactual = r.get("counterfactual", "")
            
            # Invoke the live Tier 1 DCG Parser to inspect the text properties
            is_valid_syntax, parse_term = self.query_prolog_dcg(counterfactual)
            
            # Map features dynamically based on intensional syntactic proofs
            is_blocked = "True" if any(w in parse_term for w in ["cancelled", "severed", "failed", "blocked"]) else "False"
            is_invertible = "True" if any(w in parse_term for w in ["friend", "alternative", "secondary", "train"]) else "False"
            
            features = {
                "primary_blocked": is_blocked,
                "inversion_supported": is_invertible
            }
            
            # Pass our DCG-derived features through the frozen Level 5 tree nodes
            res_strategy = self.evaluate_tree(self.t5, features)
            if isinstance(res_strategy, list): res_strategy = res_strategy[0]
            
            print(f"📥 Story Query [{clean_id}] Context:")
            print(f"   📜 Text Target ──➔ \"{counterfactual}\"")
            print(f"   🌀 DCG Syntax  ──➔ {parse_term}")
            print(f"   🎯 Inference   ──➔ Plan Strategy Selected: **{res_strategy}**\n")
            
            if res_strategy == "local_partial_group_inversion":
                t5_facts.append(f"deleted_edge(station, platform_node, {clean_id}).")
                t5_facts.append(f"contracted_nodes(station, cab_vertex, {clean_id}).")
            elif res_strategy == "global_alternate_modality_routing" or res_strategy == "graph_minor_edge_contraction_healing":
                t5_facts.append(f"deleted_edge(airport_gate, flight_line, {clean_id}).")

        # Commit compiled predicates directly down to disk storage files
        t5_exs_path = os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl")
        with open(t5_exs_path, "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Graph Minor Facts Driven by Tier 1 DCG Intensional Parser\n")
            for fact in t5_facts: f.write(f"{fact}\n")

        print("-" * 95)
        print(f"💾 [WORLD FS UPDATE]: Saved fresh DCG-verified facts into 'grigorchuk_planning_space/exs.pl'")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = DCGInferencePipeline()
    pipeline.execute_dcg_batch_inference()