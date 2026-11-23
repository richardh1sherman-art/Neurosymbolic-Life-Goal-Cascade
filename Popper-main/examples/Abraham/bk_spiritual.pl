% --- Spiritual Attributes & Relationships ---
relationship(abraham, isaac, parent_child).
attribute(isaac, brave).
attribute(abraham, faithful).

% --- The Hierarchical Operational Logic ---
% Step 1: God issues a direction to Abraham.
divine_instruction(abraham, sacrifice(isaac)).

% Step 2: The physical capability must be verified using Level 1 logic.
can_initiate_test(State) :-
    divine_instruction(abraham, sacrifice(isaac)),
    supplies_ready(State).  % <-- Call to Level 1 Sub-Tree

% Step 3: Isaac's internal bravery enables submission, preventing physical struggle.
altar_binding_successful(State) :-
    can_initiate_test(State),
    current_location(State, mount_moriah),
    attribute(isaac, brave).

% Step 4: Abraham acts purely on the instruction, creating the ultimate test state.
knife_raised(State) :-
    altar_binding_successful(State),
    intent(abraham, obey).

% Step 5: The Angelic Intervention rule executes when obedience is proven.
angel_intervenes(State) :-
    knife_raised(State),
    relationship(abraham, isaac, parent_child).
% Ensure these rules are at the end of bk_spiritual.pl:

covenant_confirmed(State) :-
    angel_intervenes(State),
    substitution_available(State).
