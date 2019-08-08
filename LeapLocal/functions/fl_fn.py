import torch # Assume torch is loaded in cloud/sites

def get_model(hyperparams):
    class LinearModel(torch.nn.Module):
        def __init__(self, d_x, d_y):
            super(LinearModel, self).__init__()
            self.linear = torch.nn.Linear(d_x, d_y)
        
        def forward(self, x):
            out = self.linear(x)
            return out 
    return LinearModel(hyperparams["d_x"], hyperparams["d_y"])

def get_optimizer(params, hyperparams):
    return torch.optim.SGD(params, hyperparams["lr"])

def get_criterion(hyperparams):
    return torch.nn.MSELoss()

def get_dataloader(hyperparams, data):
    class Dataset(torch.utils.data.Dataset):
        def __init__(self, X, Y):
            self.X = X
            self.Y = Y
        
        def __len__(self):
            return len(self.X)
        
        def __getitem__(self, idx):
            x = self.X[idx]
            y = self.Y[idx]
            return x, y
    dataset = Dataset(data[0], data[1])
    dataloader = torch.utils.data.DataLoader(dataset, 
        batch_size=hyperparams["batch_size"],
        shuffle=False)
    return dataloader