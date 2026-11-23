%% Formal Axiomatic Proof Log: Test Case Benchmark 12
%% Execution Status: SUCCESS
%% Premise: and(or(p11,p12),and(or(p21,p22),or(p31,p32))).
%% Target:  or(and(p11,p21),or(and(p11,p31),or(and(p21,p31),or(and(p12,p22),or(and(p12,p32),and(p22,p32)))))).

step(00, "and(or(p11,p12),and(or(p21,p22),or(p31,p32)))").
step(01, "Apply Axiom 7 -> and(or(p11,p12),and(or(p21,p22),or(p31,p32)))").
step(02, "Apply Axiom 6 -> and(or(p11,p12),and(or(p21,p22),or(p31,p32)))").
step(03, "Apply Axiom 7 -> and(or(p11,p12),and(or(p21,p22),or(p31,p32)))").
step(04, "Apply Axiom 1 -> and(or(p12,p11),and(or(p21,p22),or(p31,p32)))").
