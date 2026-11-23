%% Formal Axiomatic Proof Log: Test Case Benchmark 16
%% Execution Status: SUCCESS
%% Premise: in_circle(12,15,50) ; in_circle(14,17,50).
%% Target:  or(in_circle(12,15,50),in_box(12.0,15.0,10)).

step(00, "in_circle(12,15,50) ; in_circle(14,17,50)").
step(01, "Apply Axiom 12 -> in_circle(12,15,50) ; in_circle(14,17,50)").
step(02, "Apply Axiom 8 -> in_circle(12,15,50) ; in_circle(14,17,50)").
step(03, "Apply Axiom 8 -> in_circle(12,15,50) ; in_circle(14,17,50)").
step(04, "Apply Axiom 11 -> in_circle(12,15,50) ; in_circle(14,17,50) ; or(in_circle(12,15,50),in_box(12.0,15.0,10))").
