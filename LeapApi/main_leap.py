import sys
sys.path.append("../")
import LeapApi.leap as leap
import pdb
import json
import LeapLocal.functions as leap_fn

def main():
    leap_udf = leap.UDF()
    module = leap_fn.var_fn

    leap_udf.get_map_fn = module.get_map_fn
    leap_udf.get_update_fn = module.get_update_fn
    leap_udf.get_agg_fn = module.get_agg_fn
    leap_udf.choice_fn = module.choice_fn
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
