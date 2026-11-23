import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# PARALLEL GENERATOR NON-ABELIAN COMPILER (Multi-Agent Subspaces)
# =====================================================================
class ParallelGrigorchukCompiler:
    """
    Implements a multi-generator Grigorchuk group structure.
    Manages independent structural states for multiple waitresses concurrently.
    """
    def __init__(self, max_depth=15, num_tables=10):
        self.max_depth = max_depth
        self.d = num_tables
        self.dim = self.d ** max_depth

    def apply_action(self, absolute_action, state_tuple):
        """
        Maps 8 unique action tokens onto 2 parallel waitresses.
        Tokens 0-3 mutate state_1 (Waitress 1). Tokens 4-7 mutate state_2 (Waitress 2).
        """
        state_1, state_2 = state_tuple
        
        # Determine which waitress is acting and extract her local action token (0 to 3)
        waitress_id = absolute_action // 4
        local_action_idx = absolute_action % 4
        
        target_idx = int(state_1.item()) if waitress_id == 0 else int(state_2.item())
        
        if local_action_idx == 0:
            # Generator 'a' cycles the root digit of the base-d tree
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (target_idx // root_weight) % self.d
            new_root_digit = (root_digit + 1) % self.d
            target_idx = target_idx - (root_digit * root_weight) + (new_root_digit * root_weight)
        else:
            # Generators b, c, and d evaluate recursively down the subtrees
            divisor = self.d ** (self.max_depth - 1)
            current_depth = 0
            act = local_action_idx
            
            while divisor > 0 and current_depth < self.max_depth:
                digit = (target_idx // divisor) % self.d
                if digit == 0:
                    next_level_weight = divisor // self.d
                    if next_level_weight > 0:
                        sub_digit = (target_idx // next_level_weight) % self.d
                        new_sub_digit = (sub_digit + 1) % self.d
                        target_idx = target_idx - (sub_digit * next_level_weight) + (new_sub_digit * next_level_weight)
                    break
                else:
                    if act == 1:   act = 2
                    elif act == 2: act = 3
                    elif act == 3: act = 1
                divisor //= self.d
                current_depth += 1
                
        # Return the updated joint state configuration
        if waitress_id == 0:
            return torch.tensor(target_idx, device=device), state_2
        else:
            return state_1, torch.tensor(target_idx, device=device)

# =====================================================================
# JOINT SPACE SCHEDULING AGENT (Dual State Tracking)
# =====================================================================
class ParallelSchedulingAgent(torch.nn.Module):
    """
    Receives BOTH tree indices, unpacks both into base-d digit configurations, 
    and predicts from an expanded pool of 8 group generators.
    """
    def __init__(self, max_depth=15, num_tables=10):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        
        # Dual inputs: reads the path positions of both waitresses simultaneously
        self.fc1 = torch.nn.Linear(max_depth * 2, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, 8)  # 8 outputs: [a1,b1,c1,d1,  a2,b2,c2,d2]
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_tuple):
        state_1, state_2 = state_tuple
        
        # Unpack digits for Waitress 1
        digits_1 = []
        temp1 = int(state_1.item())
        for _ in range(self.max_depth):
            digits_1.append(temp1 % self.d)
            temp1 //= self.d
            
        # Unpack digits for Waitress 2
        digits_2 = []
        temp2 = int(state_2.item())
        for _ in range(self.max_depth):
            digits_2.append(temp2 % self.d)
            temp2 //= self.d
            
        # Combine into a single combined input embedding vector
        joint_digits = digits_1 + digits_2
        state_tensor = torch.tensor(joint_digits, dtype=torch.float32, device=device)
        
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        return self.softmax(self.fc3(x))

# =====================================================================
# MULTI-WAITRESS ASYNCHRONOUS ENVIRONMENT ENVIRONMENT
# =====================================================================
class ParallelRestaurantEnvironment:
    def __init__(self, num_tables=10):
        self.num_tables = num_tables
        self.reset()

    def reset(self):
        # 0=empty, 1=ordered, 2=coffee, 3=done
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        
        # Waitresses have separate focal tables to avoid conflicting paths
        self.waitress_focus = [0, 5] 
        
    def evaluate_step(self, absolute_action):
        reward = 0.0
        
        waitress_id = absolute_action // 4
        action_type = absolute_action % 4
        
        t = self.waitress_focus[waitress_id]
        current_stage = self.table_stages[t]
        
        # Rule 1: Action 'a' -> Take Order
        if action_type == 0 and current_stage == 0:
            self.table_stages[t] = 1
            reward += 5.0
            
        # Rule 2: Action 'b' -> Serve Coffee
        elif action_type == 1 and current_stage == 1:
            self.table_stages[t] = 2
            reward += 10.0
            
        # Rule 3: Action 'c' -> Serve Meal
        elif action_type == 2 and current_stage == 2:
            self.table_stages[t] = 3
            reward += 20.0
            # Move this specific waitress to the next table sequence loop
            self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
            
        # Rule 4: Action 'd' -> Household maintenance shift focus
        else:
            reward -= 0.2
            if action_type == 3:
                self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
                
        return reward

    def get_filled_orders_count(self):
        return int(np.sum(self.table_stages == 3))
        
    def get_coffee_served_count(self):
        return int(np.sum(self.table_stages >= 2))

# =====================================================================
# MULTI-GENERATOR INTEGRATED TRAINING LOOP
# =====================================================================
def train_parallel_loop(iterations=200, schedule_horizon=80, depth=15, tables=10):
    print("=== STARTING GROUP-PARALLEL MULTI-WAITRESS LOOP ===")
    print(f"Tables: {tables} | Tree Depth: {depth} | Waitresses: 2 Parallel Groups | Generators: 8")
    
    compiler = ParallelGrigorchukCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = ParallelSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = ParallelRestaurantEnvironment(num_tables=tables)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.003)
    history_scores = []
    
    for iteration in range(iterations):
        env_agent.reset()
        
        # Track states independently as a tuple of tree coordinate roots
        state_tuple = (torch.tensor(0, device=device), torch.tensor(0, device=device))
        
        log_probabilities = []
        rewards = []
        
        for step in range(schedule_horizon):
            action_probs = scheduler_agent(state_tuple)
            action_dist = torch.distributions.Categorical(action_probs)
            action = action_dist.sample()
            
            log_probabilities.append(action_dist.log_prob(action))
            
            # Step the algebraic group structures in parallel coordinate spaces
            state_tuple = compiler.apply_action(action.item(), state_tuple)
            
            # Evaluate step execution natively inside the environment
            step_reward = env_agent.evaluate_step(action.item())
            rewards.append(step_reward)
            
        # Reinforcement learning gradient evaluation block
        discounted_rewards = []
        R = 0
        for r in reversed(rewards):
            R = r + 0.95 * R
            discounted_rewards.insert(0, R)
            
        discounted_rewards = torch.tensor(discounted_rewards, device=device)
        discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-8)
        
        loss = 0
        for log_prob, reward in zip(log_probabilities, discounted_rewards):
            loss -= log_prob * reward
            
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        filled_count = env_agent.get_filled_orders_count()
        coffee_count = env_agent.get_coffee_served_count()
        history_scores.append(filled_count)
        
        if (iteration + 1) % 10 == 0:
            print(f"  Iteration {iteration+1:03d} -> Tables Served Coffee: {coffee_count}/{tables} | Fully Completed: {filled_count}/{tables}")
            
    plt.figure(figsize=(10, 5))
    plt.plot(history_scores, color='crimson', linewidth=2, label='2 Parallel Waitresses')
    plt.title(f'Parallel Group Scheduling Curve (10 Tables, Depth {depth})')
    plt.xlabel('Training Iterations')
    plt.ylabel('Fully Satisfied Tables')
    plt.grid(True)
    plt.savefig('scheduling_performance.png')
    print("\n📊 Done! Parallelized visualization saved to 'scheduling_performance.png'.")

if __name__ == "__main__":
    train_parallel_loop(iterations=200, schedule_horizon=80, depth=15, tables=10)
