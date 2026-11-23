import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# DUAL-RESOURCE MEGA-SCALE COMPILER (5-Tuple State Space)
# =====================================================================
class DualPotSharedResourceCompiler:
    def __init__(self, max_depth=9, num_tables=100):
        self.max_depth = max_depth
        self.d = num_tables  
        self.dim = self.d ** max_depth

    def apply_action(self, absolute_action, state_tuple):
        """
        State Tuple layout: (state_1, state_2, state_3, pot_A, pot_B)
        pot_A, pot_B: 0=Free, 1=W1, 2=W2, 3=W3
        """
        state_1, state_2, state_3, pot_A, pot_B = state_tuple
        pA = int(pot_A.item())
        pB = int(pot_B.item())
        
        waitress_id = absolute_action // 4
        local_action_idx = absolute_action % 4
        w_flag = waitress_id + 1
        
        # Courtesy Step Logic: Action 1 is 'b' (Serve Coffee)
        if local_action_idx == 1:
            # Check if this waitress already owns a pot
            if pA == w_flag or pB == w_flag:
                pass 
            # If not, try to claim Pot A first, then Pot B
            elif pA == 0:
                pA = w_flag
            elif pB == 0:
                pB = w_flag
            else:
                # BOTH POTS ARE BUSY: Force courtesy idle 'd' (token 3)
                local_action_idx = 3 
        
        # Action 2 is 'c' (Serve Meal) -> Release whatever pot she holds
        elif local_action_idx == 2:
            if pA == w_flag: pA = 0
            if pB == w_flag: pB = 0
            
        # Select the active tree coordinate subspace
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
                
        return (
            torch.tensor(target_idx, device=device), 
            state_2, state_3, 
            torch.tensor(pA, device=device), 
            torch.tensor(pB, device=device)
        )

# =====================================================================
# DUAL-POT SCHEDULING AGENT
# =====================================================================
class DualPotSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=9, num_tables=100):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        # Inputs: 3 Waitresses * max_depth digits + 2 elements for both pots
        self.fc1 = torch.nn.Linear((max_depth * 3) + 2, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, 128)
        self.fc4 = torch.nn.Linear(128, 12)  
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_tuple):
        state_1, state_2, state_3, pot_A, pot_B = state_tuple
        
        features = []
        for s in [state_1, state_2, state_3]:
            temp = int(s.item())
            for _ in range(self.max_depth):
                features.append(temp % self.d)
                temp //= self.d
                
        features.append(float(pot_A.item()))
        features.append(float(pot_B.item()))
        state_tensor = torch.tensor(features, dtype=torch.float32, device=device)
        
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.softmax(self.fc4(x))

# =====================================================================
# DUAL-POT TIME-LOCKED ENVIRONMENT
# =====================================================================
class DualPotEnvironment:
    def __init__(self, num_tables=100, lock_duration=3):
        self.num_tables = num_tables
        self.lock_duration = lock_duration
        self.reset()

    def reset(self):
        self.table_stages = np.zeros(self.num_tables, dtype=int)
        self.waitress_focus = [0, 33, 66]
        self.pot_A_owner = 0  
        self.pot_B_owner = 0  
        self.pot_A_timer = 0
        self.pot_B_timer = 0
        
    def evaluate_step(self, absolute_action):
        reward = 0.0
        waitress_id = absolute_action // 4
        action_type = absolute_action % 4
        w_flag = waitress_id + 1
        
        # Countdown lockout timers
        if self.pot_A_timer > 0:
            self.pot_A_timer -= 1
            if self.pot_A_timer == 0: self.pot_A_owner = 0
        if self.pot_B_timer > 0:
            self.pot_B_timer -= 1
            if self.pot_B_timer == 0: self.pot_B_owner = 0
                
        # Courtesy intercept check: if trying to pour coffee but both locked, force wait 'd'
        if action_type == 1:
            if (self.pot_A_owner != 0 and self.pot_A_owner != w_flag) and \
               (self.pot_B_owner != 0 and self.pot_B_owner != w_flag):
                action_type = 3
            
        # Trigger successful coffee locks
        if action_type == 1:
            if self.pot_A_owner == w_flag or self.pot_B_owner == w_flag:
                pass # Already holds one
            elif self.pot_A_owner == 0:
                self.pot_A_owner = w_flag
                self.pot_A_timer = self.lock_duration
            elif self.pot_B_owner == 0:
                self.pot_B_owner = w_flag
                self.pot_B_timer = self.lock_duration
            
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
            # Release pots upon serving final meal
            if self.pot_A_owner == w_flag: {self.pot_A_owner == 0, self.pot_A_timer == 0}
            if self.pot_B_owner == w_flag: {self.pot_B_owner == 0, self.pot_B_timer == 0}
            self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
        else:
            reward -= 0.1
            if self.pot_owner_check(w_flag) and action_type == 3:
                # Voluntarily drop if idling to be a good coworker
                if self.pot_A_owner == w_flag: self.pot_A_owner, self.pot_A_timer = 0, 0
                if self.pot_B_owner == w_flag: self.pot_B_owner, self.pot_B_timer = 0, 0
            if action_type == 3:
                self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
                
        return reward

    def pot_owner_check(self, w_flag):
        return self.pot_A_owner == w_flag or self.pot_B_owner == w_flag

    def get_filled_orders_count(self): return int(np.sum(self.table_stages == 3))
    def get_coffee_served_count(self): return int(np.sum(self.table_stages >= 2))

# =====================================================================
# DUAL-POT MAIN RUNNER
# =====================================================================
def train_dual_pot_loop(iterations=300, schedule_horizon=450, depth=9, tables=100):
    print("=== STARTING UPGRADED DUAL-POT SYSTEM (100 TABLES) ===")
    print(f"Tables: {tables} | Horizon: {schedule_horizon} | Infrastructures: 2 Coffee Pots")
    
    compiler = DualPotSharedResourceCompiler(max_depth=depth, num_tables=tables)
    scheduler_agent = DualPotSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = DualPotEnvironment(num_tables=tables, lock_duration=3)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.002)
    history_scores = []
    history_word_lengths = []
    
    for iteration in range(iterations):
        env_agent.reset()
        state_tuple = (
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0.0, device=device), # Pot A
            torch.tensor(0.0, device=device)  # Pot B
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
            
            if env_agent.get_filled_orders_count() < tables:
                active_op_count += 1
                
            s1, s2, s3, _, _ = state_tuple
            state_tuple = (
                s1, s2, s3, 
                torch.tensor(float(env_agent.pot_A_owner), device=device),
                torch.tensor(float(env_agent.pot_B_owner), device=device)
            )
            
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
    
    plt.title('Mega-Scale 100-Table Convergence Profile (Dual Coffee Pots)')
    fig.tight_layout()
    plt.savefig('scheduling_performance.png')
    print("\n📊 Equipment upgraded! Metrics exported to 'scheduling_performance.png'.")

if __name__ == "__main__":
    train_dual_pot_loop(iterations=300, schedule_horizon=450, depth=9, tables=100)
