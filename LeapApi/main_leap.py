import sys
sys.path.append("../")
import LeapApi.leap as leap
import pdb

import LeapLocal.functions as leap_fn

def main():
    leap_udf = leap.UDF()
    module = leap_fn.count_fn
    leap_udf.set_map_fn(module.map_fn)

if __name__ == "__main__":
    main()
