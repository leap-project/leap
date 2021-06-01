import json
import copy


def generate_cloud_algo_config(cloud_ip):
    config = {
        "ip_port": cloud_ip[0] + ":7000",
        "coordinator_ip_port": cloud_ip[0] + ":50000",
        "secure_with_tls": "y",
        "cert": "../certs/cloudalgo.crt",
        "key": "../certs/cloudalgo.key",
        "certificate_authority": "../certs/myCA.crt",
        "coord_cn": "Coord"
    }

    with open("../../config/cloudalgo_config.json", 'w') as outfile:
        json.dump(config, outfile)


def generate_site_conn_config(private_ip_file, cloud_ip):
    config = {
        "IpPort": "10.0.1.8:50001",
        "CoordinatorIpPort": cloud_ip[0] + ":50000",
        "AlgoIpPort": "10.0.1.8:60001",
        "SiteId": 0,
        "Secure": True,
        "Crt": "../certs/siteconn.crt",
        "Key": "../certs/siteconn.key",
        "CertAuth": "../certs/myCA.crt",
        "CoordCN": "Coord",
        "SiteAlgoCN": "SiteAlgo"
    }

    i = 0
    for line in private_ip_file.readlines():
        line = line.split("\n")[0]
        site_config = copy.deepcopy(config)
        site_config["IpPort"] = line + ":50001"
        site_config["AlgoIpPort"] = line + ":60001"
        site_config["SiteId"] = i
        site_config["Crt"] = "../certs/siteconn" + str(i) + ".crt"
        site_config["Key"] = "../certs/siteconn" + str(i) + ".key"
        with open('../../config/conn' + str(i) + "-config.json", 'w') as outfile:
            json.dump(site_config, outfile)
        i += 1


def generate_site_algo_config(private_ip_file):
    config = {
        "ip_port": "10.0.1.8:60001",
        "connector_ip_port": "10.0.1.8:50001",
        "csv_true": "0",
        "site_id": 0,
        "secure_with_tls": "y",
        "cert": "../certs/sitealgo.crt",
        "key": "../certs/sitealgo.key",
        "certificate_authority": "../certs/myCA.crt",
        "redcap_url": "http://localhost/redcap/api",
        "redcap_auth": "fa2901c70d5ee07e0eacc9068f46431e",
        "redcap_pid": 15
    }

    i = 0
    for line in private_ip_file.readlines():
        line = line.split("\n")[0]
        site_config = copy.deepcopy(config)
        site_config["ip_port"] = line + ":60001"
        site_config["connector_ip_port"] = line + ":50001"
        site_config["site_id"] = i
        site_config["cert"] = "../certs/sitealgo" + str(i) + ".crt"
        site_config["key"] = "../certs/sitealgo" + str(i) + ".key"
        with open('../../config/sitealgo' + str(i) + "_config.json", 'w') as outfile:
            json.dump(site_config, outfile)
        i += 1


def generate_coord_config(coord_ip):
    config = {
        "IpPort": coord_ip[0] + ":50000",
        "CloudAlgoIpPort": coord_ip[0] + ":7000",
        "Secure": True,
        "Crt": "../certs/coord.crt",
        "Key": "../certs/coord.key",
        "CertAuth": "../certs/myCA.crt",
        "SiteConnCN": "Conn",
        "CloudAlgoCN": "CloudAlgo"
    }

    with open("../../config/coord-config.json", 'w') as outfile:
        json.dump(config, outfile)


def get_cloud_ip(file):
    ips = []
    for line in file.readlines():
        line = line.split("\n")[0]
        ips.append(line)

    return ips

def main():
    cloud_ip_file = open("../ips-local/cloud-ips", "r")
    cloud_ip_private_file = open("../ips-local/cloud-private-ips", "r")
    site_ip_file = open("../ips-local/site-ips", "r")
    site_ip_private_file = open("../ips-local/site-private-ips", "r")

    cloud_ip = get_cloud_ip(cloud_ip_file)
    cloud_private_ip = get_cloud_ip(cloud_ip_private_file)

    generate_cloud_algo_config(cloud_private_ip)
    generate_coord_config(cloud_private_ip)
    generate_site_conn_config(site_ip_private_file, cloud_private_ip)
    site_ip_private_file.seek(0)
    generate_site_algo_config(site_ip_private_file)

if __name__ == "__main__":
    main()