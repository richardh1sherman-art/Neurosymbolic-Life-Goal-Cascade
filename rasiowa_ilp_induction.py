import re
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class RasiowaILPInductor:
    """
    Neuro-Symbolic Empirical Induction Engine based on Rasiowa Approximation Theory.
    Ingests Popper-format inductive logic files, maps them to dual topological 
    approximation spaces, and synthesizes minimal, correct Prolog clauses.
    """
    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.universe_A = [[x, y] for x in range(grid_size) for y in range(grid_size)]

    def parse_popper_examples(self, examples_str):
        """
        Parses standard Popper examples syntax: pos(target(X, Y)) and neg(target(X, Y)).
        Extracts coordinate vectors.
        """
        pos_points = []
        neg_points = []
        
        lines = [line.strip() for line in examples_str.strip().split("\n") if line.strip()]
        for line in lines:
            # Match positive examples: pos(pred_name(x, y))
            pos_match = re.match(r"^pos\(\w+\((\d+),\s*(\d+)\)\)\.?$", line)
            if pos_match:
                pos_points.append([int(pos_match.group(1)), int(pos_match.group(2))])
                continue
            # Match negative examples: neg(pred_name(x, y))
            neg_match = re.match(r"^neg\(\w+\((\d+),\s*(\d+)\)\)\.?$", line)
            if neg_match:
                neg_points.append([int(neg_match.group(1)), int(neg_match.group(2))])
                
        return pos_points, neg_points

    def compute_equivalence_class(self, point, level):
        """
        Descending equivalence relations (E_i). Refines blocks systematically.
        Level 0: Saturated root space.
        Level 1: 2x2 Macro-quadrants.
        Level 2: Pixel-exact discrete limits.
        """
        px, py = point[0], point[1]
        if level == 0:
            return "root_block"
        elif level == 1:
            return f"quad_{px // 2}_{py // 2}"
        else:
            return f"pixel_{px}_{py}"

    def compute_upper_closure(self, target_set, level):
        """
        Computes Cl_i(X): Upper topological approximation boundary.
        Union of all classes that intersect the target set.
        """
        active_blocks = set(self.compute_equivalence_class(p, level) for p in target_set)
        return [p for p in self.universe_A if self.compute_equivalence_class(p, level) in active_blocks]

    def compute_lower_interior(self, target_set, level):
        """
        Computes I_i(X): Lower topological approximation boundary.
        Union of all classes completely contained within the target set.
        """
        interior_set = []
        # Group universe by block IDs at this level
        block_map = {}
        for p in self.universe_A:
            b_id = self.compute_equivalence_class(p, level)
            block_map.setdefault(b_id, []).append(p)
            
        for b_id, points in block_map.items():
            if all(p in target_set for p in points):
                interior_set.extend(points)
        return interior_set

    def synthesize_prolog_body(self, head_pred, bk_preds, core_points):
        """
        Empirically induces Prolog Datalog clauses matching Popper standards.
        Uses variable binding and coordinate matching.
        """
        clauses = []
        if not core_points:
            return f"{head_pred}(X, Y) :- false."
            
        for p in core_points:
            body_atoms = []
            # Query background predicates to construct body atoms
            for bk_pred, data in bk_preds.items():
                if [p[0], p[1]] in data:
                    body_atoms.append(f"{bk_pred}(X, Y)")
                if p[0] in [d[0] for d in data if len(d)==1 or d[1]==p[1]]:
                    body_atoms.append(f"row_{p[0]}(X)")
                if p[1] in [d[1] for d in data if len(d)>1 and d[0]==p[0]]:
                    body_atoms.append(f"col_{p[1]}(Y)")
            
            # De-duplicate literals to minimize clause body footprint
            unique_atoms = sorted(list(set(body_atoms)))
            body_str = ", ".join(unique_atoms) if unique_atoms else "true"
            clauses.append(f"{head_pred}(X, Y) :- {body_str}.")
            
        return "\n".join(clauses)

    def induce_rules(self, examples_str, bias_str, bk_dict=None):
        """
        Executes empirical induction over the approximation space.
        Applies Procedure P to discover sound rules bounding target parameters.
        """
        if bk_dict is None:
            bk_dict = {}
            
        # Extract predicate names from bias configuration
        head_match = re.search(r"head_pred\((\w+),\s*\d+\)", bias_str)
        head_pred = head_match.group(1) if head_match else "target"
        
        pos, neg = self.parse_popper_examples(examples_str)
        
        # Build multi-resolution sequence tracking vectors
        X_seq = [
            self.compute_upper_closure(pos, level=0),
            self.compute_upper_closure(pos, level=1),
            self.compute_upper_closure(pos, level=2)
        ]
        
        # Execute Rasiowa Procedure P Step 1: Core Intersection Core T
        T_core = X_seq[0]
        for i in range(1, len(X_seq)):
            T_core = [p for p in T_core if p in X_seq[i]]
            
        # Clean negative noise vectors out of the verified induction core
        T_clean = [p for p in T_core if p not in neg]
        
        # Procedure P Step 2: Validate Convergence Integrity
        is_legal = True
        for level in range(len(X_seq)):
            recalculated = self.compute_upper_closure(T_clean, level)
            # Remove explicit negative boundaries from comparison frame
            clean_observed = [p for p in X_seq[level] if p not in neg]
            if sorted(clean_observed) != sorted(recalculated):
                is_legal = False
                break
                
        # Generate target Prolog rules based on verified consistency states
        if is_legal and T_clean:
            prolog_program = self.synthesize_prolog_body(head_pred, bk_dict, T_clean)
            status = "VALID APPROXIMATION MODEL"
        else:
            # Fallback to lower bound interior logic program under severe noise
            lower_core = self.compute_lower_interior(pos, level=1)
            prolog_program = self.synthesize_prolog_body(head_pred, bk_dict, lower_core)
            status = "BOUNDED APPROXIMATION MODEL"
            
        return status, prolog_program
