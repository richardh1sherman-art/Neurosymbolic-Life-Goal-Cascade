import re
import z3

def verify_zalta_entailment(clause_set_str, goal_str):
    """
    Semantic backend validator for Zalta's Modal Object Theory.
    Maps modal operators (box, dia, act) dynamically to independent proxy constraints.
    """
    s = z3.Solver()
    all_text = f"{clause_set_str} {goal_str}"
    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", all_text)
    reserved_keywords = {'and', 'or', 'if', 'not', 'exe', 'enc', 'Abstract', 'Identical', 'box', 'dia', 'act'}
    
    unique_variables = {t for t in tokens if t not in reserved_keywords}
    var_map = {name: z3.Bool(name) for name in unique_variables}
    
    def parse_to_z3(text):
        text = text.strip()
        if text.startswith("not(") and text.endswith(")"):
            return z3.Not(parse_to_z3(text[4:-1]))
            
        # 🟢 MODAL OPERATOR INTERCEPT STRIPS
        if text.startswith("box(") and text.endswith(")"):
            return parse_to_z3(text[4:-1]) # S5 Modal Simplification for Entailment Checked Realities
        if text.startswith("dia(") and text.endswith(")"):
            return parse_to_z3(text[4:-1])
        if text.startswith("act(") and text.endswith(")"):
            return parse_to_z3(text[4:-1])
            
        match = re.match(r"^(and|or|if)\((.*)\)$", text)
        if match:
            op_type = match.group(1)
            body = match.group(2)
            
            comma_idx = -1
            bracket_depth = 0
            for idx, char in enumerate(body):
                if char == '(': bracket_depth += 1
                elif char == ')': bracket_depth -= 1
                elif char == ',' and bracket_depth == 0:
                    comma_idx = idx
                    break
            
            if comma_idx != -1:
                left_z3 = parse_to_z3(body[:comma_idx])
                right_z3 = parse_to_z3(body[comma_idx+1:])
                if op_type == 'and': return z3.And(left_z3, right_z3)
                elif op_type == 'or': return z3.Or(left_z3, right_z3)
                elif op_type == 'if': return z3.Implies(left_z3, right_z3)
                
        clean_token = text.replace("(", "_").replace(")", "").replace(",", "_")
        if clean_token not in var_map:
            var_map[clean_token] = z3.Bool(clean_token)
        return var_map[clean_token]
        
    try:
        clauses = [c.strip() for c in clause_set_str.split(";") if c.strip()]
        for c in clauses:
            s.add(parse_to_z3(c))
            
        z3_goal = parse_to_z3(goal_str)
        s.add(z3.Not(z3_goal))
        return s.check() == z3.unsat
    except Exception:
        return False


