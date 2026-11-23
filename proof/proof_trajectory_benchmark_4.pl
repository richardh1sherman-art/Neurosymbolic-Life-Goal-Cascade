%% Formal Axiomatic Proof Log: Test Case Benchmark 4
%% Execution Status: SUCCESS
%% Premise: and(if(p,not(not(r))),if(not(q),not(r))).
%% Target:  not(and(p,not(q))).

step(00, "and(if(p,not(not(r))),if(not(q),not(r)))").
step(01, "Apply Axiom 4 -> and(if(p,not(not(r))),if(not(q),not(r)))").
step(02, "Apply Axiom 10 -> and(if(p,not(not(r))),if(not(q),not(r)))").
step(03, "Apply Axiom 7 -> and(if(p,not(not(r))),if(not(q),not(r)))").
step(04, "Apply Axiom 14 -> and(if(p,not(not(r))),if(not(q),not(r)))").
step(05, "Apply Axiom 1 -> and(if(not(q),not(r)),if(p,not(not(r))))").
