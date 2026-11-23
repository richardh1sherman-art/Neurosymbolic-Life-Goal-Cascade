import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# WIDE-TREE NON-ABELIAN COMPILER (Base-d Modular Arithmetic)
# =====================================================================
class InfiniteScaleWideGrigorchukCompiler:
    """
    Implements a generalized Grigorchuk group acting on a d-ary tree.
    Instead of binary bits, it uses base-d math to handle many tables.
    """
    def __init__(self, max_depth=15, num_tables=10):
        self.max_depth = max_depth
        self.d = num_tables  # Alphabet size / Number of tables
        self.dim = self.d ** max_depth

    def apply_action(self, action_idx, state_idx):
        """
        Applies a generator (a=0, b=1, c=2, d=3) to a base-d index.
        Memory footprint is O(1) even if the state space has trillions of elements.
        """
        idx = int(state_idx.item())
        
        # We process the index by working with its base-d digits.
        # To avoid actual string formatting, we use modular division.
        
        if action_idx == 0:
            # Generator 'a' cycles the root digit of the tree modulo d
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (idx // root_weight) % self.d
            new_root_digit = (root_digit + 1) % self.d
            
            # Reconstruct the index with the shifted root digit
            idx = idx - (root_digit * root_weight) + (new_root_digit * root_weight)
            return torch.tensor(idx, device=device)
        
        # For generators b, c, and d, trace down the base-d tree levels
        divisor = self.d ** (self.max_depth - 1)
        current_depth = 0
        
        while divisor > 0 and current_depth < self.max_depth:
            digit = (idx // divisor) % self.d
            
            if digit == 0:
                # Level matches the '0' branch rule: apply an 'a' action to the remainder
                next_level_weight = divisor // self.d
                if next_level_weight > 0:
                    sub_digit = (idx // next_level_weight) % self.d
                    new_sub_digit = (sub_digit + 1) % self.d
                    idx = idx - (sub_digit * next_level_weight) + (new_sub_digit * next_level_weight)
                break
            else:
                # Non-zero branch rule: permute the action ID according to the Grigorchuk cycle
                if action_idx == 1:   action_idx = 2  # b -> c
                elif action_idx == 2: action_idx = 3  # c -> d
                elif action_idx == 3: action_idx = 1  # d -> b
            
            divisor //= self.d
            current_depth += 1
            
        return torch.tensor(idx, device=device)

# =====================================================================
# WIDE SCHEDULING AGENT (Base-d Input Embedding)
# =====================================================================
class WideTreeSchedulingAgent(torch.nn.Module):
    """
    Instead of flat bits, this agent unpacks the state index into its 
    base-d digit configuration. Input size is exactly equal to the depth.
    """
    def __init__(self, max_depth=15, num_tables=10):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        
        # Network inputs match the number of steps in the path sequence
        self.fc1 = torch.nn.Linear(max_depth, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, 4) 
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_idx):
        idx_val = int(state_idx.item())
        
        # Unpack the integer into its base-d digits to feed into the NN
        digits = []
        temp = idx_val
        for _ in range(self.max_depth):
            digits.append(temp % self.d)
            temp //= self.d
            
        state_tensor = torch.tensor(digits, dtype=torch.float32, device=device)
        
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        return self.softmax(self.fc3(x))

# =====================================================================
# MULTI-TABLE ENVIRONMENT AGENT
# =====================================================================
class MultiTableEnvironmentAgent:
    def __init__(self, num_tables=10):
        self.num_tables = num_tables
        self.reset()

    def reset(self):
        # Tracking states for all tables simultaneously: 0=empty, 1=ordered, 2=coffee, 3=done
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        self.active_table = 0 
        
    def evaluate_step(self, action_type):
        reward = 0.0
        t = self.active_table
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
            # Table is satisfied, advance focus to the next table
            self.active_table = (self.active_table + 1) % self.num_tables
            
        # Rule 4: Action 'd' -> Shift focus / clean up
        else:
            reward -= 0.3 
            if action_type == 3:
                self.active_table = (self.active_table + 1) % self.num_tables
                
        return reward

    def get_filled_orders_count(self):
        return int(np.sum(self.table_stages == 3))
        
    def get_coffee_served_count(self):
        return int(np.sum(self.table_stages >= 2))

# =====================================================================
# WIDE RUNNER LOOP
# =====================================================================
def train_wide_loop(iterations=200, schedule_horizon=60, depth=15, tables=10):
    print("=== STARTING NON-ABELIAN MULTI-TABLE LOOP ===")
    print(f"Tables (Width): {tables} | Tree Depth: {depth} | Horizon: {schedule_horizon}")
    
    compiler = InfiniteScaleWideGrigorchukCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = WideTreeSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = MultiTableEnvironmentAgent(num_tables=tables)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.005)
    history_scores = []
    
    for iteration in range(iterations):
        env_agent.reset()
        state_idx = torch.tensor(0, device=device)
        
        log_probabilities = []
        rewards = []
        
        for step in range(schedule_horizon):
            action_probs = scheduler_agent(state_idx)
            action_dist = torch.distributions.Categorical(action_probs)
            action = action_dist.sample()
            
            log_probabilities.append(action_dist.log_prob(action))
            
            # Matrix-free base-d step evolution
            state_idx = compiler.apply_action(action.item(), state_idx)
            
            step_reward = env_agent.evaluate_step(action.item())
            rewards.append(step_reward)
            
        # REINFORCE policy processing
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
    plt.plot(history_scores, color='darkorange', linewidth=2, label=f'{tables}-Table System')
    plt.title(f'Multi-Table Execution Curve (Width={tables}, Depth={depth})')
    plt.xlabel('Training Iterations')
    plt.ylabel('Fully Satisfied Tables')
    plt.grid(True)
    plt.savefig('scheduling_performance.png')
    print("\n📊 Done! Broadened visualization saved to 'scheduling_performance.png'.")

if __name__ == "__main__":
    # We increased horizon steps slightly to give the agent time to visit all 10 tables!
    train_wide_loop(iterations=200, schedule_horizon=80, depth=15, tables=10)
