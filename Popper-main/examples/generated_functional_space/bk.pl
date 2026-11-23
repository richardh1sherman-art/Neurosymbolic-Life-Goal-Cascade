
%% Story Data: judith_rescue
abstract_object(judith_rescue, functional_role, uncontrolled_descent(judith)).

%% Story Data: kitchen_fire
abstract_object(kitchen_fire, functional_role, uncontrolled_descent(george)).

%% Extended Domain Data: planner_task
abstract_object(planner_task, functional_role, validate_tactical_step(judith, depth_zero)).

%% Extended Domain Data: theorem_prover_task
abstract_object(theorem_prover_task, functional_role, validate_tactical_step(prover, depth_zero)).

%% Extended Domain Data: consensus_protocol_task
abstract_object(consensus_protocol_task, functional_role, validate_tactical_step(node, depth_zero)).

%% Extended Domain Data: image_processing_task
abstract_object(image_processing_task, functional_role, validate_tactical_step(filter, depth_zero)).
