import pdb
import json
import inspect

import pandas as pd
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

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
"""
Assume data is already in local site and available as np
map requires PyTorch Dataset PyTorch Dataloader
"""
def map_fn1(data, state):
    batch_size = state["batch_size"]
    lr = state["lr"]
    d = state["d"]
    X = data[0]
    Y = data[1]
    dataset = NPDataset(X, Y)
    model = LinearModel(d, 1)
    criterion = torch.nn.MSELoss()
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

    if 'loss_history' in state:
        print("loss: {}".format(state["loss_history"][-1]))

    # Update model with new weights
    if 'model_weights' in state:
        model_weights = state["model_weights"]
        for i, (name, params) in enumerate(model.named_parameters()):
            params.data = torch.tensor(model_weights[i])

    # Accumulate gradients
    loss_meter = AverageMeter()

    for i, (X, Y) in enumerate(dataloader):
        X = X.float()
        Y = Y.float()
        output = model(X)
        loss = criterion(output, Y)
        loss_meter.update(loss.item())
        loss.backward()
        if i == state["iters_per_epoch"]:
            break

    client_grad = []
    for name, params in model.named_parameters():
        if params.requires_grad:
            client_grad.append(params.grad.cpu().tolist())

    result = {
        "grads": client_grad,
        "loss": loss_meter.avg
    }
    result = json.dumps(result)
    return result


map_fn = [map_fn1]

def agg_fn1(map_results, local_state):
    first_result = json.loads(map_results[0])
    agg_grad = first_result['grads']    
    loss_meter = AverageMeter()
    loss_meter.update(first_result['loss'])

    for i in range(1,len(map_results)):
        map_result = json.loads(map_results[i])
        grad_result = map_result['grads']
        for j in range(len(agg_grad)):
            agg_grad[j] += grad_result[j]
        loss_meter.update(map_result['loss'])

    result = {
        "grad":agg_grad,
        "loss":loss_meter.avg
    }
    return result

agg_fn = [agg_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

def update_fn1(agg_result, state, local_state):
    state["i"] += 1
    if "loss_history" in state:
        state["loss_history"].append(agg_result["loss"])
    else:
        state["loss_history"] = [agg_result["loss"]]
    
    # update model weights
    model = local_state["model"]
    optimizer = local_state["optimizer"]
    agg_grad = agg_result["grad"]
    for i, (name, params) in enumerate(model.named_parameters()):
        if params.requires_grad:
            params.grad = torch.tensor(agg_grad[i])
        optimizer.step()
        optimizer.zero_grad()
    model_weights = []
    for name, params in model.named_parameters():
        model_weights.append(params.cpu().tolist())

    state["model_weights"] = model_weights
    return state

update_fn = [update_fn1]

def stop_fn(agg_result, state, local_state):
    return state["i"] == state["max_iters"]

def post_fn(agg_result, state, local_state):
    return agg_result

# Formats the raw data into data usable by map_fn
# ex: Converting types, extracting rows/columns
def data_prep(data):
    data = pd.DataFrame(data)
    X = data[["age", "bmi"]].astype('float').to_numpy()
    Y = data["grade"].astype('long').to_numpy()
    return X,Y

# Initializes local variables (not passed to the site) and updates state in cloud_api
def prep(state):
    d = state["d"]
    lr = state["lr"]
    model = LinearModel(d, 1)
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    model_weights = []
    # Get model weights
    for name, params in model.named_parameters():
        if params.requires_grad:
            model_weights.append(params.cpu().tolist())
    state["model_weights"] = model_weights
    local_state = {
        "model": model,
        "optimizer": optimizer
    }
    return local_state

state = {
    "i": 0,
    "d":2,
    "iters_per_epoch":1,
    "max_iters":5,
    "batch_size":1,
    "lr":1e-5
}
