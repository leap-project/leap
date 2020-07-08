import sys
sys.path.append("../")
import api.leap as leap
import api.register.user.registration as user_reg

def distributedVerify(sites, auth_token):
    selector = {
        "type": "sql", 
        "sql_func": "count", 
        "sql_options": {
            "project_id": "13", 
            "filter" : {'pain_past3backpain': "= 1", 'yrbirth': "< 1931"}
            }
        }
    dist_leap = leap.DistributedSelectorVerification(selector, "127.0.0.1:50000", auth_token)
    result = dist_leap.get_result(sites)
    print(result)


if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    distributedVerify([1], auth_res.token)