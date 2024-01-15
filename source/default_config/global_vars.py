# global_vars.py: Global variables used by MaSIF -- mainly pointing to environment variables of programs used by MaSIF.
# Pablo Gainza - LPDI STI EPFL 2018-2019
# Released under an Apache License 2.0
# Modified by Yu-Yuan Yang (2024)

import configparser
import sys

from IPython.core.debugger import set_trace

epsilon = 1.0e-6

# Read config file.
config = configparser.ConfigParser()
path_args = __file__.split("/")[0:-1]
root_path = "/".join(path_args)
config.read(f"{root_path}/config.cfg")
config.sections()

# Set the environment variables for the programs used by MaSIF.
msms_bin = ""
if "MSMS_BIN" in config["Default"]:
    msms_bin = config["Default"]["MSMS_BIN"]
else:
    set_trace()
    print("ERROR: MSMS_BIN not set. Variable should point to MSMS program.")
    sys.exit(1)

reduce_bin = ""
if "REDUCE_BIN" in config["Default"]:
    reduce_bin = config["Default"]["REDUCE_BIN"]
else:
    print("ERROR: REDUCE_BIN not set. Variable should point to REDUCE program.")
    sys.exit(1)

pdb2pqr_bin = ""
if "PDB2PQR_BIN" in config["Default"]:
    pdb2pqr_bin = config["Default"]["PDB2PQR_BIN"]
else:
    print("ERROR: PDB2PQR_BIN not set. Variable should point to PDB2PQR_BIN program.")
    sys.exit(1)

apbs_bin = ""
if "APBS_BIN" in config["Default"]:
    apbs_bin = config["Default"]["APBS_BIN"]
else:
    print("ERROR: APBS_BIN not set. Variable should point to APBS program.")
    sys.exit(1)

multivalue_bin = ""
if "MULTIVALUE_BIN" in config["Default"]:
    multivalue_bin = config["Default"]["MULTIVALUE_BIN"]
else:
    print("ERROR: MULTIVALUE_BIN not set. Variable should point to MULTIVALUE program.")
    sys.exit(1)

class NoSolutionError(Exception):
    pass
