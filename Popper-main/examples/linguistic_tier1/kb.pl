%% ===============================================================
%% 🌀 TIER 1 BACKGROUND KNOWLEDGE: LEXICAL PRIMITIVES (□ LAWS)
%% ===============================================================
:- discontiguous token_property/2.

is_capitalized(Token, true) :- token_property(Token, capitalized).
tracks_suffix(Token, Suffix) :- token_property(Token, has_suffix(Suffix)).
