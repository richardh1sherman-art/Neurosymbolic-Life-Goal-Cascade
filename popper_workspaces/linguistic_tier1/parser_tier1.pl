%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Overhaul Phase: Complex Area Composition & Mereological Part-Of Lookups
%% References: Zhou & Köhler (2024) | Dall'Anese et al. (2026) Multi-Scale Control
%% =================================================================

:- dynamic identified_device_pattern/4.
:- dynamic part_of/2.
:- dynamic area_composite_object/1.

%% --- 🧱 COMPLEX COMPOSITE AREA DEFINITION ---
area_composite_object(new_england_ieee39_macro_grid).

%% --- 🌲 MEREOLOGICAL PART-OF FACT REGISTRY (39 BUS ENVIRONMENT) ---
% Syntax: part_of(SubComponentID, ParentCompositeID)

% 1. Synchronous Generators (5 Units Distributed)
part_of(sg_gen_01, new_england_ieee39_macro_grid).
part_of(sg_gen_02, new_england_ieee39_macro_grid).
part_of(sg_gen_03, new_england_ieee39_macro_grid).
part_of(sg_gen_04, new_england_ieee39_macro_grid).
part_of(sg_gen_05, new_england_ieee39_macro_grid).

% 2. Grid-Forming Inverters (2 Units Distributed)
part_of(gfm_inv_01, new_england_ieee39_macro_grid).
part_of(gfm_inv_02, new_england_ieee39_macro_grid).

% 3. Grid-Following Inverters (3 Units Distributed)
part_of(gfl_inv_01, new_england_ieee39_macro_grid).
part_of(gfl_inv_02, new_england_ieee39_macro_grid).
part_of(gfl_inv_03, new_england_ieee39_macro_grid).

% 4. System Substation Bus Infrastructure (Slicing examples out of 39 total)
part_of(bus_substation_39, new_england_ieee39_macro_grid).
part_of(bus_substation_30, new_england_ieee39_macro_grid).
part_of(bus_substation_12, new_england_ieee39_macro_grid).

%% --- 📊 RECOVERED PARAMETER METRIC EXEMPLARS (PEM-MHE EXTRACTED) ---
% Syntax: identified_device_pattern(ComponentID, TypeTag, PhysicsInertia, NeuralResidual)
identified_device_pattern(sg_gen_01,  sg,  1.000, 0.0012).
identified_device_pattern(gfm_inv_01, gfm, 0.650, 0.0420).
identified_device_pattern(gfl_inv_01, gfl, 0.215, 0.4856). % Critical Phase Noise Fault Vector
identified_device_pattern(gfl_inv_02, gfl, 0.985, 0.0021).

%% --- ⚙️ RECURSIVE MEREOLOGICAL SECURITY AUDIT RULES ---

% Verifies if a macro area contains an active component in a critical fault state
area_contains_fault(AreaID, ComponentID, FaultType) :-
    area_composite_object(AreaID),
    part_of(ComponentID, AreaID),
    identified_device_pattern(ComponentID, gfl, ThetaPhys, ThetaNN),
    ThetaPhys <= 0.350, ThetaNN >= 0.200,
    FaultType = pll_control_loop_chaos.

area_contains_fault(AreaID, ComponentID, FaultType) :-
    area_composite_object(AreaID),
    part_of(ComponentID, AreaID),
    identified_device_pattern(ComponentID, gfm, ThetaPhys, _),
    ThetaPhys <= 0.500,
    FaultType = inner_current_saturation.

% Certifies system-level performance based strictly on localized boundary lookups
certify_area_stability(AreaID) :-
    area_composite_object(AreaID),
    \+ area_contains_fault(AreaID, _, _).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(identified_device_pattern, interlocking_forest, level12_science_invariants).
part_of(area_composite_object, interlocking_forest, level30_subsystem_dispatcher).
part_of(area_contains_fault, interlocking_forest, level30_subsystem_dispatcher).
part_of(certify_area_stability, interlocking_forest, level12_science_invariants).
