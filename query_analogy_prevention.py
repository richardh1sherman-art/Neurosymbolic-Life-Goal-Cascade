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
    val = feature_vector.get(node.split_feature, "False")
    if str(val) == str(node.split_value): 
        return evaluate_tree_logic(node.tb, feature_vector)
    return evaluate_tree_logic(node.fb, feature_vector)

model_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models/level7_analogy_inferencing.pkl"

if not os.path.exists(model_path):
    print("🚨 Error: Pickled Level 7 analogy tree model missing.")
else:
    with open(model_path, "rb") as f:
        t7_model = pickle.load(f)
    
    # 📋 SCENARIO: A house fire occurs but the dispatcher is distracted (Action P with NO Permission Q)
    partial_analogy_features = {
        "transmission_failure": "True",
        "mitigation_vector": "True",
        "awareness_lapse": "True",
        "connection_vector": "True",
        "has_permission_q": "False",  # 🚨 Structural breach: Dispatcher fails to pass or receive clearance
        "action_p_occurred": "True"
    }
    
    result = evaluate_tree_logic(t7_model, partial_analogy_features)
    
    print("=" * 95)
    print("🔮 INTERROGATING TIER 3 ANALOGICAL INFERENCING MODEL (TREE #7)")
    print("=" * 95)
    print(f"📥 Query Context ──➔ House Kitchen Fire [Distracted Dispatcher Vector]")
    print(f"Target Feature State ──➔ [has_permission_q == False]")
    print(f"🎯 Structural Classification Result ──➔ **{result}**")
    
    if result == "pragmatic_contract_violation":
        print("⚡ [PROVED]: Tree correctly flags a second-order contract breach. Dispatcher rotation required.")
    else:
        print("❌ [PROVED]: Analogy path failed to capture the pragmatic social constraint constraint.")
    print("=" * 95 + "\n")
