%% 🌴 Background Knowledge: Decoupled Analogy Profiles
:- discontiguous situation/1.
:- discontiguous uncontrolled_descent/2.
:- discontiguous accident/3.
:- discontiguous isomorphic_role_match/2.

situation(situation_judith).
situation(situation_george).
situation(situation_rehearsal).

%% --- PROFILE 1: RESCUE OF JUDITH (SOURCE) ---
uncontrolled_descent(situation_judith, judith).
accident(situation_judith, judith, mountain).

%% --- PROFILE 2: GEORGE'S KITCHEN FIRE (TARGET ANALOGY) ---
uncontrolled_descent(situation_george, george).
accident(situation_george, george, kitchen).

%% --- PROFILE 3: FIREHOUSE REHEARSAL (DISANALOGY) ---
%% Explicitly blank parameters for functional/environmental hazards!

%% 🚨 FIX: Tightly bind the roles to their specific Situation contexts!
isomorphic_role_match(Src, Tgt) :-
    uncontrolled_descent(Src, _),
    uncontrolled_descent(Tgt, _),
    accident(Src, _, _),
    accident(Tgt, _, _).

%% The General Analogy Template mapping bound conditions
analogy_discovered(Src, Tgt) :-
    Src \== Tgt,
    isomorphic_role_match(Src, Tgt), !.
