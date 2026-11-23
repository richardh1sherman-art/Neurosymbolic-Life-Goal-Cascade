import os
import sys
import pickle
import random

class HighNoiseDataEngine:
    def __init__(self):
        self.base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.target_bk_path = os.path.join(self.base_path, "arn_analogy_space/bk.pl")
        self.data_store_path = os.path.join(self.base_path, "story_intake_directory/pickled_models/high_noise_dataset.pkl")
        os.makedirs(os.path.dirname(self.target_bk_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.data_store_path), exist_ok=True)
        random.seed(42)

        # 🌴 EXPANDED VOCABULARY CORPUS (Tier 1 Simple Objects)
        self.expanded_vocab = [
            ("Vocabulary", {"term": "judith", "capitalized": "True", "suffix": "th", "pos": "proper_noun"}, "+"),
            ("Vocabulary", {"term": "george", "capitalized": "True", "suffix": "ge", "pos": "proper_noun"}, "+"),
            ("Vocabulary", {"term": "johnny", "capitalized": "True", "suffix": "ny", "pos": "proper_noun"}, "+"),
            ("Vocabulary", {"term": "miranda", "capitalized": "True", "suffix": "da", "pos": "proper_noun"}, "+"),
            ("Vocabulary", {"term": "falls", "capitalized": "False", "suffix": "is", "pos": "intransitive_verb"}, "+"),
            ("Vocabulary", {"term": "burns", "capitalized": "False", "suffix": "ns", "pos": "intransitive_verb"}, "+"),
            ("Vocabulary", {"term": "reduces", "capitalized": "False", "suffix": "es", "pos": "intransitive_verb"}, "+"),
            ("Vocabulary", {"term": "mountain", "capitalized": "False", "suffix": "in", "pos": "catalyst_noun"}, "+"),
            ("Vocabulary", {"term": "flashlight", "capitalized": "False", "suffix": "ht", "pos": "tool_noun"}, "+"),
            ("Vocabulary", {"term": "expensive", "capitalized": "False", "suffix": "ve", "pos": "adjective"}, "+"),
            ("Vocabulary", {"term": "quantum", "capitalized": "False", "suffix": "um", "pos": "adjective"}, "+")
        ]

        # 🌴 EXPANDED SENTENCE DATASET WITH INJECTED NOISE (500 records)
        self.dataset = []
        for i in range(500):
            vocab_item = random.choice(self.expanded_vocab)
            # 🚨 FIX: Extract attributes using tuple index [1] to locate the feature dictionary
            term = vocab_item[1]["term"]
            pos = vocab_item[1]["pos"]
            
            is_valid = (i % 2 == 0)
            case_attr = "sbj" if is_valid else "obj"
            pn_attr = "3s" if (i % 3 == 0) else "1s"
            
            # NOISE INJECTION STEP (20% of dataset is intentionally corrupted)
            is_noisy = (random.random() < 0.20)
            if is_noisy:
                case_attr = random.choice(["sbj", "obj"])
                pn_attr = random.choice(["3s", "1s"])
                sign = "-" if is_valid else "+" 
            else:
                sign = "+" if is_valid else "-"

            complex_obj = (
                "Sentence",
                {
                    "term": term,
                    "pos_class": pos,
                    "case": case_attr,
                    "pn": pn_attr,
                    "is_noisy_instance": "True" if is_noisy else "False"
                },
                f"sentence_{i}",
                sign
            )
            self.dataset.append(complex_obj)

    def write_dcg_rules_to_bk(self):
        print("Public Message: Compiling Enhanced L2 DCG safeguards to background laws...")
        dcg_content = """%% ===============================================================
%% 🌀 ENHANCED L2 DEFINITE CLAUSE GRAMMAR WITH CASE SAFEGUARDS
%% ===============================================================
s(Head, S_In, S_Out) :-
    np(sbj, PN, _H, S_In, S_Temp),
    vp(PN, Head, S_Temp, S_Out).

np(sbj, 3s, judith, [judith|Tail], Tail).
np(sbj, 3s, george, [george|Tail], Tail).
np(sbj, 3s, johnny, [johnny|Tail], Tail).
np(sbj, 3s, miranda, [miranda|Tail], Tail).
np(obj, _, _, _, _) :- fail. 
vp(3s, _, [Word|Tail], Tail).
"""
        with open(self.target_bk_path, "w", encoding="utf-8") as f:
            f.write(dcg_content)

    def freeze_dataset(self):
        with open(self.data_store_path, "wb") as f:
            pickle.dump((self.expanded_vocab, self.dataset), f)
        print(f"💾 [FS FREEZE]: High-noise dataset successfully cached to disk.")

if __name__ == "__main__":
    engine = HighNoiseDataEngine()
    engine.write_dcg_rules_to_bk()
    engine.freeze_dataset()
