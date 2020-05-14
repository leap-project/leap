# - config: The path to the config file for the cloud algo
#
# Usage: python -m sitealgo_main -config=../config/sitealgo_config.json

import sys
sys.path.append('../')

from sitealgo.site_algo import SiteAlgo
import multiprocessing
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-config", "--config", default="../config/sitealgo1_config.json", help="Path to the config file")
args = parser.parse_args()

if __name__ == "__main__":
    node = SiteAlgo(args.config)
    serverProcess = multiprocessing.Process(target=node.serve)
    serverProcess.start()