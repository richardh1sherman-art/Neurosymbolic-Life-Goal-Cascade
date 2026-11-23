% =====================================================================
% FILENAME: bk.pl
% PURPOSE: Bisimulation Mapping (Structural Analogy) between the 
%          Abrahamic Testing and Christological Crucifixion Situations
%          Focus Area: Spiritual/Operational Level
% =====================================================================

% ---------------------------------------------------------------------
% 1. GROUND SITUATION LABELS
% ---------------------------------------------------------------------
situation_type(genesis_22).
situation_type(gospel_crucifixion).

% ---------------------------------------------------------------------
% 2. THE BISIMULATION MAPPING (THE COUNTERPARTS)
%    Format: spiritual_counterpart(SitA, EntityA, SitB, EntityB)
% ---------------------------------------------------------------------

% --- Role 1: The Sovereign Father Initiator ---
spiritual_counterpart(genesis_22, abraham, gospel_crucifixion, god_the_father).

% --- Role 2: The Beloved Son ---
spiritual_counterpart(genesis_22, isaac, gospel_crucifixion, jesus_christ).

% --- Role 3: The Ultimate Sacrifice Identity ---
% In Gen 22, the ultimate sacrifice is outsourced to a hidden/trapped asset.
% In the Gospels, the Son embodies that exact proxy identity directly.
spiritual_counterpart(genesis_22, ram_in_thicket, gospel_crucifixion, lamb_of_god).

% --- Action 1: The Journey of Obedience ---
spiritual_counterpart(genesis_22, route_to_moriah, gospel_crucifixion, route_to_cross).

% --- Action 2: The Core Act of Willing Surrender ---
% Isaac's passive bravery maps directly to Jesus' active surrender of life.
spiritual_counterpart(genesis_22, submission_to_binding, gospel_crucifixion, giving_up_life).

% --- Outcome: The Divine Breakthrough Sign ---
spiritual_counterpart(genesis_22, angel_interventions, gospel_crucifixion, ripped_temple_veil).


% ---------------------------------------------------------------------
% 3. INDUCTIVE SYMMETRY AXIOMS (THE SIMILARITY CALCULUS)
% ---------------------------------------------------------------------

% Relationship Symmetry: If Father and Son exist in SitA, they must map to SitB
analogous_relationship(SitA, SitB, RelationType) :-
    situation_type(SitA),
    situation_type(SitB),
    SitA \= SitB,
    spiritual_counterpart(SitA, FatherA, SitB, FatherB),
    spiritual_counterpart(SitA, SonA, SitB, SonB),
    parent_child_dynamic(SitA, FatherA, SonA, RelationType),
    parent_child_dynamic(SitB, FatherB, SonB, RelationType).

% Process Symmetry: The operational workflow must match structurally
analogous_operational_flow(SitA, SitB) :-
    situation_type(SitA),
    situation_type(SitB),
    SitA \= SitB,
    % The Route must be traversed
    spiritual_counterpart(SitA, RouteA, SitB, RouteB),
    route_traversed(SitA, RouteA),
    route_traversed(SitB, RouteB),
    % The Willing Submission must be executed
    spiritual_counterpart(SitA, ActionA, SitB, ActionB),
    voluntary_action(SitA, ActionA),
    voluntary_action(SitB, ActionB).


% ---------------------------------------------------------------------
% 4. INSTANTIATED BACKGROUND KNOWLEDGE FACTS
% ---------------------------------------------------------------------

% --- Parent-Child Relationship Dynamics ---
parent_child_dynamic(genesis_22, abraham, isaac, divine_promise_line).
parent_child_dynamic(gospel_crucifixion, god_the_father, jesus_christ, divine_promise_line).

% --- Operational Milestones Met in Both Experiences ---
route_traversed(genesis_22, route_to_moriah).
route_traversed(gospel_crucifixion, route_to_cross).

voluntary_action(genesis_22, submission_to_binding).
voluntary_action(gospel_crucifixion, giving_up_life).


% ---------------------------------------------------------------------
% 5. DEDUCTIVE CLOSURE (COVENANT FULLFILLMENT MACRO-RULE)
%    This rule enforces that the structural criteria must mirror each 
%    other across the bisimulation mapping to achieve state validation.
% ---------------------------------------------------------------------
macro_spiritual_fulfillment(Sit) :-
    situation_type(Sit),
    situation_type(AlternateSit),
    Sit \= AlternateSit,
    analogous_relationship(Sit, AlternateSit, divine_promise_line),
    analogous_operational_flow(Sit, AlternateSit),
    spiritual_counterpart(Sit, ProxyA, AlternateSit, ProxyB),
    sacrifice_identity_declared(Sit, ProxyA),
    sacrifice_identity_declared(AlternateSit, ProxyB).

% Final ground assignments for the identities
sacrifice_identity_declared(genesis_22, ram_in_thicket).
sacrifice_identity_declared(gospel_crucifixion, lamb_of_god).

% Context Setup
situation_type(state_abraham_no_knife, genesis_22).
situation_type(state_jesus_no_cross, gospel_crucifixion).

% State A: Abraham travels but forgets the tool
route_traversed(state_abraham_no_knife, route_to_moriah).
% (Missing: instruments_deployed fact for knife)

% State B: Jesus is in the location, but Roman tools are absent
route_traversed(state_jesus_no_cross, route_to_cross).
% (Missing: instruments_deployed fact for cross/nails)
% Context Setup
situation_type(state_abraham_refuses, genesis_22).
situation_type(state_jesus_saves_himself, gospel_crucifixion).

% State C: Abraham has his tools, but chooses not to obey
route_traversed(state_abraham_refuses, route_to_moriah).
instruments_deployed(state_abraham_refuses, knife).
parent_child_dynamic(state_abraham_refuses, abraham, isaac, divine_promise_line).
% (Missing: voluntary_action fact for submission)

% State D: The cross is ready, but Jesus exercises power to bypass execution
route_traversed(state_jesus_saves_himself, route_to_cross).
instruments_deployed(state_jesus_saves_himself, cross).
parent_child_dynamic(state_jesus_saves_himself, god_the_father, jesus_christ, divine_promise_line).
% (Missing: voluntary_action fact for giving_up_life)
% Context Setup
situation_type(state_abraham_success, genesis_22).
situation_type(state_jesus_success, gospel_crucifixion).

% Data for Abraham Success
route_traversed(state_abraham_success, route_to_moriah).
instruments_deployed(state_abraham_success, knife).
parent_child_dynamic(state_abraham_success, abraham, isaac, divine_promise_line).
voluntary_action(state_abraham_success, submission_to_binding).
sacrifice_identity_declared(state_abraham_success, ram_in_thicket).

% Data for Jesus Success
route_traversed(state_jesus_success, route_to_cross).
instruments_deployed(state_jesus_success, cross).
parent_child_dynamic(state_jesus_success, god_the_father, jesus_christ, divine_promise_line).
voluntary_action(state_jesus_success, giving_up_life).
sacrifice_identity_declared(state_jesus_success, lamb_of_god).
