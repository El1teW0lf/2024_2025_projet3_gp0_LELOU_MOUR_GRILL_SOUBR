<<<<<<< HEAD
=======
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Define possible actions with corresponding coordinate changes
ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

# Maze Environment
class Maze:
    def __init__(self):
        # Create a 6x6 maze with walls (1) and a starting position (2)
        self.maze = np.zeros((6, 6))
        self.maze[0, 0] = 2
        self.maze[5, :5] = 1
        self.maze[:4, 5] = 1
        self.maze[2, 2:] = 1
        self.maze[3, 2] = 1
        self.robot_position = (0, 0)  # current robot position
        self.steps = 0              # number of steps taken
        self.allowed_states = {}
        self.construct_allowed_states()
    
    def is_allowed_move(self, state, action):
        y, x = state
        dy, dx = ACTIONS[action]
        y_new, x_new = y + dy, x + dx
        # Check if move is off the board
        if y_new < 0 or x_new < 0 or y_new > 5 or x_new > 5:
            return False
        # Allow moving if the new position is empty or is the starting position
        if self.maze[y_new, x_new] == 0 or self.maze[y_new, x_new] == 2:
            return True
        return False
        
    def construct_allowed_states(self):
        allowed_states = {}
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if self.maze[(y, x)] != 1:  # if not a wall
                    allowed_states[(y, x)] = []
                    for action in ACTIONS:
                        if self.is_allowed_move((y, x), action):
                            allowed_states[(y, x)].append(action)
        self.allowed_states = allowed_states

    def update_maze(self, action):
        y, x = self.robot_position
        self.maze[y, x] = 0  # mark current cell as empty
        dy, dx = ACTIONS[action]
        y_new, x_new = y + dy, x + dx
        self.robot_position = (y_new, x_new)
        self.maze[y_new, x_new] = 2  # update robot's new position
        self.steps += 1
        
    def is_game_over(self):
        # The game is over when the robot reaches the bottom-right corner
        return self.robot_position == (5, 5)
    
    def give_reward(self):
        # Reward: 0 if goal is reached, else -1 per move
        return 0 if self.robot_position == (5, 5) else -1
        
    def get_state_and_reward(self):
        return self.robot_position, self.give_reward()
    
    def print_maze(self):
        # Print the maze in a human-readable format
        symbols = {0: '0', 1: 'X', 2: 'R'}
        for row in self.maze:
            print(" ".join(symbols[int(cell)] for cell in row))
        print("Steps taken:", self.steps)
>>>>>>> a9307784ea0502065ffc3130210d92aa62e06d53

# Agent Class
class Agent:
    def __init__(self, maze_env, alpha=0.15, random_factor=0.2):
        self.state_history = []  # stores (state, reward) tuples
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}  # expected rewards table
        self.init_reward(maze_env.maze)
    
    def init_reward(self, maze):
        # Initialize the reward table with random values (avoid initializing with zero)
        for y in range(maze.shape[0]):
            for x in range(maze.shape[1]):
                if maze[y, x] != 1:  # Only for non-wall cells
                    self.G[(y, x)] = np.random.uniform(low=0.1, high=1.0)
    
    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))
    
    def learn(self):
        # Back-propagate the rewards over the episode using the learning rule
        target = 0  # ideal reward for reaching the goal
        for state, reward in reversed(self.state_history):
            self.G[state] = self.G[state] + self.alpha * (target - self.G[state])
            target = self.G[state]
        self.state_history = []  # reset history for the next episode
        # Gradually decrease exploration
        self.random_factor = max(0.01, self.random_factor - 1e-4)
    
    def choose_action(self, state, allowed_moves):
        # Decide whether to explore or exploit
        if np.random.random() < self.random_factor:
            return np.random.choice(allowed_moves)
        else:
            maxG = -float("inf")
            best_action = None
            for action in allowed_moves:
                # Calculate new state after taking the action
                new_state = (state[0] + ACTIONS[action][0], state[1] + ACTIONS[action][1])
                # Use a very low default if state not in G
                if self.G.get(new_state, -float("inf")) >= maxG:
                    maxG = self.G[new_state]
                    best_action = action
            return best_action

<<<<<<< HEAD
def get_neighboring_tiles(tile, map):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = tile.x + dx, tile.y + dy
        if 0 <= nx < 99 and 0 <= ny < 99:
            neighbors.append(map[ny, nx])
    return neighbors
=======
# Main training loop
if __name__ == '__main__':
    episodes = 5000
    steps_list = []
    agent = None

    
# Iterating through data list of unknown length

    for episode in tqdm(range(episodes), desc="Training Episodes"):
        maze = Maze()
        if agent is None:
            agent = Agent(maze)

        progress_bar = tqdm()
        while not maze.is_game_over():
            state = maze.robot_position
            allowed_moves = maze.allowed_states[state]
            action = agent.choose_action(state, allowed_moves)
            maze.update_maze(action)
            state, reward = maze.get_state_and_reward()
            agent.update_state_history(state, reward)
            progress_bar.update(1)
        agent.learn()
        steps_list.append(maze.steps)
        if (episode + 1) % 500 == 0:
            print(f"Episode {episode + 1} completed in {maze.steps} steps")
    
    # Plot the number of steps per episode
    plt.plot(steps_list)
    plt.xlabel("Episode")
    plt.ylabel("Steps to complete the maze")
    plt.title("Maze Solving Progress Over Episodes")
    plt.show()
>>>>>>> a9307784ea0502065ffc3130210d92aa62e06d53
