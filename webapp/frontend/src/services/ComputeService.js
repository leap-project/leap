import axios from "axios";


const API_URL = "http://localhost:8000";

class ComputeService {
    async compute(req) {
        const url = `${API_URL}/compute`;

        return axios.post(url, {
            dp: req.dp,
            algo: req.algo,
        }).then(response => {
            return response.data;
        })
    }
}

export default ComputeService