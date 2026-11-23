
:- consult('kb.pl').
:- consult('exs.pl').

%% --- HARDENED COST SELECTOR ---
%% Evaluates the dynamic pathways and immediately applies a cut (!) to stop volatile backtracking
query_path_safely(StoryID, Cost) :-
    validate_path_minor(start_node, goal_vertex, StoryID, Cost), !.
query_path_safely(StoryID, Cost) :-
    validate_path_minor(station, goal_vertex, StoryID, Cost), !.
query_path_safely(StoryID, Cost) :-
    validate_path_minor(airport_gate, goal_vertex, StoryID, Cost), !.

evaluate_story_cost(StoryID) :-
    ( query_path_safely(StoryID, Cost) ->
        format(' [VALID] Path Minor Clear | Grigorchuk Cost: ~w (∘).', [Cost])
    ;
        write(' [BLOCKED] Decalogue Violation Severed Path (•).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: GRIGORCHUK COST MATRIX CLOSURE~n'),
    format('==================================================================================~n'),
    
    format('   ➔ Story [pierre_story_s1]       ──➔ STATUS:'), evaluate_story_cost(pierre_story_s1), format('~n'),
    format('   ➔ Story [pierre_story_s2]       ──➔ STATUS:'), evaluate_story_cost(pierre_story_s2), format('~n'),
    format('   ➔ Story [pierre_story_s2_prime] ──➔ STATUS:'), evaluate_story_cost(pierre_story_s2_prime), format('~n'),
    format('   ➔ Story [alec_story_s2]         ──➔ STATUS:'), evaluate_story_cost(alec_story_s2), format('~n'),
    format('   ➔ Story [alec_story_s2_prime]   ──➔ STATUS:'), evaluate_story_cost(alec_story_s2_prime), format('~n'),
    format('   ➔ Story [ana_story_s2]          ──➔ STATUS:'), evaluate_story_cost(ana_story_s2), format('~n'),
    format('   ➔ Story [ana_story_s2_prime]    ──➔ STATUS:'), evaluate_story_cost(ana_story_s2_prime), format('~n'),
    format('   ➔ Story [ana_story_s3_s5_prime] ──➔ STATUS:'), evaluate_story_cost(ana_story_s3_s5_prime), format('~n'),
    format('   ➔ Story [john_story_s1]         ──➔ STATUS:'), evaluate_story_cost(john_story_s1), format('~n'),
    
    % 🚨 EXPANDED SLOTS FOR TASK 3 INFRASTRUCTURE NARRATIVES
    format('   ➔ Story [fiber_story_s2]        ──➔ STATUS:'), evaluate_story_cost(fiber_story_s2), format('~n'),
    format('   ➔ Story [fiber_story_s2_prime]  ──➔ STATUS:'), evaluate_story_cost(fiber_story_s2_prime), format('~n'),
    format('   ➔ Story [display_story_s2]      ──➔ STATUS:'), evaluate_story_cost(display_story_s2), format('~n'),
    format('   ➔ Story [display_story_s2_prime]──➔ STATUS:'), evaluate_story_cost(display_story_s2_prime), format('~n'),
    
    % Sovereign Level Timelines
    format('   ➔ Story [moses_sovereign_flaw]  ──➔ STATUS:'), evaluate_story_cost(moses_sovereign_flaw), format('~n'),
    format('   ➔ Story [david_sovereign_flaw]  ──➔ STATUS:'), evaluate_story_cost(david_sovereign_flaw), format('~n'),
    format('   ➔ Story [paul_sovereign_flaw]   ──➔ STATUS:'), evaluate_story_cost(paul_sovereign_flaw), format('~n'),
    
    format('==================================================================================~n'),
    halt.
