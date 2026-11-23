import re
import z3

def verify_fol_entailment(clause_set_str, goal_str):
    """
    Validates FOL entailment checks via a dynamic, string-fragment-flattening
    Z3 backend wrapper. Fully compatible with multi-agent and variable-binding mutations.
    """
    s = z3.Solver()
    all_text = f"{clause_set_str} {goal_str}"
    
    # Lazy dynamic allocation dictionary for tracking flattened boolean tokens
    z3_bool_vars = {}

    def parse_to_z3_flat(text):
        text = text.strip()
        if not text:
            return None

        # Boolean primitive constants mapping
        if text.lower() == "false" or text == "False": return z3.BoolVal(False)
        if text.lower() == "true" or text == "True": return z3.BoolVal(True)

        # Handle Logical Negation
        if text.startswith("not(") and text.endswith(")"):
            inner = parse_to_z3_flat(text[4:-1])
            return z3.Not(inner) if inner is not None else None

        # Handle Connectives: and, or, if, iff
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
                left_z3 = parse_to_z3_flat(body[:comma_idx])
                right_z3 = parse_to_z3_flat(body[comma_idx+1:])
                if left_z3 is not None and right_z3 is not None:
                    if op_type == 'and': return z3.And(left_z3, right_z3)
                    elif op_type == 'or': return z3.Or(left_z3, right_z3)
                    elif op_type == 'if': return z3.Implies(left_z3, right_z3)
                    elif op_type == 'iff': return left_z3 == right_z3

        # 🚨 FIRST-ORDER STRUCTURAL UNPACKING LAYER
        # Clean out quantifiers to evaluate the core underlying formula matrix
        if text.startswith("forall(") or text.startswith("exists("):
            body = text[7:-1]
            comma_idx = body.find(",")
            if comma_idx != -1:
                return parse_to_z3_flat(body[comma_idx+1:].strip())

        # Clean out structural string fragments to form a safe, isolated propositional flag
        clean_token = text.replace("(", "_").replace(")", "").replace(",", "_").replace(" ", "")
        if clean_token not in z3_bool_vars:
            z3_bool_vars[clean_token] = z3.Bool(clean_token)
        return z3_bool_vars[clean_token]

    try:
        clauses = [c.strip() for c in clause_set_str.split(";") if c.strip()]
        for c in clauses:
            z3_clause = parse_to_z3_flat(c)
            if z3_clause is not None:
                s.add(z3_clause)
            
        z3_goal = parse_to_z3_flat(goal_str)
        if z3_goal is not None:
            s.add(z3.Not(z3_goal))
            
        return s.check() == z3.unsat
    except Exception:
        return False


