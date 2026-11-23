if __name__ == "__main__":
    inductor = RasiowaILPInductor(grid_size=4)
    
    # 📝 task file inputs using standard Popper ILP configuration formatting
    popper_examples = """
    pos(target(0, 0)).
    pos(target(1, 0)).
    pos(target(1, 1)).
    pos(target(3, 3)).  %% Noise outlier element!
    neg(target(2, 2)).
    neg(target(3, 3)).  %% Explicitly marked negative contradiction constraint
    """
    
    popper_bias = """
    head_pred(target, 2).
    body_pred(active_region, 2).
    """
    
    # Background Knowledge (BK) dictionary maps
    background_knowledge = {
        "active_region": [[0, 0], [1, 0], [1, 1], [3, 3]]
    }
    
    # Trigger the Empirical Neuro-Symbolic Induction Loop
    model_status, synthesized_prolog = inductor.induce_rules(
        examples_str=popper_examples, 
        bias_str=popper_bias, 
        bk_dict=background_knowledge
    )
    
    print("\n" + "="*70)
    print(f"🔮 INDUCTION PIPELINE STATUS : {model_status}")
    print("="*70)
    print("📝 SYNTHESIZED PROLOG PROGRAM SUBSET OUTPUT:")
    print("-"*70)
    print(synthesized_prolog)
    print("="*70 + "\n")
