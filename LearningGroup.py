import torch
import torch.nn as nn
import torch.nn.utils as utils
import numpy as np

# =====================================================================
# UPGRADED ACTOR-CRITIC GROUP AGENT (Deep Intrinsic Learning Layer)
# =====================================================================
class LearningGroupProverAgent(nn.Module):
    def __init__(self, max_depth=9, num_axioms=14):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_axioms
        
        # Shared feature representation layer
        self.shared_layer = nn.Sequential(
            nn.Linear(max_depth * 3, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU()
        )
        
        # Actor Head: Outputs policy probabilities across the 42 group operations
        self.actor_head = nn.Sequential(
            nn.Linear(128, 42),
            nn.Softmax(dim=-1)
        )
        
        # Critic Head: Predicts the expected geometric value/reward of the current group coordinate
        self.critic_head = nn.Linear(128, 1)

    def forward(self, state_tuple):
        s1, s2, s3 = state_tuple
        features = []
        # Unpack scalar group integer coordinates into distinct vector features
        for s in [s1, s2, s3]:
            temp = int(s.item())
            for _ in range(self.max_depth):
                features.append(temp % self.d)
                temp //= self.d
                
        state_tensor = torch.tensor(features, dtype=torch.float32, device=device)
        shared_out = self.shared_layer(state_tensor)
        
        probs = self.actor_head(shared_out)
        state_value = self.critic_head(shared_out)
        return probs, state_value

# =====================================================================
# ADVANTAGE POLICY LEARNING SEARCH TUNNEL
# =====================================================================
def run_learning_group_session(test_id=8, iterations=1000, horizon=35):
    start_expr, target_win = load_theorem_benchmarks(test_id)
    
    print("=== STARTING AUTONOMOUS LEARNING GROUP ENGINE ===")
    print(f"  -> Target Complex Axiom ID:   {test_id}")
    print(f"  -> Infinite Group Start Node: {start_expr}")
    print("=====================================================================")
    
    compiler = GroupTheoreticProverCompiler(max_depth=9, num_axioms=14)
    # Instantiate our deep learning model
    agent = LearningGroupProverAgent(max_depth=9, num_axioms=14).to(device)
    optimizer = torch.optim.Adam(agent.parameters(), lr=0.0005)
    
    for iteration in range(iterations):
        state_tuple = (torch.tensor(0, device=device), torch.tensor(0, device=device), torch.tensor(0, device=device))
        current_proof_expression = start_expr
        
        log_probabilities = []
        state_values = []
        rewards = []
        success_flag = False
        local_step_history = [start_expr]
        
        for step in range(horizon):
            # Upgraded Forward Pass: Extract both action distributions and critic value estimations
            action_probs, state_value = agent(state_tuple)
            
            action_dist = torch.distributions.Categorical(action_probs)
            action = action_dist.sample()
            
            log_probabilities.append(action_dist.log_prob(action))
            state_values.append(state_value)
            
            # Mutate the geometric non-abelian group coordinates
            state_tuple = compiler.apply_action(action.item(), state_tuple)
            
            axiom_to_apply = action.item() % 14
            next_expression = TokenizedLogicEngine.apply_axiom(axiom_to_apply, current_proof_expression, action.item(), target_win)
            
            local_step_history.append(f"Apply Axiom {axiom_to_apply+1} -> {next_expression}")
            
            # Learning Optimization Evaluation
            if next_expression != current_proof_expression and verify_step_entailment(next_expression, target_win):
                active_set_members = [clause.strip() for clause in next_expression.split(";")]
                if target_win.strip() in active_set_members:
                    rewards.append(1000.0) # Huge reward for hitting target conclusion
                    success_flag = True
                    break
                else:
                    rewards.append(50.0) # Reward for extending the verified set frontier
            elif next_expression != current_proof_expression:
                # Intrinsic reward proportional to new unique clause length changes
                rewards.append(10.0)
            else:
                rewards.append(-2.0) # Stagnation penalty
                
            current_proof_expression = next_expression

        # --- REINFORCEMENT LEARNING ADVANTAGE UPDATE UPDATE ---
        discounted_rewards = []
        R = 0
        for r in reversed(rewards):
            R = r + 0.99 * R
            discounted_rewards.insert(0, R)
            
        discounted_rewards = torch.tensor(discounted_rewards, device=device)
        
        actor_loss = 0
        critic_loss = 0
        
        # Calculate Advantage: Actual Reward minus the Critic's expected value estimate
        for log_prob, val, r_target in zip(log_probabilities, state_values, discounted_rewards):
            advantage = r_target - val.item()
            actor_loss -= log_prob * advantage # Guide the actor policy parameters
            critic_loss += torch.nn.functional.mse_loss(val, torch.tensor([r_target], device=device)) # Update the critic
            
        total_loss = actor_loss + 0.5 * critic_loss
        
        optimizer.zero_grad()
        total_loss.backward()
        utils.clip_grad_norm_(agent.parameters(), max_norm=0.5) # Prevent gradient explosions
        optimizer.step()
        
        if success_flag:
            print(f"\n👑 SUCCESS! GEOMETRIC CONVERGENCE ACHIEVED VIA AC2 GRADIENTS AT ITERATION {iteration+1}!")
            print("---------------------------------------------------------------------")
            for i, line in enumerate(local_step_history):
                print(f"  Step {i:02d}: {line}")
            print("---------------------------------------------------------------------")
            break
            
        if (iteration + 1) % 50 == 0:
            print(f"  Iteration {iteration+1:04d} | Set Fact Pool Depth: {len(current_proof_expression.split(';'))}")
