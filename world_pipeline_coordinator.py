import os
import pickle
import math

class WorldLevelNode:
    def __init__(self, is_leaf=False, split_feature=None, split_value=None, classification=None):
        self.split_feature = split_feature    
        self.split_value = split_value        
        self.is_leaf = is_leaf
        self.classification = classification  
        self.tb = None                        
        self.fb = None                        

class ParthoodOntologyTrainer:
    def __init__(self):
        self.model_dir = "/home/rsherman/projects/SMT-ILP/ZeroVRAM/story_intake_directory/pickled_models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 📋 Fully expanded 8-dimensional parthood profiles from your notes
        self.parthood_training_data = [
            {
                "subject": "judith", "syntax": "rescue", "abstract_type": "information_flow", "region": "mt_ateh",
                "event": "judith_falls", "argument": "map_too_old", "action": "rescue_dispatch", "set": "map_trails", "time": "peaked_at_2pm",
                "target": "system_rescue_schema"
            },
            {
                "subject": "moses", "syntax": "saves_people", "abstract_type": "leader_lifecycle", "region": "egypt",
                "event": "burning_bush", "argument": "killing_egyptian", "action": "taken_from_nile", "set": "lost_in_wilderness", "time": "forty_silent_years",
                "target": "sovereign_liberation_schema"
            },
            {
                "subject": "david", "syntax": "unifies_kingdom", "abstract_type": "leader_lifecycle", "region": "jerusalem",
                "event": "defeat_goliath", "argument": "bathsheba_failure", "action": "writes_psalms", "set": "shepherd_flock", "time": "forty_years_king",
                "target": "sovereign_monarchy_schema"
            },
            {
                "subject": "paul", "syntax": "establishes_church", "abstract_type": "apostle_lifecycle", "region": "damascus_road",
                "event": "blinded_by_lightning", "argument": "defense_of_law", "action": "writes_letters", "set": "Gentile_churches", "time": "days_before_execution",
                "target": "ecclesiastical_apostolic_schema"
            },
            {
                "subject": "joseph", "syntax": "preserves_lineage", "abstract_type": "ruler_lifecycle", "region": "egypt",
                "event": "dry_pit_betrayal", "argument": "youthful_pride", "action": "manages_grain", "set": "twelve_sons", "time": "seven_years_famine",
                "target": "sovereign_providence_schema"
            },
            {
                "subject": "gideon", "syntax": "routes_oppressor", "abstract_type": "judge_lifecycle", "region": "midian_camp",
                "event": "fleece_test", "argument": "miraculous_demands", "action": "tears_baal_altar", "set": "three_hundred_men", "time": "forty_years_rest",
                "target": "judge_routing_schema"
            },
            {
                "subject": "peter", "syntax": "shepherds_flock", "abstract_type": "pillar_lifecycle", "region": "sea_of_galilee",
                "event": "walks_on_water", "argument": "trial_night_tears", "action": "cuts_malchus_ear", "set": "inner_circle", "time": "three_hidden_days",
                "target": "ecclesiastical_pastoral_schema"
            }
        ]

    def calculate_entropy(self, targets):
        if not targets: return 0
        counts = {}
        for t in targets: counts[t] = counts.get(t, 0) + 1
        entropy = 0.0
        for count in counts.values():
            p = count / len(targets)
            entropy -= p * math.log2(p)
        return entropy

    def find_best_split(self, data, features):
        base_entropy = self.calculate_entropy([d["target"] for d in data])
        best_gain, best_feat, best_val = -1, None, None
        for f in features:
            values = set(d.get(f, "unknown") for d in data)
            for val in values:
                left = [d for d in data if d.get(f, "unknown") == val]
                right = [d for d in data if d.get(f, "unknown") != val]
                if not left or not right: continue
                gain = base_entropy - ((len(left)/len(data)) * self.calculate_entropy([d["target"] for d in left]) + (len(right)/len(data)) * self.calculate_entropy([d["target"] for d in right]))
                if gain > best_gain:
                    best_gain, best_feat, best_val = gain, f, val
        return best_feat, best_val

    def build_tree(self, data, features, depth=0):
        if not data: return WorldLevelNode(is_leaf=True, classification="empty")
        targets = [d["target"] for d in data]
        if len(set(targets)) == 1: 
            return WorldLevelNode(is_leaf=True, classification=str(targets))
        
        feat, val = self.find_best_split(data, features)
        if feat is None or depth > 6:
            counts = {}
            for t in targets: counts[t] = counts.get(t, 0) + 1
            return WorldLevelNode(is_leaf=True, classification=str(max(counts, key=counts.get)))

        node = WorldLevelNode(split_feature=feat, split_value=val)
        node.tb = self.build_tree([d for d in data if d.get(feat, "unknown") == val], [f for f in features if f != feat], depth + 1)
        node.fb = self.build_tree([d for d in data if d.get(feat, "unknown") != val], [f for f in features if f != feat], depth + 1)
        return node

    def run_training(self):
        print("=" * 95)
        print("🚀 CUSTOM AI PIPELINE: RETRAINING DECISION TREE #6 OVER ALL 8 PARTHOOD COLUMNS")
        print("=" * 95)
        
        # 🚨 EXPANDED FEATURE LIST TO EVALUATE THE ENTIRE ONTOLOGY footprint
        features_list = ["syntax", "abstract_type", "region", "event", "argument", "action", "set", "time"]
        t6_root = self.build_tree(self.parthood_training_data, features_list)
        
        with open(os.path.join(self.model_dir, "level6_parthood_ontology.pkl"), "wb") as f:
            pickle.dump(t6_root, f)
            
        print("🌲 [DUMPING COLLISION-FREE LEVEL 3 PARTHOOD DECISION TREE GEOMETRY]")
        print("-" * 95)
        self.dump_tree(t6_root)
        print("=" * 95 + "\n")

    def dump_tree(self, node, indent="   "):
        if node.is_leaf:
            print(f"{indent}📦 [TERMINAL REPRESENTATION LEAF] ──➔ **{node.classification}**")
            return
        print(f"{indent}🔍 [RELATIONAL LOOKUP]: Checks if parthood category ['{node.split_feature}'] == '{node.split_value}'?")
        print(f"{indent}  ├── True  ──➔", end="")
        self.dump_tree(node.tb, indent + "  │   ")
        print(f"{indent}  └── False ──➔", end="")
        self.dump_tree(node.fb, indent + "      ")

if __name__ == "__main__":
    trainer = ParthoodOntologyTrainer()
    trainer.run_training()
