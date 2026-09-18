%% =================================================================
%% 🌀 TIER 1 DEFINITE CLAUSE GRAMMAR (DCG) INTENSIONAL PARSER
%% Maps Literal Text Variations into Structured Conceptual Concepts
%% =================================================================

%% --- MASTER PARSING ENTRY HOOK ---
parse_sentence(SentenceString, Type, ConceptName, Sign) :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    phrase(sentence(Type, ConceptName, Sign), WordsList), !.

%% Fallback match if sentence structure is complex but contains explicit keyword vectors
parse_sentence(SentenceString, phrase, ConceptName, '-') :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    member(Word, WordsList),
    negative_keyword(Word, ConceptName), !.
parse_sentence(SentenceString, phrase, ConceptName, '+') :-
    atomic_list_concat(WordsList, ' ', SentenceString),
    member(Word, WordsList),
    positive_keyword(Word, ConceptName), !.

%% --- CORE DCG SYNTAX SCHEMAS ---
%% Story I (Alec Block Matrix Mappings)
sentence(premise, blocks_help_daughter, '+') --> [alecs, daughter, wanted, more, blocks].
sentence(initial, blocks_help_daughter, '+') --> [alec, figured, blocks, develop, her, mind].
sentence(ending,  blocks_help_daughter, '+') --> [alec, was, happy, verbal, ability].
sentence(counterfactual, blocks_help_daughter, '-') --> [alec, couldnt, afford, new, blocks].

%% Pierre Costume Matrix Mappings
sentence(premise, fun, '+') --> [pierre, loved, halloween].
sentence(ending,  fun, '+') --> [pierre, couldnt, wait, trick, or, treating].
sentence(initial, costume, '+') --> [he, decided, to, be, a, vampire].
sentence(counterfactual, costume, '-') --> [he, decided, to, be, a, werewolf].

%% --- KEYWORD CONCEPT MAPS (For Robust Sub-Phrase Matching) ---
positive_keyword(mind, good_for_daughter).
positive_keyword(verbal, good_for_daughter).
positive_keyword(loved, fun).
positive_keyword(treating, fun).

negative_keyword(couldnt, good_for_daughter).
negative_keyword(afford, good_for_daughter).
negative_keyword(uncomfortable, costume).
