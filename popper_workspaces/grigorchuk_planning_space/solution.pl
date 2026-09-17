%% Target Verified Logic Rules for Edge Contraction Healing
path_resolved(X) :- contracted_nodes(X, secondary_failover_vertex).
