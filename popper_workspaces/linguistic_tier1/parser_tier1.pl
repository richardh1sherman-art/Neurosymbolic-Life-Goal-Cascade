%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Grammar 4 Security Domain: DRL Game Matrices & Perplexity Gates
%% =================================================================

:- dynamic drl_reward_vector/4.
:- dynamic perplexity_threshold_gate/3.

%% --- 🛡️ DEFENDER-ATTACKER GAME REWARDS ---
% Syntax: drl_reward_vector(AgentRole, ActionType, BasePenalty, Observability)
drl_reward_vector(defender, exploit_leak, -2000.0, fully_observable).
drl_reward_vector(defender, server_impact, -1000.0, fully_observable).
drl_reward_vector(defender, service_restore, -500.0, fully_observable).
drl_reward_vector(attacker, server_impact, 1000.0, partially_observable).

%% --- 🔍 GOOGLE PERPLEXITY FILTER METRICS ---
% Syntax: perplexity_threshold_gate(FilterType, WindowSize, LogLikelihoodLimit)
perplexity_threshold_gate(beam_search_detector, 5, -3.5).
perplexity_threshold_gate(gcg_adversarial_jailbreak, 8, -4.2).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(drl_reward_vector, interlocking_forest, level30_subsystem_dispatcher).
part_of(perplexity_threshold_gate, interlocking_forest, level12_science_invariants).
