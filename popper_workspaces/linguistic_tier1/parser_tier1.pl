%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Core: Unified SCADA/CIM Axioms & Active Besnard-Hunter Rules
%% References: Philippe Besnard & Anthony Hunter (Deductive Arguments)
%% =================================================================

:- dynamic argument_tuple/4.
:- dynamic undercutter/3.
:- dynamic defeasible_claim/2.
:- dynamic core_system_invariant/2.
:- dynamic kuramoto_swing_parameter/4.
:- dynamic multi_facility_load_sensing/4.
:- dynamic de_sousa_vieira_chaos_boundary/4.

%% =================================================================
%% 🧱 PART 1: AXIOAMTIC BASE FACT REGISTRY
%% =================================================================

%% --- 🛡️ IMMUTABLE CORE SYSTEM INVARIANTS ---
core_system_invariant(leak_prevention_perimeter, allow_data_bypass).
core_system_invariant(grid_frequency_envelope, load_surge_unmapped).

%% --- 📥 INCOMING PAYLOAD ARGUMENT TUPLES ⟨Phi, alpha⟩ ---
argument_tuple(arg_src_01, [telemetry_drift, load_surge_unmapped], allow_data_bypass, agent_1_specialist).
argument_tuple(arg_tgt_01, [system_invariant_leak_false, grid_frequency_envelope], deny_data_bypass, agent_2_worker).

%% --- 🌀 SECOND-ORDER SWING PHYSICS CONSTANTS ---
kuramoto_swing_parameter(substation_bus_1, 1.0, 0.5, 0.8).
kuramoto_swing_parameter(substation_bus_2, 1.0, 0.5, 0.8).

%% --- ⚡ MULTI-FACILITY LOCAL LOAD METRICS ---
multi_facility_load_sensing(facility_alpha, 50, 15.00, normal_phase_locked).
multi_facility_load_sensing(facility_beta, 50, 15.00, critical_carrier_busy).

%% --- 🛑 DE SOUSA VIEIRA SYNCHRONIZED CHAOS BOUNDS ---
de_sousa_vieira_chaos_boundary(synchronous_batch_forcing, 0.5, 0.20, period_doubling_bifurcation).


%% =================================================================
%% ⚙️ PART 2: ACTIVE DEDUCTIVE INFERENCE RULES
%% =================================================================

% Rule 1: Evaluates whether any premise inside a support set violates a core invariant
contradicts_invariant(SupportSet, InvariantName) :-
    core_system_invariant(InvariantName, ConflictingToken),
    member(ConflictingToken, SupportSet).
contradicts_invariant(SupportSet, InvariantName) :-
    core_system_invariant(InvariantName, ConflictingToken),
    argument_tuple(_, SupportSet, ConflictingToken, _).

% Rule 2: Automatically instantiates an undercutter targeting a corrupted premise
generate_undercutter(IncomingArgID, CounterArgID, TargetPremise) :-
    argument_tuple(IncomingArgID, IncomingSupport, _, _),
    argument_tuple(CounterArgID, CounterSupport, _, _),
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
    \+ undercutter(AttackerID, ArgID, TargetPremise),
    assertz(undercutter(AttackerID, ArgID, TargetPremise)).
evaluate_argument_status(ArgID, valid_standing) :-
    argument_tuple(ArgID, _, _, _),
    \+ undercutter(_, ArgID, _),
    \+ generate_undercutter(ArgID, _, _).

% Helper predicate: Standard list member verification
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(argument_tuple, interlocking_forest, level30_subsystem_dispatcher).
part_of(undercutter, interlocking_forest, level12_science_invariants).
part_of(defeasible_claim, interlocking_forest, level30_subsystem_dispatcher).
part_of(core_system_invariant, interlocking_forest, level12_science_invariants).
part_of(kuramoto_swing_parameter, interlocking_forest, level12_science_invariants).
part_of(multi_facility_load_sensing, interlocking_forest, level30_subsystem_dispatcher).
part_of(de_sousa_vieira_chaos_boundary, interlocking_forest, level12_science_invariants).
