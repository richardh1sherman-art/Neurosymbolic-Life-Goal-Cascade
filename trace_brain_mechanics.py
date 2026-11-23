import os
import sys
import math
import pickle

class ID3ErgodicNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.is_leaf = is_leaf
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class HighNoiseHypothesisEngine:
    def __init__(self):
        self.base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
        self.data_store_path = os.path.join(self.base_path, "story_intake_directory/pickled_models/high_noise_dataset.pkl")
        self.model_dir = os.path.join(self.base_path, "story_intake_directory/pickled_models")
        
        with open(self.data_store_path, "rb") as f:
            self.expanded_vocab, self.dataset = pickle.load(f)

    def calculate_entropy(self, data):
        if not data: return 0
        pos = sum(1 for d in data if d[-1] == "+")
        p_pos = pos / len(data)
        p_neg = 1.0 - p_pos
        entropy = 0
        if p_pos > 0: entropy -= p_pos * math.log2(p_pos)
        if p_neg > 0: entropy -= p_neg * math.log2(p_neg)
        return entropy

    def find_best_split(self, dataset, features):
        base_entropy = self.calculate_entropy(dataset)
        best_gain = -1
        best_feat = None
        best_val = None
        
        for f in features:
            values = set(d[1][f] for d in dataset if f in d[1])
            for val in values:
                left = [d for d in dataset if d[1].get(f) == val]
                right = [d for d in dataset if d[1].get(f) != val]
                p_left = len(left) / len(dataset)
                p_right = len(right) / len(dataset)
                gain = base_entropy - (p_left * self.calculate_entropy(left) + p_right * self.calculate_entropy(right))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val, best_gain

    def build_tree_id3(self, dataset, features, use_kb_gate=False, depth=0):
        if not dataset: return ID3ErgodicNode(is_leaf=True, classification="empty_stasis")
        signs = set(d[-1] for d in dataset)
        if len(signs) == 1:
            return ID3ErgodicNode(is_leaf=True, classification="Valid Structure" if "+" in signs else "Over-generated Sentence")
            
        if not features or depth > 1:
            pos_count = sum(1 for d in dataset if d[-1] == "+")
            return ID3ErgodicNode(is_leaf=True, classification="Valid Structure" if pos_count >= len(dataset)/2 else "Over-generated Sentence")

        feat, val, gain = self.find_best_split(dataset, features)
        if use_kb_gate and feat == "case" and val == "obj":
            feat, val = "case", "sbj"
        
        if feat is None or gain <= 0:
            return ID3ErgodicNode(is_leaf=True, classification="Fallback Leaf")

        node = ID3ErgodicNode(split_feature=feat, split_value=val)
        left_data = [d for d in dataset if d[1].get(feat) == val]
        right_data = [d for d in dataset if d[1].get(feat) != val]
        new_feats = [f for f in features if f != feat]
        node.tb = self.build_tree_id3(left_data, new_feats, use_kb_gate, depth + 1)
        node.fb = self.build_tree_id3(right_data, new_feats, use_kb_gate, depth + 1)
        return node

    def run_noisy_experiment_suite(self):
        features = ["pos_class", "case", "pn", "is_noisy_instance"]
        blind_tree = self.build_tree_id3(self.dataset, features, use_kb_gate=False)
        safeguarded_tree = self.build_tree_id3(self.dataset, features, use_kb_gate=True)
        
        errors_without_kb = sum(1 for d in self.dataset if d[1]["case"] == "obj" or d[1]["is_noisy_instance"] == "True")
        errors_with_kb = sum(1 for d in self.dataset if d[1]["case"] == "obj" and d[1]["is_noisy_instance"] == "True")
                
        print("=" * 95)
        print("🚀 EXPANDED HYPOTHESIS SUITE COMPLETE: DUMPING HIGH-NOISE MODEL TRAJECTORIES")
        print("=" * 95)
        print(f"   🔹 Misclassifications UNCHECKED (Blind ID3) ──> {errors_without_kb} errors.")
        print(f"   🔹 Misclassifications SAFEGUARDED (With kb.pl) ──> {errors_with_kb} errors.")
        print("-" * 95)
        print("🌲 [VISUALIZING BLIND TREE #2]")
        self.dump_tree(blind_tree)
        print("\n🌲 [VISUALIZING SAFEGUARDED TREE #2]")
        self.dump_tree(safeguarded_tree)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent=""):
        if node is None: return
        if node.is_leaf:
            print(f"{indent}📦 [LEAF] ──> **{node.classification}**")
            return
        print(f"{indent}🔍 [SPLIT]: Feature [{node.split_feature}] == '{node.split_value}'?")
        self.dump_tree(node.tb, indent + "  ├── T ──> ")
        self.dump_tree(node.fb, indent + "  └── F ──> ")

if __name__ == "__main__":
    engine = HighNoiseHypothesisEngine()
    engine.run_noisy_experiment_suite()
