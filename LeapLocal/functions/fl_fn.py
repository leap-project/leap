import pdb
import json
import inspect

import torch
import torch.utils.data

class NPDataset(torch.utils.data.Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):        
        x = self.data[idx]
        y = self.labels[idx]
        return x, y

class LinearModel(torch.nn.Module):
    def __init__(self, d, len_y):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(d, len_y)
    
    def forward(self, x):
        out = self.linear(x)
        return out

"""
Assume data is already in local site and available as np
map requires PyTorch Dataset PyTorch Dataloader
"""
def map_fn1(data, state):
    print(data)
    batch_size = state["batch_size"]
    lr = state["lr"]
    d = 100
    X = data[:,:d]
    Y = data[:,d:]
    dataset = NPDataset(X, Y)
    model = LinearModel(d, 1)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

    for i, (X, Y) in enumerate(dataloader):
        X = X.float()
        Y = Y.float()
        output = model(X)
        loss = criterion(output, Y)
        loss.backward()
        optimizer.step()
        client_grad = []
        for name, params in model.named_parameters():
            if params.requires_grad:
                client_grad.append(params.grad.cpu().clone())



    return client_grad


map_fn = [map_fn1]

def agg_fn1(map_results):
    agg_grad = map_results[0]

    for i in range(1,len(map_results)):
        for j in range(len(agg_grad)):
            agg_grad[j] += map_results[i][j]

    return agg_grad

agg_fn = [agg_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

def update_fn1(agg_result, state):
    state["i"] += 1
    return state

update_fn = [update_fn1]

def stop_fn(agg_result, state):
    return state["i"] == 10

def post_fn(agg_result, state):
    return agg_result

state = {
    "i": 0,
    "iters_per_epoch":2,
    "batch_size":16,
    "lr":1e-3
}