
:- consult('kb.pl').

%% Asserting experimental context facts to validate 2nd order transfer properties
fact_holds_in_situation(prevent_via_friend_accompaniment, judith_mountain_rescue).

execute_transfer_evaluation :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG EVALUATOR: VERIFYING HIGH-ORDER ANALOGY FACT TRANSFERS~n'),
    format('==================================================================================~n'),
    
    % Test Reflexive Transfer: Mountain Rescue -> Kitchen Fire Setting
    ( transfer_fact_reflexive(prevent_via_friend_accompaniment, judith_mountain_rescue, george_kitchen_fire) ->
        format(' 🔄 [REFLEXIVE SUCCESS]: Fact transferred symmetrically to [george_kitchen_fire] (∘).~n')
    ;
        format(' ❌ Reflexive link failed.~n')
    ),
    
    % Test Transitive Chain: Mountain Rescue -> Kitchen Fire Setting -> Community Safety Rehearsal Workspace
    ( transfer_fact_transitive(prevent_via_friend_accompaniment, judith_mountain_rescue, george_kitchen_fire, community_safety_rehearsal) ->
        format(' 🔗 [TRANSITIVE SUCCESS]: Fact chained through to [community_safety_rehearsal] (∘).~n')
    ;
        format(' ❌ Transitive chain broken.~n')
    ),
    format('==================================================================================~n'),
    halt.
