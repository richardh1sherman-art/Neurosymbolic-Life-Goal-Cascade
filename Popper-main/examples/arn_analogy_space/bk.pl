%% ===============================================================
%% 🌀 AUGMENTED L2 DEFINITE CLAUSE GRAMMAR (□ HOALES LAW BASE)
%% Parameter Matrix: c = Case, pn = Person/Number, head = Head Word
%% ===============================================================
s(Head, S_In, S_Out) :-
    np(sbj, PN, _H, S_In, S_Temp),
    vp(PN, Head, S_Temp, S_Out).

np(sbj, 3s, judith, [judith|Tail], Tail).
np(obj, 3s, judith, [judith|Tail], Tail) :- fail.
vp(3s, falls, [falls|Tail], Tail).
