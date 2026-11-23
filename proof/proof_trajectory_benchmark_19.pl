%% Formal Axiomatic Proof Log: Test Case Benchmark 19
%% Execution Status: SUCCESS
%% Premise: not(forall(x, Perfect(x))).
%% Target:  exists(x, not(Perfect(x))).

step(00, "not(forall(x, Perfect(x)))").
step(01, "Apply Axiom 5 -> not(forall(x, Perfect(x)))").
step(02, "Apply Axiom 5 -> not(forall(x, Perfect(x)))").
step(03, "Apply Axiom 8 -> not(forall(x, Perfect(x)))").
step(04, "Apply Axiom 10 -> not(forall(x, Perfect(x))) ; exists(x, not(Perfect(x)))").
