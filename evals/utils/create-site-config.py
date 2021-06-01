import json


def create_sitealgo_config():
    config = {"ip_port": "",
              "connector_ip_port": "",
              "csv_true": "0",
              "site_id": 0,
              "secure_with_tls": "y",
              "cert": "../certs/sitealgo0.crt",
              "key": "../certs/sitealgo0.key",
              "certificate_authority": "../certs/myCA.crt",
              "redcap_url": "http://localhost/redcap/api",
              "redcap_auth": "fa2901c70d5ee07e0eacc9068f46431e",
              "redcap_pid": 15}

    with open("../ips-local/site-private-ips") as f:
        i = 0
        for line in f.readlines():
            private_ip = line.split()[0]
            config["ip_port"] = private_ip + ":60001"
            config["connector_ip_port"] = private_ip + ":50001"
            config["site_id"] = i

            with open("../../config/sitealgo" + str(i) + "-config.json", 'w') as config_file:
                json.dump(config, config_file)

            i += 1


def create_connector_config():
    config = {"IpPort": "",
              "CoordinatorIpPort": "",
              "AlgoIpPort": "",
              "SiteId": 0,
              "Secure": True,
              "Crt": "../certs/siteconn0.crt",
              "Key": "../certs/siteconn0.key",
              "CertAuth": "../certs/myCA.crt",
              "CoordCN": "Coord",
              "SiteAlgoCN": "SiteAlgo"}

    with open("../ips-local/cloud-private-ips") as f:
        for line in f.readlines():
            private_ip = line.split()[0]
            config["CoordinatorIpPort"] = private_ip + ":50000"

    with open("../ips-local/site-private-ips") as f:
        i = 0
        for line in f.readlines():
            private_ip = line.split()[0]
            config["IpPort"] = private_ip + ":50001"
            config["AlgoIpPort"] = private_ip + ":60001"
            config["SiteId"] = i

            with open("../../config/conn" + str(i) + "-config.json", 'w') as config_file:
                json.dump(config, config_file)

            i += 1


if __name__ == "__main__":
    create_connector_config()
    create_sitealgo_config()
