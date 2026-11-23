import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# 3-AGENT MEGA-SCALE COMPILER (Base-100 Modular Arithmetic)
# =====================================================================
class TriAgentSharedResourceCompiler:
    def __init__(self, max_depth=15, num_tables=100):
        self.max_depth = max_depth
        self.d = num_tables  # Base-100 Width
        self.dim = self.d ** max_depth

    def apply_action(self, absolute_action, state_tuple):
        state_1, state_2, state_3, pot_status = state_tuple
        pot_val = int(pot_status.item())
        
        waitress_id = absolute_action // 4
        local_action_idx = absolute_action % 4
        
        # Courtesy Step Logic
        if local_action_idx == 1:
            if pot_val != 0 and pot_val != (waitress_id + 1):
                local_action_idx = 3  # Divert to courtesy housekeeping 'd'
            else:
                pot_val = waitress_id + 1
        
        elif local_action_idx == 2 and pot_val == (waitress_id + 1):
            pot_val = 0
            
        if waitress_id == 0:   target_idx = int(state_1.item())
        elif waitress_id == 1: target_idx = int(state_2.item())
        else:                  target_idx = int(state_3.item())
        
        # Matrix-free base-100 tree mutation math
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
# MEGA-SCALE TRI-STATE SCHEDULING AGENT
# =====================================================================
class TriAgentSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=15, num_tables=100):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        self.fc1 = torch.nn.Linear((max_depth * 3) + 1, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, 128)
        self.fc4 = torch.nn.Linear(128, 12)  
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_tuple):
        state_1, state_2, state_3, pot_status = state_tuple
        
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
# 100-TABLE TIME-LOCKED ENVIRONMENT
# =====================================================================
class TriAgentEnvironment:
    def __init__(self, num_tables=100, lock_duration=3):
        self.num_tables = num_tables
        self.lock_duration = lock_duration
        self.reset()

    def reset(self):
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        # Evenly distribute the 3 waitresses across 100 tables (0, 33, 66)
        self.waitress_focus = [0, 33, 66]
        self.pot_owner = 0  
        self.pot_lock_timer = 0
        
    def evaluate_step(self, absolute_action):
        reward = 0.0
        waitress_id = absolute_action // 4
        action_type = absolute_action % 4
        
        if self.pot_lock_timer > 0:
            self.pot_lock_timer -= 1
            if self.pot_lock_timer == 0:
                self.pot_owner = 0
                
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
# SCALED TRAINING LOOP RUNNER
# =====================================================================
def train_mega_loop(iterations=300, schedule_horizon=450, depth=15, tables=100):
    print("=== STARTING MEGA-SCALE TRI-AGENT SYSTEM (100 TABLES) ===")
    print(f"Tables: {tables} | Horizon: {schedule_horizon} | Lock: 3 Steps")
    
    compiler = TriAgentSharedResourceCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = TriAgentSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = TriAgentEnvironment(num_tables=tables, lock_duration=3)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.002)
    history_scores = []
    history_word_lengths = []
    
    for iteration in range(iterations):
        env_agent.reset()
        state_tuple = (
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0.0, device=device)
        )
        
        log_probabilities = []
        rewards = []
        active_op_count = 0
        
        for step in range(schedule_horizon):
            action_probs = scheduler_agent(state_tuple)
            action_dist = torch.distributions.Categorical(action_probs)
            action = action_dist.sample()
            
            log_probabilities.append(action_dist.log_prob(action))
            
            state_tuple = compiler.apply_action(action.item(), state_tuple)
            step_reward = env_agent.evaluate_step(action.item())
            rewards.append(step_reward)
            
            # Freeze geodesic tracking once all 100 tables are satisfied
            if env_agent.get_filled_orders_count() < tables:
                active_op_count += 1
                
            s1, s2, s3, _ = state_tuple
            state_tuple = (s1, s2, s3, torch.tensor(float(env_agent.pot_owner), device=device))
            
        # Optimization reward adjustments
        filled_count = env_agent.get_filled_orders_count()
        if filled_count == tables:
            efficiency_bonus = (schedule_horizon - active_op_count) * 0.5
            rewards[-1] += (100.0 + efficiency_bonus)
        else:
            rewards[-1] -= (tables - filled_count) * 5.0
            
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
        
        torch.nn.utils.clip_grad_norm_(scheduler_agent.parameters(), max_norm=1.0)
        optimizer.step()
        
        history_scores.append(filled_count)
        history_word_lengths.append(active_op_count)
        
        # Modified print frequency to handle the larger 1,000 iteration sweep cleanly
        if (iteration + 1) % 50 == 0:
            print(f"  Iteration {iteration+1:04d} -> Completed: {filled_count}/{tables} Tables | Cayley Path Length: {active_op_count}")
            
    fig, ax1 = plt.subplots(figsize=(10, 5))
    color = 'firebrick'
    ax1.set_xlabel('Training Iterations')
    ax1.set_ylabel('Fully Satisfied Tables', color=color)
    ax1.plot(history_scores, color=color, linewidth=2, label='Fulfillment Rate')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle=':')
    
    ax2 = ax1.twinx()  
    color = 'teal'
    ax2.set_ylabel('Active Cayley Word Length', color=color)
    ax2.plot(history_word_lengths, color=color, linewidth=1.5, linestyle='--', label='Word Compression')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Mega-Scale 100-Table Convergence Profile (Extended Training)')
    fig.tight_layout()
    plt.savefig('scheduling_performance.png')
    print("\n📊 Scaling complete! Metrics exported to 'scheduling_performance.png'.")

if __name__ == "__main__":
    # Expanded iterations to 1,000 to let the Neural Network fully optimize the base-100 tree
    train_mega_loop(iterations=1000, schedule_horizon=450, depth=9, tables=100)
