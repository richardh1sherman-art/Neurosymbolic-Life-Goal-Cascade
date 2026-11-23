def apply_recursive(curr, op_num):
    if not isinstance(curr, list): return None

    # INTERCEPT TRAP: If this node is explicitly our active subgoal, 
    # force the axiom mutations to evaluate ONLY inside its local arguments.
    if curr[0] == 'subgoal_12':
        # Drill directly into the Left (index 1) and Right (index 2) subgoal terms
        for i in:
            res = apply_recursive(curr[i], op_num)
            if res:
                new_node = list(curr)
                new_node[i] = res
                return new_node
        
        # If internal elements are stable, try executing Op 12 directly on the wrapper itself
        if op_num == 12:
            res = python_operator(curr, op_num)
            if res: return res
        return None

    # Standard Fallback: Unconditional Left-to-Right drill down
    for i in range(1, len(curr)):
        res = apply_recursive(curr[i], op_num)
        if res:
            new_node = list(curr)
            new_node[i] = res
            return new_node
                
    # Apply operator at the parent layer if child sub-branches are stable
    res = python_operator(curr, op_num)
    if res:
        print(f"  [TRACE] Op {op_num} applied to: {curr} -> {res}")
        return res
        
    return None


# =====================================================================
# THE RECONSTRUCTED GPS CORE MAIN SEARCH ENGINE
# =====================================================================
# Re-initializing memory states for a clean, deterministic execution path
attempted_ops_per_state.clear()
current_state = start
step_counter = 0
max_steps = 30
history_trail = [current_state]

print(f"\n🚀 BEGINNING DEDUCTION LOOP FOR THEOREM BENCHMARK ID...")
print(f"  -> Initial Premise: {current_state}")
print(f"  -> Target Goal:    {win}\n")

while not is_win(current_state, win) and step_counter < max_steps:
    step_counter += 1
    
    # 1. Sense state delta differences to predict the strategic D-Code
    diff_code = identify_highest_diff(current_state, win)
    
    # 2. Call the Strategist LLM to extract the optimal operator path
    chosen_op = call_strategist(current_state, win, diff_code)
    
    # 3. Handle Tree-of-Thought Backtracking anomalies gracefully
    if chosen_op is None:
        if len(stack) > 1:
            stack.pop() # Evict failed leaf branch
            current_state = stack[-1]
            print(f"🔄 [ToT BACKTRACK] Reverting to previous stable state: {current_state}")
            continue
        else:
            print("❌ [CRITICAL FAILURE] Pure search space exhausted. No valid proof path exists.")
            break
            
    # 4. Apply the selected axiom mutation rules positionally
    next_state = apply_recursive(current_state, chosen_op)
    
    if next_state is not None:
        # Check if the mutation actually advanced our configuration state
        if next_state != current_state:
            current_state = next_state
            stack.append(current_state)
            history_trail.append(current_state)
            print(f"  Step {step_counter:02d}: Action Approved -> New State Layout: {current_state}")
        else:
            print(f"  [MUTATION WARNING] Op {chosen_op} yielded identical characters. Retrying...")
    else:
        print(f"  [MUTATION WARNING] Op {chosen_op} failed syntactic match checks. Forcing fallback...")

# Final verification audit check block
if is_win(current_state, win):
    print(f"\n👑 SUCCESS! GPS LOGIC THEORIST PROOF TRAIL STAMPED VALID IN {step_counter} STEPS!")
    print("---------------------------------------------------------------------")
    for i, trace_node in enumerate(history_trail):
        print(f"  State Node {i:02d}: {trace_node}")
    print("---------------------------------------------------------------------")
else:
    print(f"\n⚠️ SESSION CLOSURE: Proof path could not stabilize within {max_steps} steps limit.")
