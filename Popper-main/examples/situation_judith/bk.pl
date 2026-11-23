%% Stage 1 & 2: Synthesized Prolog Atom Primitives via POS Mapping
person(judith).
trouble(judith, fall).
device(flashlight).
signal(flashlight, sos).
dispatcher(permission_helicopter).
outcome(judith, rescued).

%% Stage 3: Knowledge Base Hypothesis Rule Derivations
person_in_trouble(S, P) :- person(P), trouble(P, _).
signaling_device(S, D) :- device(D), signal(D, _).
dispatcher_clear(S, Disp) :- dispatcher(Disp).
final_outcome(S, P, Status) :- outcome(P, Status).
