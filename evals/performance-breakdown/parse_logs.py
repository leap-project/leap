import json
import numpy as np
import glob
import matplotlib.pyplot as plt


def parse(coord_file, cloudalgo_file, sites_files, baseline_files):
    requests = {}
    parse_coord(coord_file, requests)
    parse_cloudalgo(cloudalgo_file, requests)
    parse_sites(sites_files, requests)
    baseline = parse_baseline(baseline_files)
    total_time = requests["0"]["end-time"] - requests["0"]["start-time"]

    coord_site_send = (np.array(requests["0"]["endsend-tosite-fromcoord"]) - np.array(requests["0"]["startsend-tosite-fromcoord"])).sum()
    coord_cloud_send = (np.array(requests["0"]["endsend-tocloud-fromcoord"]) - np.array(requests["0"]["startsend-tocloud-fromcoord"])).sum()
    coord_cloud_rcv = (np.array(requests["0"]["endrcv-fromcloud-tocoord"]) - np.array(requests["0"]["startrcv-fromcloud-tocoord"])).sum()

    cloud_time = (np.array(requests["0"]["enditer-cloud"]) - np.array(requests["0"]["startiter-cloud"])).sum()
    validation_time = (np.array(requests["0"]["valend-cloud"]) - np.array(requests["0"]["valstart-cloud"])).sum()
    site_to_coord_send, site_iter_time = get_time_spent_on_sites(requests, "0")


    coord_site_io = coord_site_send + site_to_coord_send
    coord_cloud_io = coord_cloud_send + coord_cloud_rcv

    baseline_total_time = baseline["end"] - baseline["start"]
    baseline_validation_time = (np.array(baseline["val_end"]) - np.array(baseline["val_start"])).sum()
    baseline_total_time = baseline_total_time - baseline_validation_time
    baseline_total_time = 10

    print(total_time)
    print(coord_cloud_io)
    print(cloud_time)
    print(coord_site_io)
    print(site_iter_time)
    print(baseline_total_time)
    plot(total_time, coord_cloud_io, cloud_time, coord_site_io, site_iter_time, validation_time, baseline_total_time)

def get_time_spent_on_sites(requests, req_id):
    logs = requests[req_id]
    total_send_time = np.array([np.array(logs["sites"]["0"]["endsend-tocoord-fromsite"]) - np.array(logs["sites"]["0"]["startsend-tocoord-fromsite"])])
    total_iter_time = np.array([np.array(logs["sites"]["0"]["enditer-site"]) - np.array(logs["sites"]["0"]["startiter-site"])])

    for site_id in logs["sites"]:
        if site_id == "0":
            continue

        site = logs["sites"][site_id]
        send_time = np.array(site["endsend-tocoord-fromsite"]) - np.array(site["startsend-tocoord-fromsite"])
        iter_time = np.array(site["enditer-site"]) - np.array(site["startiter-site"])
        total_send_time = np.vstack((total_send_time, send_time))
        total_iter_time = np.vstack((total_iter_time, iter_time))

    total_send_time = total_send_time.max(axis=0).sum()
    total_iter_time = total_iter_time.max(axis=0).sum()
    return total_send_time, total_iter_time


def parse_coord(file, requests):
    start_send_flag = True
    end_send_flag = True
    for line in file.readlines():
        line_json = json.loads(line)
        if line_json["msg"] == "Start timing":
            req_id = str(line_json["request-id"])
            requests[req_id] = {"start-time": line_json["unix-nano"],
                                                      "startsend-tocloud-fromcoord": [],
                                                      "endsend-tocloud-fromcoord": [],
                                                      "startsend-tosite-fromcoord": [],
                                                      "endsend-tosite-fromcoord": [],
                                                      "startrcv-fromcloud-tocoord": [],
                                                      "endrcv-fromcloud-tocoord": [],
                                                      "startiter-cloud": [],
                                                      "enditer-cloud": [],
                                                      "valstart-cloud": [],
                                                      "valend-cloud": [],
                                                      "sites": {},
                                                      "acc": []}
        elif line_json["msg"] == "End timing":
            req_id = str(line_json["request-id"])
            requests[req_id]["end-time"] = line_json["unix-nano"]
        elif line_json["msg"] == "Start send to cloud algo":
            req_id = str(line_json["request-id"])
            requests[req_id]["startsend-tocloud-fromcoord"].append(line_json["unix-nano"])
        elif line_json["msg"] == "End send to cloud algo":
            req_id = str(line_json["request-id"])
            requests[req_id]["endsend-tocloud-fromcoord"].append(line_json["unix-nano"])
        elif line_json["msg"] == "Start send to site connector":
            req_id = str(line_json["request-id"])
            if start_send_flag:
                requests[req_id]["startsend-tosite-fromcoord"].append(line_json["unix-nano"])
            else:
                length = len(requests[req_id]["startsend-tosite-fromcoord"])
                requests[req_id]["startsend-tosite-fromcoord"][length - 1] = max(line_json["unix-nano"],
                                                                                 requests[req_id]["startsend-tosite-fromcoord"][length - 1])
            start_send_flag = False
        elif line_json["msg"] == "End send to site connector":
            req_id = str(line_json["request-id"])
            if end_send_flag:
                requests[req_id]["endsend-tosite-fromcoord"].append(line_json["unix-nano"])
            else:
                length = len(requests[req_id]["startsend-tosite-fromcoord"])
                requests[req_id]["endsend-tosite-fromcoord"][length - 1] = max(line_json["unix-nano"],
                                                                                 requests[req_id]["endsend-tosite-fromcoord"][length - 1])
            end_send_flag = False
        elif line_json["msg"] == "Start receive from cloud algo":
            start_send_flag = True
            end_send_flag = True
            req_id = str(line_json["request-id"])
            requests[req_id]["startrcv-fromcloud-tocoord"].append(line_json["unix-nano"])
        elif line_json["msg"] == "End receive from cloud algo":
            req_id = str(line_json["request-id"])
            requests[req_id]["endrcv-fromcloud-tocoord"].append(line_json["unix-nano"])



