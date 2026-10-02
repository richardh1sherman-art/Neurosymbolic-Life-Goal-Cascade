%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Isolated Sub-Tree Primitives Supporting Single Network Controls
%% =================================================================

:- dynamic sub_tree_routing/3.

%% --- 🪐 SEPARATE TREE REGISTRIES FOR SINGLE NETWORK CONTROLS ---
% Syntax: sub_tree_routing(NetworkID, SpecializedTree, InvariantPruningRule)
sub_tree_routing(physical_layer, tree_12_sub_p, enforce_collision_boundaries).
sub_tree_routing(communication_layer, tree_12_sub_c, enforce_line_of_sight_30mi).
sub_tree_routing(computational_layer, tree_12_sub_comp, balance_task_saturation_loads).

%% --- MASTER INTER-TREE LOOKUP CONNECTIONS ---
part_of(NetworkID, single_control_loop, Tree) :-
    sub_tree_routing(NetworkID, Tree, _).
