import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from IPython.display import clear_output

def plot(scores, mean_scores):
    clear_output(wait=True)
    plt.figure(figsize=(10,5))
    plt.title('Training...')
    plt.xlabel('Game')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.legend()
    plt.show()

def plot_weights(model):
    weights = model.linear1.weight.data.cpu().numpy()
    plt.figure(figsize=(10, 5))
    plt.imshow(weights, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.title("First Layer Weights")
    plt.xlabel("Input Neurons")
    plt.ylabel("Hidden Neurons")
    plt.show()

class Trainer():
    def __init__(self,game):
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0

        self.current_tick = 0
        self.max_tick = 100
        self.game = game
        self.total_score = 0
        self.epoch = 0

        self.bar = tqdm(total=self.max_tick,desc=f"Epoch: {self.epoch},Record: {self.record}")

    def restart(self):
        self.epoch += 1
        for agent in self.game.ai:
            score = agent.nation.score
            agent.n_games += 1

            # Train Long Memory properly
            agent.train_long_memory()

            if score > self.record:
                self.record = score
                #agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', self.record)

            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / agent.n_games
            self.plot_mean_scores.append(mean_score)

            
        self.current_tick = 0
        self.game.reset()
        self.bar = tqdm(total=self.max_tick,desc=f"Epoch: {self.epoch},Record: {self.record}")

    def tick(self):
        self.current_tick += 1

        done = False

        if self.current_tick > self.max_tick:
            done = True
        
        for agent in self.game.ai:

            state_old = agent.get_state()
            state_old_flat = state_old.flatten() 

            final_move = agent.get_action(state_old)

            nation = agent.nation

            shape = (100, 100)

            if final_move != None:
                y, x = np.unravel_index(final_move, shape)

                can_conquer = agent.nation._possible_conquer()

                reward = 0

                if self.game.map.map[y,x] in can_conquer:
                    nation.conquer(self.game.map.map[y,x])
                    reward += (self.game.map.map[y,x].value*(self.game.map.map[y,x].pop/10))/1000
                else:
                    reward -= 10 


                state_new = agent.get_state()
                state_new_flat = state_new.flatten()

                agent.train_short_memory(state_old_flat, final_move, reward, state_new_flat,done)

                agent.remember(state_old_flat, final_move, reward, state_new_flat,done)
    
                self.bar.update()

        self.current_tick += 1
        if done:
            self.restart()
            return

