%% Formal Axiomatic Proof Log: Test Case Benchmark 8
%% Execution Status: SUCCESS
%% Premise: and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical)))).
%% Target:  if(polar_bear,not(flamingo)).

step(00, "and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical))))").
step(01, "Apply Axiom 7 -> and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical))))").
step(02, "Apply Axiom 7 -> and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical))))").
step(03, "Apply Axiom 4 -> and(if(polar_bear,arctic),and(and(if(arctic,cold),if(tropical,not(cold))),if(flamingo,tropical)))").
