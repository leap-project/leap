import sys
sys.path.append("../")
import pdb
import json
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn
import LeapApi.codes as codes

def main():
    leap_udf = leap_fn.PredefinedFunction(codes.COUNT_ALGO)
    selector = "[age] > 50 and [bmi] < 25"
    leap_udf.selector = selector
    dist_leap = leap.DistributedLeap(leap_udf)
    dist_leap.send_request()

    # leap_udf.map_fns = module.map_fns
    # leap_udf.update_fns = module.update_fns
    # leap_udf.agg_fns = module.agg_fns
    # leap_udf.choice_fn = module.choice_fn
    # leap_udf.stop_fn = module.stop_fn
    # leap_udf.dataprep_fn = module.dataprep_fn
    # leap_udf.postprocessing_fn = module.postprocessing_fn
    # leap_udf.init_state_fn = module.init_state_fn

    # make request

if __name__ == "__main__":
    main()
