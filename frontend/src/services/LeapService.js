const {WebRequest, ComputeResponse} = require('../proto/computation-msgs_pb.js');
const {CloudAlgoClient} = require('../proto/cloud-algos_grpc_web_pb.js');

class LeapService {

    constructor() {
        this.LeapService = new CloudAlgoClient("127.0.0.1:70000");
    }

    compute(request) {
        console.log("Triggered compute");
        let req = new WebRequest();
        req.setDp(request.dp);
        req.setAlgoType(request.algoType);

        this.LeapService.webRequest(req, {}, function(err, response) {
            console.log("Finished web request?");
            console.log(response);
            console.log(err);
            return {error: err, computationResult: response};
        });
    }
}

export default LeapService