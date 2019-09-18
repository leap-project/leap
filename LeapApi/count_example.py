import sys
sys.path.append("../")
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn
import LeapApi.codes as codes

if __name__ == "__main__":
    leap_predef = leap_fn.PredefinedFunction(codes.COUNT_ALGO)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    dist_leap = leap.DistributedLeap(leap_predef)
    result = dist_leap.get_result()
    print(result)
