import os
import pickle

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

def evaluate_tree_logic(node, feature_vector):
    if node is None: return "unknown"
    if node.is_leaf: 
        return str(node.classification).lower().strip()
    val = feature_vector.get(node.split_feature, "unknown")
    if str(val) == str(node.split_value): 
        return evaluate_tree_logic(node.tb, feature_vector)
    return evaluate_tree_logic(node.fb, feature_vector)

model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"

with open(os.path.join(model_dir, "level8_graph_topologies.pkl"), "rb") as f: t8 = pickle.load(f)
with open(os.path.join(model_dir, "level9_fallacy_patterns.pkl"), "rb") as f: t9 = pickle.load(f)

print("=" * 95)
print("🔮 INTERROGATING DUAL-REPRESENTATION TRIANGULATION FIELDS")
print("=" * 95)

# Query 1: Evaluating the sovereign dynamic growth graph
moses_graph_query = {"topology": "cyclic_mesh", "logic_property": "dynamic_growth"}
res_graph = evaluate_tree_logic(t8, moses_graph_query)
print(f"📥 Query Target ──➔ Moses Microscopic Narrative Topology Expansion")
print(f"🎯 Topological Classification Result ──➔ **{res_graph}**")
print("-" * 95)

# Query 2: Evaluating the unquoted authority error
corona_fallacy_query = {"pattern": "unknown", "authority_error": "True"}
res_fallacy = evaluate_tree_logic(t9, corona_fallacy_query)
print(f"📥 Query Target ──➔ Coronavirus Symptom Fallacy Assertion")
print(f"🎯 Fallacy Classification Result     ──➔ **{res_fallacy}**")
print("=" * 95 + "\n")
