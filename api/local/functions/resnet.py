import torch # Assume torch is loaded in cloud/sites
import torchvision
import io
import utils.redcap as redcap
from PIL import Image

def get_model(hyperparams):
    model = torchvision.models.resnet18(pretrained=True)
    in_features = model.fc.in_features
    model.fc = torch.nn.Linear(in_features, hyperparams["d_y"])
    return model

def get_optimizer(params, hyperparams):
    return torch.optim.Adam(params, hyperparams["lr"])

def get_criterion(hyperparams):
    return torch.nn.CrossEntropyLoss()

def get_dataloader(hyperparams, data):
    
    def custom_collate(batch):
        batch = torch.utils.data.dataloader.default_collate(batch)
        batch[1] = batch[1].reshape(-1, 1)
        return batch

    class HAMDataset(torch.utils.data.Dataset):
    
        def __init__(self, ids, transform=None):
            self.url = "http://localhost/redcap/api/"
            self.token = "936AF3AE86AEB1FDD2CA231EDE7D2D2D"
            
            records = redcap.export_records(ids, ["id", "lesion_type", "image"], 
                                            self.token, self.url) 
    
            self.records = {int(record["record_id"]): record for record in records}
            self.ids = ids
            self.transform = transform
        
        def __len__(self):
            return len(self.ids)
    
        def __getitem__(self, idx): 
           
            record_id = int(self.ids[idx])
            
            record = self.records[record_id]
            content, headers = redcap.export_file(record_id, self.url, "image")
            
            image = Image.open(io.BytesIO(content))
            sample = {"id": record_id, 
                      "lesion_type": self.lesion_to_int(record["dx"]), 
                      "image": image}
            
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
     
    transforms_train = torchvision.transforms.Compose([torchvision.transforms.Resize((224,224)), 
                                          torchvision.transforms.RandomHorizontalFlip(),
                                          torchvision.transforms.RandomVerticalFlip(),
                                          torchvision.transforms.RandomRotation(20),
                                          torchvision.transforms.ColorJitter(brightness=0.1, contrast=0.1, hue=0.1),
                                          torchvision.transforms.ToTensor(),
                                          torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    print("Transform 1")
    transforms_val = torchvision.transforms.Compose([torchvision.transforms.Resize((224,224)), 
                                          torchvision.transforms.ToTensor(),
                                          torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    print("Transform 2")
    
    site_id = hyperparams.get("site_id")
    train_ids = hyperparams["train_ids"]
    if site_id is not None:
        first_id = int(site_id * len(train_ids) / hyperparams["num_sites"])
        last_id = int((site_id * len(train_ids) / hyperparams["num_sites"]) + (len(train_ids) / hyperparams["num_sites"]))
        train_ids = train_ids[first_id:last_id]
    print("Got ids") 
    dataset_train = HAMDataset(train_ids, transform=transforms_train)
    print("Train dataset")
    dataset_val = HAMDataset(hyperparams["val_ids"], transform=transforms_val)
    print("Val dataset")
    dataloader_train = torch.utils.data.DataLoader(dataset_train, batch_size=hyperparams["batch_size"], shuffle=True, num_workers=4)
    print("Train dataloader")
    dataloader_val = torch.utils.data.DataLoader(dataset_val, batch_size=hyperparams["batch_size"], shuffle=True, num_workers=4)
    print("Val dataloader")
    return dataloader_train, dataloader_val
