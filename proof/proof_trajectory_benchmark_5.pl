%% Formal Axiomatic Proof Log: Test Case Benchmark 5
%% Execution Status: SUCCESS
%% Premise: and(if(r,not(p)),if(not(r),q)).
%% Target:  not(and(not(q),p)).

step(00, "and(if(r,not(p)),if(not(r),q))").
step(01, "Apply Axiom 12 -> and(if(r,not(p)),if(not(r),q))").
step(02, "Apply Axiom 4 -> and(if(r,not(p)),if(not(r),q))").
step(03, "Apply Axiom 2 -> and(if(r,not(p)),if(not(q),not(not(r))))").