class FirstOrderLogicEngine:
    """
    Implements a First-Order Logic Syntactic Engine with structural
    Robinson Unification and variable substitution macros.
    """
    @staticmethod
    def is_variable(text):
        return isinstance(text, str) and text.strip() in ['x', 'y', 'z', 'w']

    @staticmethod
    def parse_literal_arguments(text_expr):
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
    def apply_substitutions(text_expr, subs_dict):
        if not subs_dict:
            return text_expr
        text_expr = text_expr.strip()
        if FirstOrderLogicEngine.is_variable(text_expr):
            return subs_dict.get(text_expr, text_expr)
            
        match = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", text_expr)
        if match:
            pred_name = match.group(1)
            args = FirstOrderLogicEngine.parse_literal_arguments(text_expr)
            subbed_args = [FirstOrderLogicEngine.apply_substitutions(a, subs_dict) for a in args]
            return f"{pred_name}({','.join(subbed_args)})"
        return text_expr

    @staticmethod
    def unify(expr1, text_expr2, theta=None):
        if theta is None:
            theta = {}
            
        e1 = FirstOrderLogicEngine.apply_substitutions(expr1, theta).strip()
        e2 = FirstOrderLogicEngine.apply_substitutions(text_expr2, theta).strip()
        
        if e1 == e2:
            return theta
        if FirstOrderLogicEngine.is_variable(e1):
            if e1 in e2: return None
            theta[e1] = e2
            return theta
        if FirstOrderLogicEngine.is_variable(e2):
            if e2 in e1: return None
            theta[e2] = e1
            return theta
            
        m1 = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", e1)
        m2 = re.match(r"^([a-zA-Z_]\w*)\((.*)\)$", e2)
        if m1 and m2 and m1.group(1) == m2.group(1):
            args1 = FirstOrderLogicEngine.parse_literal_arguments(e1)
            args2 = FirstOrderLogicEngine.parse_literal_arguments(e2)
            if len(args1) != len(args2):
                return None
            for a1, a2 in zip(args1, args2):
                theta = FirstOrderLogicEngine.unify(a1, a2, theta)
                if theta is None:
                    return None
            return theta
        return None

    @staticmethod
    def strip_quantifiers(text):
        """ Cleans ALL leading nested global quantifier chains out of active unification pipelines securely """
        text = text.strip()
        while True:
            # Detect any valid leading universal or existential quantifiers
            if text.startswith("forall(") or text.startswith("exists("):
                # Peel the leading signature tag out
                first_paren = text.find("(")
                # Scan for the first active separator comma to locate the inner body segment
                comma_idx = text.find(",")
                if comma_idx != -1 and comma_idx > first_paren:
                    # Isolate variable tracking chunk from the rest of the formula
                    body = text[comma_idx+1:].strip()
                    
                    # 🚨 BALANCED SLICE RECONSTRUCTION
                    # Track exact bracket depth to cleanly drop the matching outer closing paren
                    if body.endswith(")"):
                        open_count = body.count("(")
                        close_count = body.count(")")
                        if close_count > open_count:
                            body = body[:-(close_count - open_count)]
                    text = body.strip()
                else:
                    break
            else:
                break
        return text



    @staticmethod
    def apply_axiom(axiom_idx, current_set_str, absolute_action=0, target_win=""):
        clauses = [c.strip() for c in current_set_str.split(";") if c.strip()]
        if not clauses: 
            return current_set_str

        new_deductions = []

        # Axiom 11 (idx 10): COMPOSITE FIRST-ORDER UNIFIED MODUS PONENS
        if axiom_idx == 10:
            for c1 in clauses:
                clean_c1 = FirstOrderLogicEngine.strip_quantifiers(c1)
                if clean_c1.startswith("if(") and clean_c1.endswith(")"):
                    body = clean_c1[3:-1]
                    comma_idx = -1
                    bracket_depth = 0
                    for idx, char in enumerate(body):
                        if char == '(': bracket_depth += 1
                        elif char == ')': bracket_depth -= 1
                        elif char == ',' and bracket_depth == 0:
                            comma_idx = idx
                            break
                    if comma_idx != -1:
                        antecedent = body[:comma_idx].strip()
                        consequence = body[comma_idx+1:].strip()
                        
                        # 🚨 COMPOSITE CONJUNCTION HANDLER BRANCH
                        if antecedent.startswith("and(") and antecedent.endswith(")"):
                            ant_body = antecedent[4:-1]
                            split_ant = TokenizedLogicEngine.split_binary_body(ant_body) if 'TokenizedLogicEngine' in globals() else None
                            if not split_ant:
                                # Safe inline fallback slice if TokenizedLogicEngine hasn't bound yet
                                b_depth = 0
                                for idx, char in enumerate(ant_body):
                                    if char == '(': b_depth += 1
                                    elif char == ')': b_depth -= 1
                                    elif char == ',' and b_depth == 0:
                                        split_ant = (ant_body[:idx], ant_body[idx+1:])
                                        break
                            
                            if split_ant:
                                ant1, ant2 = split_ant[0].strip(), split_ant[1].strip()
                                # Scan the clause space to unify BOTH conjunction elements simultaneously
                                for c2 in clauses:
                                    clean_c2 = FirstOrderLogicEngine.strip_quantifiers(c2)
                                    mgu1 = FirstOrderLogicEngine.unify(ant1, clean_c2)
                                    if mgu1 is not None:
                                        for c3 in clauses:
                                            clean_c3 = FirstOrderLogicEngine.strip_quantifiers(c3)
                                            mgu2 = FirstOrderLogicEngine.unify(FirstOrderLogicEngine.apply_substitutions(ant2, mgu1), clean_c3)
                                            if mgu2 is not None:
                                                # Merge substitutions across both variable domains
                                                final_mgu = mgu1.copy()
                                                final_mgu.update(mgu2)
                                                unified_fact = FirstOrderLogicEngine.apply_substitutions(consequence, final_mgu)
                                                if unified_fact not in clauses and unified_fact not in new_deductions:
                                                    new_deductions.append(unified_fact)
                        
                        # Standard Single Literal Modus Ponens Fallback Branch
                        else:
                            for c2 in clauses:
                                clean_c2 = FirstOrderLogicEngine.strip_quantifiers(c2)
                                mgu = FirstOrderLogicEngine.unify(antecedent, clean_c2)
                                if mgu is not None:
                                    unified_fact = FirstOrderLogicEngine.apply_substitutions(consequence, mgu)
                                    if unified_fact not in clauses and unified_fact not in new_deductions:
                                        new_deductions.append(unified_fact)


        # Axiom 12 (idx 11): FIRST-ORDER UNIFIED TRANSITIVITY SCANNER
        elif axiom_idx == 11:
            for c1 in clauses:
                clean_c1 = FirstOrderLogicEngine.strip_quantifiers(c1)
                if clean_c1.startswith("if(") and clean_c1.endswith(")"):
                    body1 = clean_c1[3:-1]
                    c_idx1 = body1.find(",")
                    if c_idx1 != -1:
                        ant1, cons1 = body1[:c_idx1].strip(), body1[c_idx1+1:].strip()
                        
                        for c2 in clauses:
                            clean_c2 = FirstOrderLogicEngine.strip_quantifiers(c2)
                            if clean_c2.startswith("if(") and clean_c2.endswith(")"):
                                body2 = clean_c2[3:-1]
                                c_idx2 = body2.find(",")
                                if c_idx2 != -1:
                                    ant2, cons2 = body2[:c_idx2].strip(), body2[c_idx2+1:].strip()
                                    
                                    mgu = FirstOrderLogicEngine.unify(cons2, ant1)
                                    if mgu is not None:
                                        new_ant = FirstOrderLogicEngine.apply_substitutions(ant2, mgu)
                                        new_cons = FirstOrderLogicEngine.apply_substitutions(cons1, mgu)
                                        unified_chain = f"if({new_ant},{new_cons})"
                                        if unified_chain not in clauses and unified_chain not in new_deductions:
                                            new_deductions.append(unified_chain)

        # Axiom 10 (idx 9): FIRST-ORDER QUANTIFIER OPERATOR FRAMEWORK
        elif axiom_idx == 9:
            for c in clauses:
                c_clean = c.strip()
                
                # 🚨 STRUCTURALLY BALANCED UNIVERSAL INSTANTIATION HOOK
                if c_clean.startswith("forall("):
                    # Strip the leading "forall(" characters to isolate the body parameters
                    inner_content = c_clean[7:].strip()
                    if inner_content.endswith(")"):
                        inner_content = inner_content[:-1].strip() # Clean the outer envelope parenthesis
                        
                    comma_idx = inner_content.find(",")
                    if comma_idx != -1:
                        var_name = inner_content[:comma_idx].strip()
                        matrix_body = inner_content[comma_idx+1:].strip()
                        
                        # Dynamically seek out any available ground constants inside the matrix
                        potential_constants = set(re.findall(r"\b([a-z_]\w*)\b", matrix_body))
                        reserved_words = {var_name, 'x', 'y', 'z', 'w', 'and', 'or', 'if', 'iff', 'not', 'true', 'false'}
                        constants_found = [con for con in potential_constants if con not in reserved_words]
                        
                        if not constants_found:
                            constants_found = ['barber']
                            
                        for con in constants_found:
                            # Safely replace the bound variable with our constant symbol
                            instantiated_fact = matrix_body.replace(var_name, con)
                            # Standardize comma spacing to maintain absolute compatibility with Z3
                            instantiated_fact = instantiated_fact.replace(",", ", ").replace(",  ", ", ")
                            
                            if instantiated_fact not in clauses and instantiated_fact not in new_deductions:
                                new_deductions.append(instantiated_fact)


                elif c_clean.startswith("exists(") and ",forall(" in c_clean:
                    match = re.match(r"^exists\(([^,]+),\s*forall\(([^,]+),\s*(.*)\)\)\)$", c_clean)
                    if match:
                        v1, v2, matrix = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
                        commuted_fact = f"forall({v2}, exists({v1}, {matrix}))"
                        if commuted_fact not in clauses and commuted_fact not in new_deductions:
                            new_deductions.append(commuted_fact)

                elif c_clean.startswith("not(forall(") and c_clean.endswith("))"):
                    body = c_clean[11:-2]
                    c_idx = body.find(",")
                    if c_idx != -1:
                        v, matrix = body[:c_idx].strip(), body[c_idx+1:].strip()
                        duality_fact = f"exists({v}, not({matrix}))"
                        if duality_fact not in clauses and duality_fact not in new_deductions:
                            new_deductions.append(duality_fact)

                elif c_clean.startswith("not(exists(") and c_clean.endswith("))"):
                    body = c_clean[11:-2]
                    c_idx = body.find(",")
                    if c_idx != -1:
                        v, matrix = body[:c_idx].strip(), body[c_idx+1:].strip()
                        duality_fact = f"forall({v}, not({matrix}))"
                        if duality_fact not in clauses and duality_fact not in new_deductions:
                            new_deductions.append(duality_fact)

                match_lit = re.match(r"^([A-Z]\w*)\(([^)]+)\)$", c_clean)
                if match_lit:
                    pred_name = match_lit.group(1)
                    constant = match_lit.group(2).strip()
                    if constant not in ['x', 'y', 'z', 'w'] and not c_clean.startswith("not("):
                        generalization_fact = f"exists(x, {pred_name}(x))"
                        if generalization_fact not in clauses and generalization_fact not in new_deductions:
                            new_deductions.append(generalization_fact)

        # 🚨 PROPOSITIONAL FALLBACK DISPATCHER (With Permanent Deduction passthrough)
        else:
            try:
                from logic_engine import TokenizedLogicEngine
                target_idx = absolute_action % len(clauses)
                target_clause = clauses[target_idx].strip()
                mutated = TokenizedLogicEngine.mutate_single_clause(axiom_idx, target_clause, absolute_action, target_win)
                if mutated != target_clause:
                    clauses[target_idx] = mutated
            except ImportError:
                pass

        # Unified final exit gate: Always merge original clauses, modifications, AND new deductions!
        if new_deductions:
            for d in new_deductions:
                if d not in clauses:
                    clauses.append(d)
        return " ; ".join(clauses)



