% The ultimate target predicate learned by the system
redemption_accomplished(State) :-
    sacrifice_validated(State),
    item_at(veil, temple),
    veil_status(State, ripped). % <-- Structural cosmic validation sign from Level 1
% --- State Definitions for 'current_state' ---
current_location(current_state, mount_moriah).

% This fixes the has_item/2 error by giving the engine data to find!
has_item(current_state, knife).
has_item(current_state, wood).

% --- Spiritual & Intent Data for 'current_state' ---
% (Add these to the top of bk_spiritual.pl or bk_hardware.pl)
intent(abraham, obey).
% --- Initial Physical State Facts ---
location(abraham_home).
location(mount_moriah).
accessible(abraham_home, mount_moriah, path_to_altar).

item_at(knife, abraham_home).
item_at(wood, abraham_home).
item_at(ram, thicket).
item_at(thicket, mount_moriah).

% --- Physical Capability Rules ---
% To travel to the altar, a valid path must connect the origin and destination.
route_clear(Origin, Destination) :-
    accessible(Origin, Destination, path_to_altar).

% Items must be actively packed and moved from home to the mountain.
supplies_ready(State) :-
    route_clear(abraham_home, mount_moriah),
    has_item(State, knife),
    has_item(State, wood).

% The ram is physically trapped and hidden in the brush until a specific coordinate is reached.
substitution_available(State) :-
    current_location(State, mount_moriah),
    item_at(ram, thicket),
    item_at(thicket, mount_moriah).
