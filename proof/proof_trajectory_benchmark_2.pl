%% Formal Axiomatic Proof Log: Test Case Benchmark 2
%% Execution Status: SUCCESS
%% Premise: if(p,q).
%% Target:  if(not(q),not(p)).

step(00, "if(p,q)").
step(01, "Apply Axiom 7 -> if(p,q)").
step(02, "Apply Axiom 2 -> if(not(q),not(p))").
