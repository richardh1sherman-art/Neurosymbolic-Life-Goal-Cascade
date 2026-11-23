%% Formal Axiomatic Proof Log: Test Case Benchmark 14
%% Execution Status: SUCCESS
%% Premise: forall(x, if(Human(x), Mortal(x))) ; Human(john).
%% Target:  Mortal(john).

step(00, "forall(x, if(Human(x), Mortal(x))) ; Human(john)").
step(01, "Apply Axiom 2 -> forall(x, if(Human(x), Mortal(x))) ; Human(john)").
step(02, "Apply Axiom 2 -> forall(x, if(Human(x), Mortal(x))) ; Human(john)").
step(03, "Apply Axiom 3 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(04, "Apply Axiom 6 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(05, "Apply Axiom 5 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(06, "Apply Axiom 7 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(07, "Apply Axiom 4 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(08, "Apply Axiom 4 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(09, "Apply Axiom 13 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(10, "Apply Axiom 14 -> forall(x,if(Human(x), Mortal(x))) ; Human(john)").
step(11, "Apply Axiom 10 -> forall(x,if(Human(x), Mortal(x))) ; Human(john) ; if(Human(barber), Mortal(barber)) ; exists(x, Human(x))").
step(12, "Apply Axiom 11 -> forall(x,if(Human(x), Mortal(x))) ; Human(john) ; if(Human(barber), Mortal(barber)) ; exists(x, Human(x)) ; Mortal(john) ; Mortal(x) ; Mortal(barber)").
