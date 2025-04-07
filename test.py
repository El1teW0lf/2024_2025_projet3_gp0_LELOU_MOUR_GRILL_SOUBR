import sys
import random
import numpy as np
import pygame
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# Define a simple Maze environment
class MazeEnv:
    def __init__(self):
        # Maze layout: 0 = free, 1 = wall, 3 = goal
        self.maze = np.array([
            [0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 3, 1]
        ])
        self.n_rows, self.n_cols = self.maze.shape
        self.start = (0, 0)  # starting cell
        self.goal = (4, 3)   # goal cell (maze[4,3] == 3)
        self.reset()

    def reset(self):
        self.agent_pos = self.start
        return self.get_state()

    def get_state(self):
        # Represent state as normalized (row, col)
        return np.array([self.agent_pos[0] / self.n_rows, self.agent_pos[1] / self.n_cols], dtype=np.float32)

    def step(self, action):
        # Define actions: 0=up, 1=down, 2=left, 3=right
        moves = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        dr, dc = moves[action]
        new_r = self.agent_pos[0] + dr
        new_c = self.agent_pos[1] + dc

        # Check boundaries
        if new_r < 0 or new_r >= self.n_rows or new_c < 0 or new_c >= self.n_cols:
            return self.get_state(), -1.0, False  # hit boundary

        # Check for wall
        if self.maze[new_r, new_c] == 1:
            return self.get_state(), -1.0, False  # hit wall

        # Valid move: update agent position
        self.agent_pos = (new_r, new_c)
        # Check for goal
        if self.maze[new_r, new_c] == 3:
            return self.get_state(), 10.0, True
        else:
            return self.get_state(), -0.1, False

    def render(self, screen, cell_size=100):
        # Draw maze grid
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                cell = self.maze[r, c]
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
                if cell == 0:
                    color = (255, 255, 255)  # free: white
                elif cell == 1:
                    color = (0, 0, 0)        # wall: black
                elif cell == 3:
                    color = (0, 255, 0)      # goal: green
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)
        # Draw the agent as a red circle
        r, c = self.agent_pos
        center = (int(c * cell_size + cell_size / 2), int(r * cell_size + cell_size / 2))
        pygame.draw.circle(screen, (255, 0, 0), center, cell_size // 3)

# Define a simple Q-Network using PyTorch
class QNetwork(nn.Module):
    def __init__(self, input_dim=2, output_dim=4):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 32)
        self.fc2 = nn.Linear(32, 32)
        self.out = nn.Linear(32, output_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)

# Main training loop
def train():
    # Initialize PyGame
    pygame.init()
    cell_size = 100
    screen = pygame.display.set_mode((cell_size * 5, cell_size * 5))
    pygame.display.set_caption("Maze RL")

    env = MazeEnv()

    # For reproducibility
    np.random.seed(0)
    torch.manual_seed(0)

    device = torch.device("cpu")
    q_net = QNetwork().to(device)
    optimizer = optim.Adam(q_net.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    num_episodes = 500
    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.1

    for episode in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0.0
        steps = 0

        while not done:
            # Epsilon-greedy action selection
            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
                with torch.no_grad():
                    q_vals = q_net(state_tensor)
                action = torch.argmax(q_vals).item()

            next_state, reward, done = env.step(action)
            total_reward += reward

            # Compute target: r + gamma * max_a Q(s', a)
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
            q_vals = q_net(state_tensor)
            q_val = q_vals[0, action]
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0).to(device)
            with torch.no_grad():
                next_q_vals = q_net(next_state_tensor)
                max_next_q = torch.max(next_q_vals)
            target = reward + (gamma * max_next_q if not done else 0.0)

            target_tensor = torch.tensor(target, dtype=torch.float32).to(device)
            loss = loss_fn(q_val, target_tensor)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state
            steps += 1

            # Process PyGame events to allow window closing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Optional: render every 50 episodes
            if episode % 50 == 0:
                screen.fill((220, 220, 220))
                env.render(screen, cell_size)
                pygame.display.flip()

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        print(f"Episode {episode:3d}: Steps={steps:3d}, Total Reward={total_reward:5.2f}, Epsilon={epsilon:4.2f}")

    # Display the learned policy by running one episode without exploration
    state = env.reset()
    done = False
    while not done:
        screen.fill((220, 220, 220))
        env.render(screen, cell_size)
        pygame.display.flip()
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(device)
        with torch.no_grad():
            action = torch.argmax(q_net(state_tensor)).item()
        next_state, reward, done = env.step(action)
        state = next_state

    # Wait until the user closes the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    train()
