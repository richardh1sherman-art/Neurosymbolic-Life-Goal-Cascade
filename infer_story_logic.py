import os
import pickle
import subprocess

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class ConsolidatedInferencePipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.dcg_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/popper_workspaces/linguistic_tier1/parser_tier1.pl"
        
        # Load both models securely from disk
        with open(os.path.join(self.model_dir, "level6_parthood_ontology.pkl"), "rb") as f:
            self.t6 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level7_analogy_inferencing.pkl"), "rb") as f:
            self.t7 = pickle.load(f)

    def query_prolog_parthood(self, subject, dimension):
        prolog_query = f"consult('{self.dcg_path}'), (part_of({subject}, {dimension}, Value) -> write(Value) ; write('unknown')), halt."
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=3
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def query_prolog_homomorphism(self, src_element, dst_element):
        prolog_query = f"consult('{self.dcg_path}'), (part_of({src_element}, target_map({dst_element}), Role) -> write(Role) ; write('unknown')), halt."
        try:
            result = subprocess.run(
                ["swipl", "-q", "-g", prolog_query],
                capture_output=True, text=True, timeout=3
            )
            return result.stdout.strip()
        except Exception:
            return "unknown"

    def evaluate_tree(self, node, feature_vector):
        if node is None: return "unknown"
        if node.is_leaf: 
            raw = str(node.classification).lower().strip()
            return raw.replace("[", "").replace("]", "").replace("'", "")
        val = feature_vector.get(node.split_feature, "unknown")
        if str(val) == str(node.split_value): 
            return self.evaluate_tree(node.tb, feature_vector)
        return self.evaluate_tree(node.fb, feature_vector)

    def run_comprehensive_cascade(self):
        print("=" * 95)
        print("🔮 INTENSIONAL INFERENCE SUITE: RUNNING CONSOLIDATED MULTI-REPRESENTATION CORES")
        print("=" * 95)
        
        t5_facts = []

        # --- PHASE 1: EVALUATING SITUATION REPRESENTATIONS (TREE #6) ---
        print("📥 Phase 1: Processing Multi-Sentence Timelines...")
        multi_sentence_stories = [
            {"id": "st1_timeline", "narrative_units": ["without a raise", "kept working hard", "request for a raise is refused", "decided to withdraw his effort"]},
            {"id": "sb_timeline_pos", "narrative_units": ["was overwhelmed at work", "tried hard and finished everything", "boss rewarded him"]},
            {"id": "st2_timeline_neg", "narrative_units": ["painful breakup", "attend a party", "anniversary"]},
            {"id": "john_reversal_timeline", "narrative_units": ["planned using several travel events", "missed the amtrak", "reverse his plans and call a cab"]},
            {"id": "judith_rescue_timeline", "narrative_units": ["switch is on", "bulb is lit", "signal sos in morse code", "helicopter guided specifically to coordinates"]}
        ]

        all_ontology_features = [
            "stagnate", "diligent", "rejection", "withdraw", "difficulty", "effort", "reward", 
            "grief", "engagement", "success", "planned_trajectory", "switch_on", "bulb_lit", 
            "flash_sos", "guided_rescue"
        ]

        for story in multi_sentence_stories:
            features = {f: "False" for f in all_ontology_features}
            for unit in story["narrative_units"]:
                # Lookup concept via situation_tree
                prolog_query = f"consult('{self.dcg_path}'), (part_of('{unit}', situation_tree, Concept) -> write(Concept) ; write('unknown')), halt."
                try:
                    res = subprocess.run(["swipl", "-q", "-g", prolog_query], capture_output=True, text=True, timeout=3)
                    concept = res.stdout.strip()
                    if concept != "unknown": features[concept] = "True"
                except Exception:
                    pass
            
            inferred_schema = self.evaluate_tree(self.t6, features)
            t5_facts.append(f"situation_classification({story['id']}, schema_{inferred_schema}).")

        # --- PHASE 2: EVALUATING ANALOGICAL INFERENCING (TREE #7) ---
        print("\n📥 Phase 2: Processing Relational Homomorphism Maps...")
        structural_pairs = [
            ("dead_battery", "blocked_chimney"),
            ("helicopter_engine", "fire_truck_pump"),
            ("miranda_asleep", "dispatcher_distracted"),
            ("flashlight_beacon", "smoke_detector_alarm")
        ]
        
        analogy_features = {
            "transmission_failure": "False", "mitigation_vector": "False", "awareness_lapse": "False",
            "connection_vector": "False", "has_permission_q": "True", "action_p_occurred": "True"
        }
        
        for src, dst in structural_pairs:
            role = self.query_prolog_homomorphism(src, dst)
            if role != "unknown":
                analogy_features[role] = "True"
                print(f"   🔗 Linked Homomorphism ──➔ [{src}] maps to [{dst}] as a '{role}' role.")
        
        inferred_analogy = self.evaluate_tree(self.t7, analogy_features)
        print(f"🎯 Analogy Result ──➔ **{inferred_analogy}**")
        t5_facts.append(f"analogy_evaluation(kitchen_fire_transfer, schema_{inferred_analogy}).")

        # --- PHASE 3: WRITE PROTECTED UNIFIED OUTPUT TRANSACTION ---
        exs_path = os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl")
        os.makedirs(os.path.dirname(exs_path), exist_ok=True)
        with open(exs_path, "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Consolidated Multi-Tree Facts Sheet\n")
            for fact in t5_facts:
                f.write(f"{fact}\n")
        print("\n💾 [FS UPDATE]: All representations successfully unified and frozen inside 'exs.pl'")
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = ConsolidatedInferencePipeline()
    pipeline.run_comprehensive_cascade()
