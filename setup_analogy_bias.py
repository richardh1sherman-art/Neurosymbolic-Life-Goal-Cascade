import os

def deploy_analogy_bias_workspace():
    base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    target_dir = os.path.join(base_path, "analogy_discovery_space")
    os.makedirs(target_dir, exist_ok=True)

    bias_content = (
        "head_pred(analogy_discovered,2).\n"
        "body_pred(isomorphic_role_match,2).\n"
        "body_pred(uncontrolled_descent,2).\n"
        "body_pred(accident,3).\n"
    )

    bk_content = (
        "%% 🌴 Background Knowledge: Decoupled Analogy Profiles\n"
        ":- discontiguous situation/1.\n"
        ":- discontiguous uncontrolled_descent/2.\n"
        ":- discontiguous accident/3.\n"
        ":- discontiguous isomorphic_role_match/2.\n\n"
        "situation(situation_judith).\n"
        "situation(situation_george).\n"
        "situation(situation_rehearsal).\n\n"
        "%% --- PROFILE 1: RESCUE OF JUDITH (SOURCE) ---\n"
        "uncontrolled_descent(situation_judith, judith).\n"
        "accident(situation_judith, judith, mountain).\n\n"
        "%% --- PROFILE 2: GEORGE'S KITCHEN FIRE (TARGET ANALOGY) ---\n"
        "uncontrolled_descent(situation_george, george).\n"
        "accident(situation_george, george, kitchen).\n\n"
        "%% --- PROFILE 3: FIREHOUSE REHEARSAL (DISANALOGY) ---\n"
        "%% Explicitly blank parameters for functional/environmental hazards!\n\n"
        "%% 🚨 FIX: Tightly bind the roles to their specific Situation contexts!\n"
        "isomorphic_role_match(Src, Tgt) :-\n"
        "    uncontrolled_descent(Src, _),\n"
        "    uncontrolled_descent(Tgt, _),\n"
        "    accident(Src, _, _),\n"
        "    accident(Tgt, _, _).\n\n"
        "%% The General Analogy Template mapping bound conditions\n"
        "analogy_discovered(Src, Tgt) :-\n"
        "    Src \\== Tgt,\n"
        "    isomorphic_role_match(Src, Tgt), !.\n"
    )

    exs_content = (
        "pos(analogy_discovered(situation_judith, situation_george)).\n"
        "neg(analogy_discovered(situation_judith, situation_rehearsal)).\n"
    )

    with open(os.path.join(target_dir, "bias.pl"), "w", encoding="utf-8") as f: f.write(bias_content)
    with open(os.path.join(target_dir, "bk.pl"), "w", encoding="utf-8") as f: f.write(bk_content)
    with open(os.path.join(target_dir, "exs.pl"), "w", encoding="utf-8") as f: f.write(exs_content)

    print("=" * 85)
    print("✅ WORKSPACE RE-BUILT: SITUATION CONTEXT BOUNDARIES ALIGNED!")
    print("=" * 85)

if __name__ == "__main__":
    deploy_analogy_bias_workspace()
