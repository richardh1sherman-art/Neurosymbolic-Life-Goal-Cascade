%% =================================================================
%% 🌀 TIER 0 & TIER 1/3 INTERLOCKING FORESTS OF DECISION TREES
%% Complete System Composition Ontology Matrix - "part_of" Invariants
%% =================================================================

:- dynamic part_of_system/3.

%% --- 🛸 CORE SYSTEM PARTHOOD STRUCTURAL ANCHORS ---
% Syntax: part_of_system(SubComponent, ParentSystem, OperationalRole)
part_of_system(physical_graph_gp, large_swarm_sds, kinematic_double_integrator_plant).
part_of_system(communications_graph_gc, large_swarm_sds, line_of_sight_mesh_links).
part_of_system(computational_graph_gcomp, large_swarm_sds, resource_task_allocation_queues).

%% --- 🪐 SUBSYSTEM COMPOSITE OPERATIONAL ANCHORS ---
part_of_system(apf_collision_avoidance, physical_graph_gp, non_convex_safety_shield).
part_of_system(wavelet_transform_sensor, communications_graph_gc, multiscale_gradient_filter).
part_of_system(graph_minor_contraction, large_swarm_sds, dimensional_reduction_operator).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(SubComponent, system_hierarchy, ParentSystem) :-
    part_of_system(SubComponent, ParentSystem, _).
