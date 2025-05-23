import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize a simple feedforward neural network with one hidden layer.

        :param input_size: Number of input features
        :param hidden_size: Number of neurons in the hidden layer
        :param output_size: Number of output neurons (actions)
        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)  # First linear layer
        self.linear2 = nn.Linear(hidden_size, output_size)  # Output linear layer

    def forward(self, x):
        """
        Forward pass through the network.
        Applies ReLU activation after the first layer.

        :param x: Input tensor
        :return: Output tensor (Q-values for each action)
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Save the model's state dictionary to a file.

        :param file_name: Filename for saving the model
        """
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)  # Create folder if it doesn't exist

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)  # Save model weights


class QTrainer:
    def __init__(self, model, lr, gamma):
        """
        Initialize the trainer.

        :param model: The Q-network model
        :param lr: Learning rate for the optimizer
        :param gamma: Discount factor for future rewards
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)  # Adam optimizer
        self.criterion = nn.MSELoss()  # Mean Squared Error loss

    def train_step(self, state, action, reward, next_state, done):
        """
        Perform one training step of the Q-learning algorithm.

        :param state: Current state(s), tensor or array
        :param action: Action(s) taken, tensor or array (one-hot encoded or indices)
        :param reward: Reward(s) received
        :param next_state: Next state(s) after action
        :param done: Boolean(s) indicating if episode ended
        """
        # Convert inputs to tensors if not already
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # If single sample (no batch dimension), add batch dimension
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )  # Make done iterable

        # 1: Get predicted Q values from current states
        pred = self.model(state)

        # Clone predictions to modify target Q values
        target = pred.clone()

        # Update target for each sample in batch
        for idx in range(len(done)):
            Q_new = reward[idx]  # Immediate reward
            if not done[idx]:
                # If not done, add discounted max future reward
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            # Find the index of the action taken
            # If action is one-hot encoded, torch.argmax(action[idx]) gets the action index
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Zero gradients from previous step
        self.optimizer.zero_grad()

        # Calculate loss between target Q values and predicted Q values
        loss = self.criterion(target, pred)
        loss.backward()  # Backpropagation

        # Perform optimization step to update weights
        self.optimizer.step()
