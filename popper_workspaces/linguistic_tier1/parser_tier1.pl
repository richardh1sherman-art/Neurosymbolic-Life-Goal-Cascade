%% =================================================================
%% 🪐 TIER 1 & TIER 3 INTERLOCKING FORESTS OF DECISION TREES
%% Phase Next Core: Integrated SCADA Ontology & CIM Feature Schema
%% References: IEC 61850 Substation Models & Sherman-Gable (1983)
%% =================================================================

:- dynamic scada_class_subsumption/3.
:- dynamic cim_relation_tuple/4.

%% --- ⚡ SCADA TAXONOMY SUBSUMPTION (OWL-Style SubClassOf) ---
% Syntax: scada_class_subsumption(SubClass, SuperClass, SerializationLevel)
scada_class_subsumption(active_power_bus, electrical_node, level2_ontology).
scada_class_subsumption(detrended_telemetry, scada_metric, level1_proprietary).
scada_class_subsumption(synchronized_episode, grid_anomaly, level3_strategy).

%% --- 📊 CIM RELATIONAL PROPERTY INVARIANTS ---
% Syntax: cim_relation_tuple(SourceBus, TargetSubstation, ElectricalProperty, Status)
cim_relation_tuple(bus_alpha_1, substation_1, cross_correlated_load, active_surge).
cim_relation_tuple(bus_beta_2, substation_2, independent_reserve, stable_idle).

%% --- MASTER INTER-TREE DELEGATION CORE ---
part_of(scada_class_subsumption, interlocking_forest, level12_science_invariants).
part_of(cim_relation_tuple, interlocking_forest, level30_subsystem_dispatcher).
