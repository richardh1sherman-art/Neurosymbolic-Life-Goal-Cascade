:- discontiguous infon/3.
:- discontiguous part_of/2.

%% Top Level Situation Infon Layouts
infon(sit_rescue_pos, person, judith). part_of(f_pos, sit_rescue_pos). part_of(h_pos, sit_rescue_pos).
infon(sit_rescue_neg, person, judith). part_of(f_neg1, sit_rescue_neg). part_of(h_pos, sit_rescue_neg).

%% Cross-Tree Decision Memory Routing Links
evaluate_tree(outing_support_flashlight, f_pos, pos). evaluate_tree(outing_support_flashlight, f_neg1, neg).
evaluate_tree(outing_support_helicopter, h_pos, pos). evaluate_tree(outing_support_helicopter, h_neg1, neg).
