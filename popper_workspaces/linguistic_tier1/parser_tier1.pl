%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Universal Matrix Supporting MIT Memo Food Truck State Spaces
%% =================================================================

:- dynamic food_truck_state/3.
:- dynamic kinematic_action/2.

%% --- 🍱 MIT FOOD TRUCK STATE CONFIGURATIONS ---
% Syntax: food_truck_state(SpotID, CuisineType, VisibilityStatus)
food_truck_state(spot_y_loc, korean_truck, visible_nearby).
food_truck_state(spot_x_loc, lebanese_or_mexican, hidden_behind_wall).

%% --- 🛸 KINEMATIC TRANSITION MANIFOLDS ---
kinematic_action(left_right_up_down, jax_clip_bounded).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(spot_x_loc, food_truck_topology, hidden_simplex).
part_of(left_right_up_down, action_space, overdamped_kinematics).
