:- discontiguous infon/5.
:- discontiguous part_of_selector/3.
:- discontiguous evaluate_tree/3.

part_of_selector(source_device, alignment_exemplar, flashlight_pos).
part_of_selector(target_device, alignment_exemplar, smoke_detector_pos).
part_of_selector(source_dispatch, alignment_exemplar, helicopter_perm).
part_of_selector(target_dispatch, alignment_exemplar, hook_and_ladder_perm).

part_of_selector(source_device, broken_alignment_exemplar, flashlight_dead).
part_of_selector(target_device, broken_alignment_exemplar, smoke_detector_dead).

infon(flashlight_pos, hardware, state, live, 1).
infon(smoke_detector_pos, hardware, state, live, 1).
infon(helicopter_perm, contract, authorization, cleared, 1).
infon(hook_and_ladder_perm, contract, authorization, cleared, 1).
infon(flashlight_dead, hardware, state, live, 0).
infon(smoke_detector_dead, hardware, state, live, 0).
evaluate_tree(outing_support, flashlight_pos, pos).
evaluate_tree(outing_support, smoke_detector_pos, pos).
evaluate_tree(outing_support, helicopter_perm, pos).
evaluate_tree(outing_support, hook_and_ladder_perm, pos).
evaluate_tree(outing_support, flashlight_dead, neg).
evaluate_tree(outing_support, smoke_detector_dead, neg).
