%% =================================================================
%% 🌀 TIER 1 DEFINITE CLAUSE GRAMMAR (DCG) INTENSIONAL PARSER
%% Recursively Structures Natural Language Inputs into Logical Constants
%% =================================================================

%% --- MASTER PARSING ENTRY HOOK ---
parse_sentence(SentenceString, StructuredTerm) :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    phrase(sentence(StructuredTerm), WordsList).

%% --- CORE DCG SYNTAX SCHEMAS ---
sentence(sentence(NP, VP)) --> 
    noun_phrase(NP, Number), 
    verb_phrase(VP, Number).

%% Inverted Proper Override: Handles sequences like [john, train, cancelled]
sentence(sentence(proper_noun(Name), object(Noun), verb_transitive(V))) -->
    [Name], { proper_name_invariant(Name) },
    [Noun], { noun_invariant(Noun) },
    [V], { verb_transitive_invariant(V) }.

%% 🚨 PASSIVE DETERMINER OVERRIDE: Handles dense sequences like [the, link, severed]
sentence(sentence(determiner(Det), object(Noun), verb_transitive(V))) -->
    determiner(Det, singular),
    [Noun], { noun_invariant(Noun) },
    [V], { verb_transitive_invariant(V) }.

noun_phrase(proper_noun(Name), singular) --> [Name], { proper_name_invariant(Name) }.
noun_phrase(pronoun(Word), singular)     --> [Word], { pronoun_invariant(Word) }.
noun_phrase(noun_phrase(Det, Noun), Num)  --> determiner(Det, Num), noun(Noun, Num).

verb_phrase(verb(Word), Num)           --> verb_intransitive(Word, Num).
verb_phrase(verb_transitive(V, NP), Num) --> verb_transitive(V, Num), noun_phrase(NP, _).

%% --- INTENSIONAL CONCEPT LEXICON (□ LAWS) ---
determiner(the, singular) --> [the].
determiner(a, singular) --> [a].

proper_name_invariant(john).
proper_name_invariant(moses).
proper_name_invariant(david).
proper_name_invariant(paul).
proper_name_invariant(judith).

pronoun_invariant(he).
pronoun_invariant(she).
pronoun_invariant(it).

noun(train, singular)        --> [train].
noun(flight, singular)       --> [flight].
noun(link, singular)         --> [link].
noun(friend, singular)       --> [friend].
noun(intersection, singular) --> [intersection].

noun_invariant(train).
noun_invariant(flight).
noun_invariant(link).
noun_invariant(friend).
noun_invariant(intersection).

verb_intransitive(falls, singular)   --> [falls].
verb_intransitive(glides, singular)  --> [glides].
verb_intransitive(crashed, singular) --> [crashed].

verb_transitive(cancelled, singular) --> [cancelled].
verb_transitive(severed, singular)   --> [severed].
verb_transitive(blocked, singular)   --> [blocked].
verb_transitive(persecuted, singular)--> [persecuted].

verb_transitive_invariant(cancelled).
verb_transitive_invariant(severed).
verb_transitive_invariant(blocked).
verb_transitive_invariant(persecuted).
