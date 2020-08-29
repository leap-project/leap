import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import api.register.user.registration as user_reg

from proto import computation_msgs_pb2

def predef_count_selector():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO_RC)
    selector = {"type": codes.DEFAULT, "filter": "[pain_past3backpain] = 1 and [yrbirth] < 1931"}
    leap_predef.selector = selector
    return leap_predef

def predef_count_selector_sql():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO_RC_QUERY)
    selector = {"type": codes.SQL, "sql_func": "count", "sql_options": {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}}}
    leap_predef.selector = selector
    return leap_predef

def predef_max_selector_sql():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.MAX_ALGO_RC)
    selector = {"type": codes.SQL, "sql_func": "max", "sql_options": {"project_id": 13, "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}, "field": "yrbirth"}}
    leap_predef.selector = selector
    return leap_predef

def predef_mean_selector_sql():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.MEAN_ALGO)
    selector = {"type": codes.DEFAULT,  "filter": "[pain_past3backpain] = 1 and [yrbirth] < 1960"}
    leap_predef.selector = selector
    return leap_predef

def distributed(sites, auth_token):
    leap_fn = predef_mean_selector_sql()
    dist_leap = leap.DistributedLeap(leap_fn, "127.0.0.1:50000", auth_token)
    print(dist_leap.get_result(sites))


if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    distributed([1], auth_res.token)