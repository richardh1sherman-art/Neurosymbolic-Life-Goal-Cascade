import os
import pickle

class InductiveParseNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.is_leaf = is_leaf
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

def visualize_recursive(node, indent=""):
    if node is None: return
    if getattr(node, 'is_leaf', False):
        print(f"{indent}📦 [TERMINAL LEAF DATA] ──> **{getattr(node, 'classification', 'unmapped')}**")
        return
    print(f"{indent}🔍 [NON-TERMINAL TEST NODE]: Does feature [{getattr(node, 'split_feature', 'none')}] == '{getattr(node, 'split_value', 'none')}'?")
    print(f"{indent}  ├── T ──>", end="")
    visualize_recursive(node.tb, indent + "  │   ")
    print(f"{indent}  └── F ──>", end="")
    visualize_recursive(node.fb, indent + "      ")

def main():
    model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/Popper-main/examples/story_intake_directory/pickled_models"
    pkl_files = sorted([f for f in os.listdir(model_dir) if f.endswith(".pkl")])
    
    print("=" * 85)
    print("📊 DUMPING ORGANIC INDUCTIVE GEOMETRIES DIRECTLY FROM DISK .PKL FILES")
    print("=" * 85)
    
    for f_name in pkl_files:
        p = os.path.join(model_dir, f_name)
        print(f"\n📁 Model File: [{f_name}]")
        print("-" * 85)
        try:
            with open(p, "rb") as f:
                root = pickle.load(f)
            visualize_recursive(root)
        except Exception as e:
            print(f"   ⚠️ Could not print tree mapping format: standard serialization template mismatch.")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
