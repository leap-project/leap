# - config: The path to the config file for the cloud algo
#
# Usage: python -m cloudalgo_main -config=../config/cloudalgo_config.json

import sys
sys.path.append("../")

from cloudalgo.cloud_algo import CloudAlgo
import multiprocessing
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", default="../config/cloudalgo_config.json", help="Path to the config file")
args = parser.parse_args()


if __name__ == "__main__":
    node = CloudAlgo(args.config)
    serverProcess = multiprocessing.Process(target=node.serve)
    serverProcess.start()