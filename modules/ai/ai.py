import torch
import random
import numpy as np
from collections import deque
from modules.ai.model import Linear_QNet, QTrainer
from modules.generation.biomes import biomes

# Constants for memory management and training
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001  # Learning rate for optimizer

class AI:
    def __init__(self, map, nation):
        """
        Initialize the AI agent.

        :param map: The game map object containing tiles and biomes
        :param nation: The nation object this AI controls
        """
        self.nation = nation
        self.map = map

        # Find a valid starting position (non-water tile)
        self.start_pos = self.find_start_pos()

        # Initialize nation properties and assign AI to the nation
        self.init_nation(self.nation)

        self.n_games = 0  # Number of games played by this AI
        self.epsilon = 0  # Exploration rate for epsilon-greedy action selection
        self.gamma = 0.9  # Discount factor for future rewards

        # Memory buffer for experience replay (stores transitions)
        self.memory = deque(maxlen=MAX_MEMORY)

        # Initialize the Q-network with input/output size 10,000 (100x100 grid flattened)
        # and hidden size 1024
        self.model = Linear_QNet(10000, 1024, 10000)

        # Q-learning trainer that handles training updates
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def init_nation(self, nation):
        """
        Setup the nation with AI and conquer initial tile at start_pos.

        :param nation: Nation controlled by this AI
        """
        self.nation = nation
        self.start_pos = self.find_start_pos()

        # Attach AI instance to the nation object for reference
        nation.ai = self

        # Conquer the initial tile on the map at start position
        nation.conquer(self.map.map[self.start_pos[0], self.start_pos[1]])

    def get_action_mask(self):
        """
        Creates a flattened boolean mask representing which tiles can be conquered.

        :return: 1D numpy boolean array of length 10,000 where True indicates conquerable tile
        """
        can_conquer = self.nation._possible_conquer()  # Get list of conquerable tiles

        mask2d = np.zeros((100, 100), dtype=bool)
        for y in range(100):
            for x in range(100):
                # Mark True if tile is conquerable, False otherwise
                mask2d[y, x] = self.map.map[y, x] in can_conquer

        return mask2d.flatten()

    def find_start_pos(self):
        """
        Find a random starting position on the map that is not water.

        :return: Tuple (y, x) of valid starting coordinates
        """
        possible = (random.randint(0, 99), random.randint(0, 99))

        # Keep picking random points until the tile biome is not water
        while self.map.map[possible[0], possible[1]].biome == "water":
            possible = (random.randint(0, 99), random.randint(0, 99))

        return possible

    def get_state(self):
        """
        Builds a state representation of the map for the AI.

        State is a 100x100 numpy array with values representing:
        - Biome type (coded and normalized)
        - Tile value and population scaled and weighted
        
        Only tiles that the nation can conquer are considered (others remain 0).

        :return: 2D numpy float array (100x100) representing the state
        """
        can_conquer = self.nation._possible_conquer()
        mask = np.zeros((100, 100), dtype=float)

        for y in range(100):
            for x in range(100):
                tile = self.map.map[y, x]

                if tile in can_conquer:
                    # Weighted sum of normalized biome code, tile value, and population
                    mask[y, x] = (
                        tile.value/2000             # value normalized + weighted                 # population normalized + weighted
                    )
        return mask

    def remember(self, state, action, reward, next_state, done):
        """
        Store experience tuple in replay memory for training later.

        :param state: Current state representation
        :param action: Action taken (index)
        :param reward: Reward received
        :param next_state: Next state after action
        :param done: Boolean indicating if episode ended
        """
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """
        Sample a batch from memory and perform a training step.
        Uses experience replay to improve learning stability.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # Random sample batch
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train immediately on the latest transition (short-term memory).

        :param state: Current state flattened
        :param action: Action taken
        :param reward: Reward received
        :param next_state: Next state flattened
        :param done: Boolean if episode finished
        """
        # Flatten states to 1D arrays as model expects flat input
        state = state.flatten()
        next_state = next_state.flatten()

        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """
        Decide next action using epsilon-greedy policy.

        With probability epsilon, pick a random valid action (exploration).
        Otherwise, pick the action with the highest predicted Q-value among valid actions (exploitation).

        :param state: Current state array
        :return: Integer index of action chosen or None if no valid moves
        """
        # Decay epsilon over time to reduce exploration as training progresses
        self.epsilon = max(5, 80 - 0.5 * self.n_games)

        # Get mask of valid moves
        action_mask = self.get_action_mask()  # Boolean array length 10,000

        if random.randint(0, 200) < self.epsilon:
            # Exploration: randomly choose among valid moves
            valid_indices = np.nonzero(action_mask)[0]
            if len(valid_indices) == 0:
                return None  # No valid moves
            return int(np.random.choice(valid_indices))
        else:
            # Exploitation: choose best Q-value action among valid moves
            state0 = torch.tensor(state.flatten(), dtype=torch.float)
            q_vals = self.model(state0)

            # Mask out invalid actions by setting their Q-values to -inf
            invalid = ~torch.tensor(action_mask, dtype=torch.bool)
            q_vals[invalid] = -float('inf')

            # Return the index of the highest Q-value action
            return int(torch.argmax(q_vals).item())
