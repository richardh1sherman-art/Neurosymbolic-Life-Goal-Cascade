
:- consult('kb.pl').
:- consult('exs.pl').

verify_situation_status(SituationID) :-
    ( situation_classification(SituationID, SchemaDecision) ->
        format(' [VALID] Situation Core Aligned | Forest Node: ~w (∘).', [SchemaDecision])
    ;
        write(' [ERROR] Defective Situation Signature Detected (•).')
    ).

execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG DEDUCTION RUNNER: UNIVERSAL FOREST CLOSURE AUDIT~n'),
    format('==================================================================================~n'),
    
    format('   ➔ Situation [st1_timeline]             ──➔ STATUS:'), verify_situation_status(st1_timeline), format('~n'),
    format('   ➔ Situation [sb_timeline_pos]          ──➔ STATUS:'), verify_situation_status(sb_timeline_pos), format('~n'),
    format('   ➔ Situation [st2_timeline_neg]         ──➔ STATUS:'), verify_situation_status(st2_timeline_neg), format('~n'),
    format('   ➔ Situation [john_reversal_timeline]   ──➔ STATUS:'), verify_situation_status(john_reversal_timeline), format('~n'),
    format('   ➔ Situation [moses_scripture_timeline] ──➔ STATUS:'), verify_situation_status(moses_scripture_timeline), format('~n'),
    format('   ➔ Situation [david_scripture_timeline] ──➔ STATUS:'), verify_situation_status(david_scripture_timeline), format('~n'),
    
    format('==================================================================================~n'),
    halt.
