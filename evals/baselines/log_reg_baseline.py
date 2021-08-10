import torch # Assume torch is loaded in cloud/sites
import random
import torchvision
import requests
import pandas as pd
import io
import os
import logging
from pylogrus import PyLogrus, TextFormatter, JsonFormatter
import time
from PIL import Image
import pandas as pd
import numpy

def measure_acc(dataloader, ml_model):
    with torch.no_grad():
        val_sum = 0
        val_total = 0
        for i, (X, Y) in enumerate(dataloader):
            output = ml_model(X.float())
            correct_sum, total = acc_sum(output, Y)
            val_sum += correct_sum
            val_total += total
        print("Acc: " + str(val_sum / val_total))
        return val_sum / val_total

def acc_sum(pred, target):
    with torch.no_grad():
        pred_softmax = torch.log_softmax(pred, dim=1)
        _, pred_tags = torch.max(pred_softmax, dim=1)
        correct_pred = (pred_tags == target).float()
        return correct_pred.sum(), len(correct_pred)

def custom_collate(batch):
    batch = torch.utils.data.dataloader.default_collate(batch)
    batch[1] = batch[1].reshape(-1, 1)
    return batch


class LogisticRegression(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LogisticRegression, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)

    def forward(self, x):
        outputs = self.linear(x)
        return outputs


class HAMDataset(torch.utils.data.Dataset):

    def __init__(self, ids, token_path, transform=None):
        self.ids = ids
        self.transform = transform
        self.token = self.get_token(token_path)


    def get_token(self, token_path):
        with open(token_path, 'r') as f:
            token = f.read().replace('\n', '')
            return token


    def __len__(self):
        return len(self.ids)


    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        idx = self.ids[idx]
        record_id_label = 'records[' + str(idx) + ']'
        data = {
            'token': self.token,
            'content': 'record',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            record_id_label: str(idx),
            'fields[0]': 'age',
            'fields[1]': 'dx',
            'fields[2]': 'dx_type',
            'fields[3]': 'image_id',
            'fields[4]': 'lesion_id',
            'fields[5]': 'localization',
            'fields[6]': 'record_id',
            'fields[7]': 'sex',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json'
        }
        r = requests.post('http://localhost/redcap/api/',data=data)
        sample = r.json()[0]
        one_hot_sample = self.get_one_hot_sample(sample["record_id"])
        one_hot_sample = self.set_dx(one_hot_sample, sample["dx"])
        one_hot_sample = self.set_dx_type(one_hot_sample, sample["dx_type"])
        one_hot_sample = self.set_sex(one_hot_sample, sample["sex"])
        one_hot_sample = self.set_localization(one_hot_sample, sample["localization"])
        tensor_sample = self.sample_to_tensor(one_hot_sample)
        y = tensor_sample[11]
        x = torch.cat([tensor_sample[:11], tensor_sample[12:]])
        return (x, y)

    def set_dx(self, sample, val):
        key = "dx_" + str(val)
        sample[key] = 1
        return sample

    def set_dx_type(self, sample, val):
        key = "dx_type_" + str(val)
        sample[key] = 1
        return sample
        
    def set_sex(self, sample, val):
        key = "sex_" + str(val)
        sample[key] = 1
        return sample

    
    def set_localization(self, sample, val):
        key = "localization_" + str(val)
        key = key.replace(" ", "_")
        sample[key] = 1
        return sample
        

    def sample_to_tensor(self, sample):
        sample_list = []
        for key in sample:
            if key == "record_id":
                continue
            val = sample[key]
            sample_list.append(int(val))
        return torch.tensor(sample_list)


    def get_one_hot_sample(self, record_id):
        one_hot_sample = {"record_id": record_id,
                          "dx_bkl": 0,
                          "dx_nv": 0,
                          "dx_df": 0,
                          "dx_mel": 0,
                          "dx_vasc": 0,
                          "dx_bcc": 0,
                          "dx_akiec": 0,
                          "dx_type_histo":0,
                          "dx_type_consensus": 0,
                          "dx_type_confocal": 0,
                          "dx_type_follow_up": 0,
                          "sex_male": 0,
                          "sex_female": 0,
                          "sex_unknown": 0,
                          "localization_scalp": 0,
                          "localization_ear": 0,
                          "localization_face": 0,
                          "localization_back": 0,
                          "localization_trunk": 0,
                          "localization_chest": 0,
                          "localization_upper_extremity": 0,
                          "localization_abdomen": 0,
                          "localization_unknown": 0,
                          "localization_lower_extremity": 0,
                          "localization_genital": 0,
                          "localization_neck": 0,
                          "localization_hand": 0,
                          "localization_foot": 0,
                          "localization_acral": 0}
        
        return one_hot_sample 

    def lesion_to_int(self, lesion_type):
        if lesion_type == "akiec":
            return 0
        elif lesion_type == "bcc":
            return 0
        elif lesion_type == "bkl":
            return 0
        elif lesion_type == "df":
            return 0
        elif lesion_type == "mel":
            return 0
        elif lesion_type == "nv":
            return 1
        elif lesion_type == "vasc":
            return 0

if __name__ == "__main__":
    max_iters = 100
    iters_per_epoch = 10 
    learning_rate = 1e-6
    batch_size = 16
    token_path = "/home/stolet/gopath/src/leap/config/token"

    logging.setLoggerClass(PyLogrus)
    logger = logging.getLogger(__name__)  # type: PyLogrus
    logger.setLevel(logging.DEBUG)
    
    formatter = TextFormatter(datefmt='Z', colorize=True)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    
    jsonformatter = JsonFormatter(datefmt='Z')
    fh = logging.FileHandler("logs/resnet_baseline.log", 'w+')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(jsonformatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    log = logger.withFields({"node": "baseline"})
    
    model = LogisticRegression(28, 2) 

    optimizer = torch.optim.Adam(model.parameters(), learning_rate)
    
    criterion = torch.nn.CrossEntropyLoss()

    ids = list(range(1, 10001))
    random_ids = random.sample(ids, 10000)
    train_ids = random_ids[:8000]
    val_ids = random_ids[8000:]
   
    dataset_train = HAMDataset(train_ids, token_path)
    dataset_val = HAMDataset(val_ids, token_path)
    
    dataloader_train = torch.utils.data.DataLoader(dataset_train, 
                                                   batch_size=batch_size,
                                                   shuffle=True)
    dataloader_val = torch.utils.data.DataLoader(dataset_val,
                                                 batch_size=batch_size,
                                                 shuffle=True)

    start = time.time_ns()
    log.withFields({"unix-nano": start}).info("Start")
    for e in range(max_iters):
        for i, (X, Y) in enumerate(dataloader_train):
            output = model(X.float())
            loss = criterion(output, Y)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            print(str(i) + ": " + str(loss))

            if i == iters_per_epoch - 1:
                val_start = time.time_ns()
                log.withFields({"unix-nano": val_start}).info("ValStart")
                accuracy = measure_acc(dataloader_val, model)
                log.withFields({"accuracy": str(accuracy.cpu().detach().numpy())}).info("Acc")
                log.withFields({"accuracy": str(accuracy)}).info("Acc")
                val_end = time.time_ns()
                log.withFields({"unix-nano": val_end}).info("ValEnd")
                break

    end = time.time_ns()
    log.withFields({"unix-nano": end}).info("End")
    print(end - start)
