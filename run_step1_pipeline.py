import os
import sys
import re

class ParseTreeNode:
    """A live situation tree node tracking terminal leaf exemplar memory."""
    def __init__(self, feature=None, value=None, is_leaf=False, classification=None):
        self.feature = feature          
        self.value = value              
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                  
        self.fb = None                  

class AutomatedBootstrappingPipeline:
    def __init__(self):
        # Tree #1: POS Tagging Tree
        self.level1_root = ParseTreeNode(is_leaf=True, classification="noun")
        # Tree #3: Logical Schema Parser Tree
        self.tree3_root = ParseTreeNode(is_leaf=True, classification="atom")

    def evaluate_tree(self, node, feature_vector):
        if node.is_leaf:
            return node.classification
        feat_val = feature_vector.get(node.feature)
        if feat_val == node.value:
            return self.evaluate_tree(node.tb, feature_vector)
        return self.evaluate_tree(node.fb, feature_vector)

    def train_node(self, node, feature_vector, target_class, split_feat, split_val):
        """👑 THE LIVE NODE-SPLITTING LOOP: Forces a crisp branch split on conflict."""
        if node.is_leaf:
            if node.classification != target_class:
                node.is_leaf = False
                node.feature = split_feat
                node.value = split_val
                node.tb = ParseTreeNode(is_leaf=True, classification=target_class)
                node.fb = ParseTreeNode(is_leaf=True, classification=node.classification)
            return
        feat_val = feature_vector.get(node.feature)
        if feat_val == node.value:
            self.train_node(node.tb, feature_vector, target_class, split_feat, split_val)
        else:
            self.train_node(node.fb, feature_vector, target_class, split_feat, split_val)

    def compile_text_to_abstract_prolog(self, raw_sentence, strategy):
        """👑 COGNITIVE PARSING PASS: Varies the execution logic depending on target tree type."""
        words = raw_sentence.split()
        resolved_subject = "X"
        resolved_context = "context"
        action_token = "action"
        
        for word in words:
            # Tree #1 feature extraction pass
            l1_features = {
                "capitalized": word[0].isupper() if word else False,
                "suffix": word[-2:] if len(word) >= 2 else "none"
            }
            inferred_pos = self.evaluate_tree(self.level1_root, l1_features)
            
            # Tree #2 & #3 feature assignment layers
            l3_features = {"pos_tag": inferred_pos}
            if inferred_pos == "proper_noun":
                l3_features["word_role"] = "subject"
            elif inferred_pos == "context_noun":
                l3_features["word_role"] = "modifier"
            elif "verb" in inferred_pos:
                l3_features["word_role"] = "action"

            prolog_primitive_type = self.evaluate_tree(self.tree3_root, l3_features)
            clean_token = word.lower() if prolog_primitive_type == "atom" else word.capitalize()
            
            if inferred_pos == "proper_noun":
                resolved_subject = clean_token
            elif inferred_pos == "context_noun":
                resolved_context = clean_token
            elif "verb" in inferred_pos:
                action_token = word.lower()

        # 🚨 ALTERNATIVE ABSTRACTION GENERATION MATRIX 🚨
        compiled_facts = []
        if strategy == "Syntactic Literal":
            compiled_facts.append(f"{action_token}({resolved_subject}).")
        elif strategy == "Functional Role":
            # Focuses on actor capabilities/movement anomalies
            if action_token in ["falls", "burns"]:
                compiled_facts.append(f"uncontrolled_descent({resolved_subject}).")
            else:
                compiled_facts.append(f"operational_state({resolved_subject}, active).")
        elif strategy == "Environmental Impact":
            # Ignores action mechanics, locks onto safety risk metrics
            compiled_facts.append(f"accident({resolved_subject}, {resolved_context}).")
                
        return compiled_facts

