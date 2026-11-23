:- discontiguous infon/5.
:- discontiguous part_of_selector/3.
:- discontiguous evaluate_tree/3.

part_of_selector(pos_2nd, judith_hiking_rescue, flashlight_pos).
part_of_selector(pos_3rd, judith_hiking_rescue, helicopter_pos).

infon(flashlight_pos, hardware, state, live, 1).
infon(helicopter_pos, hardware, state, live, 1).
evaluate_tree(outing_support, flashlight_pos, pos).
evaluate_tree(outing_support, helicopter_pos, pos).
