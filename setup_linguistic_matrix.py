import os

def initialize_workspace():
    repo_root = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    
    # ---------------------------------------------------------------------
    # TIER 1 FILE SYSTEM POOL DEPLOYMENT (VOCABULARY PRIMITIVES)
    # ---------------------------------------------------------------------
    tier1_dir = os.path.join(repo_root, "linguistic_tier1")
    os.makedirs(tier1_dir, exist_ok=True)
    
    t1_bias = "head_pred(evaluate_vocab,3).\nbody_pred(infon,3).\n"
    t1_bk = (
        "%% Tier 1 Background Knowledge Ground Truths\n"
        "infon(firefighter, word_type, noun).\n"
        "infon(helicopter, word_type, noun).\n"
        "infon(stove, word_type, noun).\n"
        "infon(hydrant, word_type, noun).\n\n"
        "infon(rescues, word_type, verb).\n"
        "infon(deploys, word_type, verb).\n"
        "infon(extinguishes, word_type, verb).\n"
        "infon(charges, word_type, verb).\n\n"
        "infon(brave, word_type, adjective).\n"
        "infon(trapped, word_type, adjective).\n"
        "infon(hot, word_type, adjective).\n"
        "infon(live, word_type, adjective).\n"
    )
    t1_exs = (
        "pos(evaluate_vocab(linguistic_tier1, firefighter, noun)).\n"
        "pos(evaluate_vocab(linguistic_tier1, rescues, verb)).\n"
        "pos(evaluate_vocab(linguistic_tier1, brave, adjective)).\n"
        "neg(evaluate_vocab(linguistic_tier1, firefighter, verb)).\n"
    )
    
    with open(os.path.join(tier1_dir, "bias.pl"), "w") as f: f.write(t1_bias)
    with open(os.path.join(tier1_dir, "bk.pl"), "w") as f: f.write(t1_bk)
    with open(os.path.join(tier1_dir, "exs.pl"), "w") as f: f.write(t1_exs)

    # ---------------------------------------------------------------------
    # TIER 2 FILE SYSTEM POOL DEPLOYMENT (SENTENCE HYPOTHESIS RULES)
    # ---------------------------------------------------------------------
    tier2_dir = os.path.join(repo_root, "linguistic_tier2")
    os.makedirs(tier2_dir, exist_ok=True)
    
    t2_bias = "head_pred(sentence_valid,1).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_vocab,3).\n"
    t2_bk = (
        "%% Tier 2 Background Knowledge - Mapping Structural Sequence Tokens\n"
        "part_of_selector(pos_1st, sentence_alpha, brave).\n"
        "part_of_selector(pos_2nd, sentence_alpha, firefighter).\n"
        "part_of_selector(pos_3rd, sentence_alpha, rescues).\n\n"
        "part_of_selector(pos_1st, sentence_beta, trapped).\n"
        "part_of_selector(pos_2nd, sentence_beta, helicopter).\n"
        "part_of_selector(pos_3rd, sentence_beta, deploys).\n\n"
        "%% Local Inheritance Subroutine Stubs\n"
        "evaluate_vocab(linguistic_tier1, brave, adjective).\n"
        "evaluate_vocab(linguistic_tier1, firefighter, noun).\n"
        "evaluate_vocab(linguistic_tier1, rescues, verb).\n"
        "evaluate_vocab(linguistic_tier1, trapped, adjective).\n"
        "evaluate_vocab(linguistic_tier1, helicopter, noun).\n"
        "evaluate_vocab(linguistic_tier1, deploys, verb).\n"
    )
    t2_exs = (
        "pos(sentence_valid(sentence_alpha)).\n"
        "pos(sentence_valid(sentence_beta)).\n"
    )
    
    with open(os.path.join(tier2_dir, "bias.pl"), "w") as f: f.write(t2_bias)
    with open(os.path.join(tier2_dir, "bk.pl"), "w") as f: f.write(t2_bk)
    with open(os.path.join(tier2_dir, "exs.pl"), "w") as f: f.write(t2_exs)
    
    print("=" * 85)
    print("✅ FILE SYSTEM WORKSPACE SYNCHRONIZED SUCCESSFULLY!")
    print("=" * 85)
    print(f"📁 Tier 1 Deployed to: {tier1_dir}")
    print(f"📁 Tier 2 Deployed to: {tier2_dir}")
    print("=" * 85)

if __name__ == "__main__":
    initialize_workspace()
