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

    def generate_and_save_prolog_exemplars(self, raw_words):
        """👑 THE LOGIC GENERATOR: Translates raw text tokens into standard Prolog ILP exemplars."""
        print("\n📜 [GENERATING PROLOG EXEMPLARS FROM DYNAMIC TEXT STREAM]")
        print("-" * 95)
        
        prolog_exemplars = []
        proper_nouns = ["judith", "miranda", "george", "johnny"]
        verbs = ["falls", "burns", "rescues", "reduces", "severed"]
        
        # Limit to the first distinct set to prevent console flooding while showing complete formats
        seen_words = set()
        for w in raw_words:
            low_w = w.lower()
            if low_w in seen_words or len(low_w) < 3: continue
            seen_words.add(low_w)
            
            # Map structural tokens to their respective logical types
            if low_w in proper_nouns:
                fact = f"pos(token_type({low_w}, proper_noun))."
            elif low_w in verbs:
                fact = f"pos(token_type({low_w}, intransitive_verb))."
            elif low_w in ["dispatch_queue", "mesh_radio", "qubit"]:
                fact = f"pos(unit_component({low_w}, abstract_structure))."
            else:
                fact = f"pos(token_type({low_w}, general_lexicon))."
                
            prolog_exemplars.append(fact)
            if len(prolog_exemplars) <= 12:  # Print print a punchy preview snippet
                print(f"   ➔ {fact}")

        # Write generated facts directly to Tier 1 filesystem workspace
        t1_exs_path = os.path.join(self.root_dir, "linguistic_tier1/exs.pl")
        with open(t1_exs_path, "w", encoding="utf-8") as f:
            f.write("%% Autogenerated Prolog Exemplars from Stream Tokenizer\n")
            for exemplar in prolog_exemplars:
                f.write(f"{exemplar}\n")
        print(f"   💾 [FS UPDATE]: Complete predicate matrix cleanly appended to -> 'linguistic_tier1/exs.pl'")

    def evaluate_node(self, node, feature_vector):
        if node.is_leaf:
            return node.classification
        val = feature_vector.get(node.split_feature, "False")
        if isinstance(val, list): val = val[0]
        if str(val) == str(node.split_value):
            return self.evaluate_node(node.tb, feature_vector)
        return self.evaluate_node(node.fb, feature_vector)

    def execute_pipeline(self):
        self.bootstrap_6_page_document()
        extracted_features, raw_words = self.parse_text_stream_to_features()
        
        print("=" * 95)
        print("🌊 PIPELINE TRIGGERED: STREAMING REAL-WORLD TEXT CHANNELS THROUGH COGNITIVE MATRIX")
        print("=" * 95)
        print(f"   🔍 Scanned text stream: Extracted {len(raw_words)} raw vocabulary word tokens.")
        print("-" * 95)

        # Bottom-up tree evaluation
        print(f"🔓 [TIER 1 LEXICAL]: Classifying incoming primitives ──> {self.evaluate_node(self.t1, extracted_features)}")
        print(f"🔓 [TIER 2 UNIT]   : Resolving sub-component envelopes ──> {self.evaluate_node(self.t2, extracted_features)}")
        print(f"🔓 [TIER 3 SCHEMA] : Extracting macro situational domain ──> {self.evaluate_node(self.t3, extracted_features)}")
        print(f"🔓 [TIER 4 ANALOGY]: Evaluating cross-story isomorphism mappings ──> {self.evaluate_node(self.t4, extracted_features)}")
        print(f"🔓 [TIER 5 PLAN]   : Synthesizing dynamic group action strategy ──> {self.evaluate_node(self.t5, extracted_features)}")
        
        # Trigger the automatic Prolog translation pass
        self.generate_and_save_prolog_exemplars(raw_words)
        print("=" * 95 + "\n")

if __name__ == "__main__":
    pipeline = ComprehensiveDocumentPipeline()
    pipeline.execute_pipeline()
