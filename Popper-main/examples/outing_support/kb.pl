%% ===============================================================
%% 🌀 TIER 2 BACKGROUND KNOWLEDGE: UNIT CONTAINER ENVELOPES (□ LAWS)
%% ===============================================================
:- discontiguous component_links/2.

%% Zalta Parthood Operator: s <| s' <==> Any property encoded in s is in s'
situation_part(SubComponent, MasterEnvelope) :- 
    component_links(SubComponent, MasterEnvelope).
