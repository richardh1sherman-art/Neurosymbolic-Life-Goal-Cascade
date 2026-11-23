%% Formal Axiomatic Proof Log: Test Case Benchmark 17
%% Execution Status: SUCCESS
%% Premise: enc(object_x,Blueprint_A) ; exe(Physical,object_x) ; enc(object_y,Blueprint_B).
%% Target:  Consistent(state_s).

step(00, "enc(object_x,Blueprint_A) ; exe(Physical,object_x) ; enc(object_y,Blueprint_B)").
step(01, "Apply Axiom 7 -> enc(object_x,Blueprint_A) ; exe(Physical,object_x) ; enc(object_y,Blueprint_B) ; Consistent(state_s)").
