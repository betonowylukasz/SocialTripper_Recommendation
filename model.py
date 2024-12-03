import torch.nn as nn

class MLPModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(MLPModel, self).__init__()
        self.hidden = nn.Sequential(
            nn.Linear(input_size, hidden_size[0]),
            nn.ReLU(),
            nn.Linear(hidden_size[0], hidden_size[1]),
            nn.ReLU(),
            # nn.Linear(hidden_size[1], hidden_size[2]),
            # nn.ReLU(),
        )
        self.output = nn.Linear(hidden_size[1], 1)  # Ostatnia warstwa
        self.sigmoid = nn.Sigmoid()  # Ograniczenie do [0, 1]

    def forward(self, x):
        x = self.hidden(x)
        x = self.output(x)
        return self.sigmoid(x)
