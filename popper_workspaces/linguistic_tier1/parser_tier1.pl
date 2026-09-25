%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Tree #11 Observational Learning Schemas
%% =================================================================

:- dynamic structural_lesson/3.
:- dynamic map_situation_unit/3.

%% --- 🧠 TREE #11: PROBLEM-SOLVING ARCHITECTURAL MEMORY ---
% Legacy Episodes
structural_lesson(missionaries_cannibals, algebraic_operator, self_similar_generators).
structural_lesson(missionaries_cannibals, resolution_metric, word_reduction).

% 🐒 New Episode: The Monkey-and-Bananas Extraction Problem
structural_lesson(monkey_bananas, algebraic_operator, self_similar_generators).
structural_lesson(monkey_bananas, resolution_metric, word_reduction).
structural_lesson(monkey_bananas, agent_perspective, operator).

% 🧑‍🔬 New Episode: The Experimenter-and-Bananas Setup Problem
structural_lesson(experimenter_bananas, algebraic_operator, self_similar_generators).
structural_lesson(experimenter_bananas, resolution_metric, word_reduction).
structural_lesson(experimenter_bananas, agent_perspective, environment_setter).

%% --- CROSS-TREE MEMORY LOOKUP ENGINE ---
part_of(Problem, memory_cluster, SchemaType) :-
    structural_lesson(Problem, algebraic_operator, self_similar_generators),
    structural_lesson(Problem, agent_perspective, operator),
    SchemaType = automaton_group_solver.

part_of(Problem, memory_cluster, SchemaType) :-
    structural_lesson(Problem, algebraic_operator, self_similar_generators),
    structural_lesson(Problem, agent_perspective, environment_setter),
    SchemaType = homomorphic_imitation_learning.
