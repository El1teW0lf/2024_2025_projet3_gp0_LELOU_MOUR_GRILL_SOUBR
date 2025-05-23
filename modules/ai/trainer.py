import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from IPython.display import clear_output

<<<<<<< HEAD
def plot(scores, mean_scores):
    """
    Plot the training scores and their running mean.

    :param scores: List of scores per game
    :param mean_scores: List of mean scores over games
    """
    clear_output(wait=True)  # Clear previous plot in Jupyter
    plt.figure(figsize=(10,5))
    plt.title('Training...')
    plt.xlabel('Game')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.legend()
    plt.show()

def plot_weights(model):
    """
    Visualize weights of the model's first linear layer.

    :param model: Neural network model with attribute linear1.weight
    """
    weights = model.linear1.weight.data.cpu().numpy()
    plt.figure(figsize=(10, 5))
    plt.imshow(weights, cmap='viridis', aspect='auto')
    plt.colorbar()
    plt.title("First Layer Weights")
    plt.xlabel("Input Neurons")
    plt.ylabel("Hidden Neurons")
    plt.show()

=======
>>>>>>> 520d51639b16285b0bb77deade606e55499a27fd
class Trainer():
    def __init__(self, game):
        """
        Initialize the Trainer for managing training loops.

        :param game: Game instance with AI agents to train
        """
        self.plot_scores = []         # Scores to plot
        self.plot_mean_scores = []    # Mean scores to plot
        self.total_score = 0          # Total accumulated score
        self.record = 0               # Best score so far

        self.current_tick = 0         # Current tick count in game
        self.max_tick = 1000          # Max ticks per epoch/game
        self.game = game
        self.epoch = 0                # Training epoch count

        # Progress bar for current epoch/tick
        self.bar = tqdm(total=self.max_tick, desc=f"Epoch: {self.epoch}, Record: {self.record}")

        for agent in self.game.ai:
            agent.model.load()

    def restart(self):
        """
        Called at the end of each game/epoch:
        - Increment epoch
        - Train agents' long-term memory
        - Update scores and records
        - Reset game state and progress bar
        """
        self.epoch += 1
        for agent in self.game.ai:
            score = agent.nation.score
            agent.n_games += 1

            # Train the agent with experience replay
            agent.train_long_memory()

            # Update record score and save model if new record
            if score > self.record:
                self.record = score
<<<<<<< HEAD
                # agent.model.save()  # Uncomment to save model on new record
=======
                agent.model.save()
>>>>>>> 520d51639b16285b0bb77deade606e55499a27fd

            print(f'Game {agent.n_games}, Score {score}, Record: {self.record}')

            # Update plotting lists
            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / agent.n_games
            self.plot_mean_scores.append(mean_score)

        # Reset counters and game for next epoch
        self.current_tick = 0
        self.game.reset()
        self.bar = tqdm(total=self.max_tick, desc=f"Epoch: {self.epoch}, Record: {self.record}")

    def tick(self):
        """
        Called each game tick to:
        - Update the tick count
        - Get agents' actions and states
        - Calculate rewards and train short memory
        - Add experience to memory buffer
        - Restart game if max ticks reached
        """
        self.current_tick += 1
        done = False

        # End game if max ticks reached
        if self.current_tick > self.max_tick:
            done = True
        
        for agent in self.game.ai:
            # Get current state, flatten for model input
            state_old = agent.get_state()
            state_old_flat = state_old.flatten() 

            # Decide on the next action from the model
            final_move = agent.get_action(state_old)

            nation = agent.nation
            shape = (100, 100)  # Map dimensions

            if final_move is not None:
                # Convert action index to map coordinates
                y, x = np.unravel_index(final_move, shape)

                # Check tiles agent can conquer
                can_conquer = agent.nation._possible_conquer()

                reward = 0

                # If chosen tile is conquerable, conquer and assign positive reward
                if self.game.map.map[y, x] in can_conquer:
                    nation.conquer(self.game.map.map[y, x])
                    reward += (self.game.map.map[y, x].value * (self.game.map.map[y, x].pop / 10)) / 1000
                else:
                    # Penalize invalid moves
                    reward -= 10 

                # Get new state after action
                state_new = agent.get_state()
                state_new_flat = state_new.flatten()

                # Train short-term memory with this step
                agent.train_short_memory(state_old_flat, final_move, reward, state_new_flat, done)

                # Remember experience for replay
                agent.remember(state_old_flat, final_move, reward, state_new_flat, done)

                # Update progress bar
                self.bar.update()

        if done:
            # Restart training/game at end of epoch
            self.restart()
            return
