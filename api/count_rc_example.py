import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import api.register.user.registration as user_reg
import time

from proto import computation_msgs_pb2

def predef_count_selector():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO_RC)
    selector = {"type": "default", "useLocalData": False}
    leap_predef.selector = selector
    return leap_predef

def distributed(sites, auth_token):
    leap_fn = predef_count_selector()
    dist_leap = leap.DistributedLeap(leap_fn, "127.0.0.1:50000", auth_token)
    print(dist_leap.get_result(sites))


if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    for i in range(7):
        t0 = time.time()
        distributed([1], auth_res.token)
        t1 = time.time()
        print("Time:", t1-t0)
    