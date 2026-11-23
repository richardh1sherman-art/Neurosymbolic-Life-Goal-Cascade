import torch

def load_theorem_benchmarks(test_num):
    # --- Propositional Logic Baselines ---
    if test_num == 1:   return "and(p,q)", "and(q,p)"
    elif test_num == 2: return "if(p,q)", "if(not(q),not(p))"
    elif test_num == 3: return "and(if(p,q),p)", "q"
    elif test_num == 4: return "and(if(p,not(not(r))),if(not(q),not(r)))", "not(and(p,not(q)))"
    elif test_num == 5: return "and(if(r,not(p)),if(not(r),q))", "not(and(not(q),p))"
    elif test_num == 6: return "and(if(p,r),if(q,not(r)))", "not(and(p,q))"
    elif test_num == 7: return "and(if(gas,matter),and(if(vacuum,not(matter)),if(void,vacuum)))", "if(void,not(gas))"
    elif test_num == 8: return "and(if(polar_bear,arctic),and(if(arctic,cold),and(if(tropical,not(cold)),if(flamingo,tropical))))", "if(polar_bear,not(flamingo))"
    
    # --- Hard Complex Problems ---
    elif test_num == 9:  return "if(if(if(p,q),p),p)", "p"  # Peirce's Law
    elif test_num == 10: return "and(if(p,q),and(if(p,r),and(if(q,s),and(if(r,s),if(s,t)))))", "if(p,t)"  # Diamond Lattice
    elif test_num == 11: return "and(if(p,q),and(if(q,and(r,s)),if(and(r,s),t)))", "if(p,t)"  # Statman's Lock
    elif test_num == 12: return "and(or(p11,p12),and(or(p21,p22),or(p31,p32)))", "or(and(p11,p21),or(and(p11,p31),or(and(p21,p31),or(and(p12,p22),or(and(p12,p32),and(p22,p32))))))" # PHP_2
    
    # --- Non-Classical Multi-Agent Extensions ---
    elif test_num == 13: # Rasiowa Multi-Agent Consensus
        return "if(and(d_w(q),d_s(r)),d_u(p)) ; d_t(r) ; d_s(q)", "d_w(p)"
#    elif test_num == 14: # First-Order Logic (FOL) Syllogism
#        return "if(Human(x),Mortal(x)) ; Human(john)", "Mortal(john)"
#        return " exists z Mentors(z) specialist", "Mentors(specialist)"
    elif test_num == 15: # Upgraded Modal Zalta Object Theory Test
        return "exe(Abstract,object_1) ; exe(Abstract,object_2) ; enc(object_1,Being_Even) ; enc(object_2,Being_Even)", "box(Identical(object_1,object_2))"
    elif test_num == 17: # Zalta Negative Free Logic (NFL) Consistency Matrix
        return "enc(object_x,Blueprint_A) ; exe(Physical,object_x) ; enc(object_y,Blueprint_B)", "Consistent(state_s)"
 # --- True First-Order Logic (FOL) Benchmarks ---
    elif test_num == 14: 
        # Standard Universal Syllogism (Socrates/John problem)
        return "forall(x, if(Human(x), Mortal(x))) ; Human(john)", "Mortal(john)"
        
    elif test_num == 18:
        # Existential Generalization (If John is a doctor, a doctor exists)
        return "Doctor(john)", "exists(x, Doctor(x))"
        
    elif test_num == 19:
        # De Morgan's Law for Quantifiers (Not everyone is perfect -> someone is not perfect)
        return "not(forall(x, Perfect(x)))", "exists(x, not(Perfect(x)))"
        
    elif test_num == 20:
        # Quantifier Commutation / Scope (If a mentor exists for everyone, everyone has a mentor)
        return "exists(y, forall(x, Mentors(y, x)))", "forall(x, exists(y, Mentors(y, x)))"
        
    elif test_num == 21:
        # Barber Paradox / Russell's Paradox Style (Satisfiability / Contradiction check)
        # "The barber shaves everyone who does not shave themselves." -> Contradiction.
        return "forall(x, iff(Shaves(barber, x), not(Shaves(x, x))))", "False"

    elif test_num == 22:
        # Multi-variable transitivity (Grader problem)
        return "forall(x, forall(y, forall(z, if(and(Greater(x,y), Greater(y,z)), Greater(x,z))))) ; Greater(a, b) ; Greater(b, c)", "Greater(a, c)"
    
    else:                # Zilber Continuous Logic / Metric Geometry
        return "in_circle(12,15,50) ; in_circle(14,17,50)", "or(in_circle(12,15,50),in_box(12.0,15.0,10))"

class GroupTheoreticProverCompiler:
    def __init__(self, max_depth=9, num_axioms=14):
        self.max_depth = max_depth
        self.d = num_axioms
        self.omega = [(0, 1, 2)] * ((max_depth // 3) + 2)

    def apply_action(self, absolute_action, state_tuple, device):
        state_1, state_2, state_3 = state_tuple
        agent_id = absolute_action // 14
        local_action_idx = absolute_action % 14
        
        target_idx = int(state_1.item()) if agent_id == 0 else (int(state_2.item()) if agent_id == 1 else int(state_3.item()))
        
        if local_action_idx == 0:
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (target_idx // root_weight) % self.d
            target_idx = target_idx - (root_digit * root_weight) + (((root_digit + 1) % self.d) * root_weight)
        elif local_action_idx > 0:
            divisor = self.d ** (self.max_depth - 1)
            current_layer = 0
            while divisor > 0 and current_layer < self.max_depth:
                digit = (target_idx // divisor) % self.d
                if digit == 0:
                    next_w = divisor // self.d
                    if next_w > 0:
                        sub_d = (target_idx // next_w) % self.d
                        target_idx = target_idx - (sub_d * next_w) + (((sub_d + 1) % self.d) * next_w)
                    break
                else:
                    omega_val = self.omega[current_layer][local_action_idx - 1 if local_action_idx - 1 < len(self.omega[current_layer]) else 0]
                    row_idx = local_action_idx - 1
                    is_perm = (omega_val == 0 and row_idx == 0) or (omega_val == 1 and row_idx < 2) or (omega_val == 2 and row_idx == 1)
                    if is_perm:
                        target_idx = target_idx - (digit * divisor) + (((digit + 1) % self.d) * divisor)
                        break
                divisor //= self.d
                current_layer += 1
                
        new_tensor = torch.tensor(target_idx, device=device)
        return (new_tensor, state_2, state_3) if agent_id == 0 else ((state_1, new_tensor, state_3) if agent_id == 1 else (state_1, state_2, new_tensor))
