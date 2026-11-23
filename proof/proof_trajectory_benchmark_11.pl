%% Formal Axiomatic Proof Log: Test Case Benchmark 11
%% Execution Status: SUCCESS
%% Premise: and(if(p,q),and(if(q,and(r,s)),if(and(r,s),t))).
%% Target:  if(p,t).

step(00, "and(if(p,q),and(if(q,and(r,s)),if(and(r,s),t)))").
step(01, "Apply Axiom 14 -> and(if(p,q),and(if(q,and(r,s)),if(and(r,s),t)))").
step(02, "Apply Axiom 6 -> and(if(p,q),and(if(q,and(r,s)),or(not(and(r,s)),t)))").
