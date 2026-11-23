import torch
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RasiowaApproximationEngine:
    """
    Implements Rasiowa's Approximation Space Logic & Procedure P.
    Uses descending equivalence chains over self-similar branch coordinate tracks
    to empirically induct formulas from multi-resolution pixel/tree data.
    """
    def __init__(self, max_level=4):
        self.max_level = max_level
        # FIX: Dynamically auto-generate the 4x4 matrix grid to ensure it is 100% copy-safe!
        self.universe_A = [[x, y] for x in range(4) for y in range(4)]

    def compute_equivalence_class(self, point, level):
        """
        Defines the descending equivalence relations (E_i).
        As level i increases, blocks get smaller (equivalence relations get sharper).
        Level 0: Whole space is 1 block.
        Level 1: 2x2 Macro-blocks.
        Level 2: 1x1 Exact-blocks (Discrete limit).
        """
        px, py = point[0], point[1]
        if level == 0:
            return "root_block"
        elif level == 1:
            bx = px // 2
            by = py // 2
            return f"quad_{bx}_{by}"
        else:
            return f"pixel_{px}_{py}"

    def compute_closure_operation(self, target_set, level):
        """
        Computes Cl_i(X): The union of all equivalence blocks of E_i 
        that contain at least one point belonging to the target set.
        """
        active_blocks = set()
        for point in target_set:
            block_id = self.compute_equivalence_class(point, level)
            active_blocks.add(block_id)
            
        closure_set = []
        for point in self.universe_A:
            block_id = self.compute_equivalence_class(point, level)
            if block_id in active_blocks:
                closure_set.append(point)
        return closure_set

    def run_procedure_p(self, sequence_X):
        """
        Executes Rasiowa's Procedure P to verify if an empirical observation 
        sequence represents a legally sound logical model.
        Inputs: sequence_X (List of closed sets T_i for level 0, 1, 2)
        Output: (Decision boolean, Largest induced core set T, Induced Formula String)
        """
        print("\n[LAUNCHING RASIOWA PROCEDURE P OVER MULTI-RESOLUTION CHANNELS]")
        
        # Step 1: Compute the intersection of all multi-resolution observation fields: T = Intersection(T_i)
        T_intersection = []
        first_set = sequence_X[0]
        
        for point in first_set:
            in_all = True
            for i in range(1, len(sequence_X)):
                if point not in sequence_X[i]:
                    in_all = False
                    break
            if in_all:
                T_intersection.append(point)
                
        print(f"  -> Step 1: Intersection Core T derived with size: {len(T_intersection)} units.")
        print(f"     Intersected Coordinates: {T_intersection}")
        
        # Step 2: Project T backwards through the grids to check if T_i == Cl_i(T)
        is_approximation_sequence = True
        for level in range(len(sequence_X)):
            calculated_closure = self.compute_closure_operation(T_intersection, level)
            
            str_observed = sorted([f"{p[0]},{p[1]}" for p in sequence_X[level]])
            str_calculated = sorted([f"{p[0]},{p[1]}" for p in calculated_closure])
            
            if str_observed != str_calculated:
                print(f"  ❌ ANOMALY DETECTED AT RESOLUTION LEVEL {level}!")
                print(f"     Observed Frame != Recalculated Closure. Noise pattern verified.")
                is_approximation_sequence = False
                break
                
        if is_approximation_sequence:
            print("  👑 INDUCTION VERIFIED: Input sequence matches a true structural reality.")
            atoms = [f"point({p[0]},{p[1]})" for p in T_intersection]
            induced_formula = atoms[0]
            for atom in atoms[1:]:
                induced_formula = f"or({atom},{induced_formula})"
            return True, T_intersection, induced_formula
        else:
            print("  🛑 INDUCTION REJECTED: Sequence contains illegal un-aligned anomalies.")
            return False, [], "false"

if __name__ == "__main__":
    engine = RasiowaApproximationEngine()
    
    # Hidden Reality: An L-shaped physical feature inside our grid
    hidden_reality = [[0, 0], [1, 0], [1, 1]]
    
    # Simulate empirical observations T_i gathered across three separate grid levels
    T0 = engine.compute_closure_operation(hidden_reality, level=0) # Coarse (level 0)
    T1 = engine.compute_closure_operation(hidden_reality, level=1) # Macro-quadrant (level 1)
    T2 = engine.compute_closure_operation(hidden_reality, level=2) # Exact sharp pixels (level 2)
    
    empirical_sequence = [T0, T1, T2]
    
    success, core_set, logic_strand = engine.run_procedure_p(empirical_sequence)
    
    print("--------------------------------------------------------------------------------")
    print(f"🔮 INDUCTION RESULTS SUCCESS FLAG: {success}")
    print(f"📝 INDUCED COMPACT LOGICAL FORMULA: {logic_strand}")
    print("================================================================================")
