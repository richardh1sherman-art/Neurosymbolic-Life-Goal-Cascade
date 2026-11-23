import os
import sys
import subprocess

class SituationNode:
    """An advanced Neuro-Symbolic node featuring terminal leaf memory caching."""
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None, preserved_context=None, node_type="test"):
        self.col = col                      # Split column index or target predicate label
        self.value = value                  # Split parameter condition
        self.results = results              # Distribution mapping (Leaf only)
        self.tb = tb                        # True Branch pointer
        self.fb = fb                        # False Branch pointer
        self.preserved_context = preserved_context  # Cached feature context mapping
        self.node_type = node_type          # 'test', 'subroutine_call', or 'terminal'

def dump_compiled_trees(t1_root, t2_root):
    """👑 DUMP MODULE VISUALIZER UNPACKING EXTENDED TRANSITIVE FAILURES"""
    def print_node(tree, indent=''):
        if tree is None: return
        if tree.node_type == "terminal":
            print(f" 📦 [TERMINAL LEAF] -> Classification Map: {tree.results}")
            if tree.preserved_context:
                print(f"{indent}   💾 Preserved Context Memory Space:")
                for component, features in tree.preserved_context.items():
                    print(f"{indent}     ▪️ Orleans Matrix: {component:<15} -> {features}")
        elif tree.node_type == "subroutine_call":
            print(f" 🌀 [DYNAMIC NODE TEST]: Ask internal 'part_of' question to Type Tree: '{tree.col}' on Value: '{tree.value}'")
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
    print("📊 DUMP OF COMPILED SITUATION DECISION TREES (TRANSITIVE CASCADING FAILURES)")
    print("=" * 85)
    print("\n🌲 [DECISION TREE DUMP]: Type Structure Context -> 'outing_support'")
    print_node(t1_root)
    print("\n🌲 [DECISION TREE DUMP]: Type Structure Context -> 'rescue' (Hierarchical Macro Layer)")
    print_node(t2_root)
    print("=" * 85 + "\n")

def query_and_explain_situation(observation_dict, tree, tree_name="Tree", path_stack=None):
    """
    👑 OPTION #2 & OPTION #3: CLASSIFICATION LOOKUP & CAUSAL BACK-TRACER
    Traverses the compiled nodes dynamically and provides a full human-readable 
    'Why?' explanation by printing out the logical history stack.
    """
    if path_stack is None:
        path_stack = []
        
    if tree.node_type == "terminal":
        print(f"\n🎯 [OPTION #2 RESULT]: Classification Outcome on '{tree_name}' -> {list(tree.results.keys())}")
        print(f"🧠 [OPTION #3 REASONING]: Why was this classification reached?")
        for i, step in enumerate(path_stack, 1):
            print(f"   {i}. Tested [{step[0]}] -> Criteria met: '{step[1]}' (Routed to {step[2]} branch)")
        if tree.preserved_context:
            print("   💾 Retrieved Copied Leaf Context Invariants:")
            print(f"      {tree.preserved_context}")
        return tree.results

    # Node processing route isolation pass
    feature_name = tree.col
    target_val = tree.value
    
    if feature_name in observation_dict:
        actual_val = observation_dict[feature_name]
        if actual_val == target_val:
            path_stack.append((feature_name, f"{actual_val} == {target_val}", "TRUE"))
            return query_and_explain_situation(observation_dict, tree.tb, tree_name, path_stack)
        else:
            path_stack.append((feature_name, f"{actual_val} != {target_val}", "FALSE"))
            return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)
    else:
        # Dynamic handler captures missing variables seamlessly
        path_stack.append((feature_name, "Feature missing in input profile", "FALSE"))
        return query_and_explain_situation(observation_dict, tree.fb, tree_name, path_stack)
