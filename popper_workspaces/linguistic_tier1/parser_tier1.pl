%% =================================================================
%% 🌀 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Hardcoded Grammatical Invariants and Intensional Schema Mappings
%% =================================================================

:- discontiguous tree_syntax_pos/3.
:- discontiguous tree_phrase_structure/3.
:- discontiguous map_situation_unit/3.

%% --- TREE #1: THE SYNTAX & PARTS-OF-SPEECH (POS) TAGGING CORE ---
tree_syntax_pos(judith, noun, '+').
tree_syntax_pos(falls, verb, '+').
tree_syntax_pos(mountain, adv, '+').
tree_syntax_pos(alec, noun, '+').
tree_syntax_pos(pierre, noun, '+').
tree_syntax_pos(she, noun, '+').
tree_syntax_pos(he, noun, '+').
tree_syntax_pos(john, noun, '+').
tree_syntax_pos(moses, noun, '+').
tree_syntax_pos(david, noun, '+').

%% --- TREE #2: GRAMMATICAL ROLE & PHRASE STRUCTURE EXTRACTOR ---
tree_phrase_structure([judith, falls], sentence(subject(judith), action(falls)), '+').

%% --- TREE #3: SITUATIONAL SCHEMAS & INTENSIONAL UNITS ---
% Story ST1: A man and his job
map_situation_unit('without a raise', stagnate, '+').
map_situation_unit('kept working hard', diligent, '+').
map_situation_unit('request for a raise is refused', rejection, '+').
map_situation_unit('decided to withdraw his effort', withdraw, '+').

% Story SB: Johnny overwhelmed
map_situation_unit('was overwhelmed at work', difficulty, '+').
map_situation_unit('tried hard and finished everything', effort, '+').
map_situation_unit('boss rewarded him', reward, '+').

% Story ST2: Breakup and party
map_situation_unit('painful breakup', grief, '+').
map_situation_unit('attend a party', engagement, '+').
map_situation_unit('anniversary', success, '+').

% 🚨 NEW DOMAIN: John's Planned Routing & Reversal Matrix
map_situation_unit('planned using several travel events', planned_trajectory, '+').
map_situation_unit('missed the amtrak', edge_deletion, '+').
map_situation_unit('reverse his plans and call a cab', node_contraction, '+').

% 🚨 NEW DOMAIN: Historical Sovereign Lifecycles
map_situation_unit('committed murder in egypt', decalogue_violation, '+').
map_situation_unit('losing his illegal son', decalogue_violation, '+').
map_situation_unit('going back to being king', path_healing, '+').
map_situation_unit('writing the bible', scripture_authorship, '+').

%% --- TIER 3 CROSS-TREE PARTHOOD LOOKUP ENGINE ( s <| s' ) ---
part_of(Word, syntax_tree, POSTag) :- 
    tree_syntax_pos(Word, POSTag, '+').

part_of(PhraseList, phrase_tree, Role) :- 
    tree_phrase_structure(PhraseList, Role, '+').

part_of(TextSegment, situation_tree, UnitConcept) :- 
    map_situation_unit(TextSegment, UnitConcept, '+').

parse_story_to_situation(StoryID, SentencesList, OutSituation) :-
    collect_situation_units(SentencesList, CollectedUnits),
    OutSituation = situation(id(StoryID), units(CollectedUnits)).

collect_situation_units([], []).
collect_situation_units([H|T], [Unit|Rest]) :-
    part_of(H, situation_tree, Unit), !,
    collect_situation_units(T, Rest).
collect_situation_units([_|T], Rest) :-
    collect_situation_units(T, Rest).
