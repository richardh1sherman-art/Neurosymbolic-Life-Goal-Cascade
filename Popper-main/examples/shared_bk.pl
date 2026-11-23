:- discontiguous infon/5.
:- discontiguous part_of_selector/3.
:- discontiguous evaluate_tree/3.

%% Level 1 Primitive Objects (Used by level 2 and level 3 encodings)
infon(judith_pos, trouble, state, fall, 1).
infon(george_pos, trouble, state, near_fire, 1).
infon(flashlight_pos, signal, mode, sos, 1). infon(flashlight_pos, hardware, state, live, 1).
infon(smoke_detector_pos, signal, mode, wifi, 1). infon(smoke_detector_pos, hardware, state, live, 1).
infon(helicopter_perm, contract, authorization, cleared, 1).
infon(hook_and_ladder_perm, contract, authorization, cleared, 1).

%% Level 1 Counter-Exemplar Hardware Failures
infon(flashlight_dead, hardware, state, live, 0).
infon(smoke_detector_dead, hardware, state, live, 0).

%% Level 2 & 3 Structural Context Containment Links
part_of_selector(pos_2nd, judith_hiking_rescue, flashlight_pos).
part_of_selector(pos_3rd, judith_hiking_rescue, helicopter_pos).
part_of_selector(source_person, alignment_exemplar, judith_pos).
part_of_selector(target_person, alignment_exemplar, george_pos).
part_of_selector(source_device, alignment_exemplar, flashlight_pos).
part_of_selector(target_device, alignment_exemplar, smoke_detector_pos).
part_of_selector(source_dispatch, alignment_exemplar, helicopter_perm).
part_of_selector(target_dispatch, alignment_exemplar, hook_and_ladder_perm).

part_of_selector(source_device, broken_alignment_exemplar, flashlight_dead).
part_of_selector(target_device, broken_alignment_exemplar, smoke_detector_dead).

%% Intensional Concept Provers evaluating contained_in queries down to level 1
evaluate_tree(outing_support, Node, pos) :-
    (infon(Node, hardware, state, live, 1) ; infon(Node, contract, authorization, cleared, 1)), !.
evaluate_tree(outing_support, Node, neg) :-
    infon(Node, hardware, state, live, 0).
