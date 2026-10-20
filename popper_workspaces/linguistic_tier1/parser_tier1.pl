%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Revision: Branching Poset Lattice and Fitting Semantics
%% =================================================================

:- dynamic agent_poset_edge/3.
:- dynamic fitting_consensus_rule/4.

%% --- 📊 NEW: RE-ALIGNED BRANCHING POSET EDGES ---
% Syntax: agent_poset_edge(LowerAgent, HigherAgent, LatticeType)
agent_poset_edge(agent_3_observer, agent_2_worker, branching_poset).
agent_poset_edge(agent_3_observer, agent_1_specialist, branching_poset).
agent_poset_edge(agent_2_worker, agent_0_master, branching_poset).
agent_poset_edge(agent_1_specialist, agent_0_master, branching_poset).

%% --- 📜 FITTING ANTIMONOTONIC MODAL RULES ---
% Syntax: fitting_consensus_rule(AgentID, PerceptionDepth, ValuationMode, LogicalClause)
fitting_consensus_rule(agent_w, 1, coarse_gullible, clause_d_implication).
fitting_consensus_rule(agent_t, 3, sharp_strict, clause_e_negation).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(agent_poset_edge, interlocking_forest, level12_science_invariants).
part_of(fitting_consensus_rule, interlocking_forest, level30_subsystem_dispatcher).
