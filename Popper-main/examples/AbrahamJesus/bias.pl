% =====================================================================
% FILENAME: bias.pl
% PURPOSE: Language Bias Constraints for the Abraham/Jesus Bisimulation
%          Controls the search space for the Popper ILP Engine
% =====================================================================

% ---------------------------------------------------------------------
% 1. DEFINE MAX TYPE DEPTHS AND CLAUSE LIMITS
% ---------------------------------------------------------------------
max_clauses(3).       % The learned program cannot exceed 3 total rules.
max_vars(5).          % No individual rule can juggle more than 5 distinct variables.
max_body(4).          % Each rule can have at most 4 conditions in its body.

% ---------------------------------------------------------------------
% 2. MODE DECLARATIONS (WHAT POPPER IS ALLOWED TO TEST)
%    Format: modeb(Recall, Predicate(Type1, Type2, ...))
%    + represents an input variable (must be bound by a previous literal)
%    - represents an output variable (introduces a new connected entity)
% ---------------------------------------------------------------------

% Allow the engine to check the current situation context
modeb(1, situation_type(+situation)).

% Allow the engine to look up the structural counterparts across the stories
modeb(1, spiritual_counterpart(+situation, +entity, +situation, -entity)).
modeb(1, spiritual_counterpart(+situation, -entity, +situation, +entity)).

% Allow checking relationship dynamics between two entities
modeb(1, parent_child_dynamic(+situation, +entity, +entity, #dynamic_type)).

% Allow checking operational action milestones
modeb(1, route_traversed(+situation, +entity)).
modeb(1, voluntary_action(+situation, +entity)).
modeb(1, sacrifice_identity_declared(+situation, +entity)).

% ---------------------------------------------------------------------
% 3. TYPE DEFINITIONS
%    Tells Popper how variables map to specific physical categories
% ---------------------------------------------------------------------
type(situation_type, (situation,)).
type(spiritual_counterpart, (situation, entity, situation, entity)).
type(parent_child_dynamic, (situation, entity, entity, dynamic_type)).
type(route_traversed, (situation, entity)).
type(voluntary_action, (situation, entity)).
type(sacrifice_identity_declared, (situation, entity)).

% ---------------------------------------------------------------------
% 4. PRUNING CONSTRAINTS (THE GUARDRAILS)
%    Deductively forbids Popper from building illogical branches
% ---------------------------------------------------------------------

% Rule A: Forbid testing a counterpart mapping within the exact same story context.
% (e.g., trying to map Abraham to Isaac within genesis_22 is a structural hallucination).
:-
    body(Literal),
    Literal = spiritual_counterpart(Sit, _, Sit, _).

% Rule B: Prevent Popper from checking an action or identity variable 
% unless it has already established the situation context it belongs to.
:-
    body(Literal),
    Literal = voluntary_action(Sit, _),
    not body(situation_type(Sit)).

% Rule C: Enforce symmetry. If the engine maps an analogy from Situation A 
% to Situation B, it must actively use elements from both situations in the body.
:-
    body(situation_type(SitA)),
    not body(situation_type(SitB)),
    SitA \= SitB,
    body(spiritual_counterpart(SitA, _, SitB, _)).
