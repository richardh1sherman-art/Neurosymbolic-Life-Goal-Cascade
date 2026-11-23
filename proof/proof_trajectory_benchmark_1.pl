%% Formal Axiomatic Proof Log: Test Case Benchmark 1
%% Execution Status: SUCCESS
%% Premise: and(p,q).
%% Target:  and(q,p).

step(00, "and(p,q)").
step(01, "Apply Axiom 10 -> and(p,q)").
step(02, "Apply Axiom 5 -> and(p,q)").
step(03, "Apply Axiom 6 -> and(p,q)").
step(04, "Apply Axiom 13 -> and(p,q)").
step(05, "Apply Axiom 7 -> and(p,q)").
step(06, "Apply Axiom 8 -> and(p,q)").
step(07, "Apply Axiom 5 -> and(p,q)").
step(08, "Apply Axiom 13 -> and(p,q)").
step(09, "Apply Axiom 7 -> and(p,q)").
step(10, "Apply Axiom 9 -> and(not(not(p)),q)").
