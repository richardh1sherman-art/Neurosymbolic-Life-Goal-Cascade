%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Core: Black-Hunter-Pan Moves & IEEE 39-Bus EMT Invariants
%% References: Black, Hunter & Pan (Ontologies) | PowerSimulationsDynamics.jl
%% =================================================================

:- dynamic dialogue_move_record/4.
:- dynamic emt_simulation_profile/4.
:- dynamic scada_class_subsumption/3.

%% --- 📡 BLACK-HUNTER-PAN MOVE REGISTRY ---
% Syntax: dialogue_move_record(MoveIndex, AgentID, MoveType, MovePayload)
dialogue_move_record(m1, agent_data_center_a, query, capacity_at(bus_39)).
dialogue_move_record(m2, agent_power_utility, posit, argument_tuple(arg_util_01, [emt_voltage_breach], drop_load_demand)).

%% --- 🌀 HIGH-FIDELITY EMT TEST-BED CONSTANTS ---
% Syntax: emt_simulation_profile(BusSystemID, PlatformSource, TargetMetric, Status)
emt_simulation_profile(ieee_39_bus, power_simulations_dynamics_jl, sub_millisecond_voltage_droop, transient_active).
emt_simulation_profile(ieee_39_bus, pscad_typhoon_core, high_frequency_wave_reflection, compliant_stable).

%% --- ⚡ SCADA TAXONOMY SUB-CLASSES ---
scada_class_subsumption(inverter_resource, electrical_node, level2_ontology).
scada_class_subsumption(transient_profile, scada_metric, level1_emt_ground).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(dialogue_move_record, interlocking_forest, level30_subsystem_dispatcher).
part_of(emt_simulation_profile, interlocking_forest, level12_science_invariants).
part_of(scada_class_subsumption, interlocking_forest, level12_science_invariants).
