import pdb 
import utils
import json

class Client():
    def __init__(self, cloud):
        self.cloud = cloud        
    
    def send_request(self, u_module):
        q_selector = {} # select everything

        req = {}
        req["module"] = u_module 

        result = self.cloud.handle_request(req)
        print("Result: {}".format(result))
        return result
    

    def send_fl_request(self):
        pass
    

