import torch
import random
import numpy as np
from collections import deque
from modules.ai.model import Linear_QNet, QTrainer
from modules.ai.helper import plot

from modules.generation.biomes import biomes

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class AI:
    def __init__(self, map,nation):
        self.nation = nation
        self.map = map
        self.start_pos = self.find_start_pos()

        self.init_nation(self.nation)

        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(10000, 1024, 10000)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def init_nation(self,nation):
        self.nation = nation
        self.start_pos = self.find_start_pos()
        nation.ai = self
        nation.conquer(self.map.map[self.start_pos[0],self.start_pos[1]])

    def get_action_mask(self):
        """
        Returns a 1D boolean array of length 10000 where True means
        the tile at that index is conquerable this turn.
        """
        can_conquer = self.nation._possible_conquer()
        mask2d = np.zeros((100, 100), dtype=bool)
        for y in range(100):
            for x in range(100):
                if self.map.map[y, x] in can_conquer:
                    mask2d[y, x] = True
        return mask2d.flatten()


    def find_start_pos(self):
        possible = (random.randint(0, 99), random.randint(0, 99))
        while self.map.map[possible[0],possible[1]].biome == "water":
            possible = (random.randint(0, 99), random.randint(0, 99))
        return possible
    
    
    def get_state(self):
        can_conquer = self.nation._possible_conquer()
        mask = np.zeros((100, 100), dtype=int)

        for y in range(100):
            for x in range(100):
                i = self.map.map[y, x]

                if i in can_conquer:
                    mask[y, x] = (biomes[i.biome]["code"]+1)/7

        return mask


    def remember(self, state, action, reward, next_state,done):
        self.memory.append((state, action, reward, next_state,done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state,done):
        state = state.flatten()
        next_state = next_state.flatten()
        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = max(5, 80 - 0.5 * self.n_games)
        action_mask = self.get_action_mask()  # boolean array of size 10000

        if random.randint(0, 200) < self.epsilon:
            # random valid move only
            valid_indices = np.nonzero(action_mask)[0]
            if len(valid_indices) == 0:
                # no valid move—handle as you like, e.g. pass or random
                return None
            return int(np.random.choice(valid_indices))
        else:
            # exploit: mask out invalid Q-values
            state0 = torch.tensor(state.flatten(), dtype=torch.float)
            q_vals = self.model(state0)            # shape: [10000]
            # set impossible actions to a very low number
            invalid = ~torch.tensor(action_mask, dtype=torch.bool)
            q_vals[invalid] = -float('inf')
            return int(torch.argmax(q_vals).item())


  