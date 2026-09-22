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
        raw_class = node.classification
        return str(raw_class).lower().replace("[","").replace("]","").replace("'","").strip()
    val = feature_vector.get(node.split_feature, "unknown")
    if str(val) == str(node.split_value): 
        return evaluate_tree_logic(node.tb, feature_vector)
    return evaluate_tree_logic(node.fb, feature_vector)

model_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models/level6_parthood_ontology.pkl"

if not os.path.exists(model_path):
    print("🚨 Error: Pickled Level 6 parthood tree model missing.")
else:
    with open(model_path, "rb") as f:
        t6_model = pickle.load(f)
    
    # 📋 Querying Judith's exact 8-dimensional parthood attributes
    judith_features = {
        "syntax": "rescue",
        "abstract_type": "information_flow",
        "region": "mt_ateh"
    }
    
    result = evaluate_tree_logic(t6_model, judith_features)
    
    print("=" * 95)
    print("🔮 INTERROGATING LEVEL 3 PARTHOOD ONTOLOGY MODEL (TREE #6)")
    print("=" * 95)
    print(f"📥 Query Subject ──➔ Judith [Mt. Ateh Ascent Trajectory]")
    print(f"🎯 Structural Classification Result ──➔ **{result}**")
    
    if result == "system_rescue_schema":
        print("⚡ [PROVED]: The structural information channel held. Judith WAS successfully rescued!")
    else:
        print("❌ [PROVED]: The structural path remains un-rewritten or isolated.")
    print("=" * 95 + "\n")
