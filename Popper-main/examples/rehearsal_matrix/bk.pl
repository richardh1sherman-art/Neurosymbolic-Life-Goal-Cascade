:- discontiguous infon/5.
:- discontiguous part_of_selector/3.
:- discontiguous evaluate_tree/3.

%% Mapping rehearsal props and fire hydrant lines into tactical drill metrics
part_of_selector(rehearsal_prop, drill_alpha, smoke_detector_pos).
part_of_selector(water_source, drill_alpha, hydrant_pos).

evaluate_tree(outing_support, smoke_detector_pos, pos).
evaluate_tree(outing_support, hydrant_pos, pos).
