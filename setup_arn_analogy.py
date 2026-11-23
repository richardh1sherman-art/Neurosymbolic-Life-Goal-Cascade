import os

def deploy_arn_workspace():
    base_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    target_dir = os.path.join(base_path, "arn_analogy_space")
    os.makedirs(target_dir, exist_ok=True)

    # 1. Write bias.pl containing General Structural Mapping Constraints
    bias_content = (
        "head_pred(arn_analogy,2).\n"
        "body_pred(relational_payoff_match,2).\n"
        "body_pred(has_catalyst,1).\n"
        "body_pred(positive_payoff,1).\n"
    )

    # 2. Write bk.pl mapping the Crisp Abstraction Roles
    bk_content = (
        "%% 🌴 Background Knowledge: ARN Narrative Relational Symmetries\n"
        ":- discontiguous narrative/1.\n"
        ":- discontiguous has_catalyst/1.\n"
        ":- discontiguous positive_payoff/1.\n"
        ":- discontiguous relational_payoff_match/2.\n\n"
        "narrative(sb).\n"
        "narrative(st1).\n"
        "narrative(st2).\n\n"
        "%% --- BASE NARRATIVE (SB) ---\n"
        "has_catalyst(sb).\n"
        "positive_payoff(sb).             %% Payoff: Boss rewarded effort\n\n"
        "%% --- TARGET 1: NEAR DISANALOGY (ST1) ---\n"
        "has_catalyst(st1).\n"
        "%% Notice: No positive_payoff fact exists because request was refused!\n\n"
        "%% --- TARGET 2: FAR ANALOGY (ST2) ---\n"
        "has_catalyst(st2).\n"
        "positive_payoff(st2).            %% Payoff: Met someone, second anniversary!\n\n"
        "%% General Rule: Verifies if two domains share an isomorphic payoff contract\n"
        "relational_payoff_match(X, Y) :-\n"
        "    positive_payoff(X),\n"
        "    positive_payoff(Y).\n\n"
        "%% The Analogy Template derived from bias structural parameters\n"
        "arn_analogy(Src, Tgt) :-\n"
        "    Src \\== Tgt,\n"
        "    has_catalyst(Src),\n"
        "    has_catalyst(Tgt),\n"
        "    relational_payoff_match(Src, Tgt), !.\n"
    )

    # 3. Write exs.pl specifying our target discovery checks
    exs_content = (
        "pos(arn_analogy(sb, st2)).\n"
        "neg(arn_analogy(sb, st1)).\n"
    )

    with open(os.path.join(target_dir, "bias.pl"), "w", encoding="utf-8") as f: f.write(bias_content)
    with open(os.path.join(target_dir, "bk.pl"), "w", encoding="utf-8") as f: f.write(bk_content)
    with open(os.path.join(target_dir, "exs.pl"), "w", encoding="utf-8") as f: f.write(exs_content)

    print("=" * 85)
    print("✅ ARN ANALOGY PIPELINE WORKSPACE FILE SYSTEM DEPLOYED SUCCESS!")
    print("=" * 85)
    print(f"📁 Target Folder: {target_dir}")
    print("=" * 85)

if __name__ == "__main__":
    deploy_arn_workspace()
