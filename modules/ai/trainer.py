import numpy as np

class Trainer():
    def __init__(self,game):
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0

        self.current_tick = 0
        self.max_tick = 10000
        self.game = game

    def restart(self):
                    # train long memory, plot result

        for agent in self.game.ai:

            score = agent.nation.score

            agent.n_games += 1
            agent.train_long_memory()

            if score > self.record:
                self.record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', self.record)

            self.plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            self.plot_mean_scores.append(mean_score)

        raise Exception('Game Over')

    def tick(self):
        self.current_tick += 1

        done = False

        if self.current_tick > self.max_tick:
            done = True
        
        for agent in self.game.ai:

            state_old = agent.get_state()

            final_move = agent.get_action(state_old)

            nation = agent.nation

            shape = (100, 100)

            y, x = np.unravel_index(final_move, shape)

            can_conquer = agent.nation._possible_conquer()

            reward = 0

            if self.game.map.map[y,x] in can_conquer:
                nation.conquer(self.game.map.map[y,x])
                reward += self.game.map.map[y,x].value
            else:
                reward -= 100

            print(f"Agent Move: {x};{y} Reward: {reward}")

            state_new = agent.get_state()

            agent.train_short_memory(state_old, final_move, reward, state_new,done)

            agent.remember(state_old, final_move, reward, state_new,done)
    
        if done:
            self.restart()
            return

