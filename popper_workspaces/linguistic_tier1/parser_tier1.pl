%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Manifest Revision: Horizontal Control vs Vertical MPC Plane Invariants
%% References: Zhou & Köhler (2024) | Yameen et al. (2026) AMPC Architectures
%% =================================================================

:- dynamic identified_device_pattern/4.
:- dynamic horizontal_lane_status/3.
:- dynamic vertical_mpc_bounds/4.
:- dynamic part_of/3.

%% --- 📊 HORIZONTAL REAL-TIME LANE STATE REGISTRY (Δt = 500 μs) ---
% Syntax: horizontal_lane_status(ComponentID, CurrentOutputPU, ActuationStatus)
horizontal_lane_status(control_block_31, 0.5420, nominal_gated_execution).
horizontal_lane_status(control_block_32, 1.2100, hard_rail_saturation_fault).

%% --- 📊 VERTICAL OPTIMIZATION PLANE REGISTRY (HORIZON TIMELINE) ---
% Syntax: vertical_mpc_bounds(ComponentID, ThetaNN, AlphaContraction, SolverStatus)
vertical_mpc_bounds(mpc_loop_31, 0.4856, 0.4517, adjoint_converged_safe).
vertical_mpc_bounds(mpc_loop_32, 0.9500, 0.2105, adjoint_sensitivity_rupture).

%% --- 🌲 MEREOLOGICAL CONTROL COMPONENT ASSOCIATION ---
part_of(control_block_31, mpc_loop_31, new_england_ieee39_macro_grid).
part_of(control_block_32, mpc_loop_32, new_england_ieee39_macro_grid).

%% --- ⚙️ AUTOMATED MULTI-PLANE SECURITY AUDIT AXIOMS ---

% Fact 1: Catches horizontal current limit violations before transistor melt
plane_breach_detected(ComponentID, horizontal_lane_collapse) :-
    horizontal_lane_status(ComponentID, CurrentOutput, _),
    CurrentOutput >= 1.2000. % Physical transistor safety ceiling

% Fact 2: Catches vertical optimization gradient collapses under severe phase noise
plane_breach_detected(ControlID, vertical_gradient_rupture) :-
    part_of(ControlID, MpcLoopID, _),
    vertical_mpc_bounds(MpcLoopID, _, _, adjoint_sensitivity_rupture).

% Fact 3: Cross-verifies that alpha contraction corresponds tightly to the sensed noise
plane_breach_detected(ControlID, constraint_mismatch_fault) :-
    part_of(ControlID, MpcLoopID, _),
    vertical_mpc_bounds(MpcLoopID, ThetaNN, Alpha, _),
    ExpectedAlpha is 1.0 / (1.0 + 2.5 * ThetaNN),
    Variance is abs(Alpha - ExpectedAlpha),
    Variance > 0.01. % Enforces tight algebraic tolerance

% Master System Certification Law
certify_multi_plane_safety(ControlID) :-
    part_of(ControlID, _, _),
    \+ plane_breach_detected(ControlID, _).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(horizontal_lane_status, interlocking_forest, level12_science_invariants).
part_of(vertical_mpc_bounds, interlocking_forest, level12_science_invariants).
part_of(plane_breach_detected, interlocking_forest, level30_subsystem_dispatcher).
part_of(certify_multi_plane_safety, interlocking_forest, level30_subsystem_dispatcher).
