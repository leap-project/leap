import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn

from proto import computation_msgs_pb2

if __name__ == "__main__":
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    dist_leap = leap.DistributedLeap(leap_predef)
    result = dist_leap.get_result()
    print(result)
