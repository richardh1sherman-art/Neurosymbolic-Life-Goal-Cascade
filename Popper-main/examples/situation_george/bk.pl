%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping
person(george).
trouble(george, near_fire).
device(smoke_detector).
signal(smoke_detector, wifi).
dispatcher(permission_hook_and_ladder).
outcome(george, safe).

%% Stage 3: Knowledge Base Hypothesis Rule Derivations
person_in_trouble(S, P) :- person(P), trouble(P, _).
signaling_device(S, D) :- device(D), signal(D, _).
dispatcher_clear(S, Disp) :- dispatcher(Disp).
final_outcome(S, P, Status) :- outcome(P, Status).
