%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping
person(none).
trouble(none, none).
device(cell_phone).
signal(cell_phone, wifi).
dispatcher(permission_hook_and_ladder).
outcome(none, active).

%% Stage 3: Knowledge Base Hypothesis Rule Derivations
person_in_trouble(S, P) :- person(P), P \== none, trouble(P, T), T \== none.
signaling_device(S, D) :- device(D), signal(D, _).
dispatcher_clear(S, Disp) :- dispatcher(Disp).
final_outcome(S, P, Status) :- outcome(P, Status).
