%% Formal Axiomatic Proof Log: Test Case Benchmark 21
%% Execution Status: SUCCESS
%% Premise: forall(x, iff(Shaves(barber, x), not(Shaves(x, x)))).
%% Target:  False.

step(00, "forall(x, iff(Shaves(barber, x), not(Shaves(x, x))))").
step(01, "Apply Axiom 14 -> forall(x,iff(Shaves(barber, x), not(Shaves(x, x))))").
step(02, "Apply Axiom 6 -> forall(x,iff(Shaves(barber, x), not(Shaves(x, x))))").
step(03, "Apply Axiom 3 -> forall(x,iff(Shaves(barber, x), not(Shaves(x, x))))").
step(04, "Apply Axiom 10 -> forall(x,iff(Shaves(barber, x), not(Shaves(x, x)))) ; iff(Shaves(barber, barber), not(Shaves(barber, barber)))").
