%% Formal Axiomatic Proof Log: Test Case Benchmark 9
%% Execution Status: SUCCESS
%% Premise: if(if(if(p,q),p),p).
%% Target:  p.

step(00, "if(if(if(p,q),p),p)").
step(01, "Apply Axiom 8 -> if(if(if(p,q),p),p)").
step(02, "Apply Axiom 5 -> if(if(if(p,q),p),p)").
step(03, "Apply Axiom 10 -> if(if(if(p,q),p),p)").
step(04, "Apply Axiom 8 -> if(if(if(p,q),p),p)").
step(05, "Apply Axiom 14 -> if(if(if(p,q),p),p)").
step(06, "Apply Axiom 9 -> if(if(if(not(not(p)),q),p),p)").
step(07, "Apply Axiom 13 -> if(if(if(not(not(p)),q),p),p)").
step(08, "Apply Axiom 11 -> if(if(if(not(not(p)),q),p),p)").
step(09, "Apply Axiom 3 -> if(if(if(not(not(p)),q),p),p)").
step(10, "Apply Axiom 8 -> if(if(if(not(not(p)),q),p),p)").
step(11, "Apply Axiom 1 -> if(if(if(not(not(p)),q),p),p)").
step(12, "Apply Axiom 9 -> if(if(if(not(not(p)),q),p),p)").
step(13, "Apply Axiom 4 -> if(if(if(not(not(p)),q),p),p)").
step(14, "Apply Axiom 9 -> if(if(if(not(not(p)),q),p),p)").
step(15, "Apply Axiom 9 -> if(if(if(not(not(p)),q),p),p)").
step(16, "Apply Axiom 5 -> if(if(if(not(not(p)),q),p),p)").
step(17, "Apply Axiom 12 -> if(if(if(not(not(p)),q),p),p)").
step(18, "Apply Axiom 12 -> if(if(if(not(not(p)),q),p),p)").
step(19, "Apply Axiom 14 -> if(if(if(not(not(p)),q),p),p)").
step(20, "Apply Axiom 6 -> or(not(if(if(not(not(p)),q),p)),p)").
step(21, "Apply Axiom 5 -> not(and(not(not(if(if(not(not(p)),q),p))),not(p)))").
step(22, "Apply Axiom 9 -> not(and(not(not(if(if(not(not(p)),q),p))),not(p)))").
step(23, "Apply Axiom 9 -> not(and(not(not(if(if(not(not(p)),q),p))),not(p)))").
step(24, "Apply Axiom 5 -> or(if(if(not(not(p)),q),p),p)").
