import json
import numpy as np
import glob
import matplotlib.pyplot as plt


def parse(coord_file, cloudalgo_file, sites_files):
    requests = {}
    parse_coord(coord_file, requests)
    parse_cloudalgo(cloudalgo_file, requests)
    parse_sites(sites_files, requests)
    total_time = requests["0"]["end-time"] - requests["0"]["start-time"]
    coord_send_time = (np.array(requests["0"]["endsend-coord"]) - np.array(requests["0"]["startsend-coord"])).sum()
    cloud_time = (np.array(requests["0"]["enditer-cloud"]) - np.array(requests["0"]["startiter-cloud"])).sum()
    validation_time = (np.array(requests["0"]["valend-cloud"]) - np.array(requests["0"]["valstart-cloud"])).sum()
    site_send_time, site_iter_time = get_time_spent_on_sites(requests, "0")
    print(total_time)
    print(coord_send_time)
    print(cloud_time)
    print(site_send_time)
    print(site_iter_time)
    plot(total_time, coord_send_time, cloud_time, site_send_time, site_iter_time, validation_time)

def get_time_spent_on_sites(requests, req_id):
    logs = requests[req_id]
    total_send_time = np.array([np.array(logs["sites"]["0"]["endsend-site"]) - np.array(logs["sites"]["0"]["startsend-site"])])
    total_iter_time = np.array([np.array(logs["sites"]["0"]["enditer-site"]) - np.array(logs["sites"]["0"]["startiter-site"])])

    for site_id in logs["sites"]:
        if site_id == "0":
            continue

        site = logs["sites"][site_id]
        send_time = np.array(site["endsend-site"]) - np.array(site["startsend-site"])
        iter_time = np.array(site["enditer-site"]) - np.array(site["startiter-site"])
        total_send_time = np.vstack((total_send_time, send_time))
        total_iter_time = np.vstack((total_iter_time, iter_time))

    total_send_time = total_send_time.max(axis=0).sum()
    total_iter_time = total_iter_time.max(axis=0).sum()
    return total_send_time, total_iter_time


def parse_coord(file, requests):
    for line in file.readlines():
        line_json = json.loads(line)
        if line_json["msg"] == "StartTiming":
            req_id = str(line_json["request-id"])
            requests[req_id] = {"start-time": line_json["unix-nano"],
                                                      "startsend-coord": [],
                                                      "endsend-coord": [],
                                                      "startiter-cloud": [],
                                                      "enditer-cloud": [],
                                                      "valstart-cloud": [],
                                                      "valend-cloud": [],
                                                      "sites": {},
                                                      "acc": []}
        elif line_json["msg"] == "EndTiming":
            req_id = str(line_json["request-id"])
            requests[req_id]["end-time"] = line_json["unix-nano"]
        elif line_json["msg"] == "StartSend":
            req_id = str(line_json["request-id"])
            requests[req_id]["startsend-coord"].append(line_json["unix-nano"])
        elif line_json["msg"] == "EndSend":
            req_id = str(line_json["request-id"])
            requests[req_id]["endsend-coord"].append(line_json["unix-nano"])


def parse_cloudalgo(file, requests):
    for line in file.readlines():
        line_json = json.loads(line)
        if line_json["message"] == "StartIter":
            req_id = str(line_json["request-id"])
            requests[req_id]["startiter-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "EndIter":
            req_id = str(line_json["request-id"])
            requests[req_id]["enditer-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "Acc":
            req_id = str(line_json["request-id"])
            requests[req_id]["acc"].append(line_json["accuracy"])
        elif line_json["message"] == "ValStart":
            requests[req_id]["valstart-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "ValEnd":
            requests[req_id]["valend-cloud"].append(line_json["unix-nano"])


def parse_sites(files, requests):
    for file in files:
        for line in file.readlines():
            line_json = json.loads(line)
            if line_json["msg"] == "StartIter":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                if site_id in requests[req_id]["sites"]:
                    requests[req_id]["sites"][site_id]["startiter-site"].append(line_json["unix-nano"])
                else:
                    requests[req_id]["sites"][site_id] = {"startiter-site": [line_json["unix-nano"]],
                                                          "enditer-site": [],
                                                          "startsend-site": [],
                                                          "endsend-site": []}
            elif line_json["msg"] == "EndIter":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["enditer-site"].append(line_json["unix-nano"])
            elif line_json["msg"] == "BeginSend":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["startsend-site"].append(line_json["unix-nano"])
            elif line_json["msg"] == "EndSend":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["endsend-site"].append(line_json["unix-nano"])


def plot(total_time, coord_send_time, cloud_time, site_send_time, site_iter_time, validation_time):
    coord_send_time = coord_send_time * 1e-9
    site_send_time = site_send_time * 1e-9
    total_time = total_time * 1e-9
    site_iter_time = site_iter_time * 1e-9
    validation_time = validation_time * 1e-9
    labels = ["Leap"]
    width = 0.1
    fig, ax = plt.subplots()
    ax.bar(labels, [total_time - validation_time], width, label="Cloud Computation Time")
    ax.bar(labels, [site_send_time + site_iter_time + coord_send_time], width, label="Coord Send Time")
    ax.bar(labels, [site_send_time + site_iter_time], width, label="Site Computation Time")
    ax.bar(labels, [site_send_time], width, label="Site Send Time")

    ax.set_ylabel("Time (seconds)")
    ax.set_title("Training Time Resnet 18")
    ax.legend()
    plt.show()


def open_site_files():
    files = []
    for filename in glob.glob("logs/site[0-9]*.log"):
        files.append(open(filename, "r"))
    return files


if __name__ == "__main__":
    site_files = open_site_files()
    coord_file = open("logs/coordinator.log", "r")
    cloudalgo_file = open("logs/cloudalgo.log", "r")
    parse(coord_file, cloudalgo_file, site_files)
