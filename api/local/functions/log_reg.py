import torch # Assume torch is loaded in cloud/sites
import torchvision
import io
import pandas as pd
import utils.redcap as redcap
from PIL import Image

def get_model(hyperparams):
    class LogisticRegression(torch.nn.Module):
        def __init__(self, input_dim, output_dim):
            super(LogisticRegression, self).__init__()
            self.linear = torch.nn.Linear(input_dim, output_dim)
    
        def forward(self, x):
            x = x.type(torch.float)
            outputs = self.linear(x)
            return outputs

    model = LogisticRegression(hyperparams["d_x"], hyperparams["d_y"])
    return model

def get_optimizer(params, hyperparams):
    return torch.optim.Adam(params, hyperparams["lr"])

def get_criterion(hyperparams):
    return torch.nn.CrossEntropyLoss()

def get_dataloader(hyperparams, data):
    
    class HAMDataset(torch.utils.data.Dataset):
    
        def __init__(self, ids, token_path, transform=None):
            self.ids = ids
            self.transform = transform
            self.token_path = token_path

        def get_token(self, token_path):
            with open(token_path, 'r') as f:
                token = f.read().replace('\n', '')
                return token
    
        def __len__(self):
            return len(self.ids)
    
    
        def __getitem__(self, idx):
            if torch.is_tensor(idx):
                idx = idx.tolist()
    
            token = self.get_token(self.token_path)
            idx = self.ids[idx]
            record_id_label = 'records[' + str(idx) + ']'
            data = {
                'token': token,
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

    site_id = hyperparams.get("site_id")
    train_ids = hyperparams["train_ids"]
    if site_id is not None:
        first_id = int(site_id * len(train_ids) / hyperparams["num_sites"])
        last_id = int((site_id * len(train_ids) / hyperparams["num_sites"]) + (len(train_ids) / hyperparams["num_sites"]))
        train_ids = train_ids[first_id:last_id]
    
    token_path = '/home/stolet/token' 
    dataset_train = HAMDataset(train_ids, token_path)
    dataset_val = HAMDataset(hyperparams["val_ids"], token_path)
    
    dataloader_train = torch.utils.data.DataLoader(dataset_train, 
                                                   batch_size=hyperparams["batch_size"],
                                                   shuffle=True)
    dataloader_val = torch.utils.data.DataLoader(dataset_val,
                                                 batch_size=hyperparams["batch_size"],
                                                 shuffle=True)
    
    return dataloader_train, dataloader_val
