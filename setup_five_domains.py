import os
import sys

# Re-use our validated multi-tier node structure
class ParseTreeNode:
    def __init__(self, feature=None, value=None, is_leaf=False, classification=None):
        self.feature = feature          
        self.value = value              
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                  
        self.fb = None                  

class FiveDomainIntegratedPipeline:
    def __init__(self):
        self.level1_root = ParseTreeNode(is_leaf=True, classification="noun")
        self.level3_root = ParseTreeNode(is_leaf=True, classification="atom")

    def evaluate_tree(self, node, feature_vector):
        if node.is_leaf:
            return node.classification
        feat_val = feature_vector.get(node.feature)
        if feat_val == node.value:
            return self.evaluate_tree(node.tb, feature_vector)
        return self.evaluate_tree(node.fb, feature_vector)

    def train_node(self, node, feature_vector, target_class, split_feat, split_val):
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

    def compile_domain_to_prolog(self, raw_sentence, strategy):
        words = raw_sentence.split()
        resolved_subject = "variable"
        resolved_context = "context"
        action_token = "action"
        
        for word in words:
            l1_features = {
                "capitalized": word.isupper() if word else False,
                "suffix": word[-2:] if len(word) >= 2 else "none"
            }
            inferred_pos = self.evaluate_tree(self.level1_root, l1_features)
            
            l3_features = {"pos_tag": inferred_pos}
            if inferred_pos == "proper_noun":
                l3_features["word_role"] = "subject"
            elif inferred_pos in ["catalyst_noun", "domain_modifier"]:
                l3_features["word_role"] = "modifier"
            elif "verb" in inferred_pos:
                l3_features["word_role"] = "action"

            prolog_primitive_type = self.evaluate_tree(self.level3_root, l3_features)
            clean_token = word.lower() if prolog_primitive_type == "atom" else word.capitalize()
            
            if inferred_pos == "proper_noun":
                resolved_subject = clean_token
            elif inferred_pos == "domain_modifier":
                resolved_context = clean_token
            elif "verb" in inferred_pos:
                action_token = word.lower()

        compiled_facts = []
        if strategy == "Syntactic Literal":
            compiled_facts.append(f"{action_token}({resolved_subject}).")
        elif strategy == "Functional Role":
            # Unifies all 5 separate applications into the exact same algebraic group rule
            compiled_facts.append(f"validate_tactical_step({resolved_subject}, depth_zero).")
        elif strategy == "Environmental Impact":
            compiled_facts.append(f"accident({resolved_subject}, {resolved_context}).")
                
        return compiled_facts

def write_extended_tables(strategy_name, domain_id, facts_list):
    base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    folder_mapping = {
        "Syntactic Literal": "generated_literal_space",
        "Functional Role": "generated_functional_space",
        "Environmental Impact": "generated_impact_space"
    }
    target_dir = os.path.join(base_path, folder_mapping[strategy_name])
    os.makedirs(target_dir, exist_ok=True)
    
    with open(os.path.join(target_dir, "bk.pl"), "a") as f:
        f.write(f"\n%% Extended Domain Data: {domain_id}\n")
        for fact in facts_list:
            f.write(f"abstract_object({domain_id}, {strategy_name.replace(' ', '_').lower()}, {fact[:-1]}).\n")

def main():
    pipeline = FiveDomainIntegratedPipeline()

    # 📋 EXPANDED LEVEL 1 CORPUS TRAINING: Boostrap new domain lexicons from text strings
    extended_vocab = [
        ("Judith", {"capitalized": True, "suffix": "th"}, "proper_noun", "suffix", "th"),
        ("falls", {"capitalized": False, "suffix": "ls"}, "intransitive_verb", "suffix", "ls"),
        ("mountain", {"capitalized": False, "suffix": "in"}, "domain_modifier", "suffix", "in"),
        # New Domain 1: Theorem Proving
        ("Prover", {"capitalized": True, "suffix": "er"}, "proper_noun", "suffix", "er"),
        ("reduces", {"capitalized": False, "suffix": "es"}, "intransitive_verb", "suffix", "es"),
        ("clauses", {"capitalized": False, "suffix": "es"}, "domain_modifier", "suffix", "es"),
        # New Domain 2: Consensus Protocol
        ("Node", {"capitalized": True, "suffix": "de"}, "proper_noun", "suffix", "de"),
        ("anchors", {"capitalized": False, "suffix": "rs"}, "intransitive_verb", "suffix", "rs"),
        ("voting", {"capitalized": False, "suffix": "ng"}, "domain_modifier", "suffix", "ng"),
        # New Domain 3: Image Processing
        ("Filter", {"capitalized": True, "suffix": "ter"}, "proper_noun", "suffix", "ter"),
        ("maps", {"capitalized": False, "suffix": "ps"}, "intransitive_verb", "suffix", "ps"),
        ("quadtree", {"capitalized": False, "suffix": "ee"}, "domain_modifier", "suffix", "ee")
    ]
    for w, feat, t_class, s_f, s_v in extended_vocab:
        pipeline.train_node(pipeline.level1_root, feat, t_class, s_f, s_v)

    # Bootstrap Level 3 Schema Types
    t3_data = [
        ({"pos_tag": "proper_noun", "word_role": "subject"}, "atom", "pos_tag", "proper_noun"),
        ({"pos_tag": "intransitive_verb", "word_role": "action"}, "unary_predicate", "pos_tag", "intransitive_verb"),
        ({"pos_tag": "domain_modifier", "word_role": "modifier"}, "atom", "pos_tag", "domain_modifier")
    ]
    for feat, t_class, s_f, s_v in t3_data:
        pipeline.train_node(pipeline.level3_root, feat, t_class, s_f, s_v)

    # Ingesting the new multi-domain narratives
    expanded_stories = [
        ("planner_task", "Judith falls mountain"),
        ("theorem_prover_task", "Prover reduces clauses"),
        ("consensus_protocol_task", "Node anchors voting"),
        ("image_processing_task", "Filter maps quadtree")
    ]
    strategies = ["Syntactic Literal", "Functional Role", "Environmental Impact"]

    print("=" * 85)
    print("🚀 EXPANDING LEARNING FRAMEWORK: ASSEMBLING FIVE-DOMAIN ANALOGY SPACES")
    print("=" * 85)

    for domain_id, text in expanded_stories:
        print(f"\n📥 Ingesting Cross-Domain Text Stream: '{text}'")
        for strategy in strategies:
            abstract_facts = pipeline.compile_domain_to_prolog(text, strategy)
            write_extended_tables(strategy, domain_id, abstract_facts)
            print(f"   ✨ Strategy [{strategy:<20}] ──> Emitted: {abstract_facts}")

    print("\n" + "=" * 85)
    print("📊 VERIFYING MULTI-DOMAIN ISOMORPHISM TABLES ON DISK")
    print("=" * 85)
    p = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/generated_functional_space/bk.pl"
    if os.path.exists(p):
        print(f"📁 Content Matrix Inside 'generated_functional_space/bk.pl' (Functional Group Rules):")
        with open(p, "r") as f:
            for line in f:
                if "Extended Domain Data" in line or "abstract_object" in line:
                    print(f"   {line.strip()}")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
