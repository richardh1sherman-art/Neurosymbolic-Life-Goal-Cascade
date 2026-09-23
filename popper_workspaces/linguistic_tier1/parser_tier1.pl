%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Graph Structures and Fallacy Patterns
%% =================================================================

:- discontiguous part_of_relation/4.
:- discontiguous map_situation_unit/3.
:- discontiguous analogical_homomorphism/4.
:- discontiguous graph_property_invariant/3.
:- discontiguous text_fallacy_pattern/3.

%% --- TREE #1: CORE EXTENSIONAL VOCABULARY TOKENS ---
tree_syntax_pos(judith, noun, '+').
tree_syntax_pos(moses, noun, '+').
tree_syntax_pos(david, noun, '+').
tree_syntax_pos(paul, noun, '+').
tree_syntax_pos(john, noun, '+').
tree_syntax_pos(louise, noun, '+').

%% --- TREE #3: SITUATIONAL SCHEMAS & INFOMORPHISMS ---
map_situation_unit('switch is on', switch_on, '+').
map_situation_unit('bulb is lit', bulb_lit, '+').
map_situation_unit('signal sos in morse code', flash_sos, '+').
map_situation_unit('helicopter guided specifically to coordinates', guided_rescue, '+').
map_situation_unit('without a raise', stagnate, '+').
map_situation_unit('kept working hard', diligent, '+').
map_situation_unit('request for a raise is refused', rejection, '+').
map_situation_unit('decided to withdraw his effort', withdraw, '+').
map_situation_unit('was overwhelmed at work', difficulty, '+').
map_situation_unit('tried hard and finished everything', effort, '+').
map_situation_unit('boss rewarded him', reward, '+').
map_situation_unit('painful breakup', grief, '+').
map_situation_unit('attend a party', engagement, '+').
map_situation_unit('anniversary', success, '+').
map_situation_unit('planned using several travel events', planned_trajectory, '+').

%% --- 🌐 NEW DOMAIN: GRAPH PROPERTY INVARIANTS ---
graph_property_invariant(judith_network, topology, cycle).
graph_property_invariant(judith_network, logic_property, planar).
graph_property_invariant(kitchen_fire_network, topology, cycle).
graph_property_invariant(kitchen_fire_network, logic_property, planar).
graph_property_invariant(john_transit_network, topology, path).
graph_property_invariant(john_transit_network, logic_property, bounded_tree_width).
graph_property_invariant(job_loss_short, topology, none).

% 🚨 SOVEREIGN TIMELINE GRAPH EXPANSONS: Micro-details turn lines into expanding meshes
graph_property_invariant(moses_expanded_lifecycle, topology, cyclic_mesh).
graph_property_invariant(moses_expanded_lifecycle, logic_property, dynamic_growth).
graph_property_invariant(david_expanded_lifecycle, topology, cyclic_mesh).
graph_property_invariant(david_expanded_lifecycle, logic_property, dynamic_growth).
graph_property_invariant(paul_expanded_lifecycle, topology, cyclic_mesh).
graph_property_invariant(paul_expanded_lifecycle, logic_property, dynamic_growth).

%% --- ⚠️ NEW DOMAIN: LOGICAL FALLACY ATOMIC PATTERNS ---
text_fallacy_pattern(john_tree_hugger, ad_hominem, 'attacking the individual').
text_fallacy_pattern(louise_campaign, ad_hominem, 'attacking the individual').
text_fallacy_pattern(bible_circularity, circular_reasoning, 'logical loop conclusion as premise').
text_fallacy_pattern(friend_sneeze_corona, irrelevant_authority, 'status without domain expertise').

%% --- 🪐 TREE #7: RELATIONAL ROLE HOMOMORPHISM SCHEMAS ---
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
