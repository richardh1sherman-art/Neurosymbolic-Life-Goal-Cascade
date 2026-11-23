%% Formal Axiomatic Proof Log: Test Case Benchmark 20
%% Execution Status: SUCCESS
%% Premise: exists(y, forall(x, Mentors(y, x))).
%% Target:  forall(x, exists(y, Mentors(y, x))).

step(00, "exists(y, forall(x, Mentors(y, x)))").
step(01, "Apply Axiom 12 -> exists(y, forall(x, Mentors(y, x)))").
step(02, "Apply Axiom 10 -> exists(y, forall(x, Mentors(y, x)))").
step(03, "Apply Axiom 9 -> exists(y,forall(x,Mentors(y, x)))").
