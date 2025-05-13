import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys

# Paramètres de contrôle
MAX_TICK = 60
MAX_CONQUÊTES_PAR_TOUR = 5
MAX_SCORE = 1000
MEMORY_LIMIT = 100_000
REWARD_SUCCESS = 1
REWARD_FAIL = -10

# === Affichage graphique persistent ===
PLOT_FIGURE = None

def plot(scores, mean_scores):
    global PLOT_FIGURE

    if PLOT_FIGURE is None:
        plt.ion()
        PLOT_FIGURE = plt.figure(figsize=(10, 5))
    else:
        plt.clf()

    plt.title('Training...')
    plt.xlabel('Game')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')

    if len(scores) >= 10:
        window = 10
        rolling_mean = np.convolve(scores, np.ones(window) / window, mode='valid')
        plt.plot(range(window - 1, len(scores)), rolling_mean, label=f'{window}-game Rolling Mean')

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)

def plot_weights(model):
    weights = model.linear1.weight.data.cpu().numpy()
    plt.figure(figsize=(10, 5))
    plt.imshow(weights, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.title("First Layer Weights")
    plt.xlabel("Input Neurons")
    plt.ylabel("Hidden Neurons")
    plt.tight_layout()
    plt.show()

class Trainer():
    def __init__(self, game):
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0

        self.current_tick = 0
        self.max_tick = MAX_TICK
        self.game = game
        self.epoch = 0

        self.bar = tqdm(total=self.max_tick, desc=f"Epoch: {self.epoch}, Record: {self.record}")

    def restart(self):
        self.epoch += 1
        for agent in self.game.ai:
            score = agent.nation.score
            agent.n_games += 1

            agent.train_long_memory()

            if score > self.record:
                self.record = score
                agent.model.save()

            print(f'Game {agent.n_games} | Score: {score} | Record: {self.record}')

            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / agent.n_games
            self.plot_mean_scores.append(mean_score)

        # Affiche tous les 5 epochs pour limiter la charge
        if self.epoch % 5 == 0:
            plot(self.plot_scores, self.plot_mean_scores)

        self.current_tick = 0
        self.game.reset()
        self.bar = tqdm(total=self.max_tick, desc=f"Epoch: {self.epoch}, Record: {self.record}")

    def normalize_state(self, state):
        flat = state.flatten()
        return flat / np.max(flat) if np.max(flat) > 0 else flat

    def tick(self):
        self.current_tick += 1
        done = self.current_tick > self.max_tick

        for agent in self.game.ai:
            state_old = agent.get_state()
            state_old_flat = self.normalize_state(state_old)

            final_move = agent.get_action(state_old)
            nation = agent.nation
            nation.nb_conquêtes = 0  # Reset conquêtes par tick

            shape = (100, 100)
            reward = 0

            if final_move is not None:
                y, x = np.unravel_index(final_move, shape)
                tile = self.game.map.map[y, x]

                if nation.nb_conquêtes >= MAX_CONQUÊTES_PAR_TOUR:
                    reward += REWARD_FAIL
                elif tile in nation._possible_conquer():
                    nation.conquer(tile)
                    nation.nb_conquêtes += 1
                    reward += (tile.value * (tile.pop / 10)) / 1000 + REWARD_SUCCESS
                else:
                    reward += REWARD_FAIL

                if nation.score >= MAX_SCORE:
                    done = True
                    reward -= 5

                state_new = agent.get_state()
                state_new_flat = self.normalize_state(state_new)

                agent.train_short_memory(state_old_flat, final_move, reward, state_new_flat, done)
                agent.remember(state_old_flat, final_move, reward, state_new_flat, done)

                if hasattr(agent, 'memory') and len(agent.memory) > MEMORY_LIMIT:
                    agent.memory.pop(0)

                self.bar.update()

        if done:
            self.restart()
