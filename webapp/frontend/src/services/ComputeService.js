import axios from "axios";


const API_URL = "http://localhost:8000";

class ComputeService {
    async compute(req) {
        const url = `${API_URL}/compute/`;
        console.log(req)
        console.log(req.sites)
        return axios.post(url, {
            dp: req.dp,
            algo: req.algo,
            selector: req.selector,
            sites: req.sites,
        }).then(response => {
            return response.data;
        }).catch(err => {
            return err
        })
    }
}

export default ComputeService