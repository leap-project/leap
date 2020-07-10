import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import api.register.user.registration as user_reg
import numpy as np
import pandas as pd
import json

from proto import computation_msgs_pb2

def predef_log_reg():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.LOG_REG)
    leap_predef.selector = {"csv": ["/Users/adityachinchure/go/src/leap/sitealgo/training1.csv", "/Users/adityachinchure/go/src/leap/sitealgo/training2.csv"]}
    return leap_predef

def predict(X, weights, bias):
    linear_model = np.dot(X, weights) + bias
    y_predicted = 1 / (1 + np.exp(-linear_model))
    y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
    return np.array(y_predicted_cls)

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

def distributed(sites, auth_token):
    leap_fn = predef_log_reg()
    dist_leap = leap.DistributedLeap(leap_fn, "127.0.0.1:50000", auth_token)
    result = dist_leap.get_result(sites)
    print(result)
    #result = json.loads(result)
    weights = np.array(result["weights"])
    bias = result["bias"]
    X_test = pd.read_csv("/Users/adityachinchure/go/src/leap/api/local/data/Xtest.csv")
    y_test = pd.read_csv("/Users/adityachinchure/go/src/leap/api/local/data/ytest.csv", index_col=False, squeeze=True)
    predictions = predict(X_test, weights, bias)
    print("Classification accuracy:", accuracy(y_test, predictions))

if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    distributed([1,2], auth_res.token)