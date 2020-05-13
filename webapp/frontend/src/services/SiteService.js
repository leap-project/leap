import axios from "axios";

const API_URL = "http://localhost:8000";

class SiteService {
    async getSites(req) {
        const url = `${API_URL}/sites`;

        return axios.get(url).then(response => {
            return response.data;
        })
    }
}

export default SiteService