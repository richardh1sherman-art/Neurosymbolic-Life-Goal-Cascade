%% Formal Axiomatic Proof Log: Test Case Benchmark 18
%% Execution Status: SUCCESS
%% Premise: Doctor(john).
%% Target:  exists(x, Doctor(x)).

step(00, "Doctor(john)").
step(01, "Apply Axiom 1 -> Doctor(john)").
step(02, "Apply Axiom 4 -> Doctor(john)").
step(03, "Apply Axiom 10 -> Doctor(john) ; exists(x, Doctor(x))").
