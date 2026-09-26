%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Abstract Algebras and Inverted Pendulum ODEs
%% =================================================================

:- discontiguous algebraic_signature/3.
:- discontiguous simulation_case_invariant/4.

%% --- 🪐 ABSTRACT ALGEBRA SIGNATURES ---
% Syntax: algebraic_signature(AlgebraID, DomainSet, OperatorList)
algebraic_signature(real_field, real_numbers, [plus, multiply]).
algebraic_signature(pendulum_dynamics, angles_velocities, [damping, spring_restore, forcing]).

%% --- 📉 INITIAL VALUE PROBLEM DATA CASES ---
% Syntax: simulation_case_invariant(CaseID, SpringStiffness, InitialStretch, ToleranceStatus)
simulation_case_invariant(case_1, soft, unstretched, liberal).
simulation_case_invariant(case_2, soft, unstretched, stringent).
simulation_case_invariant(case_3, stiff, stretched, liberal).
simulation_case_invariant(case_4, stiff, stretched, stringent).

%% --- MASTER INTER-TREE FUNCTOR MAPPINGS ---
part_of(AlgebraID, structural_analogy, functor) :-
    algebraic_signature(AlgebraID, _, _).

part_of(CaseID, numerical_manifold, stability_collapse) :-
    simulation_case_invariant(CaseID, soft, unstretched, liberal).
part_of(CaseID, numerical_manifold, stable_trajectory) :-
    simulation_case_invariant(CaseID, stiff, stretched, stringent).
