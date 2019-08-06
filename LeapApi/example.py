








from CloudAlgos.client import Client
import inspect

import CloudAlgos.functions.count_fn as count_fn
import CloudAlgos.functions.sum_fn as sum_fn
import CloudAlgos.functions.fl_fn as fl_fn
import CloudAlgos.functions.var_fn as var_fn

def client_request():
    cloud_algos_port = '127.0.0.1:70000'
    # Create connector. TODO: Decide how client request will talk to connector
    client = Client(cloud_algos_port)

    # Get source code for map, agg, update, etc
    # module = inspect.getsource(count_fn)
    # module = inspect.getsource(var_fn)
    module = inspect.getsource(fl_fn)
    filter = "[age] > 50 and [bmi] < 25"
    client.send_request(module, filter)


if __name__ == "__main__":
    client_request()
