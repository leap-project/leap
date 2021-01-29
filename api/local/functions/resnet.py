import torch # Assume torch is loaded in cloud/sites
import torchvision
import requests
import io
from redcap import Project
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
            self.token = "0F7DCA82F38137780161143CFB6660FC"
            self.project = Project(self.url, self.token) 
            
            records = self.project.export_records(records=ids)
    
            self.records = {int(record["record_id"]): record for record in records}
            self.ids = ids
            self.transform = transform
        
        def __len__(self):
            return len(self.ids)
    
        def __getitem__(self, idx): 
           
            record_id = int(self.ids[idx])
            
            record = self.records[record_id]
            content, headers = self.export_file(record_id)
            
            image = Image.open(io.BytesIO(content))
            sample = {"id": record_id, 
                      "lesion_type": self.lesion_to_int(record["dx"]), 
                      "image": image}
            
            if self.transform:
                sample["image"] = self.transform(sample["image"])
    
            return (sample["image"], torch.tensor(sample["lesion_type"]))
        
        def export_file(self, record_id):
            data = {'token': self.token,
                    'content': 'file',
                    'action': 'export',
                    'record': record_id,
                    'field': 'image',
                    'event': '',
                    'returnFormat': 'json'}
            r = requests.post(self.url, data=data)
    
            return r.content, r.headers
    
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
    transforms_val = torchvision.transforms.Compose([torchvision.transforms.Resize((224,224)), 
                                          torchvision.transforms.ToTensor(),
                                          torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    
    dataset_train = HAMDataset(hyperparams["train_ids"], transform=transforms_train)
    dataset_val = HAMDataset(hyperparams["val_ids"], transform=transforms_val)
    dataloader_train = torch.utils.data.DataLoader(dataset_train, batch_size=hyperparams["batch_size"], shuffle=True, num_workers=4)
    dataloader_val = torch.utils.data.DataLoader(dataset_val, batch_size=hyperparams["batch_size"], shuffle=False, num_workers=4)
    return dataloader_train, dataloader_val
