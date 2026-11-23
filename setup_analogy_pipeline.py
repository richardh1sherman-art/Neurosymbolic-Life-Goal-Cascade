import os

def initialize_analogy_workspace():
    repo_root = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples"
    
    # ---------------------------------------------------------------------
    # STEP 1 & 2: SOURCE SITUATION - RESCUE OF JUDITH
    # ---------------------------------------------------------------------
    src_dir = os.path.join(repo_root, "situation_judith")
    os.makedirs(src_dir, exist_ok=True)
    
    src_bk = (
        "%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping\n"
        "person(judith).\n"
        "trouble(judith, fall).\n"
        "device(flashlight).\n"
        "signal(flashlight, sos).\n"
        "dispatcher(permission_helicopter).\n"
        "outcome(judith, rescued).\n\n"
        "%% Stage 3: Knowledge Base Hypothesis Rule Derivations\n"
        "person_in_trouble(S, P) :- person(P), trouble(P, _).\n"
        "signaling_device(S, D) :- device(D), signal(D, _).\n"
        "dispatcher_clear(S, Disp) :- dispatcher(Disp).\n"
        "final_outcome(S, P, Status) :- outcome(P, Status).\n"
    )
    src_bias = "head_pred(rescue_situation,2).\nbody_pred(person_in_trouble,2).\nbody_pred(signaling_device,2).\n"
    src_exs = "pos(rescue_situation(situation_judith, judith)).\n"
    
    with open(os.path.join(src_dir, "bk.pl"), "w") as f: f.write(src_bk)
    with open(os.path.join(src_dir, "bias.pl"), "w") as f: f.write(src_bias)
    with open(os.path.join(src_dir, "exs.pl"), "w") as f: f.write(src_exs)

    # ---------------------------------------------------------------------
    # STEP 1 & 2: TARGET SITUATION - KITCHEN FIRE (ISOMORPHIC ANALOGY)
    # ---------------------------------------------------------------------
    tgt_dir = os.path.join(repo_root, "situation_george")
    os.makedirs(tgt_dir, exist_ok=True)
    
    tgt_bk = (
        "%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping\n"
        "person(george).\n"
        "trouble(george, near_fire).\n"
        "device(smoke_detector).\n"
        "signal(smoke_detector, wifi).\n"
        "dispatcher(permission_hook_and_ladder).\n"
        "outcome(george, safe).\n\n"
        "%% Stage 3: Knowledge Base Hypothesis Rule Derivations\n"
        "person_in_trouble(S, P) :- person(P), trouble(P, _).\n"
        "signaling_device(S, D) :- device(D), signal(D, _).\n"
        "dispatcher_clear(S, Disp) :- dispatcher(Disp).\n"
        "final_outcome(S, P, Status) :- outcome(P, Status).\n"
    )
    tgt_bias = "head_pred(rescue_situation,2).\nbody_pred(person_in_trouble,2).\nbody_pred(signaling_device,2).\n"
    tgt_exs = "pos(rescue_situation(situation_george, george)).\n"
    
    with open(os.path.join(tgt_dir, "bk.pl"), "w") as f: f.write(tgt_bk)
    with open(os.path.join(tgt_dir, "bias.pl"), "w") as f: f.write(tgt_bias)
    with open(os.path.join(tgt_dir, "exs.pl"), "w") as f: f.write(tgt_exs)

    # ---------------------------------------------------------------------
    # STEP 1 & 2: DISANALOGY SITUATION - FIRE DEPARTMENT REHEARSAL
    # ---------------------------------------------------------------------
    reh_dir = os.path.join(repo_root, "situation_rehearsal")
    os.makedirs(reh_dir, exist_ok=True)
    
    reh_bk = (
        "%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping\n"
        "person(none).\n"
        "trouble(none, none).\n"
        "device(cell_phone).\n"
        "signal(cell_phone, wifi).\n"
        "dispatcher(permission_hook_and_ladder).\n"
        "outcome(none, active).\n\n"
        "%% Stage 3: Knowledge Base Hypothesis Rule Derivations\n"
        "person_in_trouble(S, P) :- person(P), P \\== none, trouble(P, T), T \\== none.\n"
        "signaling_device(S, D) :- device(D), signal(D, _).\n"
        "dispatcher_clear(S, Disp) :- dispatcher(Disp).\n"
        "final_outcome(S, P, Status) :- outcome(P, Status).\n"
    )
    reh_bias = "head_pred(rescue_situation,2).\nbody_pred(person_in_trouble,2).\nbody_pred(signaling_device,2).\n"
    reh_exs = "neg(rescue_situation(situation_rehearsal, none)).\n"
    
    with open(os.path.join(reh_dir, "bk.pl"), "w") as f: f.write(reh_bk)
    with open(os.path.join(reh_dir, "bias.pl"), "w") as f: f.write(reh_bias)
    with open(os.path.join(reh_dir, "exs.pl"), "w") as f: f.write(reh_exs)

    print("=" * 85)
    print("✅ ANALOGY PIPELINE WORKSPACE FILE SYSTEM DEPLOYED SUCCESS!")
    print("=" * 85)
    print(f"📁 Source Deployed:    {src_dir}")
    print(f"📁 Target Deployed:    {tgt_dir}")
    print(f"📁 Rehearsal Deployed: {reh_dir}")
    print("=" * 85)

if __name__ == "__main__":
    initialize_analogy_workspace()
