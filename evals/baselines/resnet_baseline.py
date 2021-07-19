import torch # Assume torch is loaded in cloud/sites
import random
import torchvision
import requests
import io
import os
import logging
from pylogrus import PyLogrus, TextFormatter, JsonFormatter
import time
from PIL import Image
import pandas
import numpy

def measure_acc(dataloader, ml_model):
    with torch.no_grad():
        val_sum = 0
        val_total = 0
        for i, (X, Y) in enumerate(dataloader, 0):
            target = Y
            image = X
    
            output = ml_model(image)
            correct_sum, total = acc_sum(output, target)
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

class HAMDataset(torch.utils.data.Dataset):

    def __init__(self, ids, csv_file, root_dir, transform=None):
        self.ids = ids
        self.records = pandas.read_csv(csv_file)
        self.records = self.records.iloc[self.ids]
        self.root_dir = root_dir
        self.transform = transform


    def __len__(self):
        return len(self.records)


    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.records.iloc[idx, 1] + ".jpg")
        
        image = Image.open(img_name)
        rec_id = self.records.iloc[idx, 0]
        lesion_type = self.lesion_to_int(self.records.iloc[idx, 3])
        sample = {"id": rec_id, "lesion_type": lesion_type, "image": image}

        if self.transform:
            sample["image"] = self.transform(sample["image"])

        return (sample["image"], torch.tensor(sample["lesion_type"]))
   

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
    learning_rate = 1e-4
    batch_size = 16
    
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
    
    model = torchvision.models.resnet18(pretrained=True)
    in_features = model.fc.in_features
    model.fc = torch.nn.Linear(in_features, 2)

    optimizer = torch.optim.Adam(model.parameters(), learning_rate)
    
    criterion = torch.nn.CrossEntropyLoss()
    transforms_train = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                                       torchvision.transforms.Resize((224,224)), 
                                                       torchvision.transforms.RandomHorizontalFlip(),
                                                       torchvision.transforms.RandomVerticalFlip(),
                                                       torchvision.transforms.RandomRotation(20),
                                                       torchvision.transforms.ColorJitter(brightness=0.1, contrast=0.1, hue=0.1),
                                                       torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    transforms_val = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                                     torchvision.transforms.Resize((224,224)),  
                                                     torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    ids = list(range(1, 10001))
    random_ids = random.sample(ids, 10000)
    train_ids = random_ids[:8000]
    val_ids = random_ids[8000:]
    dataset_train = HAMDataset(ids=train_ids,
                               csv_file="/home/stolet/ham10000/HAM10000_metadata.csv",
                               root_dir="/home/stolet/ham10000/HAM10000_images_part_1",
                               transform=transforms_train)
    
    dataset_val = HAMDataset(ids=val_ids,
                             csv_file="/home/stolet/ham10000/HAM10000_metadata.csv",
                             root_dir="/home/stolet/ham10000/HAM10000_images_part_1",
                             transform=transforms_val)
    
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
            output = model(X)
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
                val_end = time.time_ns()
                log.withFields({"unix-nano": val_end}).info("ValEnd")
                break

    end = time.time_ns()
    log.withFields({"unix-nano": end}).info("End")
    print(end - start)
