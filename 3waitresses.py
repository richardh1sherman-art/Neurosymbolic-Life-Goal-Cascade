import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# 3-AGENT SHARED-RESOURCE COMPILER (4-Tuple State Space)
# =====================================================================
class TriAgentSharedResourceCompiler:
    def __init__(self, max_depth=15, num_tables=100):
        self.max_depth = max_depth
        self.d = num_tables
        self.dim = self.d ** max_depth

    def apply_action(self, absolute_action, state_tuple):
        """
        State Tuple: (state_1, state_2, state_3, pot_status)
        pot_status: 0=Free, 1=W1, 2=W2, 3=W3
        """
        state_1, state_2, state_3, pot_status = state_tuple
        pot_val = int(pot_status.item())
        
        # Determine which of the 3 waitresses is acting (0, 1, or 2)
        waitress_id = absolute_action // 4
        local_action_idx = absolute_action % 4
        
        # Courtesy Step Logic: Action 1 is 'b' (Serve Coffee)
        if local_action_idx == 1:
            if pot_val != 0 and pot_val != (waitress_id + 1):
                # Pot is blocked by someone else's lockout! Force courtesy idle 'd'
                local_action_idx = 3 
            else:
                pot_val = waitress_id + 1
        
        # Action 2 is 'c' (Serve Meal) -> Voluntary release
        elif local_action_idx == 2 and pot_val == (waitress_id + 1):
            pot_val = 0
            
        # Select the targeted index subspace
        if waitress_id == 0:   target_idx = int(state_1.item())
        elif waitress_id == 1: target_idx = int(state_2.item())
        else:                  target_idx = int(state_3.item())
        
        # Base-d tree index mutation math
        if local_action_idx == 0:
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (target_idx // root_weight) % self.d
            new_root_digit = (root_digit + 1) % self.d
            target_idx = target_idx - (root_digit * root_weight) + (new_root_digit * root_weight)
        else:
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
                
        new_pot_status = torch.tensor(pot_val, device=device)
        
        if waitress_id == 0:
            return torch.tensor(target_idx, device=device), state_2, state_3, new_pot_status
        elif waitress_id == 1:
            return state_1, torch.tensor(target_idx, device=device), state_3, new_pot_status
        else:
            return state_1, state_2, torch.tensor(target_idx, device=device), new_pot_status

# =====================================================================
# THREE-BODY TRI-STATE SCHEDULING AGENT
# =====================================================================
class TriAgentSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=15, num_tables=10):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        self.fc1 = torch.nn.Linear((max_depth * 3) + 1, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, 128)
        # Fix: Just pass 12 as the output dimension (for our 12 generators)
        self.fc4 = torch.nn.Linear(128, 12)  
        self.softmax = torch.nn.Softmax(dim=-1)


    def forward(self, state_tuple):
        state_1, state_2, state_3, pot_status = state_tuple
        
        # Unpack indices for all three branches
        features = []
        for s in [state_1, state_2, state_3]:
            temp = int(s.item())
            for _ in range(self.max_depth):
                features.append(temp % self.d)
                temp //= self.d
                
        features.append(float(pot_status.item()))
        state_tensor = torch.tensor(features, dtype=torch.float32, device=device)
        
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.softmax(self.fc4(x))

# =====================================================================
# 3-BODY TIME-LOCKED ENVIRONMENT
# =====================================================================
class TriAgentEnvironment:
    def __init__(self, num_tables=10, lock_duration=3):
        self.num_tables = num_tables
        self.lock_duration = lock_duration
        self.reset()

    def reset(self):
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        # Staggered startup focuses: W1 starts at table 0, W2 starts at table 3, W3 starts at table 6
        self.waitress_focus = [0, 3, 6]
        self.pot_owner = 0  # 0=Free, 1=W1, 2=W2, 3=W3
        self.pot_lock_timer = 0  # Measures remaining steps for duration lock

        
    def evaluate_step(self, absolute_action):
        reward = 0.0
        waitress_id = absolute_action // 4
        action_type = absolute_action % 4
        
        # Lockout clock countdown
        if self.pot_lock_timer > 0:
            self.pot_lock_timer -= 1
            if self.pot_lock_timer == 0:
                self.pot_owner = 0
                
        # Courtesy intercept check
        if action_type == 1 and self.pot_owner != 0 and self.pot_owner != (waitress_id + 1):
            action_type = 3
            
        if action_type == 1 and self.pot_owner == 0:
            self.pot_owner = waitress_id + 1
            self.pot_lock_timer = self.lock_duration
            
        t = self.waitress_focus[waitress_id]
        current_stage = self.table_stages[t]
        
        if action_type == 0 and current_stage == 0:
            self.table_stages[t] = 1
            reward += 5.0
        elif action_type == 1 and current_stage == 1:
            self.table_stages[t] = 2
            reward += 10.0
        elif action_type == 2 and current_stage == 2:
            self.table_stages[t] = 3
            reward += 20.0
            if self.pot_owner == (waitress_id + 1):
                self.pot_owner = 0
                self.pot_lock_timer = 0
            self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
        else:
            reward -= 0.1
            if action_type == 3:
                self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
                
        return reward

    def get_filled_orders_count(self): return int(np.sum(self.table_stages == 3))
    def get_coffee_served_count(self): return int(np.sum(self.table_stages >= 2))

# =====================================================================
# TRI-AGENT TRAINING RUNNER
# =====================================================================
def train_tri_loop(iterations=250, schedule_horizon=130, depth=15, tables=10):
    print("=== STARTING TRI-AGENT SYSTEM (3 WAITRESSES / 12 GENERATORS) ===")
    print(f"Tables: {tables} | Horizon: {schedule_horizon} | Lock: 3 Steps")
    
    compiler = TriAgentSharedResourceCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = TriAgentSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = TriAgentEnvironment(num_tables=tables, lock_duration=3)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.002)
    history_scores = []
    
    for iteration in range(iterations):
        env_agent.reset()
        
        # 4-Tuple State initialization
        state_tuple = (
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0.0, device=device)
        )
        
        log_probabilities = []
        rewards = []
        
        for step in range(schedule_horizon):
            action_probs = scheduler_agent(state_tuple)
            action_dist = torch.distributions.Categorical(action_probs)
            action = action_dist.sample()
            
            log_probabilities.append(action_dist.log_prob(action))
            
            # Update compiler and environment states
            state_tuple = compiler.apply_action(action.item(), state_tuple)
            step_reward = env_agent.evaluate_step(action.item())
            rewards.append(step_reward)
            
            # Sync pot ownership metrics correctly across the 4-tuple layout
            state_tuple = (state_tuple[0], state_tuple[1], state_tuple[2], torch.tensor(float(env_agent.pot_owner), device=device))

            
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
    plt.plot(history_scores, color='firebrick', linewidth=2, label='3 Waitresses (Heavy Contention)')
    plt.title('Tri-Agent Parallel Scheduling Under High Pot Contention')
    plt.xlabel('Training Iterations')
    plt.ylabel('Fully Satisfied Tables')
    plt.grid(True)
    plt.savefig('scheduling_performance.png')
    print("\n📊 Done! Tri-agent configuration visualization saved to 'scheduling_performance.png'.")

if __name__ == "__main__":
    # Increased horizon to 130 to give 3 waitresses plenty of breathing room to share!
    train_tri_loop(iterations=250, schedule_horizon=130, depth=15, tables=10)
