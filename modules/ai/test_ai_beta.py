import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.preprocessing import StandardScaler

class NeuralNet(nn.Module):
    def __init__(self, input_size):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 32)
        self.fc2 = nn.Linear(32, 16)
        self.out = nn.Linear(16, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.sigmoid(self.out(x))

class NeuralConquestAI:
    def __init__(self):
        self.model = NeuralNet(4)  # 4 features: ressources, biome, température, population
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.BCELoss()
        self.scaler = StandardScaler()
        self.training_data = []
        self.labels = []
        self.trained = False

    def extract_features(self, tile):
        return np.array([
            tile.score_tile_resources(),
            tile.score_tile_biome(),
            tile.score_tile_temperature(),
            tile.pop
        ], dtype=np.float32)

    def record_result(self, tile, success):
        features = self.extract_features(tile)
        label = float(success)

        self.training_data.append(features)
        self.labels.append(label)

        print(f"[AI] Donnée ajoutée — Features: {features.tolist()} | Résultat: {label}")

        if len(self.training_data) >= 10:
            self.train()

    def train(self, epochs=20):
        print("[AI] Entraînement du réseau de neurones en cours...")

        # Normalisation
        X = self.scaler.fit_transform(self.training_data)
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(self.labels, dtype=torch.float32).view(-1, 1)

        for epoch in range(epochs):
            output = self.model(X_tensor)
            loss = self.criterion(output, y_tensor)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        self.trained = True
        print(f"[AI] Entraînement terminé. Perte finale : {loss.item():.4f}")

    def should_conquer(self, tile):
        features = self.extract_features(tile)
        if not self.trained:
            print("[AI] Modèle non entraîné, fallback vers règle simple.")
            return sum(features) > 50

        scaled_features = self.scaler.transform([features])
        input_tensor = torch.tensor(scaled_features, dtype=torch.float32)
        prediction = self.model(input_tensor).item()
        print(f"[AI] Prédiction du modèle : {prediction:.3f} ({'✅ Conquérir' if prediction >= 0.5 else '❌ Ignorer'})")

        return prediction >= 0.5
