%% =================================================================
%% 🌀 TIER 0 & TIER 1/3 INTERLOCKING FORESTS OF DECISION TREES
%% Complete System Composition Ontology Matrix - "part_of" Invariants
%% =================================================================

:- dynamic part_of_system/3.
:- dynamic tree_30_dispatch/3.
:- dynamic global_problem_domain/2.

%% --- 🪐 TREE #0: APEX PROBLEM DOMAIN MAPS ---
global_problem_domain(monkey_bananas, route_to_tree_11_linguistic).
global_problem_domain(parity_proofs, route_to_tree_11_algebra).
global_problem_domain(algebra_stories, route_to_tree_11_linguistic).
global_problem_domain(inverted_pendulum, route_to_tree_12_ode).
global_problem_domain(fractional_pde, route_to_tree_12_pde).
global_problem_domain(pde_blowup, route_to_tree_12_pde).
global_problem_domain(wavelet_swarm, route_to_tree_12_swarm).
global_problem_domain(dynamic_sds_swarm, route_to_tree_12_swarm).

%% --- 🛸 CORE SYSTEM PARTHOOD STRUCTURAL ANCHORS ---
part_of_system(physical_graph_gp, large_swarm_sds, kinematic_double_integrator_plant).
part_of_system(communications_graph_gc, large_swarm_sds, line_of_sight_mesh_links).
part_of_system(computational_graph_gcomp, large_swarm_sds, resource_task_allocation_queues).

%% --- 🪐 SUBSYSTEM COMPOSITE OPERATIONAL ANCHORS ---
part_of_system(apf_collision_avoidance, physical_graph_gp, non_convex_safety_shield).
part_of_system(wavelet_transform_sensor, communications_graph_gc, multiscale_gradient_filter).
part_of_system(graph_minor_contraction, large_swarm_sds, dimensional_reduction_operator).

%% --- 🌲 TREE #30: PARTHOOD SUBSYSTEM DISPATCH SIGNATURES ---
tree_30_dispatch(collision_check, kinematic, route_to_physical_sub_p).
tree_30_dispatch(signal_mesh, connection, route_to_communications_sub_c).
tree_30_dispatch(load_balancing, task_saturation, route_to_computational_sub_comp).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(Problem, apex_routing, Target) :-
    global_problem_domain(Problem, Target), !.

part_of(SubComponent, system_hierarchy, ParentSystem) :-
    part_of_system(SubComponent, ParentSystem, _), !.

part_of(TaskToken, tree_30_routing, Target) :-
    tree_30_dispatch(TaskToken, _, Target), !.
