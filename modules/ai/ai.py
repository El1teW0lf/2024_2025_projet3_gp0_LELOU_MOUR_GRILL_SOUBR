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
        self.model = Linear_QNet(20000, 1024, 10000)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def init_nation(self,nation):
        self.nation = nation
        self.start_pos = self.find_start_pos()
        nation.ai = self
        nation.conquer(self.map.map[self.start_pos[0],self.start_pos[1]])



    def find_start_pos(self):
        possible = (random.randint(0, 99), random.randint(0, 99))
        while self.map.map[possible[0],possible[1]].biome == "water":
            possible = (random.randint(0, 99), random.randint(0, 99))
        return possible
    
    
    def get_state(self):

        state = []

        can_conquer = self.nation._possible_conquer()


        for y in range(100):
            for x in range(100):
                i = self.map.map[y,x]
                state.append(biomes[i.biome]["code"])
                if i in can_conquer:
                    state.append(1)
                else:
                    state.append(0)

        return np.array(state, dtype=int)

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
        self.trainer.train_step(state, action, reward, next_state,done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        to_buy = 0
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 9999)
            to_buy = move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            to_buy = move

        return to_buy
    
  