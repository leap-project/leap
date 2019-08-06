import sys
sys.path.append("../")
import LeapApi.leap as leap
import pdb

import LeapLocal.functions as leap_fn

def main():
    leap_udf = leap.UDF()
    module = leap_fn.count_fn
    leap_udf.map_fn = module.map_fn
    leap_udf.update_fn = module.update_fn
    leap_udf.agg_fn = module.agg_fn
    leap_udf.choice_fn = module.choice_fn
    leap_udf.update_fn = module.update_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn

    filter = ""
    # make request
    leap_udf.send_request(filter)
    pdb.set_trace()
if __name__ == "__main__":
    main()
