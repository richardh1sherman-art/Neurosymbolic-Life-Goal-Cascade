%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Complex Analogy Mapping Invariants
%% =================================================================

:- discontiguous part_of_relation/4.
:- discontiguous map_situation_unit/3.
:- discontiguous analogical_homomorphism/4.

%% --- TREE #3: SITUATIONAL SCHEMAS & INFOMORPHISMS ---
map_situation_unit('switch is on', switch_on, '+').
map_situation_unit('bulb is lit', bulb_lit, '+').
map_situation_unit('signal sos in morse code', flash_sos, '+').
map_situation_unit('helicopter guided specifically to coordinates', guided_rescue, '+').
map_situation_unit('asked her friend to draw one', draw_counterfactual, '+').
map_situation_unit('ran out of minutes', resource_depletion, '+').
map_situation_unit('ugliest city he had ever seen', negative_aesthetic, '+').
map_situation_unit('cancelled all outgoing flights due to a storm', severe_weather_block, '+').

%% --- 🪐 TREE #7: RELATIONAL ROLE HOMOMORPHISM SCHEMAS ---
% Emergency Services Analogy
analogical_homomorphism(dead_battery, blocked_chimney, transmission_failure, '+').
analogical_homomorphism(helicopter_engine, fire_truck_pump, mitigation_vector, '+').
analogical_homomorphism(miranda_asleep, dispatcher_distracted, awareness_lapse, '+').
analogical_homomorphism(flashlight_beacon, smoke_detector_alarm, connection_vector, '+').
analogical_homomorphism(hiking_alone, cooking_alone, risk_multiplier, '+').

% 🚨 NEW DOMAIN: Spiritual Analogy Matrix (Judith -> Prodigal Son)
analogical_homomorphism(judith_lost_in_trouble, prodigal_in_trouble, fundamental_crisis, '+').
analogical_homomorphism(eats_chocolate_hunger, wants_pig_food_hunger, visceral_depletion, '+').
analogical_homomorphism(helicopter_rescue_deployment, father_runs_to_help, external_deliverance, '+').
analogical_homomorphism(signals_sos_distress, comes_home_servant_humility, informational_beacon, '+').
analogical_homomorphism(miranda_calls_help, father_sees_from_distance, awareness_vector, '+').
analogical_homomorphism(climbs_mountain_ascent, receives_inheritance, initial_abundance, '+').
analogical_homomorphism(tumbles_scree_fall, spiritually_hurt, structural_descent, '+').

% Boundary Mismatches (What Didn't Happen)
analogical_homomorphism(unknown_post_rescue, celebration_party_gift, boundary_asymmetry, '-').
analogical_homomorphism(judith_alone, jealous_brother_presence, boundary_asymmetry, '-').

%% --- CROSS-TREE PARTHOOD LOOKUP ENGINE ---
part_of(Word, syntax_tree, POSTag) :- current_predicate(tree_syntax_pos/3), call(tree_syntax_pos, Word, POSTag, '+').
part_of(TextSegment, situation_tree, UnitConcept) :- map_situation_unit(TextSegment, UnitConcept, '+').
part_of(Src, target_map(Dst), Role) :- analogical_homomorphism(Src, Dst, Role, '+').