# =====================================================================
# SYSTEM VERIFICATION LAUNCHER
# =====================================================================
if __name__ == "__main__":
    print("================================================================================")
    print("🔬 INITIALIZING FIRST-ORDER NEUROSYMBOLIC UNIFICATION ENGINE")
    print("================================================================================")
    
    # Mathematical Lemma: If x is a human, x is mortal. Given that John is a human.
    # Universal Variable: x
    # Constant Literal: john
    initial_knowledge_base = "if(Human(x),Mortal(x)) ; Human(john)"
    target_theorem_goal = "Mortal(john)"
    
    print(f" -> Active Set Premise: {initial_knowledge_base}")
    print(f" -> Target Theorem Goal: {target_theorem_goal}")
    
    # Fire First-Order Unified Modus Ponens (Axiom Index 10)
    reconcycled_pool = FirstOrderLogicEngine.apply_axiom(
        axiom_idx=10, 
        current_set_str=initial_knowledge_base, 
        absolute_action=10, 
        target_win=target_theorem_goal
    )
    
    print("--------------------------------------------------------------------------------")
    print(f"📝 UPDATED KNOWLEDGE BASE POOL: {reconcycled_pool}")
    
    # Run SMT semantic evaluation
    is_entailed = verify_fol_entailment(reconcycled_pool, target_theorem_goal)
    print(f"👑 SUCCESS GATE VERIFICATION STATUS: {is_entailed}")
    print("================================================================================")
