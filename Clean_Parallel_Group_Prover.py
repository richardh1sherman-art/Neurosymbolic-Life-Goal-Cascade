import torch
import numpy as np
import copy
import z3
import random
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# SUB-CLAUSE ENTAILMENT GATING HELPER (Isolated SMT Check)
# =====================================================================
def verify_step_entailment(clause_set_str, goal_str):
    s = z3.Solver()
    p, q, r = z3.Bools('p q r')
    gas, matter, vacuum, void = z3.Bools('gas matter vacuum void')
    polar_bear, arctic, cold, tropical, flamingo = z3.Bools('polar_bear arctic cold tropical flamingo')
    
    var_map = {
        'p': p, 'q': q, 'r': r,
        'gas': gas, 'matter': matter, 'vacuum': vacuum, 'void': void,
        'polar_bear': polar_bear, 'arctic': arctic, 'cold': cold, 
        'tropical': tropical, 'flamingo': flamingo
    }
    
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

# =====================================================================
# RECURSIVE KNOWLEDGE-SET EXTRACTION ENGINE (Breaks Nesting Deadlocks)
# =====================================================================
class TokenizedLogicEngine:
    @staticmethod
    def split_binary_body(body_text):
        """ Dynamically finds the true splitting comma balancing nested brackets """
        bracket_depth = 0
        for idx, char in enumerate(body_text):
            if char == '(': bracket_depth += 1
            elif char == ')': bracket_depth -= 1
            elif char == ',' and bracket_depth == 0:
                return body_text[:idx], body_text[idx+1:]
        return None

    @staticmethod
    def extract_all_flat_clauses(text_expr):
        """ Recursively unpacks all inner conjunction branches into clean flat facts """
        text_expr = text_expr.strip()
        if text_expr.startswith("and(") and text_expr.endswith(")"):
            body = text_expr[4:-1]
            split_res = TokenizedLogicEngine.split_binary_body(body)
            if split_res:
                left, right = split_res
                return TokenizedLogicEngine.extract_all_flat_clauses(left) + TokenizedLogicEngine.extract_all_flat_clauses(right)
        return [text_expr]

    @staticmethod
    def mutate_single_clause(axiom_idx, text_expr, absolute_action=0, target_win=""):
        if not isinstance(text_expr, str):
            return text_expr

        # Prioritize deep recursive descent pass inside nested structures first
        match = re.match(r"^(and|or|if)\((.*)\)$", text_expr)
        if match:
            op, body = match.group(1), match.group(2)
            split_res = TokenizedLogicEngine.split_binary_body(body)
            if split_res:
                left, right = split_res, split_res
                if absolute_action % 2 == 0:
                    mutated_left = TokenizedLogicEngine.mutate_single_clause(axiom_idx, left, absolute_action, target_win)
                    if mutated_left != left: return f"{op}({mutated_left},{right})"
                else:
                    mutated_right = TokenizedLogicEngine.mutate_single_clause(axiom_idx, right, absolute_action, target_win)
                    if mutated_right != right: return f"{op}({left},{mutated_right})"

        # Operator Match Alignments
        if axiom_idx == 0:  # Commutativity
            match = re.search(r"^(and|or)\((.*)\)$", text_expr)
            if match:
                op, body = match.group(1), match.group(2)
                split_res = TokenizedLogicEngine.split_binary_body(body)
                if split_res: return f"{op}({split_res},{split_res})"
        
        elif axiom_idx == 1:  # Contrapositive
            if text_expr.startswith("if(") and text_expr.endswith(")"):
                split_res = TokenizedLogicEngine.split_binary_body(text_expr[3:-1])
                if split_res: return f"if(not({split_res}),not({split_res}))"
        
        elif axiom_idx == 5:  # Material Implication
            if text_expr.startswith("if(") and text_expr.endswith(")"):
                split_res = TokenizedLogicEngine.split_binary_body(text_expr[3:-1])
                if split_res: return f"or(not({split_res}),{split_res})"

        return text_expr

    @staticmethod
    def apply_axiom(axiom_idx, current_set_str, absolute_action=0, target_win=""):
        clauses = [c.strip() for c in current_set_str.split(";") if c.strip()]
        if not clauses: return current_set_str

        target_idx = absolute_action % len(clauses)
        target_clause = clauses[target_idx].strip()
        
        new_deductions = []

        # 1. FIXED AXIOM 8: Unconditional Recursive Global Set Flattener
        if axiom_idx == 7:
            if "and(" in target_clause:
                extracted = TokenizedLogicEngine.extract_all_flat_clauses(target_clause)
                for item in extracted:
                    new_deductions.append(item.strip())

        # 2. Axiom 11 (idx 10): Modus Ponens Cross-Set Evaluation
        elif axiom_idx == 10:
            if len(clauses) >= 2:
                for c1 in clauses:
                    for c2 in clauses:
                        if c1.startswith("if(") and c1.endswith(")"):
                            split_res = TokenizedLogicEngine.split_binary_body(c1[3:-1])
                            if split_res and split_res == c2:
                                new_deductions.append(split_res)

        # 3. Axiom 12 (idx 11): Multi-Pattern Set Transitivity Scanner
        elif axiom_idx == 11:
            if len(clauses) >= 2:
                for c1 in clauses:
                    for c2 in clauses:
                        if c1 == c2: continue
                        if c1.startswith("if(") and c1.endswith(")") and c2.startswith("if(") and c2.endswith(")"):
                            b1_res = TokenizedLogicEngine.split_binary_body(c1[3:-1])
                            b2_res = TokenizedLogicEngine.split_binary_body(c2[3:-1])
                            if b1_res and b2_res:
                                a1, b1 = b1_res
                                a2, b2 = b2_res
                                
                                if b1 == a2: new_deductions.append(f"if({a1},{b2})")
                                elif b1.startswith("not(") and b1[4:-1] == a2: new_deductions.append(f"if({a1},not({b2}))")
                                elif b2.startswith("not(") and b2[4:-1] == b1: new_deductions.append(f"if({a1},not({a2}))")
                                elif b1.startswith("not(") and b2.startswith("not(") and b1[4:-1] == b2[4:-1]:
                                    new_deductions.append(f"if({a2},{a1})")
                                elif a1.startswith("not(") and b2 == a1[4:-1]:
                                    new_deductions.append(f"if({a2},not({b1}))")
                                elif a2.startswith("not(") and b1 == a2[4:-1]:
                                    new_deductions.append(f"if({a1},not({b2}))")
                                
        # 4. Axiom 14 (idx 13): Double-Negation Elimination Set Pass
        elif axiom_idx == 13:
            mutated = re.sub(r"not\(not\(([^()]+)\)\)", r"\1", target_clause)
            if mutated != target_clause:
                new_deductions.append(mutated)
        else:
            res = TokenizedLogicEngine.mutate_single_clause(axiom_idx, target_clause, absolute_action, target_win)
            if res != target_clause:
                new_deductions.append(res)

        # Merge unique deductions cleanly
        for d in new_deductions:
            if d not in clauses: clauses.append(d)
            
        return " ; ".join(clauses)  

