import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =====================================================================
# ZERO-VRAM TENSOR COMPILER (Bypasses Matrix Memory Wall)
# =====================================================================
class InfiniteScaleGrigorchukCompiler:
    def __init__(self, max_depth=20):
        self.max_depth = max_depth
        self.dim = 2 ** max_depth

    def apply_action(self, action_idx, state_idx):
        """ Applies a generator (a=0, b=1, c=2, d=3) via pure binary index math """
        idx = int(state_idx.item())
        if action_idx == 0:
            return torch.tensor(idx ^ (1 << (self.max_depth - 1)), device=device)
        
        bit_position = self.max_depth - 1
        while bit_position >= 0:
            bit = (idx >> bit_position) & 1
            if bit == 0:
                if bit_position > 0:
                    idx ^= (1 << (bit_position - 1))
                break
            else:
                if action_idx == 1:   action_idx = 2
                elif action_idx == 2: action_idx = 3
                elif action_idx == 3: action_idx = 1
            bit_position -= 1
        return torch.tensor(idx, device=device)

# =====================================================================
# COMPACT SCHEDULING AGENT
# =====================================================================
class CompactGrigorchukSchedulingAgent(torch.nn.Module):
    def __init__(self, max_depth=20):
        super().__init__()
        self.max_depth = max_depth
        self.fc1 = torch.nn.Linear(max_depth, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, 4) 
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, state_idx):
        idx_val = int(state_idx.item())
        bits = [(idx_val >> i) & 1 for i in range(self.max_depth)]
        state_tensor = torch.tensor(bits, dtype=torch.float32, device=device)
        x = torch.relu(self.fc1(state_tensor))
        x = torch.relu(self.fc2(x))
        return self.softmax(self.fc3(x))

# =====================================================================
# FIXED ENVIRONMENT AGENT (Decoupled from Leaf Index scale)
# =====================================================================
class FixedRestaurantEnvironmentAgent:
    def __init__(self):
        self.reset()

    def reset(self):
        # 5 customers: 0=start, 1=ordered, 2=got_coffee, 3=got_meal (fulfilled)
        self.customer_stages = np.zeros(5, dtype=int)
        self.current_customer = 0  # Round-robin customer focus tracker
        
    def evaluate_step(self, action_type):
        """
        Directly evaluates the group action token to prevent sparse rewards.
        action_type: 0=a, 1=b, 2=c, 3=d
        Maps group tokens directly to workflow state logic.
        """
        reward = 0.0
        cust = self.current_customer
        current_stage = self.customer_stages[cust]
        
        # Rule 1: Action 'a' -> Takes the order if they haven't ordered yet
        if action_type == 0 and current_stage == 0:
            self.customer_stages[cust] = 1
            reward += 5.0
            
        # Rule 2: Action 'b' -> Serves coffee if order is placed
        elif action_type == 1 and current_stage == 1:
            self.customer_stages[cust] = 2
            reward += 10.0
            
        # Rule 3: Action 'c' -> Serves meal if coffee is served
        elif action_type == 2 and current_stage == 2:
            self.customer_stages[cust] = 3
            reward += 20.0
            # Move focus to next customer once fully served
            self.current_customer = (self.current_customer + 1) % 5
            
        # Rule 4: Action 'd' -> Standard housekeeping/idle step
        else:
            reward -= 0.5  # Soft penalty for out-of-order execution
            # Rotate customer focus anyway to prevent stagnation
            if action_type == 3:
                self.current_customer = (self.current_customer + 1) % 5
                
        return reward

    def get_filled_orders_count(self):
        return int(np.sum(self.customer_stages == 3))
        
    def get_coffee_served_count(self):
        return int(np.sum(self.customer_stages >= 2))

# =====================================================================
# INTEGRATED MULTI-AGENT LOOP
# =====================================================================
def train_hierarchical_loop(iterations=200, schedule_horizon=40, depth=20):
    print("=== STARTING DECOUPLED DEEP MULTI-AGENT LOOP ===")
    print(f"Executing on: {device} | Horizon Steps: {schedule_horizon} | Iterations: {iterations} | Tree Depth: {depth}")
    
    compiler = InfiniteScaleGrigorchukCompiler(max_depth=depth)
    scheduler_agent = CompactGrigorchukSchedulingAgent(max_depth=depth).to(device)
    env_agent = FixedRestaurantEnvironmentAgent()
    
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
            
            # Step 1: Evolve the Group element mathematically on the infinite tree
            state_idx = compiler.apply_action(action.item(), state_idx)
            
            # Step 2: Feed action natively to workflow engine to get a clean feedback loop
            step_reward = env_agent.evaluate_step(action.item())
            rewards.append(step_reward)
            
        # Standard REINFORCE optimization policy block
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
            print(f"  Iteration {iteration+1:03d} -> Customers Served Coffee: {coffee_count}/5 | Fully Completed: {filled_count}/5")
            
    plt.figure(figsize=(10, 5))
    plt.plot(history_scores, color='green', linewidth=2, label=f'Decoupled Depth-{depth}')
    plt.title(f'Decoupled Restaurant Order Fulfillment (Tree Depth = {depth})')
    plt.xlabel('Training Iterations')
    plt.ylabel('Fully Completed Orders')
    plt.grid(True)
    plt.savefig('scheduling_performance.png')
    print("\n📊 Done! The revised visualization has been output to 'scheduling_performance.png'.")

if __name__ == "__main__":
    train_hierarchical_loop(iterations=200, schedule_horizon=40, depth=20)
