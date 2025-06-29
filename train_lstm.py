import torch
import torch.nn as nn
import numpy as np

def load_training_data():
    # Charger historique depuis fichier ou générer synthétique
    # Ici données synthétiques d'exemple
    data = np.random.uniform(1.0, 10.0, 500)
    X, y = [], []
    seq_len = 10
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append([data[i+seq_len]])
    X = torch.tensor(X, dtype=torch.float32).view(-1, seq_len, 1)
    y = torch.tensor(y, dtype=torch.float32)
    return X, y