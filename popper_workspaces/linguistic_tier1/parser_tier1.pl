%% =================================================================
%% 🌀 TIER 1 DEFINITE CLAUSE GRAMMAR (DCG) INTENSIONAL PARSER
%% Universal Matrix Supporting All Active Core and Sovereign Narratives
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

%% Coordinate Conjunction Overrides
sentence(initial, pierced_ears_concept, '+') --> 
    [she], [took], [her], [baby], [to], [the], [studio], [and], [pierced], [ears].
sentence(ending, pierced_ears_concept, '+') --> 
    [she], [took], compound_noun(Compound), [and], [stuck], [them],
    { map_noun_phrase_concept(Compound, pierced_ears_concept, '+', ending) }.

%% Pierre Costume Syntactic Overrides
sentence(premise, fun, '+') --> [pierre], [loved], [halloween].
sentence(ending,  fun, '+') --> [pierre], [couldnt], [wait], [trick], [or], [treating].
sentence(initial, costume, '+') --> [he], [decided], [to], [be], [a], [vampire].
sentence(counterfactual, costume, '-') --> [he], [decided], [to], [be], [a], [werewolf].

%% Story I (Alec Blocks Matrix)
sentence(premise, blocks_help_daughter, '+') --> [alecs, daughter, wanted, more, blocks].
sentence(initial, blocks_help_daughter, '+') --> [alec, figured, blocks, develop, her, mind].
sentence(counterfactual, blocks_help_daughter, '-') --> [alec, couldnt, afford, new, blocks].

%% Story III (John's Business Journey Matrix)
sentence(premise, determine_startup_roi, '+') --> [john], [needed], [to], [determine], [startup], [roi].
sentence(initial, amtrak_train_routing, '+') --> [john], [booked], [the], [morning], [amtrak], [train].
sentence(counterfactual, amtrak_train_routing, '-') --> [track], [obstruction], [blocked], [the], [engine], [station].

%% Sovereign Level Flaw Matrices
sentence(counterfactual, sovereign_decalogue_violation, '-') --> [moses], [committed], [murder], [in], [egypt].
sentence(counterfactual, sovereign_decalogue_violation, '-') --> [david], [committed], [adultery], [with], [bathsheba].
sentence(counterfactual, sovereign_decalogue_violation, '-') --> [paul], [persecuted], [the], [early], [church].

%% --- RECURSIVE COMPOUND NOUN & ADJECTIVE LATTICES ---
subject_phrase(proper_noun(Name)) --> [Name], { proper_name_invariant(Name) }.
subject_phrase(pronoun(Word))     --> [Word], { pronoun_invariant(Word) }.
subject_phrase(noun_phrase(Det, Compound)) --> determiner(Det), compound_noun(Compound).

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
determiner(in) --> [in].
determiner(with) --> [with].

proper_name_invariant(john).
proper_name_invariant(moses).
proper_name_invariant(david).
proper_name_invariant(paul).
proper_name_invariant(judith).
proper_name_invariant(alec).
proper_name_invariant(pierre).
proper_name_invariant(bathsheba).
proper_name_invariant(egypt).

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
noun_invariant(train).
noun_invariant(roi).
noun_invariant(engine).
noun_invariant(vampire).
noun_invariant(werewolf).
noun_invariant(murder).
noun_invariant(adultery).
noun_invariant(church).

%% Multi-Word Adjective/Noun Modifier Invariants
modifier_invariant(alecs).
modifier_invariant(new).
modifier_invariant(pierced).
modifier_invariant(verbal).
modifier_invariant(scientific).
modifier_invariant(tiny).
modifier_invariant(diamond).
modifier_invariant(morning).
modifier_invariant(amtrak).
modifier_invariant(startup).
modifier_invariant(track).
modifier_invariant(obstruction).
modifier_invariant(early).

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
verb_action(needed) --> [needed].
verb_action(determine) --> [determine].
verb_action(booked) --> [booked].
verb_action(blocked) --> [blocked].
verb_action(committed) --> [committed].
verb_action(persecuted) --> [persecuted].

verb_transitive_invariant(wanted).
verb_transitive_invariant(figured).
verb_transitive_invariant(develop).
verb_transitive_invariant(couldnt).
verb_transitive_invariant(afford).
verb_transitive_invariant(took).
verb_transitive_invariant(decided).
verb_transitive_invariant(stuck).
verb_transitive_invariant(needed).
verb_transitive_invariant(determine).
verb_transitive_invariant(booked).
verb_transitive_invariant(blocked).
verb_transitive_invariant(committed).
verb_transitive_invariant(persecuted).

%% --- CORE CONCEPT MAP MATRIX ---
map_verb_concept(figured, blocks_help_daughter, '+', initial).
map_verb_concept(couldnt, blocks_help_daughter, '-', counterfactual).
map_verb_concept(took, pierced_ears_concept, '+', initial).
map_verb_concept(decided, pierced_ears_concept, '-', counterfactual).
map_verb_concept(stuck, pierced_ears_concept, '+', ending).
map_verb_concept(determine, determine_startup_roi, '+', premise).
map_verb_concept(booked, amtrak_train_routing, '+', initial).
map_verb_concept(blocked, amtrak_train_routing, '-', counterfactual).
map_verb_concept(committed, sovereign_decalogue_violation, '-', counterfactual).
map_verb_concept(persecuted, sovereign_decalogue_violation, '-', counterfactual).

map_noun_phrase_concept(single(mind), blocks_help_daughter, '+', initial).
map_noun_phrase_concept(modifier(tiny, modifier(diamond, single(stickers))), pierced_ears_concept, '+', ending).

positive_keyword(mind, blocks_help_daughter).
positive_keyword(verbal, blocks_help_daughter).
positive_keyword(roi, determine_startup_roi).
positive_keyword(amtrak, amtrak_train_routing).
positive_keyword(loved, fun).
positive_keyword(vampire, costume).
negative_keyword(couldnt, blocks_help_daughter).
negative_keyword(not, pierced_ears_concept).
negative_keyword(blocked, amtrak_train_routing).
negative_keyword(werewolf, costume).
negative_keyword(murder, sovereign_decalogue_violation).
negative_keyword(adultery, sovereign_decalogue_violation).
negative_keyword(persecution, sovereign_decalogue_violation).
