%% =================================================================
%% 🌀 TIER 0 & TIER 1/3 INTERLOCKING FORESTS OF DECISION TREES
%% Complete System Composition Ontology Matrix - "part_of" Invariants
%% =================================================================

:- dynamic part_of_system/3.
:- dynamic tree_30_dispatch/3.

%% --- 🛸 CORE SYSTEM PARTHOOD STRUCTURAL ANCHORS ---
part_of_system(physical_graph_gp, large_swarm_sds, kinematic_double_integrator_plant).
part_of_system(communications_graph_gc, large_swarm_sds, line_of_sight_mesh_links).
part_of_system(computational_graph_gcomp, large_swarm_sds, resource_task_allocation_queues).

%% --- 🪐 SUBSYSTEM COMPOSITE OPERATIONAL ANCHORS ---
part_of_system(apf_collision_avoidance, physical_graph_gp, non_convex_safety_shield).
part_of_system(wavelet_transform_sensor, communications_graph_gc, multiscale_gradient_filter).
part_of_system(graph_minor_contraction, large_swarm_sds, dimensional_reduction_operator).

%% --- 🌲 TREE #30: PARTHOOD SUBSYSTEM DISPATCH SIGNATURES ---
% Syntax: tree_30_dispatch(TaskToken, PropertyCheck, TargetSubTree)
tree_30_dispatch(collision_check, kinematic, route_to_physical_sub_p).
tree_30_dispatch(signal_mesh, connection, route_to_communications_sub_c).
tree_30_dispatch(load_balancing, task_saturation, route_to_computational_sub_comp).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(SubComponent, system_hierarchy, ParentSystem) :-
    part_of_system(SubComponent, ParentSystem, _), !.

part_of(TaskToken, tree_30_routing, Target) :-
    tree_30_dispatch(TaskToken, _, Target), !.
