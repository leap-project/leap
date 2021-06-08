import json

leap_dir = "/home/stolet/Documents/MSC/leap"


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

    with open(leap_dir + "/evals/ips/site-private-ips") as f:
        i = 0
        for line in f.readlines():
            private_ip = line.split()[0]
            port_number_conn = 50001 + i
            port_number_algo = 60001 + i
            config["ip_port"] = private_ip + ":" + str(port_number_algo)
            config["connector_ip_port"] = private_ip + ":" + str(port_number_conn)
            config["site_id"] = i

            with open(leap_dir + "/config/sitealgo" + str(i) + "-config.json", 'w') as config_file:
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

    with open(leap_dir + "/evals/ips/cloud-private-ips") as f:
        for line in f.readlines():
            private_ip = line.split()[0]
            config["CoordinatorIpPort"] = private_ip + ":50000"

    with open(leap_dir + "/evals/ips/site-private-ips") as f:
        i = 0
        for line in f.readlines():
            private_ip = line.split()[0]
            port_number_conn = 50001 + i
            port_number_algo = 60001 + i
            config["IpPort"] = private_ip + ":" + str(port_number_conn)
            config["AlgoIpPort"] = private_ip + ":" + str(port_number_algo)
            config["SiteId"] = i

            with open(leap_dir + "/config/conn" + str(i) + "-config.json", 'w') as config_file:
                json.dump(config, config_file)

            i += 1


if __name__ == "__main__":
    create_connector_config()
    create_sitealgo_config()
