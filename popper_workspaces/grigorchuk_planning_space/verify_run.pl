
:- consult('kb.pl').
:- consult('exs.pl').
execute_verification_audit :-
    format('~n==================================================================================~n'),
    format('SWI-PROLOG TOPOLOGICAL DEDUCTION RUNNER: RECOVERED CHECK PASS~n'),
    format('==================================================================================~n'),
    (validate_path_minor(station, goal_vertex, s_0) -> format('   ➔ Story [s_0] ──➔ PROOF STATUS: [SUCCESS] Traversable (∘).~n', []) ; format('   ➔ Story [s_0] ──➔ PROOF STATUS: [FAILED] Blocked (•).~n', [])),
    (validate_path_minor(airport_gate, goal_vertex, s_1) -> format('   ➔ Story [s_1] ──➔ PROOF STATUS: [SUCCESS] Traversable (∘).~n', []) ; format('   ➔ Story [s_1] ──➔ PROOF STATUS: [FAILED] Blocked (•).~n', [])),
    format('==================================================================================~n'),
    halt.
