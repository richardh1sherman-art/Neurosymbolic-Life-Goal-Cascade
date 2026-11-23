import re
import z3

def verify_step_entailment(clause_set_str, goal_str):
    s = z3.Solver()
    
    # ============== 🟢 INFINITE VOCABULARY REGISTRY PASS =============
    all_text = f"{clause_set_str} {goal_str}"
    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", all_text)
    
    # Strictly isolate structural logic operators from variable names
    reserved_keywords = {'and', 'or', 'if', 'not', 'true', 'false', 'step', 'Apply', 'Axiom'}
    unique_variables = {t for t in tokens if t not in reserved_keywords}
    
    # Instantiate Z3 variables on-the-fly inside local memory context
    var_map = {name: z3.Bool(name) for name in unique_variables}
    # =====================================================================
    
    def parse_string_to_z3(text):
        text = text.strip()
        if text.startswith("not(") and text.endswith(")"):
            return z3.Not(parse_string_to_z3(text[4:-1]))
            
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
                left_z3 = parse_string_to_z3(body[:comma_idx])
                right_z3 = parse_string_to_z3(body[comma_idx+1:])
                if op_type == 'and': return z3.And(left_z3, right_z3)
                elif op_type == 'or': return z3.Or(left_z3, right_z3)
                elif op_type == 'if': return z3.Implies(left_z3, right_z3)
                
        return var_map.get(text, z3.BoolVal(False))
        
    try:
        clauses = [c.strip() for c in clause_set_str.split(";") if c.strip()]
        for c in clauses:
            s.add(parse_string_to_z3(c))
            
        z3_goal = parse_string_to_z3(goal_str)
        s.add(z3.Not(z3_goal))
        return s.check() == z3.unsat
    except Exception:
        return False
