import sys
sys.path.append("../")
import api.leap as leap
import api.register.user.registration as user_reg
import api.leap_fn as leap_fn
import api.codes as codes
import api.local.functions as leap_functions
import random

if __name__ == "__main__":
    leap_fed_learn = leap_fn.FedLearnFunction()
    
    selector = {
            "type": codes.DEFAULT,
            "useLocalData": True
    }

    leap_fed_learn.selector = selector

    module = leap_functions.resnet
    leap_fed_learn.get_model = module.get_model
    leap_fed_learn.get_optimizer = module.get_optimizer
    leap_fed_learn.get_criterion = module.get_criterion
    leap_fed_learn.get_dataloader = module.get_dataloader

    ids = list(range(1,10001))
    random_ids = random.sample(ids, 10000)
    train_ids = random_ids[:8000]
    val_ids = random_ids[8000:]
    
    hyperparams = {
        "lr": 1e-4,
        "d_x": 224, # input dimension
        "d_y": 2, # output dimension
        "batch_size": 16,
        "max_iters": 100,
        "iters_per_epoch": 100,
        "train_ids": train_ids,
        "val_ids": val_ids
    }
    leap_fed_learn.hyperparams = hyperparams

    #user_reg.register_user("TestUser", "123456", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    leap = leap.DistributedLeap(leap_fed_learn, "127.0.0.1:50000", auth_res.token)
    sites = [1]
    result = leap.get_result(sites)
    print(result)
