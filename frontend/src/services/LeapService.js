import axios from "axios";

class LeapService {
    async compute(selector) {
        const url = "localhost:someport/compute";
        return axios.get(url, {
            params: {
                selector: selector
            }
        }).then(response => response.data)
    }
}

export default LeapService