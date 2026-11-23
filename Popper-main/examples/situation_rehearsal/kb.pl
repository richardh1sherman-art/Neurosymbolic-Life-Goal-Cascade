%% =================================================================
%% 🌀 TIER 3 BACKGROUND KNOWLEDGE: TOPOLOGICAL GRAPH MINOR OPERATORS
%% Core Laws for Edge Deletion (G \ e) and Node Contraction (G / e)
%% =================================================================
:- discontiguous edge/2.
:- discontiguous deleted_edge/2.
:- discontiguous contracted_nodes/2.
:- discontiguous rasiowa_interior/2.

%% --- BASELINE GRAPH NETWORK SETUP (Simulating Story Trajectories) ---
edge(station, platform_1).
edge(platform_1, nyc_vertex).

%% --- EDGE DELETION OPERATOR (G \ e) ---
%% An edge is legally active IF it has not been explicitly deleted by a story fault
active_edge(U, V) :-
    edge(U, V),
    \+ deleted_edge(U, V).

%% --- NODE CONTRACTION OPERATOR (G / e) ---
%% Simulates an algebraic failover merging two nodes into a single structural vertex
equivalent_nodes(U, U).
equivalent_nodes(U, V) :- contracted_nodes(U, V).
equivalent_nodes(U, V) :- contracted_nodes(V, U).

%% --- TOPOLOGICAL PATHFINDING SEARCH ---
%% Evaluates traversals across the derived graph minor landscape
path_minor_clear(Start, Goal) :-
    path_minor_traverse(Start, Goal, []).

path_minor_traverse(Current, Goal, _Visited) :-
    equivalent_nodes(Current, Goal), !.
path_minor_traverse(Current, Goal, Visited) :-
    equivalent_nodes(Current, ActualCurrent),
    active_edge(ActualCurrent, Next),
    \+ member(Next, Visited),
    path_minor_traverse(Next, Goal, [ActualCurrent|Visited]).

%% --- INTEGRATION WITH RASIOWA APX OVERRIDES ---
%% If a path survives edge deletion or resolves via contraction, it stays inside the Interior Core
rasiowa_interior(StoryID, true) :-
    path_minor_clear(station, nyc_vertex), !.
rasiowa_interior(_, false).
