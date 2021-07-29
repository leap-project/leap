import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import api.register.user.registration as user_reg
import time
import numpy as np
from proto import computation_msgs_pb2

def predef_count_selector():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO_RC)
    selector = {"type": "default", "useLocalData": False}
    leap_predef.selector = selector
    return leap_predef

def distributed(sites, auth_token, root_cert, priv_key, cert_chain):
    leap_fn = predef_count_selector()
    dist_leap = leap.DistributedLeap(leap_fn, "10.0.0.6:50000", auth_token, 
                                True, root_cert, priv_key, cert_chain)
    print(dist_leap.get_result(sites))


if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    
    fd = open("../certs/myCA.crt", "rb")
    root_cert = fd.read()
    fd = open("../certs/cloudalgo.key", "rb")
    priv_key = fd.read()
    fd = open("../certs/cloudalgo.crt", "rb")
    cert_chain = fd.read()
    auth_res = user_reg.authenticate_user("TestUser", "123456", "10.0.0.6:50000",
                                          True, priv_key, cert_chain, root_cert, "Coord")
    
    times = []
    for i in range(4):
        t0 = time.time()
        distributed([0], auth_res.token, root_cert, priv_key, cert_chain)
        t1 = time.time()
        times.append(t1 - t0)

    print("Time:", np.mean(times))
    print("Variance: ", np.var(times)) 
