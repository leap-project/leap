import sys
sys.path.append("../")
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn
import LeapApi.codes as codes


if __name__ == "__main__":
    leap_predef = leap_fn.PrivatePredefinedFunction(codes.PRIVATE_SITE_COUNT_ALGO, epsilon=1, delta=0)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    leap = leap.DistributedLeap(leap_predef)
    result = leap.get_result()
    print(result)