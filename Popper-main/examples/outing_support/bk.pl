:- discontiguous infon/5.
:- discontiguous part_of_selector/3.
:- discontiguous evaluate_tree/3.

infon(flashlight_pos, hardware, state, live, 1).
infon(flashlight_dead, hardware, state, live, 0).
infon(smoke_detector_pos, hardware, state, live, 1).
infon(smoke_detector_dead, hardware, state, live, 0).
infon(helicopter_pos, hardware, state, live, 1).
infon(helicopter_neg1, hardware, state, live, 0).
infon(helicopter_perm, contract, authorization, cleared, 1).
infon(hook_and_ladder_perm, contract, authorization, cleared, 1).
%% Fire Hydrant Primitive Fact States
infon(hydrant_pos, water, pressure, active, 1).
infon(hydrant_low_pressure, water, pressure, active, 0).