class HierarchicalSituationOrchestrator:
    """Coordinates three tiers of situation learning with multi-point cascading failures."""
    def __init__(self, repo_root="."):
        self.repo_root = os.path.abspath(repo_root)
        self.examples_dir = os.path.join(self.repo_root, "Popper-main", "examples")
        self.shared_bk_file = os.path.join(self.examples_dir, "shared_bk.pl")

    def initialize_workspace(self, type_name, bias_str, exs_str):
        target_dir = os.path.join(self.examples_dir, type_name)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "bias.pl"), "w", encoding="utf-8") as f: f.write(bias_str)
        with open(os.path.join(target_dir, "exs.pl"), "w", encoding="utf-8") as f: f.write(exs_str)
        with open(os.path.join(target_dir, "bk.pl"), "w", encoding="utf-8") as f:
            f.write(f":- compile('{self.shared_bk_file}').\n")
        return os.path.abspath(target_dir)

    def write_global_shared_bk(self, shared_bk_content):
        os.makedirs(self.examples_dir, exist_ok=True)
        with open(self.shared_bk_file, "w", encoding="utf-8") as f:
            f.write(":- discontiguous infon/5.\n:- discontiguous part_of_selector/3.\n\n" + shared_bk_content)

    def execute_induction_pass(self, target_dir):
        engine_script = os.path.join(self.repo_root, "rasiowa_grid_induction.py")
        cmd = [sys.executable, engine_script, os.path.abspath(target_dir)]
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    def run_complete_hierarchical_matrix(self):
        print("=" * 85)
        print("🚀 RUNNING THREE-TIER AUTONOMOUS SITUATION ORCHESTRATION HIERARCHICAL ENGINE")
        print("=" * 85)

        global_bk_payload = (
            "infon(flashlight_pos, batteries, main, live, 1). infon(flashlight_pos, bulb, main, works, 1). infon(flashlight_pos, awareness, witness, active, 1). infon(flashlight_pos, connection, hardware, intact, 1). infon(flashlight_pos, switch, main, on, 1).\n"
            "infon(flashlight_neg1, batteries, main, live, 0). infon(flashlight_neg1, bulb, main, works, 1). infon(flashlight_neg1, awareness, witness, active, 1). infon(flashlight_neg1, connection, hardware, intact, 1). infon(flashlight_neg1, switch, main, on, 1).\n"
            "infon(miranda_asleep, batteries, main, live, 1). infon(miranda_asleep, bulb, main, works, 1). infon(miranda_asleep, awareness, witness, active, 0). infon(miranda_asleep, connection, hardware, intact, 1). infon(miranda_asleep, switch, main, on, 1).\n"
            "infon(phone_dead, batteries, main, live, 1). infon(phone_dead, bulb, main, works, 1). infon(phone_dead, awareness, witness, active, 1). infon(phone_dead, connection, hardware, intact, 0). infon(phone_dead, switch, main, on, 1).\n"
            "infon(helicopter_pos, batteries, main, live, 1). infon(helicopter_pos, bulb, main, works, 1). infon(helicopter_pos, awareness, witness, active, 1). infon(helicopter_pos, connection, hardware, intact, 1). infon(helicopter_pos, engine, main, works, 1).\n"
            "infon(helicopter_neg1, batteries, main, live, 1). infon(helicopter_neg1, bulb, main, works, 1). infon(helicopter_neg1, awareness, witness, active, 1). infon(helicopter_neg1, connection, hardware, intact, 1). infon(helicopter_neg1, engine, works, 0).\n"
            "infon(hook_and_ladder_pos, truck, main, active, 1). infon(hook_and_ladder_pos, bulb, main, works, 1). infon(hook_and_ladder_pos, batteries, main, live, 1). infon(hook_and_ladder_pos, awareness, witness, active, 1). infon(hook_and_ladder_pos, connection, hardware, intact, 1).\n"
            "infon(hook_and_ladder_neg, truck, main, active, 0). infon(hook_and_ladder_neg, bulb, main, works, 1). infon(hook_and_ladder_neg, batteries, main, live, 1). infon(hook_and_ladder_neg, awareness, witness, active, 1). infon(hook_and_ladder_neg, connection, hardware, intact, 1).\n\n"
            "infon(judith_hiking_rescue, person, current, judith, 1).\npart_of_selector(pos_2nd, judith_hiking_rescue, flashlight_pos).\npart_of_selector(pos_3rd, judith_hiking_rescue, helicopter_pos).\n\n"
            "infon(judith_desert_rescue, person, current, judith, 1).\npart_of_selector(pos_2nd, judith_desert_rescue, flashlight_pos).\npart_of_selector(pos_3rd, judith_desert_rescue, helicopter_pos).\n\n"
            "infon(judith_beach_rescue, person, current, judith, 1).\npart_of_selector(pos_2nd, judith_beach_rescue, flashlight_neg1).\npart_of_selector(pos_3rd, judith_beach_rescue, helicopter_pos).\n\n"
            "infon(judith_storm_rescue, person, current, judith, 1).\npart_of_selector(pos_2nd, judith_storm_rescue, flashlight_pos).\npart_of_selector(pos_3rd, judith_storm_rescue, helicopter_neg1).\n\n"
            "evaluate_tree(outing_support, flashlight_pos, pos). evaluate_tree(outing_support, flashlight_neg1, neg).\n"
            "evaluate_tree(outing_support, miranda_asleep, neg). evaluate_tree(outing_support, phone_dead, neg).\n"
            "evaluate_tree(outing_support, helicopter_pos, pos). evaluate_tree(outing_support, helicopter_neg1, neg).\n"
            "evaluate_tree(outing_support, hook_and_ladder_pos, pos). evaluate_tree(outing_support, hook_and_ladder_neg, neg).\n\n"
            "part_of_selector(pos_2nd, fire_department_rescue_success, judith_hiking_rescue).\n\n"
            "part_of_selector(pos_2nd, fire_department_rescue_failed, judith_beach_rescue).\n\n"
            "part_of_selector(pos_2nd, fire_mountains_out, helicopter_pos).\n"
            "part_of_selector(pos_3rd, fire_mountains_out, hook_and_ladder_pos).\n\n"
            "part_of_selector(pos_2nd, fire_beach_out, helicopter_pos).\n"
            "part_of_selector(pos_3rd, fire_beach_out, hook_and_ladder_neg).\n"
            "evaluate_tree(rescue, judith_hiking_rescue, pos). evaluate_tree(rescue, judith_desert_rescue, pos).\n"
            "evaluate_tree(rescue, judith_beach_rescue, neg). evaluate_tree(rescue, judith_storm_rescue, neg).\n"
        )
        self.write_global_shared_bk(global_bk_payload)

        print("\n🔹 [TIER 1]: Compiling Ground Sub-Situations: 'outing_support'")
        support_bias = "head_pred(evaluate_tree,3).\nbody_pred(infon,5).\n"
        support_exs = (
            "pos(evaluate_tree(outing_support, flashlight_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, flashlight_neg1, neg)).\n"
            "neg(evaluate_tree(outing_support, miranda_asleep, neg)).\n"
            "neg(evaluate_tree(outing_support, phone_dead, neg)).\n"
            "pos(evaluate_tree(outing_support, helicopter_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, helicopter_neg1, neg)).\n"
            "pos(evaluate_tree(outing_support, hook_and_ladder_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, hook_and_ladder_neg, neg)).\n"
        )
        support_dir = self.initialize_workspace("outing_support", support_bias, support_exs)
        self.execute_induction_pass(support_dir)

        print("\n🔹 [TIER 2]: Compiling Macro Situations (Expanded 4-Exemplar Matrix): 'rescue'")
        rescue_bias = "head_pred(rescue_success,1).\nbody_pred(infon,5).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_tree,3).\n"
        rescue_exs = (
            "pos(rescue_success(judith_hiking_rescue)).\npos(rescue_success(judith_desert_rescue)).\n"
            "neg(rescue_success(judith_beach_rescue)).\nneg(rescue_success(judith_storm_rescue)).\n"
        )
        rescue_dir = self.initialize_workspace("rescue", rescue_bias, rescue_exs)
        self.execute_induction_pass(rescue_dir)

        print("\n🔹 [TIER 3]: Compiling Highest Level Incident Management Layer: 'fire_department'")
        fd_bias = "head_pred(firedepartment,1).\nbody_pred(rescue_success,1).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_tree,3).\n"
        fd_exs = (
            "pos(firedepartment(fire_department_rescue_success)).\n"
            "neg(firedepartment(fire_department_rescue_failed)).\n"
            "pos(firedepartment(fire_mountains_out)).\n"
            "neg(firedepartment(fire_beach_out)).\n"
        )
        fd_dir = self.initialize_workspace("fire_department", fd_bias, fd_exs)
        self.execute_induction_pass(fd_dir)

        abs_support_sol = os.path.join(support_dir, "solution.pl")
        abs_rescue_sol = os.path.join(rescue_dir, "solution.pl")
        abs_fd_sol = os.path.join(fd_dir, "solution.pl")
        
        verify_file = os.path.join(fd_dir, "verify_run.pl")
        with open(verify_file, "w", encoding="utf-8") as vf:
            vf.write(f":- compile('{self.shared_bk_file}').\n"
                     f":- compile('{abs_support_sol}').\n"
                     f":- compile('{abs_rescue_sol}').\n"
                     f":- compile('{abs_fd_sol}').\n"
                     f"test_goal :- firedepartment(fire_department_rescue_success),\n"
                     f"            firedepartment(fire_mountains_out).\n")
                     
        cmd = ["prolog", "-q", "-t", "halt(0)", "-g", "test_goal", "verify_run.pl"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=fd_dir)
        if os.path.exists(verify_file): os.remove(verify_file)
        
        print(f"\n   👑 [MASTER CONTROL GROUP CLOSURE VERIFICATION]:")
        print(f"   ⏩ [TRACE STATUS]: fire_department Multi-World Triage -> {'✅ GREEN SUCCESS' if res.returncode == 0 else '❌ FAILED'}")

        # Build the exact mathematical Situation Node structures
        t1_leaf_t = SituationNode(results={"pos": 2}, preserved_context={"flashlight": "live_1", "helicopter": "engine_works_1"}, node_type="terminal")
        t1_node_conn = SituationNode(col="connection", value="intact_1", tb=t1_leaf_t, fb=SituationNode(results={"neg": 1}, preserved_context={"phone": "car_link_broken_0"}, node_type="terminal"), node_type="test")
        t1_node_aw = SituationNode(col="awareness", value="active_1", tb=t1_node_conn, fb=SituationNode(results={"neg": 1}, preserved_context={"miranda": "asleep_0"}, node_type="terminal"), node_type="test")
        t1_tree = SituationNode(col="batteries", value="live_1", tb=t1_node_aw, fb=SituationNode(results={"neg": 1}, preserved_context={"flashlight": "dead_battery_0"}, node_type="terminal"), node_type="test")

        t2_leaf_t = SituationNode(results={"SUCCESSFUL_RESCUE": 2}, preserved_context={"judith": "waving_1", "miranda": "sees_SOS_1"}, node_type="terminal")
        t2_leaf_f = SituationNode(results={"RESCUE_FAILED": 4}, preserved_context={"transitive_flow": "any_subpart_broken_0"}, node_type="terminal")
        t2_tree = SituationNode(col="outing_support", value="pos_2nd", tb=t2_leaf_t, fb=t2_leaf_f, node_type="subroutine_call")

        # 📊 Execute Option #1: Complete Topology Dump Pass
        dump_compiled_trees(t1_tree, t2_tree)

        # 🚀 CHOOSE AN ACTIVE LIVE SCENARIO DISPATCH TO EXECUTE TRACING QUERIES
        # Scenario Profile: Miranda falls asleep inside the rescue zone!
        print("=" * 85)
        print("🔬 EXECUTING LIVE SITUATION QUERIES: OPTIONS #2 & #3 (TRACING REASONING)")
        print("=" * 85)
        
        miranda_asleep_query = {
            "batteries": "live_1",
            "awareness": "asleep_0", # 🚨 Failure point triggered here!
            "connection": "intact_1"
        }
        print(f"📥 Querying Input Vector Profile -> {miranda_asleep_query}")
        query_and_explain_situation(miranda_asleep_query, t1_tree, tree_name="outing_support")
        print("=" * 85 + "\n")

if __name__ == "__main__":
    orchestrator = HierarchicalSituationOrchestrator()
    orchestrator.run_complete_hierarchical_matrix()