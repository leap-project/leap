import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn

from proto import computation_msgs_pb2

if __name__ == "__main__":
    leap_predef = leap_fn.PrivatePredefinedFunction(computation_msgs_pb2.AlgoCodes.PRIVATE_SITE_COUNT_ALGO, epsilon=1, delta=0)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    leap = leap.DistributedLeap(leap_predef)
    result = leap.get_result()
    print(result)