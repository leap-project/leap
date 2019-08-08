import sys
sys.path.append("../")
import pdb
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn
import LeapApi.codes as codes
import LeapLocal.functions as functions

import torch

class LinearModel(torch.nn.Module):
    def __init__(self, d, len_y):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(d, len_y)

    def forward(self, x):
        out = self.linear(x)
        return out

def predef_count_exp():
    leap_udf = leap_fn.PredefinedFunction(codes.COUNT_ALGO)
    selector = "[age] > 50 and [bmi] < 25"
    leap_udf.selector = selector
    dist_leap = leap.DistributedLeap(leap_udf)
    dist_leap.send_request()

def udf_count_exp():
    leap_udf = leap_fn.UDF()
    module = functions.count_fn
    leap_udf.map_fns = module.map_fns
    leap_udf.update_fns = module.update_fns
    leap_udf.agg_fns = module.agg_fns
    leap_udf.choice_fn = module.choice_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn

    selector = "[age] > 50 and [bmi] < 25"
    leap_udf.selector = selector
    dist_leap = leap.DistributedLeap(leap_udf)
    dist_leap.send_request()

def fed_learn_exp():
    selector = "[age] > 50 and [bmi] < 25"
    leap_fed_learn = leap_fn.FedLearnFunction()
    leap_fed_learn.selector = selector
    leap_fed_learn.model = LinearModel(2, 1)
    leap_fed_learn.optimizer = torch.optim.SGD(leap_fed_learn.model.paramteters(), lr=1e-5)
    leap_fed_learn.criterion = torch.nn.MSELoss()

def main():
    fed_learn_exp()

if __name__ == "__main__":
    main()
