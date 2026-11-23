%% Formal Axiomatic Proof Log: Test Case Benchmark 7
%% Execution Status: SUCCESS
%% Premise: and(if(gas,matter),and(if(vacuum,not(matter)),if(void,vacuum))).
%% Target:  if(void,not(gas)).

step(00, "and(if(gas,matter),and(if(vacuum,not(matter)),if(void,vacuum)))").
step(01, "Apply Axiom 4 -> and(and(if(gas,matter),if(vacuum,not(matter))),if(void,vacuum))").
