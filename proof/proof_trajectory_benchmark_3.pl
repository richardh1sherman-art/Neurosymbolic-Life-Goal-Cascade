%% Formal Axiomatic Proof Log: Test Case Benchmark 3
%% Execution Status: SUCCESS
%% Premise: and(if(p,q),p).
%% Target:  q.

step(00, "and(if(p,q),p)").
step(01, "Apply Axiom 4 -> and(if(p,q),p)").
step(02, "Apply Axiom 10 -> and(if(p,q),p)").
step(03, "Apply Axiom 2 -> and(if(p,q),p)").
step(04, "Apply Axiom 3 -> and(if(p,q),p)").
step(05, "Apply Axiom 6 -> and(if(p,q),p)").
step(06, "Apply Axiom 3 -> and(if(p,q),p)").
step(07, "Apply Axiom 12 -> and(if(p,q),p)").
step(08, "Apply Axiom 12 -> and(if(p,q),p)").
step(09, "Apply Axiom 4 -> and(if(p,q),p)").
step(10, "Apply Axiom 7 -> and(if(p,q),p)").
step(11, "Apply Axiom 10 -> and(if(p,q),p)").
step(12, "Apply Axiom 7 -> and(if(p,q),p)").
step(13, "Apply Axiom 8 -> and(if(p,q),p)").
step(14, "Apply Axiom 1 -> and(p,if(p,q))").
