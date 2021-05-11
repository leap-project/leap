# An algorithm that trains a model using federated learning.

import json
import pandas as pd
import torch
import ujson as json
import torch.utils.data
import time

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

def map_fns():
    # Expects model, dataloader, optimizer, criterion to be predefined
    def map_fn1(data, state):
        hyperparams["site_id"] = state["site_id"]
        dataloader, dataloader_val = get_dataloader(hyperparams, data)
        if 'loss_history' in state:
            print("loss: {}".format(state["loss_history"][-1]))

        def unquantize(min_val, max_val, gradients):
            interval = (max_val - min_val) / 2**8
            unquantized_grads = interval * torch.tensor(gradients, dtype=torch.float) + min_val
            return unquantized_grads
        
        # Update model with new weights
        if 'model_weights' in state:
            model_weights = state["model_weights"]
            min_max_list = state["min_max"]
            for i, (name, params) in enumerate(model.named_parameters()):
                unquantized_weights = unquantize(min_max_list[i]["min"], min_max_list[i]["max"], model_weights[i])
                params.data = unquantized_weights
        
        # Accumulate gradients
        loss_meter = AverageMeter()
        for i, (X, Y) in enumerate(dataloader):
            X = X
            Y = Y
            output = model(X)
            loss = criterion(output, Y)
            loss_meter.update(loss.item())
            loss.backward()
            if i == hyperparams["iters_per_epoch"]:
                break
        
        def quantize(min_val, max_val, gradients):
            interval = (max_val - min_val) / 2**8
            quantized_grads = torch.round((gradients - min_val) / interval).type(torch.uint8)
            return quantized_grads
        
        # Store gradient as list
        client_grad = []
        min_max_list = []
        for name, params in model.named_parameters():
            if params.requires_grad:
                min_v = torch.min(params.grad)
                max_v = torch.max(params.grad)
                grad = quantize(min_v, max_v, params.grad).cpu().tolist()
                min_max = {"min": min_v.cpu().tolist(), "max": max_v.cpu().tolist()}
                client_grad.append(grad)
                min_max_list.append(min_max)
        
        result = {
            "grads": client_grad,
            "min_max": min_max_list,
            "loss": loss_meter.avg
        }

        result = json.dumps(result)
        return result

    return [map_fn1]

def agg_fns():
    def agg_fn1(map_results):
        def unquantize(min_val, max_val, gradients):
            interval = (max_val - min_val) / 2**8
            unquantized_grads = interval * torch.tensor(gradients, dtype=torch.float) + min_val
            return unquantized_grads

        first_result = json.loads(map_results[0])
        agg_grad = first_result["grads"]
        
        for j in range(len(agg_grad)):
            agg_grad[j] = unquantize(first_result["min_max"][j]["min"], first_result["min_max"][j]["max"], agg_grad[j])

        loss_meter = AverageMeter()
        loss_meter.update(first_result['loss'])
        
        for i in range(1,len(map_results)):
            map_result = json.loads(map_results[i])
            grad_result = map_result['grads']
            
            for j in range(len(agg_grad)):
                unquantized = unquantize(map_result["min_max"][j]["min"], map_result["min_max"][j]["max"], grad_result[j]) 

                agg_grad[j] = (agg_grad[j] + unquantized)

        for j in range(len(agg_grad)):
            agg_grad[j] = agg_grad[j].cpu().tolist()
            
        loss_meter.update(first_result['loss'])
        result = {
            "grad":agg_grad,
            "loss":loss_meter.avg
        }
        
        return result

    return [agg_fn1]

def update_fns():
    # Expects model and optimizer in global state
    def update_fn1(agg_result, state):
        
        def quantize(min_val, max_val, gradients):
            interval = (max_val - min_val) / 2**8
            quantized_grads = torch.round((gradients - min_val) / interval).type(torch.uint8)
            return quantized_grads
       
        state["i"] += 1
        if "loss_history" in state:
            state["loss_history"].append(agg_result["loss"])
        else:
            state["loss_history"] = [agg_result["loss"]]

        # update model weights
        # model = state["model"]
        # optimizer = state["optimizer"]
        agg_grad = agg_result["grad"]
        for i, (name, params) in enumerate(model.named_parameters()):
            if params.requires_grad:
                params.grad = torch.tensor(agg_grad[i])
            optimizer.step()
            optimizer.zero_grad()
        model_weights = []
        min_max_list = []

        for name, params in model.named_parameters():
            min_v = torch.min(params)
            max_v = torch.max(params)
            quantized_params = quantize(min_v, max_v, params).cpu().tolist()
            model_weights.append(quantized_params)
            min_max_list.append({"min": min_v.cpu().tolist(), "max": max_v.cpu().tolist()})

        state["model_weights"] = model_weights
        state["min_max"] = min_max_list
        return state

    return [update_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

# Formats the raw data into data usable by map_fn
# ex: Converting types, extracting rows/columns
def dataprep_fn(data):
    return data
    #data = pd.DataFrame(data)
    #X = data[].astype('float').to_numpy()
    #Y = data["grade"].astype('long').to_numpy()
    #return X, Y

def stop_fn(agg_result, state):
    return state["i"] == hyperparams["max_iters"]

def postprocessing_fn(agg_result, state):
    return agg_result["loss"]

def init_state_fn():
    state = {
        "i": 0,
    }
    return state
