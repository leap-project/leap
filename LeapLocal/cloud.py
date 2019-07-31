import pdb
import json
import utils

class Cloud():
    def __init__(self, sites):
        self.sites = sites

    def handle_request(self, req):
        exec(req["module"], globals())
        state = globals()["state"]
        local_state = prep(state)
        stop = False
        while not stop:
            map_results = []
            choice = choice_fn(state)

            site_req = {
                "module": req["module"],
                "state": json.dumps(state)
            }
            site_req = json.dumps(site_req)
            for site in self.sites:
                site_res = site.local_compute(site_req)
                map_results.append(site_res)
            
            agg_result = agg_fn[choice](map_results, local_state)
            state = update_fn[choice](agg_result, state, local_state)
            stop = stop_fn(agg_result, state, local_state)
        return post_fn(agg_result, state, local_state)
    