def write_situation_files(strategy_name, story_id, facts_list):
    base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    folder_mapping = {
        "Syntactic Literal": "generated_literal_space",
        "Functional Role": "generated_functional_space",
        "Environmental Impact": "generated_impact_space"
    }
    
    target_dir = os.path.join(base_path, folder_mapping[strategy_name])
    os.makedirs(target_dir, exist_ok=True)
    
    # Materialize local logic files Under Program Control
    bk_path = os.path.join(target_dir, "bk.pl")
    with open(bk_path, "a") as f:
        f.write(f"\n%% Story Data: {story_id}\n")
        for fact in facts_list:
            f.write(f"abstract_object({story_id}, {strategy_name.replace(' ', '_').lower()}, {fact[:-1]}).\n")
            
    with open(os.path.join(target_dir, "bias.pl"), "w") as f:
        f.write("head_pred(discovered_analogy,2).\nbody_pred(abstract_object,3).\n")
        
    with open(os.path.join(target_dir, "exs.pl"), "w") as f:
        f.write("pos(discovered_analogy(judith_rescue, kitchen_fire)).\n")

def main():
    # 🚨 FIX: Aligned class constructor naming
    pipeline = AutomatedBootstrappingPipeline()

    # Bootstrap Tree #1 Facts
    t1_data = [
        ("Judith", {"capitalized": True, "suffix": "th"}, "proper_noun"),
        ("George", {"capitalized": True, "suffix": "ge"}, "proper_noun"),
        ("falls", {"capitalized": False, "suffix": "ls"}, "intransitive_verb"),
        ("burns", {"capitalized": False, "suffix": "ns"}, "intransitive_verb"),
        ("mountain", {"capitalized": False, "suffix": "in"}, "context_noun"),
        ("kitchen", {"capitalized": False, "suffix": "en"}, "context_noun")
    ]
    for w, feat, t_class in t1_data:
        pipeline.train_node(pipeline.level1_root, feat, t_class, "suffix", feat["suffix"])

    # Bootstrap Tree #3 Facts
    t3_data = [
        ({"pos_tag": "proper_noun", "word_role": "subject"}, "atom"),
        ({"pos_tag": "intransitive_verb", "word_role": "action"}, "unary_predicate"),
        ({"pos_tag": "context_noun", "word_role": "modifier"}, "atom")
    ]
    for feat, t_class in t3_data:
        pipeline.train_node(pipeline.tree3_root, feat, t_class, "pos_tag", feat["pos_tag"])

    # Define our narrative inputs
    stories = [
        ("judith_rescue", "Judith falls mountain"),
        ("kitchen_fire", "George burns kitchen")
    ]
    strategies = ["Syntactic Literal", "Functional Role", "Environmental Impact"]

    print("=" * 85)
    print("🚀 BOOTSTRAP RUN: EXECUTING MULTI-STRATEGY PARSING TREES (STEP 1)")
    print("=" * 85)

    # Clean old run traces from target directory files
    for strat in strategies:
        dir_name = os.path.join("/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples", folder_mapping_name := {
            "Syntactic Literal": "generated_literal_space",
            "Functional Role": "generated_functional_space",
            "Environmental Impact": "generated_impact_space"
        }[strat])
        dir_path = os.path.join("/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples", folder_mapping_name)
        if os.path.exists(dir_path):
            for file in ["bk.pl", "exs.pl", "bias.pl"]:
                p = os.path.join(dir_path, file)
                if os.path.exists(p): os.remove(p)

    # Process alternative parsings and generate the multiple updates to file system tables
    for story_id, text in stories:
        print(f"\n📥 Ingesting Text Story Stream: '{text}'")
        for strategy in strategies:
            abstract_facts = pipeline.compile_text_to_abstract_prolog(text, strategy)
            write_situation_files(strategy, story_id, abstract_facts)
            print(f"   ✨ Tree Strategy [{strategy:<20}] ──> Emitted Abstraction: {abstract_facts}")

    print("\n" + "=" * 85)
    print("📊 STEP 1 VERIFICATION: DUMPING GENERATED FILE SYSTEM TABLES")
    print("=" * 85)
    
    spaces = ["generated_literal_space", "generated_functional_space", "generated_impact_space"]
    for space in spaces:
        p = f"/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/{space}/bk.pl"
        if os.path.exists(p):
            print(f"📁 Content matrix inside Local Logic -> '{space}/bk.pl':")
            with open(p, "r") as f:
                for line in f:
                    if line.strip(): print(f"   {line.strip()}")
            print("-" * 85)

if __name__ == "__main__":
    main()
