import re
import z3

def verify_step_entailment(clause_set_str, goal_str):
    """
    Dynamically tracks both atomic propositional tokens and deep functional 
    First-Order logic structures using an on-the-fly Z3 variable and function mapper.
    """
    s = z3.Solver()
    all_text = f"{clause_set_str} {goal_str}"
    
    Universe = z3.DeclareSort('Universe')
    pred_names = set(re.findall(r"\b([A-Z][a-zA-Z0-9_]*)\b", all_text))
    token_names = set(re.findall(r"\b([a-z_][a-zA-Z0-9_]*)\b", all_text))
    
    reserved_keywords = {'and', 'or', 'if', 'iff', 'not', 'forall', 'exists', 'false', 'true'}
    ground_atoms = {t for t in token_names if t not in reserved_keywords and t not in ['x', 'y', 'z', 'w']}
    
    z3_functions = {name: z3.Function(name, Universe, z3.BoolSort()) for name in pred_names}
    z3_constants = {name: z3.Const(name, Universe) for name in ground_atoms}
    z3_propositional = {}

    def parse_to_z3(text, bound_vars=None):
        if bound_vars is None: bound_vars = {}
        text = text.strip()
        if not text: return None

        if text.lower() == "false": return z3.BoolVal(False)
        if text.lower() == "true": return z3.BoolVal(True)

        if text.startswith("not(") and text.endswith(")"):
            inner = parse_to_z3(text[4:-1], bound_vars)
            return z3.Not(inner) if inner is not None else None

        if text.startswith("forall(") and text.endswith(")"):
            body = text[7:-1]
            comma_idx = body.find(",")
            var_name = body[:comma_idx].strip()
            matrix_str = body[comma_idx+1:].strip()
            z3_v = z3.Const(var_name, Universe)
            extended_vars = bound_vars.copy()
            extended_vars[var_name] = z3_v
            matrix_z3 = parse_to_z3(matrix_str, extended_vars)
            return z3.ForAll([z3_v], matrix_z3) if matrix_z3 is not None else None

        if text.startswith("exists(") and text.endswith(")"):
            body = text[7:-1]
            comma_idx = body.find(",")
            var_name = body[:comma_idx].strip()
            matrix_str = body[comma_idx+1:].strip()
            z3_v = z3.Const(var_name, Universe)
            extended_vars = bound_vars.copy()
            extended_vars[var_name] = z3_v
            matrix_z3 = parse_to_z3(matrix_str, extended_vars)
            return z3.Exists([z3_v], matrix_z3) if matrix_z3 is not None else None

        match = re.match(r"^(and|or|if|iff)\((.*)\)$", text)
        if match:
            op_type, body = match.group(1), match.group(2)
            comma_idx = -1
            bracket_depth = 0
            for idx, char in enumerate(body):
                if char == '(': bracket_depth += 1
                elif char == ')': bracket_depth -= 1
                elif char == ',' and bracket_depth == 0:
                    comma_idx = idx
                    break
            if comma_idx != -1:
                left_z3 = parse_to_z3(body[:comma_idx], bound_vars)
                right_z3 = parse_to_z3(body[comma_idx+1:], bound_vars)
                if left_z3 is not None and right_z3 is not None:
                    if op_type == 'and': return z3.And(left_z3, right_z3)
                    elif op_type == 'or': return z3.Or(left_z3, right_z3)
                    elif op_type == 'if': return z3.Implies(left_z3, right_z3)
                    elif op_type == 'iff': return left_z3 == right_z3

        lit_match = re.match(r"^([A-Z]\w*)\((.*)\)$", text)
        if lit_match:
            p_name, arg_name = lit_match.group(1), lit_match.group(2).strip()
            if p_name in z3_functions:
                arg_obj = bound_vars.get(arg_name) if arg_name in bound_vars else z3_constants.get(arg_name)
                if arg_obj is None:
                    z3_constants[arg_name] = z3.Const(arg_name, Universe)
                    arg_obj = z3_constants[arg_name]
                return z3_functions[p_name](arg_obj)

        if text not in z3_propositional:
            z3_propositional[text] = z3.Bool(text)
        return z3_propositional[text]

    try:
        clauses = [c.strip() for c in clause_set_str.split(";") if c.strip()]
        for c in clauses:
            z3_clause = parse_to_z3(c)
            if z3_clause is not None: s.add(z3_clause)
        z3_goal = parse_to_z3(goal_str)
        if z3_goal is not None: s.add(z3.Not(z3_goal))
        return s.check() == z3.unsat
    except Exception:
        return False


