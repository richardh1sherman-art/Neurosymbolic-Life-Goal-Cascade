import os
import pickle

class SituationNode:
    """An advanced Neuro-Symbolic node featuring terminal leaf memory caching."""
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, preserved_context=None, node_type="test"):
        self.col = col                      
        self.value = value                  
        self.results = results              
        self.tb = tb                        
        self.fb = fb                        
        self.preserved_context = preserved_context  
        self.node_type = node_type          

def dump_compiled_trees(t1_root, t3_root, t4_root):
    """👑 CHOSEN DUMP MODULE VISUALIZER"""
    def print_node(tree, indent=''):
        if tree is None: return
        if tree.node_type == "terminal":
            print(f" 📦 [TERMINAL LEAF] -> Classification Map: {tree.results}")
            if tree.preserved_context:
                print(f"{indent}   💾 Preserved Context Memory Space:")
                for component, features in tree.preserved_context.items():
                    print(f"{indent}     ▪ Orleans Matrix: {component:<15} -> {features}")
        elif tree.node_type == "subroutine_call":
            print(f" 🌀 [CONTAINED_IN NODE TEST]: Query type tree ID '{tree.col}' with target token '{tree.value}'")
            print(indent + "T->", end='')
            print_node(tree.tb, indent + "  ")
            print(indent + "F->", end='')
            print_node(tree.fb, indent + "  ")
        else:
            print(f" 🔍 [NODE CRITERIA SPLIT] -> Feature Index [{tree.col}] == '{tree.value}'?")
            print(indent + "T->", end='')
            print_node(tree.tb, indent + "  ")
            print(indent + "F->", end='')
            print_node(tree.fb, indent + "  ")

    print("\n" + "=" * 85)
    print("📊 DUMP OF COMPILED SITUATION DECISION TREES (NESTED REHEARSAL REGISTRY)")
    print("=" * 85)
    print("\n🌲 [DECISION TREE DUMP]: Type Structure Context -> 'rehearsal_matrix' (Level #3 Firehouse Drills)")
    print_node(t4_root)
    print("=" * 85 + "\n")

def query_and_explain_situation(observation_dict, tree, tree_name="Tree", path_stack=None):
    """👑 OPTION #2 & OPTION #3: CLASSIFICATION LOOKUP & CAUSAL BACK-TRACER"""
    if path_stack is None: path_stack = []
    if tree.node_type == "terminal":
        print(f"\n🎯 [OPTION #2 RESULT]: Classification Outcome on '{tree_name}' -> {list(tree.results.keys())}")
        print(f"🧠 [OPTION #3 REASONING]: Why was this classification reached?")
        for i, step in enumerate(path_stack, 1):
            feat, cond, branch = step  
            print(f"   {i}. Tested [{feat}] -> Criteria met: '{cond}' (Routed to {branch} branch)")
        if tree.preserved_context:
            print("   💾 Retrieved Copied Leaf Context Invariants:")
            print(f"      {tree.preserved_context}")
        return tree.results

    feature_name = tree.col
    target_val = tree.value
    
    if tree.node_type == "subroutine_call":
        if target_val in observation_dict:
            actual_status = observation_dict[target_val]
            if actual_status == "pos":
                path_stack.append((feature_name, f"Subpart '{target_val}' is contained_in positive lower-tier bounds", "TRUE"))
                return query_and_explain_situation(observation_dict, tree.tb, tree_name, path_stack)
            else:
                path_stack.append((feature_name, f"Subpart '{target_val}' failed containment check (status={actual_status})", "FALSE"))
                return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)
        else:
            path_stack.append((feature_name, f"Subpart component '{target_val}' was missing from input vector", "FALSE"))
            return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)
    else:
        if feature_name in observation_dict:
            actual_val = observation_dict[feature_name]
            if actual_val == target_val:
                path_stack.append((feature_name, f"{actual_val} == {target_val}", "TRUE"))
                return query_and_explain_situation(observation_dict, tree.tb, tree_name, path_stack)
            else:
                path_stack.append((feature_name, f"{actual_val} != {target_val}", "FALSE"))
                return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)
        else:
            path_stack.append((feature_name, f"Feature missing inside profile", "FALSE"))
            return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)

def main():
    print("=" * 85)
    print("🚀 RUNNING ONSITE INTERACTIVE REHEARSAL ACTION EXPLORATION SUITE")
    print("=" * 85)
    
    if not os.path.exists("t1_tree.pkl") or not os.path.exists("t4_tree.pkl"):
        print("   ❌ Error: Frozen tree models missing. Please run train_situations.py first!")
        return
    with open("t1_tree.pkl", "rb") as f: t1_tree = pickle.load(f)
    with open("t4_tree.pkl", "rb") as f: t4_tree = pickle.load(f)
    print("   💾 [RESTORED]: 'outing_support' and 'rehearsal_matrix' maps un-pickled from disk context.")

    dump_compiled_trees(t1_tree, None, t4_tree)

    drill_observation_profile = {
        "rehearsal_prop": "pos",
        "water_source": "pos"
    }
    print("=" * 85)
    print("🔬 EXECUTING REHEARSAL ANALOGY QUERY: IS THE TACTICAL DRILL VALID?")
    print("=" * 85)
    print(f"📥 Querying Drill Input Profile -> {drill_observation_profile}")
    query_and_explain_situation(drill_observation_profile, t4_tree, tree_name="rehearsal_matrix")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
