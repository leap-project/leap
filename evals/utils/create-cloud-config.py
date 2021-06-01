import json


def create_cloudalgo_config():
    config = {"ip_port": "",
              "coordinator_ip_port": "",
              "secure_with_tls": "y",
              "cert": "../certs/cloudalgo.crt",
              "key": "../certs/cloudalgo.key",
              "certificate_authority": "../certs/myCA.crt",
              "coord_cn": "Coord"}

    with open("../ips-local/cloud-private-ips") as f:
        for line in f.readlines():
            private_ip = line.split()[0]
            config["ip_port"] = private_ip + ":7000"
            config["coordinator_ip_port"] = private_ip + ":50000"

    with open("../../config/cloudalgo_config.json", 'w') as f:
        json.dump(config, f)


def create_coord_config():
    config = {
        "IpPort": "",
        "CloudAlgoIpPort": "",
        "Secure": True,
        "Crt": "../certs/coord.crt",
        "Key": "../certs/coord.key",
        "CertAuth": "../certs/myCA.crt",
        "SiteConnCN": "Conn",
        "CloudAlgoCN": "CloudAlgo"
    }

    with open("../ips-local/cloud-private-ips") as f:
        for line in f.readlines():
            private_ip = line.split()[0]
            config["IpPort"] = private_ip + ":50000"
            config["CloudAlgoIpPort"] = private_ip + ":7000"

    with open("../../config/coord-config.json", 'w') as f:
        json.dump(config, f)


if __name__ == "__main__":
    create_cloudalgo_config()
    create_coord_config()