def parse_cloudalgo(file, requests):
    for line in file.readlines():
        line_json = json.loads(line)
        if line_json["message"] == "Start iteration":
            req_id = str(line_json["request-id"])
            requests[req_id]["startiter-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "End iteration":
            req_id = str(line_json["request-id"])
            requests[req_id]["enditer-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "Acc":
            req_id = str(line_json["request-id"])
            requests[req_id]["acc"].append(line_json["accuracy"])
        elif line_json["message"] == "Start validation":
            req_id = str(line_json["request-id"])
            requests[req_id]["valstart-cloud"].append(line_json["unix-nano"])
        elif line_json["message"] == "End validation":
            req_id = str(line_json["request-id"])
            requests[req_id]["valend-cloud"].append(line_json["unix-nano"])


def parse_sites(files, requests):
    for file in files:
        for line in file.readlines():
            line_json = json.loads(line)
            if line_json["msg"] == "Start iteration":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                if site_id in requests[req_id]["sites"]:
                    requests[req_id]["sites"][site_id]["startiter-site"].append(line_json["unix-nano"])
                else:
                    requests[req_id]["sites"][site_id] = {"startiter-site": [line_json["unix-nano"]],
                                                          "enditer-site": [],
                                                          "endsend-tocoord-fromsite": [],
                                                          "startsend-tocoord-fromsite": [],}
            elif line_json["msg"] == "End iteration":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["enditer-site"].append(line_json["unix-nano"])
            elif line_json["msg"] == "Begin send to coordinator":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["startsend-tocoord-fromsite"].append(line_json["unix-nano"])
            elif line_json["msg"] == "End send to coordinator":
                site_id = str(line_json["site-id"])
                req_id = str(line_json["request-id"])
                requests[req_id]["sites"][site_id]["endsend-tocoord-fromsite"].append(line_json["unix-nano"])


def parse_baseline(file):
    baseline = {"start": None,
                "end": None,
                "val_start": [],
                "val_end": [],
                "acc": []}
    i = 0
    for line in file.readlines():
        line_json = json.loads(line)
        if line_json["message"] == "Start":
            baseline["start"] = line_json["unix-nano"]
        elif line_json["message"] == "End":
            baseline["end"] = line_json["unix-nano"]
        elif line_json["message"] == "Acc":
            baseline["acc"].append(line_json["accuracy"])
        elif line_json["message"] == "ValStart":
            baseline["val_start"].append(line_json["unix-nano"])
        elif line_json["message"] == "ValEnd":
            baseline["val_end"].append(line_json["unix-nano"])
            i += 1

    return baseline


def plot(total_time, coord_cloud_io, cloud_time, coord_site_io, site_iter_time, validation_time, baseline_time):
    coord_cloud_io = coord_cloud_io * 1e-9
    coord_site_io = coord_site_io * 1e-9
    total_time = total_time * 1e-9
    site_iter_time = site_iter_time * 1e-9
    validation_time = validation_time * 1e-9
    baseline_time = baseline_time * 1e-9
    labels = ["Baseline", "Leap"]
    width = 0.1
    fig, ax = plt.subplots()
    ax.bar(labels, [0, total_time - validation_time], width, label="Cloud Compute")
    ax.bar(labels, [0, coord_site_io + site_iter_time + coord_cloud_io], width, label="Coord-Cloud IO")
    ax.bar(labels, [0, coord_site_io + site_iter_time], width, label="Site Compute")
    ax.bar(labels, [0, coord_site_io], width, label="Coord-Site IO")
    ax.bar(labels, [baseline_time, 0], width, label="Baseline")

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
    baseline_files = open("logs/resnet_baseline.log", "r")
    parse(coord_file, cloudalgo_file, site_files, baseline_files)
