%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Core: Besnard-Hunter Deductive Argumentation Logic
%% References: Philippe Besnard & Anthony Hunter (Deductive Arguments)
%% =================================================================

:- dynamic argument_tuple/4.
:- dynamic undercutter/3.
:- dynamic defeasible_claim/2.

%% --- 🛡️ BESNARD-HUNTER CORE ARGUMENT STRUCTURES ---
% Syntax: argument_tuple(ArgumentID, SupportSet, Claim, OriginAgent)
argument_tuple(arg_src_01, [telemetry_drift, load_surge_unmapped], allow_data_bypass, agent_1_specialist).
argument_tuple(arg_tgt_01, [system_invariant_leak_false, expected_leak_penalty], deny_data_bypass, agent_2_worker).

%% --- ⚔️ TOPOLOGICAL DEFATER & ATTACK PATHS ---
% Syntax: undercutter(AttackingArgumentID, TargetArgumentID, TargetSupportPremise)
undercutter(arg_tgt_01, arg_src_01, telemetry_drift).

%% --- 📜 DEFEASIBLE ACTION HYPOTHESES ---
% Syntax: defeasible_claim(ClaimID, ActionCommand)
defeasible_claim(allow_data_bypass, activate_delayed_recovery_routing).
defeasible_claim(deny_data_bypass, activate_mission_abort_safety_halt).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(argument_tuple, interlocking_forest, level30_subsystem_dispatcher).
part_of(undercutter, interlocking_forest, level12_science_invariants).
part_of(defeasible_claim, interlocking_forest, level30_subsystem_dispatcher).
