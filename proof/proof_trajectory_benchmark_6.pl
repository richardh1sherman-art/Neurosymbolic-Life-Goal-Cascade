%% Formal Axiomatic Proof Log: Test Case Benchmark 6
%% Execution Status: SUCCESS
%% Premise: and(if(p,r),if(q,not(r))).
%% Target:  not(and(p,q)).

step(00, "and(if(p,r),if(q,not(r)))").
step(01, "Apply Axiom 6 -> and(if(p,r),or(not(q),not(r)))").