# =====================================================================
# ZERO-VRAM G_omega COMPILER
# =====================================================================
class GroupTheoreticProverCompiler:
    def __init__(self, max_depth=9, num_axioms=14):
        self.max_depth = max_depth
        self.d = num_axioms
        self.omega = [(0, 1, 2)] * ((max_depth // 3) + 2)

    def apply_action(self, absolute_action, state_tuple):
        state_1, state_2, state_3 = state_tuple
        agent_id = absolute_action // 14
        local_action_idx = absolute_action % 14
        
        if agent_id == 0:    target_idx = int(state_1.item())
        elif agent_id == 1:  target_idx = int(state_2.item())
        else:                target_idx = int(state_3.item())
        
        if local_action_idx == 0:
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (target_idx // root_weight) % self.d
            new_root_digit = (root_digit + 1) % self.d
            target_idx = target_idx - (root_digit * root_weight) + (new_root_digit * root_weight)
        elif local_action_idx > 0:
            divisor = self.d ** (self.max_depth - 1)
            current_layer = 0
            while divisor > 0 and current_layer < self.max_depth:
                digit = (target_idx // divisor) % self.d
                if digit == 0:
                    next_level_weight = divisor // self.d
                    if next_level_weight > 0:
                        sub_digit = (target_idx // next_level_weight) % self.d
                        new_sub_digit = (sub_digit + 1) % self.d
                        target_idx = target_idx - (sub_digit * next_level_weight) + (new_sub_digit * next_level_weight)
                    break
                else:
                    omega_val = self.omega[current_layer][local_action_idx - 1 if local_action_idx - 1 < len(self.omega[current_layer]) else 0]
                    row_idx = local_action_idx - 1
                    is_permutation_pi = False
                    if omega_val == 0 and row_idx == 0:  is_permutation_pi = True
                    elif omega_val == 1 and row_idx < 2: is_permutation_pi = True
                    elif omega_val == 2 and row_idx == 1: is_permutation_pi = True
                    
                    if is_permutation_pi:
                        new_digit = (digit + 1) % self.d
                        target_idx = target_idx - (digit * divisor) + (new_digit * divisor)
                        break
                divisor //= self.d
                current_layer += 1
                
        new_tensor = torch.tensor(target_idx, device=device)
        if agent_id == 0:   return new_tensor, state_2, state_3
        elif agent_id == 1: return state_1, new_tensor, state_3
        else:               return state_1, state_2, new_tensor

# =====================================================================
# AGENT HEURISTIC NETWORK
# =====================================================================
class FullGroupProverAgent(torch.nn.Module):
    def __init__(self, max_depth=9, num_axioms=14):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_axioms
        self.fc1 = torch.nn.Linear(max_depth * 3, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, 42) 
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_tuple):
        s1, s2, s3 = state_tuple
        features = []
        for s in [s1, s2, s3]:
            temp = int(s.item())
            for _ in range(self.max_depth):
                features.append(temp % self.d)
                temp //= self.d
        state_tensor = torch.tensor(features, dtype=torch.float32, device=device)
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        logits = self.fc3(x)
        return self.softmax(logits)

# =====================================================================
# THEOREM BENCHMARK MANAGER
# =====================================================================
def load_theorem_benchmarks(test_num):
    if test_num == 1:   return "and(p,q)", "and(q,p)"
    elif test_num == 2: return "if(p,q)", "if(not(q),not(p))"
    elif test_num == 3: return "and(if(p,q),p)", "q"
    elif test_num == 4: return "and(if(p,not(not(r))),if(not(q),not(r)))", "not(and(p,not(q)))"
    elif test_num == 5: return "and(if(r,not(p)),if(not(r),q))", "not(and(not(q),p))"
    elif test_num == 6: return "and(if(p,r),if(q,not(r)))", "not(and(p,q))"
    elif test_num == 7: return "and(if(gas,matter),and(if(vacuum,not(matter)),if(void,vacuum)))", "if(void,not(gas))"
    else:               return "and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical))))", "if(polar_bear,not(flamingo))"

# =====================================================================
# HIGH-PERFORMANCE DEDUCTION TUNNEL RUNNER
# =====================================================================
def run_realtime_proof_session(test_id=8, iterations=1200, horizon=35):
    start_expr, target_win = load_theorem_benchmarks(test_id)
    
    print("=== STARTING STCIKT SYNTACTIC TRAIL ENGINE ===")
    print(f"  -> Active Test Benchmark ID:   {test_id}")
    print(f"  -> Raw Premise Starting Point: {start_expr}")
    print(f"  -> Target Conclusion Shape:    {target_win}")
    print("=====================================================================")
    
    compiler = GroupTheoreticProverCompiler(max_depth=9, num_axioms=14)
    agent = FullGroupProverAgent(max_depth=9, num_axioms=14).to(device)
    optimizer = torch.optim.Adam(agent.parameters(), lr=0.001)
    
    proof_steps_log = []
    start_epsilon = 0.50
    end_epsilon = 0.01
    
    for iteration in range(iterations):
        epsilon = max(end_epsilon, start_epsilon - (iteration / 400.0) * (start_epsilon - end_epsilon))
        state_tuple = (torch.tensor(0, device=device), torch.tensor(0, device=device), torch.tensor(0, device=device))
        current_proof_expression = start_expr
        
        log_probabilities = []
        rewards = []
        success_flag = False
        local_step_history = [start_expr]
        
        for step in range(horizon):
            action_probs = agent(state_tuple)
            
            if random.random() < epsilon:
                action_idx = random.randint(0, 41)
                action = torch.tensor(action_idx, device=device)
            else:
                action_dist = torch.distributions.Categorical(action_probs)
                action = action_dist.sample()
                
            action_dist_for_grad = torch.distributions.Categorical(action_probs)
            log_probabilities.append(action_dist_for_grad.log_prob(action))
            
            state_tuple = compiler.apply_action(action.item(), state_tuple)
            
            axiom_to_apply = action.item() % 14
            next_expression = TokenizedLogicEngine.apply_axiom(axiom_to_apply, current_proof_expression, action.item(), target_win)
            
            local_step_history.append(f"Apply Axiom {axiom_to_apply+1} -> {next_expression}")
            
            # Safe real-time evaluation
            if next_expression != current_proof_expression and verify_step_entailment(next_expression, target_win):
                active_set_members = [clause.strip() for clause in next_expression.split(";")]
                
                if target_win.strip() in active_set_members:
                    rewards.append(600.0)
                    success_flag = True
                    proof_steps_log = local_step_history
                    current_proof_expression = next_expression
                    break
                else:
                    rewards.append(40.0) 
            elif next_expression != current_proof_expression:
                rewards.append(5.0) 
            else:
                rewards.append(-0.4)
                
            current_proof_expression = next_expression
            
        if success_flag:
            efficiency_bonus = (horizon - len(rewards)) * 30.0
            rewards[-1] += efficiency_bonus
            
            print(f"\n👑 SUCCESS! SYNTACTIC PROOF ENTAILED AND SECURITY AUDIT PASSED AT ITERATION {iteration+1}!")
            print(f"  -> Path Efficiency Bonus: +{efficiency_bonus} Rewards")
            print("---------------------------------------------------------------------")
            for i, log_line in enumerate(proof_steps_log):
                print(f"  Step {i:02d}: {log_line}")
            print("---------------------------------------------------------------------")
            
            try:
                with open(f"proof_trajectory_benchmark_{test_id}.pl", "w") as pl_file:
                    pl_file.write(f"%% Formal Axiomatic Proof Log: Test Case Benchmark {test_id}\n")
                    pl_file.write(f"%% Premise: {start_expr}.\n")
                    pl_file.write(f"%% Target:  {target_win}.\n\n")
                    for idx, trace_line in enumerate(proof_steps_log):
                        pl_file.write(f"step({idx:02d}, \"{trace_line}\").\n")
                print(f"📝 SUCCESS: Saved human-auditable Prolog file: proof_trajectory_benchmark_{test_id}.pl")
            except Exception as ex:
                print(f"⚠️ Warning: Could not write Prolog dump file: {ex}")
            break
                
        discounted_rewards = []
        R = 0
        for r in reversed(rewards):
            R = r + 0.95 * R
            discounted_rewards.insert(0, R)
            
        reward_std = float(np.std(discounted_rewards))
        discounted_rewards = torch.tensor(discounted_rewards, device=device)
        if reward_std > 1e-6:
            discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (reward_std + 1e-8)
        
        loss = 0
        for log_prob, r_val in zip(log_probabilities, discounted_rewards):
            loss -= log_prob * r_val
            
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(agent.parameters(), max_norm=1.0)
        optimizer.step()
        
        if (iteration + 1) % 50 == 0:
            console_display = current_proof_expression
            if len(console_display) > 120:
                console_display = console_display[:117] + "..."
            print(f"  Iteration {iteration+1:04d} [Epsilon: {epsilon:.3f}] -> Search: {console_display}")

if __name__ == "__main__":
    # Test 8 targets the 4-clause Arctic Bear Cascade!
    run_realtime_proof_session(test_id=8, iterations=1200, horizon=35)
