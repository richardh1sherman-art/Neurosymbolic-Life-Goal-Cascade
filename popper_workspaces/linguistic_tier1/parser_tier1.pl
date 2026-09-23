%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Graph Structures and Fallacy Patterns
%% =================================================================

:- discontiguous part_of_relation/4.
:- discontiguous map_situation_unit/3.
:- discontiguous analogical_homomorphism/4.
:- discontiguous graph_property_invariant/3.
:- discontiguous text_fallacy_pattern/3.

%% =================================================================
%% 🌐 NEW DOMAIN: GRAPH PROPERTY INVARIANTS (TREES #8 & #9)
%% Syntax: graph_property_invariant(StoryOrGraphID, PropertyKey, Value)
%% =================================================================
graph_property_invariant(judith_network, topology, cycle).
graph_property_invariant(judith_network, logic_property, planar).
graph_property_invariant(judith_network, graph_border, society).

graph_property_invariant(kitchen_fire_network, topology, cycle).
graph_property_invariant(kitchen_fire_network, logic_property, planar).

graph_property_invariant(john_transit_network, topology, path).
graph_property_invariant(john_transit_network, logic_property, bounded_tree_width).

graph_property_invariant(job_loss_short, topology, none).

%% =================================================================
%% ⚠️ NEW DOMAIN: LOGICAL FALLACY ATOMIC PATTERNS (TREE #10)
%% Syntax: text_fallacy_pattern(ExemplarID, FallacyClass, TextToken)
%% =================================================================
text_fallacy_pattern(john_tree_hugger, ad_hominem, 'attacking the individual').
text_fallacy_pattern(louise_campaign, ad_hominem, 'attacking the individual').
text_fallacy_pattern(bible_circularity, circular_reasoning, 'logical loop conclusion as premise').
text_fallacy_pattern(friend_sneeze_corona, irrelevant_authority, 'status without domain expertise').

%% --- EXISTING RELATIONAL HOMOMORPHISM SCHEMAS ---
analogical_homomorphism(dead_battery, blocked_chimney, transmission_failure, '+').
analogical_homomorphism(helicopter_engine, fire_truck_pump, mitigation_vector, '+').
analogical_homomorphism(miranda_asleep, dispatcher_distracted, awareness_lapse, '+').
analogical_homomorphism(flashlight_beacon, smoke_detector_alarm, connection_vector, '+').

analogical_homomorphism(judith_lost_in_trouble, prodigal_in_trouble, fundamental_crisis, '+').
analogical_homomorphism(eats_chocolate_hunger, wants_pig_food_hunger, visceral_depletion, '+').
analogical_homomorphism(signals_sos_distress, comes_home_servant_humility, informational_beacon, '+').

%% --- CROSS-TREE PARTHOOD LOOKUP ENGINE ---
part_of(Word, syntax_tree, POSTag) :- current_predicate(tree_syntax_pos/3), call(tree_syntax_pos, Word, POSTag, '+').
part_of(TextSegment, situation_tree, UnitConcept) :- current_predicate(map_situation_unit/3), call(map_situation_unit, TextSegment, UnitConcept, '+').
part_of(Src, target_map(Dst), Role) :- analogical_homomorphism(Src, Dst, Role, '+').
part_of(GraphID, graph_metric, Prop) :- graph_property_invariant(GraphID, Prop, 'True').
part_of(Exemplar, argument_fallacy, Class) :- text_fallacy_pattern(Exemplar, Class, _).
