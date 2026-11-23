%% Formal Axiomatic Proof Log: Test Case Benchmark 13
%% Execution Status: SUCCESS
%% Premise: if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q).
%% Target:  d_w(p).

step(00, "if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(01, "Apply Axiom 10 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(02, "Apply Axiom 11 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(03, "Apply Axiom 6 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(04, "Apply Axiom 11 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(05, "Apply Axiom 11 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(06, "Apply Axiom 8 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(07, "Apply Axiom 10 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)").
step(08, "Apply Axiom 12 -> if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q) ; d_u(r) ; d_w(r) ; d_s(r)").
