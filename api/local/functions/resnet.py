import torch # Assume torch is loaded in cloud/sites
import torchvision
import io
import pandas as pd
import utils.redcap as redcap
from PIL import Image

def get_model(hyperparams):
    model = torchvision.models.resnet18(pretrained=True)
    in_features = model.fc.in_features
    model.fc = torch.nn.Linear(in_features, hyperparams["d_y"])
    return model

def get_optimizer(params, hyperparams):
    return torch.optim.SGD(params, hyperparams["lr"])

def get_criterion(hyperparams):
    return torch.nn.CrossEntropyLoss()

def get_dataloader(hyperparams, data):
    
    def custom_collate(batch):
        batch = torch.utils.data.dataloader.default_collate(batch)
        batch[1] = batch[1].reshape(-1, 1)
        return batch

    class HAMDataset(torch.utils.data.Dataset):
        def __init__(self, ids, csv_file, root_dir, transform=None):
            self.ids = ids
            self.records = pd.read_csv(csv_file)
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
    
    site_id = hyperparams.get("site_id")
    train_ids = hyperparams["train_ids"]
    if site_id is not None:
        first_id = int(site_id * len(train_ids) / hyperparams["num_sites"])
        last_id = int((site_id * len(train_ids) / hyperparams["num_sites"]) + (len(train_ids) / hyperparams["num_sites"]))
        train_ids = train_ids[first_id:last_id]
    
    dataset_train = HAMDataset(ids=train_ids,
                               csv_file="/home/stolet/ham10000/HAM10000_metadata.csv",
                               root_dir="/home/stolet/ham10000/HAM10000_images_part_1",
                               transform=transforms_train) 
    dataset_val = HAMDataset(ids=hyperparams["val_ids"],
                             csv_file="/home/stolet/ham10000/HAM10000_metadata.csv",
                             root_dir="/home/stolet/ham10000/HAM10000_images_part_1",
                             transform=transforms_val)
    
    dataloader_train = torch.utils.data.DataLoader(dataset_train, 
                                                   batch_size=hyperparams["batch_size"],
                                                   shuffle=True)
    dataloader_val = torch.utils.data.DataLoader(dataset_val,
                                                 batch_size=hyperparams["batch_size"],
                                                 shuffle=True)
     
    return dataloader_train, dataloader_val
