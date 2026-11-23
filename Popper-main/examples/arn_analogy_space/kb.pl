%% ===============================================================
%% 🌀 TIER 4 BACKGROUND KNOWLEDGE: ARN ANALOGY SPACE (□ LAWS)
%% ===============================================================
:- discontiguous shared_invariant/3.

%% Cross-domain analogies hold if a 1:1 structural graph minor invariant matches
isomorphic_analogy(SourceStory, DestStory) :-
    shared_invariant(SourceStory, DestStory, queue_routing_invariant).
isomorphic_analogy(SourceStory, DestStory) :-
    shared_invariant(SourceStory, DestStory, topological_minor_transform).
