import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# KITE-FREE OMEGA-VECTOR COMPILER (Degree-3 Minimal Graph G_omega(\neg d))
# =====================================================================
class KiteFreeVectorGrigorchukCompiler:
    """
    Implements Theorem 3.1(b). Discards the redundant generator d_omega.
    The action pool only contains {a, b_omega, c_omega}. K_4 kites are flown away.
    """
    def __init__(self, max_depth=9, num_tables=100, omega_sequence=None):
        self.max_depth = max_depth
        self.d = num_tables
        if omega_sequence is None:
            self.omega = [0, 1, 2] * ((max_depth // 3) + 2)
        else:
            self.omega = omega_sequence

    def apply_action(self, absolute_action, state_tuple):
        """
        Compressed Action Space: 9 Tokens Total (3 choices per waitress)
        Waitress 0 -> a1=0, b1=1, c1=2
        Waitress 1 -> a2=3, b2=4, c2=5
        Waitress 2 -> a3=6, b3=7, c3=8
        """
        state_1, state_2, state_3, pot_A, pot_B = state_tuple
        pA = int(pot_A.item())
        pB = int(pot_B.item())
        
        # De-multiplex from 3 choices per waitress instead of 4
        waitress_id = absolute_action // 3
        local_action_idx = absolute_action % 3
        w_flag = waitress_id + 1
        
        # Resource Pipeline for Coffee: local_action 1 is 'b'
        if local_action_idx == 1:
            if pA == w_flag or pB == w_flag:
                pass
            elif pA == 0:  pA = w_flag
            elif pB == 0:  pB = w_flag
            else:          local_action_idx = 3 # Divert to a clean placeholder wait state
        
        # Release resource flag on meal: local_action 2 is 'c'
        elif local_action_idx == 2:
            if pA == w_flag: pA = 0
            if pB == w_flag: pB = 0
            
        if waitress_id == 0:   target_idx = int(state_1.item())
        elif waitress_id == 1: target_idx = int(state_2.item())
        else:                  target_idx = int(state_3.item())
        
        # -------------------------------------------------------------
        # THE CORE DECOUPLED MATRIX-FREE ALGEBRA
        # -------------------------------------------------------------
        if local_action_idx == 0:
            # Action 'a': Root level permutation Pi
            root_weight = self.d ** (self.max_depth - 1)
            root_digit = (target_idx // root_weight) % self.d
            new_root_digit = (root_digit + 1) % self.d
            target_idx = target_idx - (root_digit * root_weight) + (new_root_digit * root_weight)
        
        # FIX: Check if local_action_idx matches generators b (1) or c (2) using explicit bracket formatting
        elif local_action_idx >0:
            # Evaluates {b, c} recursively using your paper's exact row lookup vectors
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
                    omega_val = self.omega[current_layer]
                    row_idx = local_action_idx - 1 # Map b->Row 0, c->Row 1
                    
                    is_permutation_pi = False
                    if omega_val == 0 and row_idx == 0:  is_permutation_pi = True  # Vector 0: b=Pi
                    elif omega_val == 1 and row_idx < 2: is_permutation_pi = True # Vector 1: b=Pi, c=Pi
                    elif omega_val == 2 and row_idx == 1: is_permutation_pi = True # Vector 2: c=Pi (d is dropped!)
                    
                    if is_permutation_pi:
                        new_digit = (digit + 1) % self.d
                        target_idx = target_idx - (digit * divisor) + (new_digit * divisor)
                        break
                        
                divisor //= self.d
                current_layer += 1
                
        return (
            torch.tensor(target_idx, device=device), 
            state_2, state_3, 
            torch.tensor(pA, device=device), 
            torch.tensor(pB, device=device)
        )

# =====================================================================
# KITE-FREE SCHEDULING AGENT
# =====================================================================
class KiteFreeSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=9, num_tables=100):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_tables
        self.fc1 = torch.nn.Linear((max_depth * 3) + 2, 512)
        self.fc2 = torch.nn.Linear(512, 256)
        self.fc3 = torch.nn.Linear(256, 128)
        self.fc4 = torch.nn.Linear(128, 9)  # Compressed output layer size from 12 to 9!
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
# ENVIRONMENT CONFIGURATION
# =====================================================================
class KiteFreeEnvironment:
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
        waitress_id = absolute_action // 3
        action_type = absolute_action % 3
        w_flag = waitress_id + 1
        
        if self.pot_A_timer > 0:
            self.pot_A_timer -= 1
            if self.pot_A_timer == 0: self.pot_A_owner = 0
        if self.pot_B_timer > 0:
            self.pot_B_timer -= 1
            if self.pot_B_timer == 0: self.pot_B_owner = 0
                
        # Intercept action if both pots are occupied
        if action_type == 1:
            if (self.pot_A_owner != 0 and self.pot_A_owner != w_flag) and \
               (self.pot_B_owner != 0 and self.pot_B_owner != w_flag):
                action_type = 3 # Re-route to standard placeholder wait condition
            
        if action_type == 1:
            if self.pot_A_owner == w_flag or self.pot_B_owner == w_flag:
                pass
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
            if self.pot_A_owner == w_flag: self.pot_A_owner, self.pot_A_timer = 0, 0
            if self.pot_B_owner == w_flag: self.pot_B_owner, self.pot_B_timer = 0, 0
            self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
        else:
            reward -= 0.1
            if action_type == 3:
                self.waitress_focus[waitress_id] = (self.waitress_focus[waitress_id] + 1) % self.num_tables
                
        return reward

    def get_filled_orders_count(self): return int(np.sum(self.table_stages == 3))
    def get_coffee_served_count(self): return int(np.sum(self.table_stages >= 2))

# =====================================================================
# INTEGRATED KITE-FREE EXECUTION LOOP
# =====================================================================
def train_kite_free_loop(iterations=400, schedule_horizon=450, depth=9, tables=100):
    print("=== STARTING THE KITE-FREE OPEN SYSTEM (100 TABLES) ===")
    print(f"Tables: {tables} | Horizon: {schedule_horizon} | Minimal Graph Geometry: G_omega(\\neg d)")
    
    custom_omega = [0, 1, 2] * ((depth // 3) + 2)
    compiler = KiteFreeVectorGrigorchukCompiler(max_depth=depth, num_tables=tables, omega_sequence=custom_omega)
    scheduler_agent = KiteFreeSchedulingAgent(max_depth=depth, num_tables=tables).to(device)
    env_agent = KiteFreeEnvironment(num_tables=tables, lock_duration=3)
    
    optimizer = torch.optim.Adam(scheduler_agent.parameters(), lr=0.001)
    history_scores = []
    history_word_lengths = []
    
    for iteration in range(iterations):
        env_agent.reset()
        state_tuple = (
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0, device=device), 
            torch.tensor(0.0, device=device), 
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
    
    plt.title('Mega-Scale 100-Table Convergence Profile (Kites Flown Away)')
    fig.tight_layout()
    plt.savefig('scheduling_performance.png')
    print("\n?? Kites cleared! Metrics exported to 'scheduling_performance.png'.")

if __name__ == "__main__":
    train_kite_free_loop(iterations=1500, schedule_horizon=450, depth=9, tables=100)
