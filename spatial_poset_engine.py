import re

class SpatialPosetLogicEngine:
    """
    Implements a Relational Spatial Constraint Prover.
    Applies Rasiowa poset propagation across geometric tokens (inside, left_of)
    using First-Order Unification rules.
    """
    @staticmethod
    def is_variable(text):
        return isinstance(text, str) and text.strip() in ['A', 'B', 'C', 'x', 'y']

    @staticmethod
    def parse_args(literal_str):
        match = re.search(r"\((.*)\)", literal_str.strip())
        if match:
            return [x.strip() for x in match.group(1).split(",")]
        return []

    @staticmethod
    def unify_atoms(e1, e2):
        """ Robinson unification proxy optimized for spatial relational nodes """
        a1 = SpatialPosetLogicEngine.parse_args(e1)
        a2 = SpatialPosetLogicEngine.parse_args(e2)
        
        if len(a1) < 2 or len(a2) < 2: return None
        
        # Unify center-link mappings (e.g., inside(A, B) and inside(B, C))
        if a1[1] == a2[0]:
            return {'pivot': a1[1], 'left': a1[0], 'right': a2[1]}
        return None

    @staticmethod
    def apply_spatial_lattice_axiom(axiom_idx, current_set_str):
        """
        Symmetric group action handler that propagates relational spatial transitivity.
        """
        clauses = [c.strip() for c in current_set_str.split(";") if c.strip()]
        new_deductions = []

        # Axiom 12 (idx 11): Transitive Spatial Inclusion Propagator
        if axiom_idx == 11:
            inside_clauses = [c for c in clauses if c.startswith("inside(")]
            if len(inside_clauses) >= 2:
                for c1 in inside_clauses:
                    for c2 in inside_clauses:
                        if c1 == c2: continue
                        
                        mgu = SpatialPosetLogicEngine.unify_atoms(c1, c2)
                        if mgu is not None:
                            # Propagate: inside(A,B) and inside(B,C) => inside(A,C)
                            derived_fact = f"inside({mgu['left']},{mgu['right']})"
                            if derived_fact not in clauses:
                                new_deductions.append(derived_fact)
                                
        # Axiom 11 (idx 10): Directional Poset Propagator 
        elif axiom_idx == 10:
            left_clauses = [c for c in clauses if c.startswith("left_of(")]
            if len(left_clauses) >= 2:
                for c1 in left_clauses:
                    for c2 in left_clauses:
                        if c1 == c2: continue
                        mgu = SpatialPosetLogicEngine.unify_atoms(c1, c2)
                        if mgu is not None:
                            # Propagate: left_of(A,B) and left_of(B,C) => left_of(A,C)
                            derived_fact = f"left_of({mgu['left']},{mgu['right']})"
                            if derived_fact not in clauses:
                                new_deductions.append(derived_fact)

        for d in new_deductions:
            if d not in clauses: clauses.append(d)
            
        return " ; ".join(clauses)

# =====================================================================
# SPATIAL RELATIONAL LAUNCHER
# =====================================================================
if __name__ == "__main__":
    print("================================================================================")
    print("🔮 INITIALIZING RELATIONAL SPATIAL POSET THEOREM PROVER")
    print("================================================================================")
    
    # Scene Graph Premise Layout:
    # Bounding box 'block_A' is inside 'block_B'
    # Bounding box 'block_B' is inside 'container_C'
    spatial_knowledge_base = "inside(block_A,block_B) ; inside(block_B,container_C) ; left_of(obj_1,obj_2) ; left_of(obj_2,obj_3)"
    target_goal = "inside(block_A,container_C)"
    
    print(f" -> Initial Scene Graph : {spatial_knowledge_base}")
    print(f" -> Spatial Target Goal : {target_goal}")
    
    # Fire Spatial Lattice Transitivity (Axiom Index 11)
    updated_space = SpatialPosetLogicEngine.apply_spatial_lattice_axiom(
        axiom_idx=11, 
        current_set_str=spatial_knowledge_base
    )
    
    # Fire Spatial Directional Left-Of Chain (Axiom Index 10)
    final_space = SpatialPosetLogicEngine.apply_spatial_lattice_axiom(
        axiom_idx=10, 
        current_set_str=updated_space
    )
    
    print("--------------------------------------------------------------------------------")
    print(f"📝 UPDATED TOPOLOGICAL SCENE GRAPH: {final_space}")
    
    is_contained = target_goal in [c.strip() for c in final_space.split(";")]
    print(f"👑 TOPOLOGICAL INHERITANCE INVARIANT SATISFIED: {is_contained}")
    print("================================================================================")
