:- discontiguous infon/3.

%% Top Level Situation
infon(sit_rescue_01, status, working).
infon(sit_rescue_01, person, judith).

%% Sub-Situation Parts
part_of(sit_flashlight_01, sit_rescue_01).
part_of(sit_helicopter_01, sit_rescue_01).

%% Initialized Subpart States
infon(sit_flashlight_01, status, working).
infon(sit_helicopter_01, status, working).
