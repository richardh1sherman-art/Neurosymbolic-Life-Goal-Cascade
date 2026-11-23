%% Formal Axiomatic Proof Log: Test Case Benchmark 22
%% Execution Status: SUCCESS
%% Premise: forall(x, forall(y, forall(z, if(and(Greater(x,y), Greater(y,z)), Greater(x,z))))) ; Greater(a, b) ; Greater(b, c).
%% Target:  Greater(a, c).

step(00, "forall(x, forall(y, forall(z, if(and(Greater(x,y), Greater(y,z)), Greater(x,z))))) ; Greater(a, b) ; Greater(b, c)").
step(01, "Apply Axiom 11 -> forall(x, forall(y, forall(z, if(and(Greater(x,y), Greater(y,z)), Greater(x,z))))) ; Greater(a, b) ; Greater(b, c) ; Greater(a,c)").
