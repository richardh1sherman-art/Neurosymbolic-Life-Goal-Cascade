%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Horizon: Hamilton-Jacobi-Isaacs (HJI) Reachability Gates
%% =================================================================

:- dynamic hji_game_state/4.
:- dynamic avoid_set_perimeter/3.

%% --- 🎮 HJI DIFFERENTIAL GAME PRIMITIVES ---
% Syntax: hji_game_state(SubstationID, HamiltonianStatus, DefenderPolicy, AttackerPolicy)
hji_game_state(substation_1, optimal_containment, load_curtailment, synchronized_surge_exploit).
hji_game_state(substation_2, tracking_safe_envelope, energy_storage_discharge, passive_probing).

%% --- 🛑 TOPOLOGICAL AVOID SETS (TARGET RISK BOUNDARIES) ---
% Syntax: avoid_set_perimeter(AvoidSetID, MetricThreshold, CriticalInfraction)
avoid_set_perimeter(transformer_thermal_melt, 0.95, catastrophic_grid_fracture).
avoid_set_perimeter(bus_frequency_collapse, 59.2, regional_cascade_blackout).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(hji_game_state, interlocking_forest, level30_subsystem_dispatcher).
part_of(avoid_set_perimeter, interlocking_forest, level12_science_invariants).
