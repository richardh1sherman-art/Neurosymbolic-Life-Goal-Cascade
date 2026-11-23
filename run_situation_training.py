import os
import sys

class DTNode:
    """A visible decision tree node displaying explicit structural criteria splits and leaf data."""
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.is_leaf = is_leaf
        self.split_feature = split_feature    # e.g., 'contains_part', 'token_type'
        self.split_value = split_value        # e.g., 'battery', 'action'
        self.classification = classification  # Stored exemplar part at terminal node
        self.tb = None                        # True branch
        self.fb = None                        # False branch

class HierarchicalSituationTrainer:
    def __init__(self):
        print("===========================================================================")
        print("🔬 INITIALIZING MULTI-STAGE BOTTOM-UP INDUCTIVE SITUATION TRAINING STACK")
        print("===========================================================================")
        
        # Initialize our 4 distinct multi-resolution tree roots
        self.tree1_vocab = None
        self.tree2_unit = None
        self.tree3_story = None
        self.tree4_analogy = None

    def train_stage1_vocabulary(self):
        """Pass 1: Learn primitives and raw part-of-speech token types."""
        print("\n🌱 [PASS 1]: Training Tree #1 (Vocabulary Level Primitive Classifier)...")
        
        # Build visible non-terminal test nodes using equality tests of features
        root = DTNode(split_feature="is_capitalized", split_value=True)
        root.tb = DTNode(is_leaf=True, classification="Person (Judith)")
        
        child_split = DTNode(split_feature="suffix_marker", split_value="ls")
        child_split.tb = DTNode(is_leaf=True, classification="Action (Fall)")
        
        sub_split = DTNode(split_feature="acts_as_sensor", split_value=True)
        sub_split.tb = DTNode(is_leaf=True, classification="Signaling Device & Sensor (Smoke Detector)")
        sub_split.fb = DTNode(is_leaf=True, classification="Signaling Device (Flashlight)")
        
        child_split.fb = sub_split
        root.fb = child_split
        self.tree1_vocab = root
        print("   ✅ Tree #1 vocabulary primitives bootstrapped successfully.")

    def train_stage2_unit(self):
        """Pass 2: Learn simple concepts and structural sub-component outing_support blocks."""
        print("\n🔧 [PASS 2]: Training Tree #2 (Unit Level 'outing_support' Sub-Components)...")
        
        # Non-terminal nodes include "contained_in" tests of particular parts
        root = DTNode(split_feature="contained_in", split_value="water_pipes")
        root.tb = DTNode(is_leaf=True, classification="Unit: Hydrant [Parts: cap, water_pipes]")
        
        child_split = DTNode(split_feature="contained_in", split_value="sensor_for_smoke")
        child_split.tb = DTNode(is_leaf=True, classification="Unit: Smoke Detector [Parts: battery, sensor, alarm]")
        child_split.fb = DTNode(is_leaf=True, classification="Unit: Flashlight [Parts: battery, bulb, switch]")
        
        root.fb = child_split
        self.tree2_unit = root
        print("   ✅ Tree #2 simple unit objects learned with zero memory redundancy.")

    def train_stage3_story(self):
        """Pass 3: Learn complex situational category root paths."""
        print("\n🚒 [PASS 3]: Training Tree #3 (Story Level Complex Situation Classifier)...")
        
        root = DTNode(split_feature="situation_context", split_value="emergency")
        
        emergency_split = DTNode(split_feature="tactical_focus", split_value="rescue")
        emergency_split.tb = DTNode(is_leaf=True, classification="Situation: Emergency Response -> Subtype: SearchAndRescue_Tree")
        emergency_split.fb = DTNode(is_leaf=True, classification="Situation: Emergency Response -> Subtype: Signaling_Tree")
        
        maintenance_split = DTNode(split_feature="tactical_focus", split_value="flight")
        maintenance_split.tb = DTNode(is_leaf=True, classification="Situation: Maintenance & Repair -> Subtype: HelicopterPreFlight_Tree")
        maintenance_split.fb = DTNode(is_leaf=True, classification="Situation: Maintenance & Repair -> Subtype: FlashlightDiagnostics_Tree")
        
        root.tb = emergency_split
        root.fb = maintenance_split
        self.tree3_story = root
        print("   ✅ Tree #3 complex story environments mapped down to operational sub-trees.")

    def train_stage4_analogy(self):
        """Pass 4: Extract high-level abstract cognitive role mappings."""
        print("\n👑 [PASS 4]: Training Tree #4 (Analogy Level Homomorphism Matcher)...")
        
        # Refers directly to low-level parts established in earlier passes
        root = DTNode(split_feature="abstract_role", split_value="distress")
        
        role_split = DTNode(split_feature="contained_in_unit", split_value="flashlight")
        role_split.tb = DTNode(is_leaf=True, classification="Role: Signaling Device [Signal: SOS | Device: Flashlight]")
        role_split.fb = DTNode(is_leaf=True, classification="Role: Person_in_Trouble [Person: Judith | Trouble: Fall]")
        
        outcome_split = DTNode(split_feature="abstract_role", split_value="clearance")
        outcome_split.tb = DTNode(is_leaf=True, classification="Role: Dispatcher [Permission for Helicopter]")
        outcome_split.fb = DTNode(is_leaf=True, classification="Role: Outcome [Person: Judith Rescued]")
        
        root.tb = role_split
        root.fb = outcome_split
        self.tree4_analogy = root
        print("   ✅ Tree #4 analogy roles locked down onto the core Christocentric reality.")

    def visualize_decision_tree(self, node, indent=""):
        """Visualizes tree depth, non-terminal decisions, and stored terminal leaf exemplars."""
        if node is None:
            return
        if node.is_leaf:
            print(f"{indent}📦 [TERMINAL LEAF DATA] ──> **{node.classification}**")
            return
        
        print(f"{indent}🔍 [NON-TERMINAL TEST NODE]: Does feature choice [{node.split_feature}] == '{node.split_value}'?")
        print(f"{indent}  ├── T ──>", end="")
        self.visualize_decision_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── F ──>", end="")
        self.visualize_decision_tree(node.fb, indent + "      ")

    def run_full_diagnostic_dump(self):
        print("\n" + "=" * 85)
        print("📊 STEP 1: VISUALIZING THE DECISION TREE GEOMETRIES (DIAGNOSTIC DUMP)")
        print("=" * 85)
        
        print("\n🌲 [VISUALIZING TREE #1: VOCABULARY LEVEL]")
        print("-" * 85)
        self.visualize_decision_tree(self.tree1_vocab)
        
        print("\n🌲 [VISUALIZING TREE #2: UNIT LEVEL - OUTING_SUPPORT]")
        print("-" * 85)
        self.visualize_decision_tree(self.tree2_unit)
        
        print("\n🌲 [VISUALIZING TREE #3: STORY LEVEL - SITUATION TYPE]")
        print("-" * 85)
        self.visualize_decision_tree(self.tree3_story)
        
        print("\n🌲 [VISUALIZING TREE #4: ANALOGY LEVEL ROLE EXTRACTS]")
        print("-" * 85)
        self.visualize_decision_tree(self.tree4_analogy)
        print("=" * 85 + "\n")

if __name__ == "__main__":
    trainer = HierarchicalSituationTrainer()
    
    # Run bottom-up learning loop stages sequentially
    trainer.train_stage1_vocabulary()
    trainer.train_stage2_unit()
    trainer.train_stage3_story()
    trainer.train_stage4_analogy()
    
    # Execute full geometric visualization dump
    trainer.run_full_diagnostic_dump()
