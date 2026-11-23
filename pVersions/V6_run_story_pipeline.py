import os
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

class ComprehensiveDocumentPipeline:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        self.root_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.doc_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/stories_raw/6_page_document.txt"
        
        # Load the 5 trained tree structures from disk
        with open(os.path.join(self.model_dir, "level1_vocab.pkl"), "rb") as f: self.t1 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level2_unit.pkl"), "rb") as f: self.t2 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level3_story.pkl"), "rb") as f: self.t3 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level4_analogy.pkl"), "rb") as f: self.t4 = pickle.load(f)
        with open(os.path.join(self.model_dir, "level5_plan_synthesis.pkl"), "rb") as f: self.t5 = pickle.load(f)

    def bootstrap_6_page_document(self):
        doc_content = """
        Linguistic Section: Judith falls down the mountain quickly. Miranda rescues on the terrain.
        Quantum Core Architecture: The register_core instantiates a qubit matrix. Executing a Hadamard gate produces a state superposition circuit.
        Fire Department Network Routing: The dispatcher monitors a sequential dispatch_queue. Fire trucks arrive down city_streets.
        Topological Fault Remediation: A severe storm severed the link. Logistics board engages an alternative mesh_radio.
        """
        with open(self.doc_path, "w", encoding="utf-8") as f:
            f.write(doc_content.strip())

    def parse_text_stream_to_features(self):
        with open(self.doc_path, "r", encoding="utf-8") as f:
            text = f.read()

        words = re.findall(r"\b[a-zA-Z_0-9]+\b", text)
        lower_words = [w.lower() for w in words]
        
        features = {
            "is_capitalized": "True" if any(w.isupper() for w in words) else "False",
            "suffix_is": "True" if any(w.endswith("is") for w in lower_words) else "False",
            "manages_sequence": "True" if ("dispatch_queue" in lower_words or "mesh_radio" in lower_words) else "False",
            "is_infrastructure": "True" if ("city_streets" in lower_words or "mesh_radio" in lower_words) else "False",
            "contained_in": "dispatch_queue" if "dispatch_queue" in lower_words else "False",
            "has_contingent_fault": "True" if ("severed" in lower_words or "storm" in lower_words) else "False",
            "operates_on_graph": "True" if ("network" in lower_words or "routing" in lower_words) else "False",
            "shares_sequencer_queue": "True" if "dispatch_queue" in lower_words else "False",
            "shares_topological_minor": "True" if "mesh_radio" in lower_words else "False",
            "primary_modality_blocked": "True" if "severed" in lower_words else "False",
            "local_partial_inversion_supported": "True" if "alternative" in lower_words else "False"
        }
        return features, words

    def generate_and_save_multi_tier_exemplars(self, raw_words, extracted_features):
        """👑 THE CORE SYNTHESIZER: Translates and synchronizes logic across all 5 world tiers simultaneously."""
        print("\n📜 [GENERATING COMPLETE 5-TIER PROLOG EXEMPLARS FROM TEXT STREAM]")
        print("-" * 95)
        
        t1_exemplars, t2_exemplars, t3_exemplars, t4_exemplars, t5_exemplars = [], [], [], [], []
        proper_nouns = ["judith", "miranda", "george", "johnny"]
        verbs = ["falls", "burns", "rescues", "reduces", "severed"]
        
        tactical_units = ["dispatch_queue", "trucks"]
        quantum_units = ["qubit", "register_core"]
        failover_units = ["mesh_radio", "microwave_links"]

        for w in raw_words:
            low_w = w.lower()
            
            # --- TIER 1 ---
            if low_w in proper_nouns: t1_exemplars.append(f"pos(token_type({low_w}, proper_noun)).")
            elif low_w in verbs: t1_exemplars.append(f"pos(token_type({low_w}, intransitive_verb)).")
            else: t1_exemplars.append(f"pos(token_type({low_w}, general_lexicon)).")
                
            # --- TIER 2 ---
            if low_w in tactical_units:
                t2_exemplars.append(f"pos(unit_component({low_w}, tactical_allocator)).")
                t2_exemplars.append(f"pos(contained_in({low_w}, active_dispatcher)).")
            elif low_w in quantum_units:
                t2_exemplars.append(f"pos(unit_component({low_w}, quantum_circuit)).")
                t2_exemplars.append(f"pos(contained_in({low_w}, register_core)).")
            elif low_w in failover_units:
                t2_exemplars.append(f"pos(unit_component({low_w}, topological_failover_minor)).")
                t2_exemplars.append(f"pos(contained_in({low_w}, network_minor)).")

        # --- TIER 3 ---
        t3_res = self.evaluate_node(self.t3, extracted_features)
        if isinstance(t3_res, list): t3_res = t3_res[0] if len(t3_res) > 0 else "unknown"
        t3_exemplars.append(f"pos(situation_context(active_document_stream, {t3_res})).")

        # --- TIER 4 ---
        t4_res = self.evaluate_node(self.t4, extracted_features)
        if isinstance(t4_res, list): t4_res = t4_res[0] if len(t4_res) > 0 else "unknown"
        t4_exemplars.append(f"pos(isomorphism_map(active_document_stream, {t4_res})).")

        # --- 👑 NEW: TIER 5 PLANNING LAYER TRANSLATION ---
        t5_res = self.evaluate_node(self.t5, extracted_features)
        if isinstance(t5_res, list): t5_res = t5_res[0] if len(t5_res) > 0 else "unknown"
        t5_exemplars.append(f"pos(synthesized_strategy(active_document_stream, {t5_res})).")

        # Display final output preview on the screen
        print("📁 Tier 1 Lexical Preview: ")
        for ex in t1_exemplars[:1]: print(f"   ➔ {ex}")
        print("📁 Tier 2 Unit Preview: ")
        for ex in t2_exemplars[:1]: print(f"   ➔ {ex}")
        print(f"📁 Tier 3 Context Fact : \n   ➔ {t3_exemplars[0]}")
        print(f"📁 Tier 4 Analogy Fact : \n   ➔ {t4_exemplars[0]}")
        print(f"📁 👑 Tier 5 Generative Strategy Fact : \n   ➔ {t5_exemplars[0]}")

        # Commit all files synchronously to disk
        with open(os.path.join(self.root_dir, "linguistic_tier1/exs.pl"), "w", encoding="utf-8") as f:
            for ex in t1_exemplars: f.write(f"{ex}\n")
        with open(os.path.join(self.root_dir, "outing_support/exs.pl"), "w", encoding="utf-8") as f:
            for ex in t2_exemplars: f.write(f"{ex}\n")
        with open(os.path.join(self.root_dir, "situation_rehearsal/exs.pl"), "w", encoding="utf-8") as f:
            for ex in t3_exemplars: f.write(f"{ex}\n")
        with open(os.path.join(self.root_dir, "arn_analogy_space/exs.pl"), "w", encoding="utf-8") as f:
            for ex in t4_exemplars: f.write(f"{ex}\n")
        with open(os.path.join(self.root_dir, "grigorchuk_planning_space/exs.pl"), "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Tier 5 Invertible Strategy Facts\n")
            for ex in t5_exemplars: f.write(f"{ex}\n")
            
        print("-" * 95)
        print("💾 [WORLD FILES SYSTEM COMPLETION]: All 5 tiers of exs.pl registries are fully synchronized!")

    def evaluate_node(self, node, feature_vector):
        if node.is_leaf: return node.classification
        val = feature_vector.get(node.split_feature, "False")
        if str(val) == str(node.split_value): return self.evaluate_node(node.tb, feature_vector)
        return self.evaluate_node(node.fb, feature_vector)

    def execute_pipeline(self):
        self.bootstrap_6_page_document()
        extracted_features, raw_words = self.parse_text_stream_to_features()
        
        print("=" * 95)
        print("🌊 PIPELINE TRIGGERED: STREAMING REAL-WORLD TEXT CHANNELS THROUGH COGNITIVE MATRIX")
        print("=" * 95)
        print(f"   🔍 Scanned text stream: Extracted {len(raw_words)} raw vocabulary word tokens.")
        print("-" * 95)

        print(f"🔓 [TIER 1 LEXICAL]: Classifying incoming primitives ──> {self.evaluate_node(self.t1, extracted_features)}")
        print(f"🔓 [TIER 2 UNIT]   : Resolving sub-component envelopes ──> {self.evaluate_node(self.t2, extracted_features)}")
        print(f"🔓 [TIER 3 SCHEMA] : Extracting macro situational domain ──> {self.evaluate_node(self.t3, extracted_features)}")
        print(f"🔓 [TIER 4 ANALOGY]: Evaluating cross-story isomorphism mappings ──> {self.evaluate_node(self.t4, extracted_features)}")
        print(f"🔓 [TIER 5 PLAN]   : Synthesizing dynamic group action strategy ──> {self.evaluate_node(self.t5, extracted_features)}")
        
        self.generate_and_save_multi_tier_exemplars(raw_words, extracted_features)
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = ComprehensiveDocumentPipeline()
    pipeline.execute_pipeline()
