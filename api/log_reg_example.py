import sys
sys.path.append("../")
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import api.register.user.registration as user_reg
import numpy as np
import pandas as pd
import json
import time

from proto import computation_msgs_pb2

def predef_log_reg():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.LOG_REG)
    selector = {
        "type": codes.DEFAULT,
        "useLocalData": True
    }
    leap_predef.selector = selector
    return leap_predef

def predict(X, weights, bias):
    linear_model = np.dot(X, weights) + bias
    y_predicted = 1 / (1 + np.exp(-linear_model))
    y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
    return np.array(y_predicted_cls)

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

def runEval(weights, bias):
    df_test = pd.read_csv("../data/test_orig.csv")
    df_test = df_test.drop(columns=["record_id", "pid", "data_complete"])
    df_test[df_test.columns] = df_test[df_test.columns].apply(pd.to_numeric, errors='coerce')
    
    y_test = df_test['rfi']
    X_test = df_test.drop(columns=['rfi'])
    
    predictions = predict(X_test, weights, bias)
    print("Classification accuracy:", accuracy(y_test, predictions))

def distributed(sites, auth_token):
    leap_fn = predef_log_reg()
    dist_leap = leap.DistributedLeap(leap_fn, "127.0.0.1:50000", auth_token)
    
    t0 = time.time()
    result = dist_leap.get_result(sites)
    t1 = time.time()
    print(result)
    print("Time:", t1-t0)
    
    runEval(np.array(result["weights"]), result["bias"])

if __name__ == "__main__":
    #user_reg.register_user("TestUser2", "1234561", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    distributed([1,2,3], auth_res.token)