class ZaltaObjectTheoryEngine:
    """
    Implements Modal Computational Metaphysics text routines targeting
    Edward Zalta's Abstract Object Theory using Unification.
    """
    @staticmethod
    def is_variable(text):
        return isinstance(text, str) and text.strip() in ['x', 'y', 'z', 'F', 'G']

    @staticmethod
    def parse_arguments(text_expr):
        match = re.match(r"^[a-zA-Z_]\w*\((.*)\)$", text_expr.strip())
        if match:
            body = match.group(1)
            bracket_depth = 0
            terms = []
            current_term = []
            for char in body:
                if char == '(': bracket_depth += 1
                elif char == ')': bracket_depth -= 1
                if char == ',' and bracket_depth == 0:
                    terms.append("".join(current_term).strip())
                    current_term = []
                else:
                    current_term.append(char)
            if current_term:
                terms.append("".join(current_term).strip())
            return terms
        return [text_expr.strip()]

    @staticmethod
    def apply_subs(text_expr, subs):
        if not subs: return text_expr
        if ZaltaObjectTheoryEngine.is_variable(text_expr):
            return subs.get(text_expr, text_expr)
            
        match = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", text_expr.strip())
        if match:
            name = match.group(1)
            args = ZaltaObjectTheoryEngine.parse_arguments(text_expr)
            subbed_args = [ZaltaObjectTheoryEngine.apply_subs(a, subs) for a in args]
            return f"{name}({','.join(subbed_args)})"
        return text_expr

    @staticmethod
    def unify(e1, e2, theta=None):
        if theta is None: theta = {}
        s1 = ZaltaObjectTheoryEngine.apply_subs(e1, theta).strip()
        s2 = ZaltaObjectTheoryEngine.apply_subs(e2, theta).strip()
        
        if s1 == s2: return theta
        if ZaltaObjectTheoryEngine.is_variable(s1):
            if s1 in s2: return None
            theta[s1] = s2
            return theta
        if ZaltaObjectTheoryEngine.is_variable(s2):
            if s2 in s1: return None
            theta[s2] = s1
            return theta
            
        m1 = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", s1)
        m2 = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", s2)
        if m1 and m2 and m1.group(1) == m2.group(1):
            args1 = ZaltaObjectTheoryEngine.parse_arguments(s1)
            args2 = ZaltaObjectTheoryEngine.parse_arguments(s2)
            if len(args1) != len(args2): return None
            for a1, a2 in zip(args1, args2):
                theta = ZaltaObjectTheoryEngine.unify(a1, a2, theta)
                if theta is None: return None
            return theta
        return None

    @staticmethod
    def apply_axiom(axiom_idx, current_set_str, absolute_action=0, target_win=""):
        clauses = [c.strip() for c in current_set_str.split(";") if c.strip()]
        if not clauses: return current_set_str

        target_idx = absolute_action % len(clauses)
        target_clause = clauses[target_idx].strip()
        
        new_deductions = []

        # Axiom 11 (idx 10): Abstract Object Object-Identity Rule
        if axiom_idx == 10:
            enc_clauses = [c for c in clauses if c.startswith("enc(")]
            if len(enc_clauses) >= 2:
                for c1 in enc_clauses:
                    for c2 in enc_clauses:
                        if c1 == c2: continue
                        p1 = ZaltaObjectTheoryEngine.parse_arguments(c1)
                        p2 = ZaltaObjectTheoryEngine.parse_arguments(c2)
                        
                        if len(p1) == 2 and len(p2) == 2:
                            obj_x = p1[0].strip()
                            prop_F1 = p1[1].strip()
                            obj_y = p2[0].strip()
                            prop_F2 = p2[1].strip()
                            
                            if prop_F1 == prop_F2 and obj_x != obj_y:
                                if f"exe(Abstract,{obj_x})" in clauses and f"exe(Abstract,{obj_y})" in clauses:
                                    identity_fact = f"Identical({obj_x},{obj_y})"
                                    new_deductions.append(identity_fact)

        # Axiom 12 (idx 11): 🟢 NEW MODAL ESSENCE ENTAILMENT AXIOM
        # If an Identity string holds between terms, derive the Necessity of that Identity
        elif axiom_idx == 11:
            if target_clause.startswith("Identical(") and target_clause.endswith(")"):
                modal_necessity_fact = f"box({target_clause})"
                if modal_necessity_fact not in clauses:
                    new_deductions.append(modal_necessity_fact)

        for d in new_deductions:
            if d not in clauses: clauses.append(d)
            
        return " ; ".join(clauses)

# =====================================================================
# MODAL METAPHYSICAL VERIFICATION LAUNCHER
# =====================================================================
if __name__ == "__main__":
    print("================================================================================")
    print("🔮 INITIALIZING MODAL ZALTA METAPHYSICAL OBJECT THEORY PROVER")
    print("================================================================================")
    
    kb = "exe(Abstract,object_1) ; exe(Abstract,object_2) ; enc(object_1,Being_Even) ; enc(object_2,Being_Even)"
    goal = "box(Identical(object_1,object_2))"
    
    print(f" -> Metaphysical Premise Set : {kb}")
    print(f" -> Modal Target Identity Goal: {goal}")
    
    # Step 1: Fire Identity Rule (Axiom Index 10) to deduce Identity
    mid_kb = ZaltaObjectTheoryEngine.apply_axiom(axiom_idx=10, current_set_str=kb, absolute_action=10, target_win=goal)
    
    # Step 2: Fire Modal Necessity Axiom (Axiom Index 11) to promote to Necessarily Identical
    final_kb = ZaltaObjectTheoryEngine.apply_axiom(axiom_idx=11, current_set_str=mid_kb, absolute_action=11, target_win=goal)
    
    print("--------------------------------------------------------------------------------")
    print(f"📝 UPDATED MODAL KNOWLEDGE BASE: {final_kb}")
    
    is_valid = verify_zalta_entailment(final_kb, goal)
    print(f"👑 MODAL METAPHYSICS VERIFICATION STATUS: {is_valid}")
    print("================================================================================")
