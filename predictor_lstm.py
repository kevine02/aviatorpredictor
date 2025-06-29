import torch
import torch.nn as nn
import os

MODEL_PATH = "model_lstm.pt"

class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, output_size=1):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

def train_lstm_model():
    if os.path.exists(MODEL_PATH):
        return
    from train_lstm import load_training_data
    X, y = load_training_data()
    model = LSTMModel()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(50):
        model.train()
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
    torch.save(model.state_dict(), MODEL_PATH)

def predict_next_lstm(sequence):
    model = LSTMModel()
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
    import numpy as np
    seq = sequence[-10:]
    X = torch.tensor(seq, dtype=torch.float32).view(1, -1, 1)
    with torch.no_grad():
        pred = model(X).item()
    return round(pred, 2)