class TokenizedLogicEngine:
    @staticmethod
    def split_binary_body(body_text):
        bracket_depth = 0
        for idx, char in enumerate(body_text):
            if char == '(': bracket_depth += 1
            elif char == ')': bracket_depth -= 1
            elif char == ',' and bracket_depth == 0:
                return body_text[:idx], body_text[idx+1:]
        return None

    @staticmethod
    def mutate_single_clause(axiom_idx, text_expr, absolute_action=0, target_win=""):
        if not isinstance(text_expr, str): return text_expr
        text_expr = text_expr.strip()

        # Decouple Quantifiers for FOL
        if text_expr.startswith("forall(") and text_expr.endswith(")"):
            body = text_expr[7:-1]
            c_idx = body.find(",")
            if c_idx != -1:
                v, matrix = body[:c_idx].strip(), body[c_idx+1:].strip()
                mutated = TokenizedLogicEngine.mutate_single_clause(axiom_idx, matrix, absolute_action, target_win)
                return f"forall({v},{mutated})"

        if text_expr.startswith("exists(") and text_expr.endswith(")"):
            body = text_expr[7:-1]
            c_idx = body.find(",")
            if c_idx != -1:
                v, matrix = body[:c_idx].strip(), body[c_idx+1:].strip()
                mutated = TokenizedLogicEngine.mutate_single_clause(axiom_idx, matrix, absolute_action, target_win)
                return f"exists({v},{mutated})"

         # 🟢 RESTORED ORIGINAL ALTERNATING NAVIGATION
        match = re.match(r"^(and|or|if)\((.*)\)$", text_expr)
        if match:
            op, body = match.group(1), match.group(2)
            split_res = TokenizedLogicEngine.split_binary_body(body)
            if split_res:
                left, right = split_res[0], split_res[1]
                if absolute_action % 2 == 0:
                    mutated_left = TokenizedLogicEngine.mutate_single_clause(axiom_idx, left, absolute_action, target_win)
                    if mutated_left != left: return f"{op}({mutated_left},{right})"
                else:
                    mutated_right = TokenizedLogicEngine.mutate_single_clause(axiom_idx, right, absolute_action, target_win)
                    if mutated_right != right: return f"{op}({left},{mutated_right})"


        # Axiom 0: Commutativity
        if axiom_idx == 0:
            match = re.search(r"^(and|or)\((.*)\)$", text_expr)
            if match:
                op, body = match.group(1), match.group(2)
                split_res = TokenizedLogicEngine.split_binary_body(body)
                if split_res: return f"{op}({split_res[1]},{split_res[0]})"
        
        # Axiom 1: Contraposition
        elif axiom_idx == 1:
            if text_expr.startswith("if(") and text_expr.endswith(")"):
                split_res = TokenizedLogicEngine.split_binary_body(text_expr[3:-1])
                if split_res: return f"if(not({split_res[1]}),not({split_res[0]}))"
                
        # Axiom 2: Idempotency
        elif axiom_idx == 2:
            match = re.search(r"^(and|or)\((.*)\)$", text_expr)
            if match:
                op, body = match.group(1), match.group(2)
                split_res = TokenizedLogicEngine.split_binary_body(body)
                if split_res and split_res[0] == split_res[1]: return split_res[0]
                
        # Axiom 3: Associativity
        elif axiom_idx == 3:
            match = re.search(r"^(and|or)\((.*)\)$", text_expr)
            if match:
                op, body = match.group(1), match.group(2)
                split_res = TokenizedLogicEngine.split_binary_body(body)
                if split_res:
                    l, r = split_res[0], split_res[1]
                    if r.startswith(f"{op}("):
                        inner = TokenizedLogicEngine.split_binary_body(r[4:-1])
                        if inner: return f"{op}({op}({l},{inner[0]}),{inner[1]})"
                    if l.startswith(f"{op}("):
                        inner = TokenizedLogicEngine.split_binary_body(l[4:-1])
                        if inner: return f"{op}({inner[0]},{op}({inner[1]},{r}))"
                        
        # Axiom 4 (idx 4): De Morgan's Law (Dual Form Logic Restoration)
        elif axiom_idx == 4:
            # Dual Form: not(and(not(not(A)), not(B))) -> or(A, B)
            if text_expr.startswith("not(and(not(not(") and text_expr.endswith(")))"):
                match = re.search(r"^not\(and\(not\(not\((.*)\)\),not\((.*)\)\)\)$", text_expr)
                if match:
                    return f"or({match.group(1)},{match.group(2)})"
                    
            # Standard Form: or(A,B) -> not(and(not(A),not(B)))
            match = re.search(r"^or\((.*)\)$", text_expr)
            if match:
                split_res = TokenizedLogicEngine.split_binary_body(match.group(1))
                if split_res: 
                    return f"not(and(not({split_res[0]}),not({split_res[1]})))"

        
        # Axiom 5: Implication Materialization
        elif axiom_idx == 5:
            if text_expr.startswith("if(") and text_expr.endswith(")"):
                split_res = TokenizedLogicEngine.split_binary_body(text_expr[3:-1])
                if split_res: return f"or(not({split_res[0]}),{split_res[1]})"
                
        # Axiom 6: Distributivity
        elif axiom_idx == 6:
            match = re.search(r"^or\((.*)\)$", text_expr)
            if match:
                split_res = TokenizedLogicEngine.split_binary_body(match.group(1))
                if split_res:
                    l, r = split_res[0], split_res[1]
                    if r.startswith("and("):
                        inner = TokenizedLogicEngine.split_binary_body(r[4:-1])
                        if inner: return f"and(or({l},{inner[0]}),or({l},{inner[1]}))"
                    if l.startswith("and("):
                        inner = TokenizedLogicEngine.split_binary_body(l[4:-1])
                        if inner: return f"and(or({inner[0]},{r}),or({inner[1]},{r}))"
        # Axiom 8 (idx 8): Double Negation Insertion (Saturated Filter Added)
        elif axiom_idx == 8:
            if text_expr and not text_expr.startswith("and(") and not ";" in text_expr:
                # 🚨 HALT if the variable space is already modified or contains a negation shell
                if "not(" in text_expr or len(text_expr) > 10:
                    return text_expr
                return f"not(not({text_expr}))"

                
        # Axiom 9: Absorption
        elif axiom_idx == 9:
            match = re.search(r"^and\((.*)\)$", text_expr)
            if match:
                split_res = TokenizedLogicEngine.split_binary_body(match.group(1))
                if split_res:
                    l, r = split_res[0], split_res[1]
                    if r.startswith("or("):
                        inner = TokenizedLogicEngine.split_binary_body(r[3:-1])
                        if inner and inner[0] == l: return l
                    if l.startswith("or("):
                        inner = TokenizedLogicEngine.split_binary_body(l[3:-1])
                        if inner and inner[0] == r: return r
                        
        # Axiom 12: Complement Contradiction
        elif axiom_idx == 12:
            match = re.search(r"^and\((.*)\)$", text_expr)
            if match:
                split_res = TokenizedLogicEngine.split_binary_body(match.group(1))
                if split_res:
                    l, r = split_res[0], split_res[1]
                    if r == f"not({l})" or l == f"not({r})": return "false"

        return text_expr

    @staticmethod
    def apply_axiom(axiom_idx, current_set_str, absolute_action=0, target_win=""):
        clauses = [c.strip() for c in current_set_str.split(";") if c.strip()]
        if not clauses: return current_set_str

        # 🚨 SAFE FOL RE-DIRECTION INNER GATEWAY
        if axiom_idx in [10, 11] and ";" in current_set_str:
            try:
                from fol_engine import FirstOrderLogicEngine
                return FirstOrderLogicEngine.apply_axiom(axiom_idx, current_set_str, absolute_action, target_win)
            except ImportError:
                pass

        target_idx = absolute_action % len(clauses)
        target_clause = clauses[target_idx].strip()
        
        mutated = TokenizedLogicEngine.mutate_single_clause(axiom_idx, target_clause, absolute_action, target_win)
        if mutated != target_clause:
            clauses[target_idx] = mutated
            
        return " ; ".join(clauses)
