%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting High-Level Algebraic Meta-Properties
%% =================================================================

:- dynamic algebraic_meta_property/3.

%% --- 🪐 SYSTEM COMPLIANCE METADATA REGISTER ---
% Syntax: algebraic_meta_property(ProblemID, PropertyType, Configuration)
algebraic_meta_property(flat_thermal_diffusion, structure, linear).
algebraic_meta_property(rotational_wave_manifold, group_type, semi_simple_continuous).
algebraic_meta_property(inverted_pendulum_singularity, local_bound, linear_approximation_at_origin).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(ProblemID, synthesis_shortcut, linear_pruning) :-
    algebraic_meta_property(ProblemID, structure, linear).

part_of(ProblemID, synthesis_shortcut, lie_algebra_basis) :-
    algebraic_meta_property(ProblemID, group_type, semi_simple_continuous).

part_of(ProblemID, synthesis_shortcut, local_jacobian_quench) :-
    algebraic_meta_property(ProblemID, local_bound, linear_approximation_at_origin).
