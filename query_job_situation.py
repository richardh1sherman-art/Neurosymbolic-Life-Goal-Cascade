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
        return node.classification
    val = feature_vector.get(node.split_feature, "False")
    if str(val) == str(node.split_value): 
        return evaluate_tree_logic(node.tb, feature_vector)
    return evaluate_tree_logic(node.fb, feature_vector)

# Path settings matching your plural workspace drive layouts
model_path = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models/level5_plan_synthesis.pkl"

if not os.path.exists(model_path):
    print("🚨 Error: Pickled Level 5 tree model missing. Run the training coordinator first.")
else:
    with open(model_path, "rb") as f:
        t5_model = pickle.load(f)
    
    # 📋 Your custom real-world query feature profile
    user_features = {
        "difficulty": "True",
        "effort": "True",
        "reward": "False",
        "grief": "False",
        "rejection": "False",
        "stagnate": "False"
    }
    
    result = evaluate_tree_logic(t5_model, user_features)
    
    print("=" * 95)
    print("🔮 INTERROGATING LEVEL 3 SITUATIONAL SCHEMA FOREST MODEL")
    print("=" * 95)
    print(f"📥 Active Query Context ──➔ [High Effort + No Reward]")
    print(f"🎯 Terminal Node Classification Result ──➔ **{result}**")
    print("=" * 95 + "\n")
