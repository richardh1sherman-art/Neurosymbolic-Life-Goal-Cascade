
:- consult('kb.pl').

%% Mocking active situational instances directly for 2nd order logic verification
action_p_occurred(house_fire_dispatch).
has_permission_q(dispatcher_alert_rotation) :- fail. %% 🚨 Force a contract permission omission state

evaluate_system_breach :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG EVALUATOR: CHECKING 2ND ORDER PRAGMATIC CONTRACT INVARIANTS~n'),
    format('==================================================================================~n'),
    
    ( pragmatic_contract_breach(house_fire_dispatch, dispatcher_alert_rotation) ->
        format(' 🛑 [BREACH DETECTED]: Action [house_fire_dispatch] executed without permission constraint!~n')
    ;
        format(' 🟢 [CLEAR]: No social contract violations active in current manifold.~n')
    ),
    format('==================================================================================~n'),
    halt.
