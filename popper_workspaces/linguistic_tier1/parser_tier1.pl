%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Core: Active Besnard-Hunter Dialectical Evaluation Loops
%% References: Besnard & Hunter, "A Logic for Deductive Arguments"
%% =================================================================

:- dynamic argument_tuple/4.
:- dynamic undercutter/3.
:- dynamic defeasible_claim/2.
:- dynamic core_system_invariant/2.

%% --- 🛡️ IMMUTABLE SYSTEM INVARIANTS ---
% Syntax: core_system_invariant(InvariantName, ConflictingToken)
core_system_invariant(leak_prevention_perimeter, allow_data_bypass).
core_system_invariant(grid_frequency_envelope, load_surge_unmapped).

%% --- 📥 INCOMING PAYLOAD ARGUMENT TUPLES ⟨Phi, alpha⟩ ---
% Syntax: argument_tuple(ArgumentID, SupportSet, Claim, OriginAgent)
argument_tuple(arg_src_01, [telemetry_drift, load_surge_unmapped], allow_data_bypass, agent_1_specialist).
argument_tuple(arg_tgt_01, [system_invariant_leak_false], deny_data_bypass, agent_2_worker).

%% --- ⚙️ ACTIVE BESNARD-HUNTER DEDUCTIVE INFERENCE RULES ---

% Rule 1: Detects structural boundary breaches against core invariants
contradicts_invariant(SupportSet, InvariantName) :-
    core_system_invariant(InvariantName, ConflictingToken),
    member(ConflictingToken, SupportSet).
contradicts_invariant(SupportSet, InvariantName) :-
    core_system_invariant(InvariantName, ConflictingToken),
    argument_tuple(_, SupportSet, ConflictingToken, _).

% Rule 2: Automatically instantiates an undercutter targeting the corrupted premise
generate_undercutter(IncomingArgID, CounterArgID, TargetPremise) :-
    argument_tuple(IncomingArgID, IncomingSupport, _, _),
    argument_tuple(CounterArgID, CounterSupport, _, TargetAgent),
    CounterArgID \== IncomingArgID,
    member(TargetPremise, IncomingSupport),
    core_system_invariant(InvariantName, TargetPremise),
    member(InvariantName, CounterSupport).

% Rule 3: Dialectical status evaluation (Determines if a claim is active or DEFEATED)
evaluate_argument_status(ArgID, defeated_by(AttackerID)) :-
    undercutter(AttackerID, ArgID, _).
evaluate_argument_status(ArgID, defeated_by(AttackerID)) :-
    argument_tuple(ArgID, Support, _, _),
    generate_undercutter(ArgID, AttackerID, TargetPremise),
    % Dynamically assert the undercutter fact into the dynamic registry
    assertz(undercutter(AttackerID, ArgID, TargetPremise)).
evaluate_argument_status(ArgID, valid_standing) :-
    argument_tuple(ArgID, _, _, _),
    \+ undercutter(_, ArgID, _),
    \+ generate_undercutter(ArgID, _, _).

% Helper predicate: Standard list member check
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(argument_tuple, interlocking_forest, level30_subsystem_dispatcher).
part_of(undercutter, interlocking_forest, level12_science_invariants).
part_of(defeasible_claim, interlocking_forest, level30_subsystem_dispatcher).
part_of(core_system_invariant, interlocking_forest, level12_science_invariants).
