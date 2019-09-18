import sys
sys.path.append("../")
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn
import LeapApi.LeapLocal.functions as leap_functions


if __name__ == "__main__":
    leap_fed_learn = leap_fn.FedLearnFunction()
    selector = "[age] > 50 and [bmi] < 25"
    leap_fed_learn.selector = selector

    module = leap_functions.fl_fn
    leap_fed_learn.get_model = module.get_model
    leap_fed_learn.get_optimizer = module.get_optimizer
    leap_fed_learn.get_criterion = module.get_criterion
    leap_fed_learn.get_dataloader = module.get_dataloader

    hyperparams = {
        "lr": 1e-5,
        "d_x": 2, # input dimension
        "d_y": 1, # output dimension
        "batch_size": 1,
        "max_iters": 4,
        "iters_per_epoch":1
    }
    leap_fed_learn.hyperparams = hyperparams

    leap = leap.DistributedLeap(leap_fed_learn)
    result = leap.get_result()
    print(result)