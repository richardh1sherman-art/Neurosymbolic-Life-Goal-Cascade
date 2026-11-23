import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# DURATION-LOCKED SHARED-RESOURCE COMPILER (Tuple State Space)
# =====================================================================
class DurationLockedGrigorchukCompiler:
    def __init__(self, max_depth=15, num_tables=10):
        self.max_depth = max_depth
        self.d = num_tables
        self.dim = self.d ** max_depth

    def apply_action(self, absolute_action, state_tuple):
        """
        State Tuple: (state_1, state_2, pot_status)
        pot_status represents who holds the pot. The duration/lockout math 
        is managed by the environment tracking steps.
        """
        state_1, state_2, pot_status = state_tuple
        pot_val = int(pot_status.item())
        
        waitress_id = absolute_action // 4
        local_action_idx = absolute_action % 4
        
        # Courtesy Step Logic: Action 1 is 'b' (Serve Coffee)
        if local_action_idx == 1:
            if pot_val != 0 and pot_val != (waitress_id + 1):
                # Pot is occupied by the other agent's duration lock! Divert to 'd'
                local_action_idx = 3 
            else:
                # Claim the pot
                pot_val = waitress_id + 1
        
        # Action 2 is 'c' (Serve Meal) -> Voluntary release if they still have it
        elif local_action_idx == 2 and pot_val == (waitress_id + 1):
            pot_val = 0
            
        # Execute base-d tree index math for the active waitress
        target_idx = int(state_1.item()) if waitress_id == 0 else int(state_2.item())
        
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
            return torch.tensor(target_idx, device=device), state_2, new_pot_status
        else:
            return state_1, torch.tensor(target_idx, device=device), new_pot_status

# =====================================================================
# RESOURCE-AWARE SCHEDULING AGENT
# =====================================================================
class ResourceAwareSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=15, num_tables=10):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        self.fc1 = torch.nn.Linear((max_depth * 2) + 1, 256)
        self.fc2 = torch.nn.Linear(256, 128)
        self.fc3 = torch.nn.Linear(128, 8) 
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_tuple):
        state_1, state_2, pot_status = state_tuple
        
        digits_1 = []
        temp1 = int(state_1.item())
        for _ in range(self.max_depth):
            digits_1.append(temp1 % self.d)
            temp1 //= self.d
            
        digits_2 = []
        temp2 = int(state_2.item())
        for _ in range(self.max_depth):
            digits_2.append(temp2 % self.d)
            temp2 //= self.d
            
        joint_features = digits_1 + digits_2 + [float(pot_status.item())]
        state_tensor = torch.tensor(joint_features, dtype=torch.float32, device=device)
        
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        return self.softmax(self.fc3(x))

# =====================================================================
# ENVIRONMENT WITH DURATION LOCKOUT LOGIC
# =====================================================================
class DurationLockedEnvironment:
    def __init__(self, num_tables=10, lock_duration=3):
        self.num_tables = num_tables
        self.lock_duration = lock_duration
        self.reset()

    def reset(self):
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        # Distributed startup focus: Waitress 1 starts at table 0, Waitress 2 starts at table 5
        self.waitress_focus = [0, 5]
        self.pot_owner = 0  # 0=Free, 1=W1, 2=W2
        self.pot_lock_timer = 0  # Measures remaining steps for duration lock

        
    def evaluate_step(self, absolute_action):
        reward = 0.0
        waitress_id = absolute_action // 4
        action_type = absolute_action % 4
        
        # Tick down the physical duration timer at the start of every step
        if self.pot_lock_timer > 0:
            self.pot_lock_timer -= 1
            if self.pot_lock_timer == 0:
                self.pot_owner = 0  # Duration complete, coffee pot is released!
        
        # Intercept conflict if the pot is actively locked by someone else
        if action_type == 1 and self.pot_owner != 0 and self.pot_owner != (waitress_id + 1):
            action_type = 3  # Force courtesy shift to housekeeping
        
        # Triggering a successful coffee grab sets the duration lock
        if action_type == 1 and self.pot_owner == 0:
            self.pot_owner = waitress_id + 1
            self.pot_lock_timer = self.lock_duration  # Pot is now locked for N steps
            
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
            if self.pot_owner == (waitress_id + 1):
                self.pot_owner = 0
                self.pot_lock_timer = 0
            self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
            
        # Rule 4: Action 'd' -> Polite Housekeeping / Wait step
        else:
            reward -= 0.1
            if action_type == 3:
                self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
                
        return reward

    def get_filled_orders_count(self): return int(np.sum(self.table_stages == 3))
    def get_coffee_served_count(self): return int(np.sum(self.table_stages >= 2))

# =====================================================================
# MAIN EXECUTOR
# =====================================================================
def train_duration_loop(iterations=200, schedule_horizon=120, depth=15, tables=10):
    print("=== STARTING DURATION-LOCKED RESOURCE SCHEDULER ===")
    print(f"Tables: {tables} | Horizon: {schedule_horizon} | Coffee Pot Lock: 3 Steps")
    
    compiler = DurationLockedGrigorchukCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = ResourceAwareSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = DurationLockedEnvironment(num_tables=tables, lock_duration=3)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.003)
    history_scores = []
    
    for iteration in range(iterations):
        env_agent.reset()
        state_tuple = (torch.tensor(0, device=device), torch.tensor(0, device=device), torch.tensor(0.0, device=device))
        
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
            
            # Sync compiler pot state with the environment's internal duration clock
            state_tuple = (state_tuple[0], state_tuple[1], torch.tensor(float(env_agent.pot_owner), device=device))
            
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
    plt.plot(history_scores, color='teal', linewidth=2, label='3-Step Lockout Model')
    plt.title('Parallel Scheduling Stabilized with Duration Lockouts')
    plt.xlabel('Training Iterations')
    plt.ylabel('Fully Satisfied Tables')
    plt.grid(True)
    plt.savefig('scheduling_performance.png')
    print("\n📊 Done! The revised visualization has been output to 'scheduling_performance.png'.")

if __name__ == "__main__":
    train_duration_loop(iterations=200, schedule_horizon=120, depth=15, tables=10)
