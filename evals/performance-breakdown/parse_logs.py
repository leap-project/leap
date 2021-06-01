import json
import numpy as np
import glob
import matplotlib.pyplot as plt
import os

# TODO: Fix problem with some sites not having 15 sends to coordinator (they have only 14 instead)


def get_time_baseline(baseline_files):
    baseline = parse_baseline(baseline_files)
    baseline_total_time = baseline["end"] - baseline["start"]
    baseline_validation_time = (np.array(baseline["val_end"]) - np.array(baseline["val_start"])).sum()
    baseline_total_time = baseline_total_time - baseline_validation_time
    return baseline_total_time, baseline["acc"]


def get_time_leap(coord_file_path, cloudalgo_file_path, sites_files):
    requests = {}
    parse_coord(coord_file_path, requests)
    parse_cloudalgo(cloudalgo_file_path, requests)
    parse_sites(sites_files, requests)
    total_time = requests["0"]["end-time"] - requests["0"]["start-time"]
    coord_site_send = (np.array(requests["0"]["endsend-tosite-fromcoord"]) - np.array(requests["0"]["startsend-tosite-fromcoord"])).sum()
    coord_cloud_send = (np.array(requests["0"]["endsend-tocloud-fromcoord"]) - np.array(requests["0"]["startsend-tocloud-fromcoord"])).sum()
    coord_cloud_rcv = (np.array(requests["0"]["endrcv-fromcloud-tocoord"]) - np.array(requests["0"]["startrcv-fromcloud-tocoord"])).sum()

    cloud_time = (np.array(requests["0"]["enditer-cloud"]) - np.array(requests["0"]["startiter-cloud"])).sum()
    validation_time = (np.array(requests["0"]["valend-cloud"]) - np.array(requests["0"]["valstart-cloud"])).sum()
    site_to_coord_send, site_iter_time = get_time_spent_on_sites(requests, "0")

    accuracies = requests["0"]["acc"]

    coord_site_io = coord_site_send + site_to_coord_send
    coord_cloud_io = coord_cloud_send + coord_cloud_rcv
    return {"total_time": total_time,
            "coord_cloud_io": coord_cloud_io,
            "cloud_time": cloud_time,
            "coord_site_io": coord_site_io,
            "site_iter_time": site_iter_time,
            "validation_time": validation_time,
            "acc": accuracies}


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

        if send_time.size == 14:
            total_send_time = np.vstack((total_send_time, np.append(send_time, 0)))

        if iter_time.size == 14:
            total_iter_time = np.vstack((total_iter_time, np.append(iter_time, 0)))

    total_send_time = total_send_time.max(axis=0).sum()
    total_iter_time = total_iter_time.max(axis=0).sum()
    return total_send_time, total_iter_time


def parse_coord(file_path, requests):
    with open(file_path, "rb") as file:
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


def parse_cloudalgo(file_path, requests):
    with open(file_path, "rb") as file:
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


def plot_bar_charts(baseline_time, measurements_list):
    baseline_time = baseline_time * 1e-9
    labels = ["Baseline"]
    width = 0.3
    fig, ax = plt.subplots()

    cloud_compute_all = [0]
    coord_cloud_io_all = [0]
    site_compute_all = [0]
    coord_site_io_all = [0]
    baseline_time_all = [baseline_time]

    for measurement in measurements_list:
        labels.append(str(measurement["n_sites"]))
        coord_cloud_io = measurement["coord_cloud_io"] * 1e-9
        coord_site_io = measurement["coord_site_io"] * 1e-9
        total_time = measurement["total_time"] * 1e-9
        site_iter_time = measurement["site_iter_time"] * 1e-9
        validation_time = measurement["validation_time"] * 1e-9

        cloud_compute_all.append(total_time - validation_time)
        coord_cloud_io_all.append(coord_site_io + site_iter_time + coord_cloud_io)
        site_compute_all.append(coord_site_io + site_iter_time)
        coord_site_io_all.append(coord_site_io)
        baseline_time_all.append(0)

    ax.bar(labels, cloud_compute_all, width, label="Cloud Compute")
    ax.bar(labels, coord_cloud_io_all, width, label="Coord-Cloud IO")
    ax.bar(labels, site_compute_all, width, label="Site Compute")
    ax.bar(labels, coord_site_io_all, width, label="Coord-Site IO")
    ax.bar(labels, baseline_time_all, width, label="Baseline")

    ax.set_ylabel("Time (seconds)")
    ax.set_title("Training Time Resnet 18")
    ax.legend()
    plt.show()


def plot_accuracies(baseline_accuracy, measurements):
    baseline_accuracy = list(map(float, baseline_accuracy))
    iters = range(1, len(baseline_accuracy) + 1)
    plt.plot(iters, baseline_accuracy, label="Baseline")
    for measurement in measurements:
        accuracies = measurement["acc"]
        plt.plot(iters, accuracies, label=str(measurement["n_sites"]))

    title = "Validation Accuracy During Training"
    plt.title(title)
    plt.xlabel("Iterations")
    plt.ylabel("Classification Accuracy")
    plt.ylim(0, 1)
    plt.legend()
    plt.show()


def open_site_files(logs_path):
    files = []
    for filename in glob.glob(logs_path + "/site[0-9]*.log"):
        files.append(open(filename, "rb"))
    return files


def get_avg_measurements(n_sites, measurements):
    # TODO: Find best way to deal with multiple runs and val accuracy
    avg_measurements = {
        "n_sites": n_sites,
        "total_time": 0,
        "coord_cloud_io": 0,
        "cloud_time": 0,
        "coord_site_io": 0,
        "site_iter_time": 0,
        "validation_time": 0,
        "acc": np.zeros(len(measurements[0]["acc"]))}

    for measurement in measurements:
        avg_measurements["total_time"] += measurement["total_time"] / len(measurements)
        avg_measurements["coord_cloud_io"] += measurement["coord_cloud_io"] / len(measurements)
        avg_measurements["cloud_time"] += measurement["cloud_time"] / len(measurements)
        avg_measurements["coord_site_io"] += measurement["coord_site_io"] / len(measurements)
        avg_measurements["site_iter_time"] += measurement["site_iter_time"] / len(measurements)
        avg_measurements["validation_time"] += measurement["validation_time"] / len(measurements)
        avg_measurements["acc"] += np.array(measurement["acc"]) / len(measurements)

    return avg_measurements


def main():
    scalability = [1, 5, 10, 15]
    measurements_list = []
    for n_sites in scalability:
        exp_path = "logs/sites" + str(n_sites) + "/"
        trials_paths = os.listdir(exp_path)
        measurements = []
        for trial_path in trials_paths:
            trial_path = exp_path + trial_path
            site_files = open_site_files(trial_path)
            coord_file_path = trial_path + "/coordinator.log"
            clodalgo_file_path = trial_path + "/cloudalgo.log"
            measurement = get_time_leap(coord_file_path, clodalgo_file_path, site_files)
            measurements.append(measurement)

        avg_measurements = get_avg_measurements(n_sites, measurements)
        measurements_list.append(avg_measurements)

    baseline_time = None
    baseline_accuracies = None
    with open("../baselines/logs/resnet_baseline.log", "rb") as baseline_file:
        baseline_time, baseline_accuracies = get_time_baseline(baseline_file)

    plot_bar_charts(baseline_time, measurements_list)
    plot_accuracies(baseline_accuracies, measurements_list)


if __name__ == "__main__":
    main()

