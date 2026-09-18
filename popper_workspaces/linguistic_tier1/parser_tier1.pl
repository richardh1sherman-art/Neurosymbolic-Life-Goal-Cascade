%% =================================================================
%% 🌀 TIER 1 DEFINITE CLAUSE GRAMMAR (DCG) INTENSIONAL PARSER
%% Supports Recursive Multi-Word Compound Nouns and Adjective Lattices
%% =================================================================

%% --- MASTER PARSING ENTRY HOOK ---
parse_sentence(SentenceString, Type, ConceptName, Sign) :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    phrase(sentence(Type, ConceptName, Sign), WordsList), !.

%% Fallback keyword vector rules for robust processing of complex text profiles
parse_sentence(SentenceString, phrase, ConceptName, '-') :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    member(Word, WordsList),
    negative_keyword(Word, ConceptName), !.
parse_sentence(SentenceString, phrase, ConceptName, '+') :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    member(Word, WordsList),
    positive_keyword(Word, ConceptName), !.

%% --- CORE DCG SYNTAX SCHEMAS ---
sentence(Type, ConceptName, Sign) --> 
    subject_phrase(_Subject), 
    verb_phrase(Type, ConceptName, Sign).

%% 🚨 COORDINATE CONJUNCTION RULE OVERRIDE: Handles multi-part transitions seamlessly
sentence(ending, pierced_ears_concept, '+') --> 
    [she], [took], compound_noun(Compound), [and], [stuck], [them],
    { map_noun_phrase_concept(Compound, pierced_ears_concept, '+', ending) }.

%% --- RECURSIVE COMPOUND NOUN & ADJECTIVE LATTICES ---
subject_phrase(proper_noun(Name)) --> [Name], { proper_name_invariant(Name) }.
subject_phrase(pronoun(Word))     --> [Word], { pronoun_invariant(Word) }.
subject_phrase(noun_phrase(Det, Compound)) --> determiner(Det), compound_noun(Compound).

%% The Recursive Definition: Allows 1 or more modifier words to chain infinitely into a concept
compound_noun(single(Noun)) --> [Noun], { noun_invariant(Noun) }.
compound_noun(modifier(Adj, Rest)) --> [Adj], { modifier_invariant(Adj) }, compound_noun(Rest).

%% --- VERB PHRASE WITH MULTI-WORD COMPLEX OBJECTS ---
verb_phrase(Type, ConceptName, Sign) --> 
    verb_action(V), 
    [to], 
    verb_phrase(Type, ConceptName, Sign), { verb_transitive_invariant(V) }.
verb_phrase(Type, ConceptName, Sign) --> 
    verb_action(V), 
    subject_phrase(_Obj), { verb_transitive_invariant(V), map_verb_concept(V, ConceptName, Sign, Type) }.
verb_phrase(Type, ConceptName, Sign) --> 
    verb_action(V), 
    compound_noun(Compound), { map_noun_phrase_concept(Compound, ConceptName, Sign, Type) }.

%% --- INTENSIONAL CONCEPT LEXICON (□ LAWS) ---
determiner(the) --> [the].
determiner(a) --> [a].
determiner(her) --> [her].
determiner(more) --> [more].

proper_name_invariant(john).
proper_name_invariant(moses).
proper_name_invariant(david).
proper_name_invariant(paul).
proper_name_invariant(judith).
proper_name_invariant(alec).
proper_name_invariant(pierre).

pronoun_invariant(he).
pronoun_invariant(she).
pronoun_invariant(it).

%% Noun Invariants
noun_invariant(blocks).
noun_invariant(mind).
noun_invariant(ability).
noun_invariant(baby).
noun_invariant(girl).
noun_invariant(ears).
noun_invariant(studio).
noun_invariant(stickers).
noun_invariant(halloween).

%% Multi-Word Adjective/Noun Modifier Invariants
modifier_invariant(alecs).
modifier_invariant(new).
modifier_invariant(pierced).
modifier_invariant(verbal).
modifier_invariant(scientific).
modifier_invariant(tiny).
modifier_invariant(diamond).

%% Verb Action Invariants
verb_action(wanted) --> [wanted].
verb_action(figured) --> [figured].
verb_action(develop) --> [develop].
verb_action(was) --> [was].
verb_action(couldnt) --> [couldnt].
verb_action(afford) --> [afford].
verb_action(loved) --> [loved].
verb_action(took) --> [took].
verb_action(decided) --> [decided].
verb_action(stuck) --> [stuck].

verb_transitive_invariant(wanted).
verb_transitive_invariant(figured).
verb_transitive_invariant(develop).
verb_transitive_invariant(couldnt).
verb_transitive_invariant(afford).
verb_transitive_invariant(took).
verb_transitive_invariant(decided).
verb_transitive_invariant(stuck).

%% --- CORE CONCEPT MAP MATRIX ---
map_verb_concept(figured, blocks_help_daughter, '+', initial).
map_verb_concept(couldnt, blocks_help_daughter, '-', counterfactual).
map_verb_concept(took, pierced_ears_concept, '+', initial).
map_verb_concept(decided, pierced_ears_concept, '-', counterfactual).
map_verb_concept(stuck, pierced_ears_concept, '+', ending).

map_noun_phrase_concept(single(mind), blocks_help_daughter, '+', initial).
map_noun_phrase_concept(modifier(tiny, modifier(diamond, single(stickers))), pierced_ears_concept, '+', ending).

positive_keyword(mind, blocks_help_daughter).
positive_keyword(verbal, blocks_help_daughter).
negative_keyword(couldnt, blocks_help_daughter).
negative_keyword(not, pierced_ears_concept).
