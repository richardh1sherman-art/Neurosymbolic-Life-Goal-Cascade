import torch
import torch.nn as nn

class LearningGroupProverAgent(nn.Module):
    def __init__(self, max_depth=9, num_axioms=14):
        super().__init__()
        self.max_depth = max_depth
        self.d = num_axioms
        
        self.shared_layer = nn.Sequential(
            nn.Linear(max_depth * 3, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU()
        )
        self.actor_head = nn.Sequential(
            nn.Linear(128, 42),
            nn.Softmax(dim=-1)
        )
        self.critic_head = nn.Linear(128, 1)

    def forward(self, state_tuple, device):
        s1, s2, s3 = state_tuple
        features = []
        for s in [s1, s2, s3]:
            temp = int(s.item())
            for _ in range(self.max_depth):
                features.append(temp % self.d)
                temp //= self.d
                
        state_tensor = torch.tensor(features, dtype=torch.float32, device=device)
        shared_out = self.shared_layer(state_tensor)
        return self.actor_head(shared_out), self.critic_head(shared_out)
