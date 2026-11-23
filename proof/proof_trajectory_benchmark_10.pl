%% Formal Axiomatic Proof Log: Test Case Benchmark 10
%% Execution Status: SUCCESS
%% Premise: and(if(p,q),and(if(p,r),and(if(q,s),and(if(r,s),if(s,t))))).
%% Target:  if(p,t).

step(00, "and(if(p,q),and(if(p,r),and(if(q,s),and(if(r,s),if(s,t)))))").
step(01, "Apply Axiom 3 -> and(if(p,q),and(if(p,r),and(if(q,s),and(if(r,s),if(s,t)))))").
step(02, "Apply Axiom 6 -> and(if(p,q),and(if(p,r),and(if(q,s),and(if(r,s),or(not(s),t)))))").
