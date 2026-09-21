%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting Infomorphisms and Multi-Tiered Systems
%% =================================================================

:- discontiguous tree_syntax_pos/3.
:- discontiguous tree_phrase_structure/3.
:- discontiguous map_situation_unit/3.

%% --- TREE #1: SYNTAX PROCESSING ---
tree_syntax_pos(judith, noun, '+').
tree_syntax_pos(miranda, noun, '+').
tree_syntax_pos(andrea, noun, '+').
tree_syntax_pos(charles, noun, '+').
tree_syntax_pos(neil, noun, '+').
tree_syntax_pos(tom, noun, '+').

%% --- TREE #3: SITUATIONAL SCHEMAS & INFOMORPHISMS (□ LAWS) ---
% Judith Macro-System & Refinements
map_situation_unit('switch is on', switch_on, '+').
map_situation_unit('bulb is lit', bulb_lit, '+').
map_situation_unit('signal sos in morse code', flash_sos, '+').
map_situation_unit('helicopter guided specifically to coordinates', guided_rescue, '+').

% New TimeTravel Story Batches
map_situation_unit('asked her friend to draw one', draw_counterfactual, '+').
map_situation_unit('ran out of minutes', resource_depletion, '+').
map_situation_unit('ugliest city he had ever seen', negative_aesthetic, '+').
map_situation_unit('cancelled all outgoing flights due to a storm', severe_weather_block, '+').

% Existing Legacy Ontologies
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
map_situation_unit('missed the amtrak', edge_deletion, '+').
map_situation_unit('reverse his plans and call a cab', node_contraction, '+').
map_situation_unit('committed murder in egypt', decalogue_violation, '+').
map_situation_unit('losing his illegal son', decalogue_violation, '+').
map_situation_unit('going back to being king', path_healing, '+').
map_situation_unit('writing the bible', scripture_authorship, '+').

%% --- CROSS-TREE PARTHOOD LOOKUP ENGINE ---
part_of(Word, syntax_tree, POSTag) :- tree_syntax_pos(Word, POSTag, '+').
part_of(TextSegment, situation_tree, UnitConcept) :- map_situation_unit(TextSegment, UnitConcept, '+').
