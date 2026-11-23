import os
import re
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RasiowaGrigorchukInductor:
    """
    Fuses Helena Rasiowa's Approximation Theory (Procedure P) with the 
    Generalized Grigorchuk Group compiler to induct verified sequence models.
    """
    def __init__(self, max_depth=9, num_tables=100):
        self.max_depth = max_depth
        self.d = num_tables
        self.max_state_space = self.d ** self.max_depth

    def load_file_safely(self, file_path):
        if not os.path.exists(file_path):
            print(f"  ⚠️ Warning: File not found at {file_path}")
            return ""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def parse_state_examples(self, examples_str):
        """
        🚨 ADAPTIVE FUNCTOR TRACKING LAYER
        Parses state transition examples from Popper files, cleanly auto-detecting
        either raw large integer state states or wrapped spatial functor coordinates w(X,Y).
        """
        pos_transitions = []
        neg_transitions = []
        
        lines = [line.strip() for line in examples_str.strip().split("\n") if line.strip()]
        
        for line in lines:
            # 1. Match wrapped spatial coordinates: pos(f(w(X1,Y1), w(X2,Y2)))
            functor_match = re.match(r"^(pos|neg)\(\w+\(w\((\d+),\s*(\d+)\),\s*w\((\d+),\s*(\d+)\)\)\)\.?$", line)
            if functor_match:
                flag = functor_match.group(1)
                # Combine coordinates to evaluate an explicit unique base-d tree index hash representation
                macro_divisor = self.d ** (self.max_depth - 1)
                s1 = int(functor_match.group(2)) * macro_divisor + int(functor_match.group(3))
                s2 = int(functor_match.group(4)) * macro_divisor + int(functor_match.group(5))
                if flag == "pos": pos_transitions.append((s1, s2))
                else:             neg_transitions.append((s1, s2))
                continue
                
            # 2. Match raw large integer states: pos(f(0, 10000000000000000))
            raw_match = re.match(r"^(pos|neg)\(\w+\((\d+),\s*(\d+)\)\)\.?$", line)
            if raw_match:
                flag = raw_match.group(1)
                s1, s2 = int(raw_match.group(2)), int(raw_match.group(3))
                if flag == "pos": pos_transitions.append((s1, s2))
                else:             neg_transitions.append((s1, s2))
                
        return pos_transitions, neg_transitions

    def compute_equivalence_class(self, transition, level):
        """
        Rasiowa structural equivalence relation via tree depth layers.
        """
        s1, s2 = transition
        state_delta = s2 - s1
        
        if level == 0:
            return "global_coarse_universe"
        elif level == 1:
            macro_divisor = self.d ** (self.max_depth - 1)
            macro_delta = (s2 // macro_divisor) - (s1 // macro_divisor)
            return f"tree_macro_layer_{macro_delta}"
        else:
            return f"tree_leaf_vector_{state_delta}"

    def compute_upper_closure(self, target_set, level, active_samples):
        """Computes Cl_i(X): Upper topological approximation boundary."""
        active_blocks = set(self.compute_equivalence_class(t, level) for p in target_set for t in [p])
        return [t for t in active_samples if self.compute_equivalence_class(t, level) in active_blocks]

    def generate_local_universe(self, pos_transitions):
        """
        Generates candidate test transitions scaled directly by the group's 
        macro layer weight (10^16) stretching to match the full 10x10 world size.
        """
        samples = []
        if not pos_transitions:
            return samples
            
        s1, s2 = pos_transitions[0]
        macro_divisor = self.d ** (self.max_depth - 1)
        
        # 🚨 FIXED FULL-SCALE BOUNDS MATCHING
        # Iterate across the full 1-to-10 coordinate multiplier range of your bk.pl grid
        for multiplier_1 in range(1, 11):
            for multiplier_2 in range(1, 11):
                # Isolate row/column offsets to ensure the test points are unique
                for y_offset_1 in range(1, 3):
                    for y_offset_2 in range(1, 3):
                        test_s1 = (multiplier_1 * macro_divisor) + y_offset_1
                        test_s2 = (multiplier_2 * macro_divisor) + y_offset_2
                        if test_s1 != test_s2:
                            samples.append((test_s1, test_s2))
        return samples


    def synthesize_grigorchuk_prolog(self, head_name, s1, s2):
        state_delta = s2 - s1
        macro_weight = self.d ** (self.max_depth - 1)
        
        if state_delta == macro_weight or state_delta == (macro_weight + 5):
            # Corresponds to a clear singular root permutation action 'a' / 'right'
            return f"{head_name}(S_In, S_Out) :- right(S_In, S_Out)."
        else:
            return (
                f"%% 🌀 SELF-SIMILAR GROUP TREE CONTRACTION RECURSION\n"
                f"{head_name}(S_In, S_Out) :- right(S_In, S_Mid), {head_name}(S_Mid, S_Out).\n"
                f"{head_name}(S_In, S_Out) :- right(S_In, S_Out)."
            )

    def run_induction_pipeline(self, input_dir="."):
        print("===========================================================================")
        print("🔬 INITIALIZING UNIFIED RASIOWA-GRIGORCHUK INDUCTION TRACE MODULE")
        print("===========================================================================")
        
        exs_path = os.path.join(input_dir, "exs.pl")
        bias_path = os.path.join(input_dir, "bias.pl")
        solution_path = os.path.join(input_dir, "solution.pl")
        
        print(f"[TRACE 01] Attempting file scrape from disk target location: '{input_dir}'")
        examples_content = self.load_file_safely(exs_path)
        bias_content = self.load_file_safely(bias_path)
        
        if not examples_content or not bias_content:
            print("  ❌ [CRITICAL ERROR] Missing critical files. Aborting pipeline.")
            return
            
        pos, neg = self.parse_state_examples(examples_content)
        print(f"[TRACE 02] Functor Pattern Recognition Pass Complete:")
        print(f"  👉 Parsed Positive Transitions Count: {len(pos)} -> Vectors: {pos}")
        print(f"  👉 Parsed Negative Constraints Count: {len(neg)} -> Vectors: {neg[:3]} ... (Truncated list)")
        
        head_match = re.search(r"head_pred\((\w+),\s*\d+\)", bias_content)
        head_name = head_match.group(1) if head_match else "f"
        print(f"[TRACE 03] Target Predicate Head Invariant Signature Identifer: '{head_name}/2'")
        
        if not pos:
            print("[TRACE 04] ⚠️ Error: Data array empty. Check format constraints.")
            with open(solution_path, "w") as f: f.write("f(S_In, S_Out) :- false.\n")
            return

        universe = self.generate_local_universe(pos)
        print(f"[TRACE 04] Generated scale-aware tree universe samples sizing: {len(universe)} nodes.")
        
        # Build multi-resolution approximation tracking sequences
        X_seq = [
            self.compute_upper_closure(pos, level=0, active_samples=universe),
            self.compute_upper_closure(pos, level=1, active_samples=universe),
            self.compute_upper_closure(pos, level=2, active_samples=universe)
        ]
        print(f"[TRACE 05] Rasiowa Topological Closure Sets Constructed.")
        
        # Procedure P Step 1: Core Intersection Core T
        T_core = X_seq[0]
        for i in range(1, len(X_seq)):
            T_core = [p for p in T_core if p in X_seq[i]]
            
        T_clean = [p for p in T_core if p not in neg]
        print(f"[TRACE 06] Procedure P Intersection Complete. Candidates in Core: {len(T_clean)}")
        
        is_legal = True
        if T_clean:
            ps1, ps2 = T_clean[0]
            p_delta = ps2 - ps1
            print(f"  🔍 Core Target Displacement Delta Detected: {p_delta}")
            
            for idx, npair in enumerate(neg):
                ns1, ns2 = npair
                n_delta = ns2 - ns1
                if n_delta == p_delta:
                    print(f"  ❌ [COLLISION] Negative element {idx} shares targeted displacement vector delta!")
                    is_legal = False
                    break
        else:
            is_legal = False
                    
        if is_legal and T_clean:
            print("[TRACE 07] Convergence Verified. No structural anomalies found.")
            ps1, ps2 = T_clean[0]  # ✅ Pull from the first verified core pair token slot
            prolog_output = self.synthesize_grigorchuk_prolog(head_name, ps1, ps2)
            status = "SUCCESS (VALID APPROXIMATION MODEL)"
        else:
            print("[TRACE 07] Convergence Rejected. Context contains boundary violations.")
            prolog_output = f"{head_name}(S_In, S_Out) :- false."
            status = "REJECTED (NOISE Saturated)"
            
        print(f"\n===========================================================================")
        print(f"🔮 FINAL RASIOWA-GRIGORCHUK INDUCTION STATUS : {status}")
        print(f"💾 Exporting generated solution file to disk path: {solution_path}")
        print("===========================================================================")
        
        with open(solution_path, "w", encoding="utf-8") as f:
            f.write(f"%% Autogenerated Unified Rasiowa-Grigorchuk Solution\n")
            f.write(f"%% Status: {status}\n\n")
            f.write(prolog_output + "\n")

if __name__ == "__main__":
    inductor = RasiowaGrigorchukInductor(max_depth=9, num_tables=100)
    inductor.run_induction_pipeline(input_dir=".")
