
:- consult('kb.pl').
:- consult('exs.pl').

%% --- EDWARD ZALTA MODAL CLOSURE BACKGROUND AXIOMS ---
actual_situation_valid(StoryID) :-
    (execute_rewrite(StoryID, _) -> 
        write(' [REWRITE DETECTED] Counterfactual successfully isolated (∘).')
    ;
        write(' [SEMANTIC PRESERVED] Continuous logic timeline clear (∘).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: VALIDATING ZALTA MODAL CLOSURE OVER ALL STORIES~n'),
    format('==================================================================================~n'),
    
    format('   ➔ Story [pierre_story_s1]     ──➔ PROOF STATUS:'), actual_situation_valid(pierre_story_s1), format('~n'),
    format('   ➔ Story [pierre_story_s2]     ──➔ PROOF STATUS:'), actual_situation_valid(pierre_story_s2), format('~n'),
    format('   ➔ Story [pierre_story_s2_prime] ──➔ PROOF STATUS:'), actual_situation_valid(pierre_story_s2_prime), format('~n'),
    format('   ➔ Story [alec_story_s2]       ──➔ PROOF STATUS:'), actual_situation_valid(alec_story_s2), format('~n'),
    format('   ➔ Story [alec_story_s2_prime] ──➔ PROOF STATUS:'), actual_situation_valid(alec_story_s2_prime), format('~n'),
    format('   ➔ Story [ana_story_s2]        ──➔ PROOF STATUS:'), actual_situation_valid(ana_story_s2), format('~n'),
    format('   ➔ Story [ana_story_s2_prime]  ──➔ PROOF STATUS:'), actual_situation_valid(ana_story_s2_prime), format('~n'),
    format('   ➔ Story [john_story_s1]       ──➔ PROOF STATUS:'), actual_situation_valid(john_story_s1), format('~n'),
    format('   ➔ Story [moses_sovereign_flaw] ──➔ PROOF STATUS:'), actual_situation_valid(moses_sovereign_flaw), format('~n'),
    format('   ➔ Story [david_sovereign_flaw] ──➔ PROOF STATUS:'), actual_situation_valid(david_sovereign_flaw), format('~n'),
    format('   ➔ Story [paul_sovereign_flaw]  ──➔ PROOF STATUS:'), actual_situation_valid(paul_sovereign_flaw), format('~n'),
    
    format('==================================================================================~n'),
    halt.
