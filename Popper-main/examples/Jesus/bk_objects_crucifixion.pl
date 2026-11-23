% --- Initial Physical State Facts ---
location(calvary).
location(temple).

item_at(cross, calvary).
item_at(nails, calvary).
item_at(crown_of_thorns, calvary).
item_at(clothes, calvary).
item_at(veil, temple).

% --- Physical State Assertions ---
body_status(current_state, torn).
bodily_need(current_state, thirst).
veil_status(current_state, ripped).
blood_shed(current_state, true).

% --- Physical Readiness Rules ---
% Physical execution requires the presence of the instruments of crucifixion.
instruments_deployed(State) :-
    item_at(cross, calvary),
    item_at(nails, calvary),
    item_at(crown_of_thorns, calvary).

% The physical trauma is complete when the physical toll matches the narrative.
physical_sacrifice_complete(State) :-
    instruments_deployed(State),
    body_status(State, torn),
    bodily_need(State, thirst),
    blood_shed(State, true).
