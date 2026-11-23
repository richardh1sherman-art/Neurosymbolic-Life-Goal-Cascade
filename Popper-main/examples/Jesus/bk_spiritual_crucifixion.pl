% --- Spiritual Relationships & Identities ---
relationship(god, jesus, father_son).
identity(jesus, lamb_of_god).

% --- The Hierarchical Operational Logic ---
% Step 1: The designated route to the cross must be traversed.
route_traversed(jesus, route_to_cross, calvary).

% Step 2: The physical capability and completion must be verified from Level 1.
can_fulfill_sacrifice(State) :-
    route_traversed(jesus, route_to_cross, calvary),
    physical_sacrifice_complete(State). % <-- Call to Level 1 Sub-Tree

% Step 3: Divine communication establishes the explicit relationship context.
divine_witness(State) :-
    can_fulfill_sacrifice(State),
    relationship(god, jesus, father_son). % <-- God talking to Jesus as His Son

% Step 4: Jesus actively chooses to surrender His spirit, transforming the execution into a voluntary offering.
willing_submission(State) :-
    divine_witness(State),
    action(jesus, give_up_life).

% Step 5: The substitutionary theological outcome triggers.
sacrifice_validated(State) :-
    willing_submission(State),
    identity(jesus, lamb_of_god).
