import os
import sys
import pickle
import subprocess

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

class HierarchicalSituationTrainer:
    """Coordinates situation learning by generating completely self-contained background logic files."""
    def __init__(self, repo_root="."):
        self.repo_root = os.path.abspath(repo_root)
        self.examples_dir = os.path.join(self.repo_root, "Popper-main", "examples")

    def initialize_workspace(self, type_name, bias_str, bk_str, exs_str):
        target_dir = os.path.join(self.examples_dir, type_name)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, "bias.pl"), "w", encoding="utf-8") as f: f.write(bias_str)
        with open(os.path.join(target_dir, "bk.pl"), "w", encoding="utf-8") as f:
            f.write(":- discontiguous infon/5.\n:- discontiguous part_of_selector/3.\n:- discontiguous evaluate_tree/3.\n\n" + bk_str)
        with open(os.path.join(target_dir, "exs.pl"), "w", encoding="utf-8") as f: f.write(exs_str)
        return os.path.abspath(target_dir)

    def execute_induction_pass(self, target_dir):
        engine_script = os.path.join(self.repo_root, "rasiowa_grid_induction.py")
        cmd = [sys.executable, engine_script, os.path.abspath(target_dir)]
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    def run_training_pipeline(self):
        print("=" * 85)
        print("🚀 EXECUTING FOUR-TIER SITUATION TRAINING & DECOUPLED SERIALIZATION")
        print("=" * 85)

        # --- TIER 1: PRIMITIVE DEVICE ATTRIBUTE GROUND REGISTER ---
        print("\n🔹 [TIER 1]: Compiling 'outing_support'")
        support_bias = "head_pred(evaluate_tree,3).\nbody_pred(infon,5).\n"
        support_bk = (
            "infon(flashlight_pos, hardware, state, live, 1).\n"
            "infon(flashlight_dead, hardware, state, live, 0).\n"
            "infon(smoke_detector_pos, hardware, state, live, 1).\n"
            "infon(smoke_detector_dead, hardware, state, live, 0).\n"
            "infon(helicopter_pos, hardware, state, live, 1).\n"
            "infon(helicopter_neg1, hardware, state, live, 0).\n"
            "infon(helicopter_perm, contract, authorization, cleared, 1).\n"
            "infon(hook_and_ladder_perm, contract, authorization, cleared, 1).\n"
            "%% Fire Hydrant Primitive Fact States\n"
            "infon(hydrant_pos, water, pressure, active, 1).\n"
            "infon(hydrant_low_pressure, water, pressure, active, 0).\n"
        )
        support_exs = (
            "pos(evaluate_tree(outing_support, flashlight_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, flashlight_dead, neg)).\n"
            "pos(evaluate_tree(outing_support, smoke_detector_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, smoke_detector_dead, neg)).\n"
            "pos(evaluate_tree(outing_support, hydrant_pos, pos)).\n"
            "neg(evaluate_tree(outing_support, hydrant_low_pressure, neg)).\n"
        )
        support_dir = self.initialize_workspace("outing_support", support_bias, support_bk, support_exs)
        self.execute_induction_pass(support_dir)

        # --- TIER 2: RESCUE NARRATIVE INDEX ---
        print("\n🔹 [TIER 2]: Compiling 'rescue'")
        rescue_bias = "head_pred(rescue_success,1).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_tree,3).\n"
        rescue_bk = (
            "part_of_selector(pos_2nd, judith_hiking_rescue, flashlight_pos).\n"
            "part_of_selector(pos_3rd, judith_hiking_rescue, helicopter_pos).\n\n"
            "infon(flashlight_pos, hardware, state, live, 1).\n"
            "infon(helicopter_pos, hardware, state, live, 1).\n"
            "evaluate_tree(outing_support, flashlight_pos, pos).\n"
            "evaluate_tree(outing_support, helicopter_pos, pos).\n"
        )
        rescue_exs = "pos(rescue_success(judith_hiking_rescue)).\n"
        rescue_dir = self.initialize_workspace("rescue", rescue_bias, rescue_bk, rescue_exs)
        self.execute_induction_pass(rescue_dir)

        # --- TIER 3: NESTED ANALOGY MATRIX ---
        print("\n🔹 [TIER 3]: Compiling 'analogy_matrix'")
        analogy_bias = "head_pred(analogy_verified,1).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_tree,3).\n"
        analogy_bk = (
            "part_of_selector(source_device, alignment_exemplar, flashlight_pos).\n"
            "part_of_selector(target_device, alignment_exemplar, smoke_detector_pos).\n"
            "part_of_selector(source_dispatch, alignment_exemplar, helicopter_perm).\n"
            "part_of_selector(target_dispatch, alignment_exemplar, hook_and_ladder_perm).\n\n"
            "part_of_selector(source_device, broken_alignment_exemplar, flashlight_dead).\n"
            "part_of_selector(target_device, broken_alignment_exemplar, smoke_detector_dead).\n\n"
            "infon(flashlight_pos, hardware, state, live, 1).\n"
            "infon(smoke_detector_pos, hardware, state, live, 1).\n"
            "infon(helicopter_perm, contract, authorization, cleared, 1).\n"
            "infon(hook_and_ladder_perm, contract, authorization, cleared, 1).\n"
            "infon(flashlight_dead, hardware, state, live, 0).\n"
            "infon(smoke_detector_dead, hardware, state, live, 0).\n"
            "evaluate_tree(outing_support, flashlight_pos, pos).\n"
            "evaluate_tree(outing_support, smoke_detector_pos, pos).\n"
            "evaluate_tree(outing_support, helicopter_perm, pos).\n"
            "evaluate_tree(outing_support, hook_and_ladder_perm, pos).\n"
            "evaluate_tree(outing_support, flashlight_dead, neg).\n"
            "evaluate_tree(outing_support, smoke_detector_dead, neg).\n"
        )
        analogy_exs = (
            "pos(analogy_verified(alignment_exemplar)).\n"
            "neg(analogy_verified(broken_alignment_exemplar)).\n"
        )
        analogy_dir = self.initialize_workspace("analogy_matrix", analogy_bias, analogy_bk, analogy_exs)
        self.execute_induction_pass(analogy_dir)

        # --- TIER 4: THE HYDRANT-INTEGRATED REHEARSAL TREE ---
        print("\n🔹 [NEW SITUATION TYPE]: Compiling 'rehearsal_matrix' for Firehouse Drills")
        rehearsal_bias = "head_pred(drill_valid,1).\nbody_pred(part_of_selector,3).\nbody_pred(evaluate_tree,3).\n"
        rehearsal_bk = (
            "%% Mapping rehearsal props and fire hydrant lines into tactical drill metrics\n"
            "part_of_selector(rehearsal_prop, drill_alpha, smoke_detector_pos).\n"
            "part_of_selector(water_source, drill_alpha, hydrant_pos).\n\n"
            "evaluate_tree(outing_support, smoke_detector_pos, pos).\n"
            "evaluate_tree(outing_support, hydrant_pos, pos).\n"
        )
        rehearsal_exs = "pos(drill_valid(drill_alpha)).\n"
        rehearsal_dir = self.initialize_workspace("rehearsal_matrix", rehearsal_bias, rehearsal_bk, rehearsal_exs)
        self.execute_induction_pass(rehearsal_dir)

        print("\n🔹 [PICKLE SERIALIZATION]: Freezing structural type trees to disk...")
        t1_leaf_t = SituationNode(results={"pos": 1}, preserved_context={"primitive_check": "live_or_authorized"}, node_type="terminal")
        t1_leaf_f = SituationNode(results={"neg": 1}, preserved_context={"primitive_check": "hardware_dead"}, node_type="terminal")
        t1_tree = SituationNode(col="hardware_state", value="live_1", tb=t1_leaf_t, fb=t1_leaf_f, node_type="test")

        t3_leaf_t = SituationNode(results={"ISOMORPHIC_ANALOGY_VALID": 1}, preserved_context={"source": "judith_rescue", "target": "kitchen_fire"}, node_type="terminal")
        t3_leaf_f = SituationNode(results={"ANALOGICAL_BROKEN_FAULT": 1}, preserved_context={"source": "hardware_failure", "target": "isolation"}, node_type="terminal")
        t3_node_dispatch = SituationNode(col="outing_support", value="target_dispatch", tb=t3_leaf_t, fb=t3_leaf_f, node_type="subroutine_call")
        t3_node_device = SituationNode(col="outing_support", value="target_device", tb=t3_node_dispatch, fb=t3_leaf_f, node_type="subroutine_call")
        t3_tree = SituationNode(col="outing_support", value="source_device", tb=t3_node_device, fb=t3_leaf_f, node_type="subroutine_call")

        # 👑 UPDATED DYNAMIC REHEARSAL TREE INCORPORATING HYDRANT ROUTING CHECKS
        t4_leaf_t = SituationNode(results={"REHEARSAL_MATCHES_REAL_WORLD": 1}, preserved_context={"drill_type": "tactical_hydrant_charge"}, node_type="terminal")
        t4_node_hydrant = SituationNode(col="outing_support", value="water_source", tb=t4_leaf_t, fb=t3_leaf_f, node_type="subroutine_call")
        t4_tree = SituationNode(col="outing_support", value="rehearsal_prop", tb=t4_node_hydrant, fb=t3_leaf_f, node_type="subroutine_call")

        with open(os.path.join(self.repo_root, "t1_tree.pkl"), "wb") as f: pickle.dump(t1_tree, f)
        with open(os.path.join(self.repo_root, "t3_tree.pkl"), "wb") as f: pickle.dump(t3_tree, f)
        with open(os.path.join(self.repo_root, "t4_tree.pkl"), "wb") as f: pickle.dump(t4_tree, f)
        print("   ✅ [SAVED]: t1, t3, and t4 trees frozen securely to disk storage locations!")
        print("=" * 85 + "\n")

if __name__ == "__main__":
    trainer = HierarchicalSituationTrainer()
    trainer.run_training_pipeline()
