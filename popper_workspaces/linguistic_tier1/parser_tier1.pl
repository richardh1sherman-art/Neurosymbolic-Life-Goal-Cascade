%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Tree #12 Multi-Agent Swarm Safety
%% =================================================================

:- dynamic swarm_safety_profile/5.

%% --- 🪐 TREE #12: SWARM SAFETY INVARIANT ARCHIVE ---
%% Syntax: swarm_safety_profile(CaseID, FilteringType, RepulsionState, MinSeparation, ControlStatus)
swarm_safety_profile(dense_crossing_trial_1, haar_wavelet, weak_apf, close, chattering_boundary_breach).
swarm_safety_profile(dense_crossing_trial_2, haar_wavelet, amplified_apf, safe, safety_invariant_preserved).

%% --- MASTER INTER-TREE LOOKUP CONNECTIONS ---
part_of(CaseID, safety_metric, status(Status)) :-
    swarm_safety_profile(CaseID, _, _, _, Status).
