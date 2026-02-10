# MaSIF (Molecular Surface Interaction Fingerprints)
# Fork with modifications: https://github.com/yuyuan871111/masif
# Upstream: https://github.com/LPDI-EPFL/masif
#
# This file has been modified in this fork.
#
# Original work Copyright (c) 2019 Gainza P, Sverrisson F, Monti F, Rodola,
# Bronstein MM, Correia BE
# Modifications Copyright (c) 2024-2026 Yu-Yuan (Stuart) Yang /
# Arianna Fornili's Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# NOTICE: This product includes software developed by the MaSIF authors and contributors.
#
# (Optional) Change log / compare view:
# https://github.com/LPDI-EPFL/masif/compare/master...yuyuan871111:masif:master

import configparser
import sys

from IPython.core.debugger import set_trace

epsilon = 1.0e-6

# Read config file.
config = configparser.ConfigParser()
path_args = __file__.split("/")[0:-1]
root_path = "/".join(path_args)
# config.read(f"{root_path}/config.cfg")            # serve as a main module
config.read(f"{root_path}/../../../../config.cfg")  # serve as a submodule
config.sections()

# Set the environment variables for the programs used by MaSIF.
msms_bin = ""
if "MSMS_BIN" in config["ThirdParty"]:
    msms_bin = config["ThirdParty"]["MSMS_BIN"]
else:
    set_trace()
    print("ERROR: MSMS_BIN not set. Variable should point to MSMS program.")
    sys.exit(1)

reduce_bin = ""
if "REDUCE_BIN" in config["ThirdParty"]:
    reduce_bin = config["ThirdParty"]["REDUCE_BIN"]
else:
    print("ERROR: REDUCE_BIN not set. Variable should point to REDUCE program.")
    sys.exit(1)

pdb2pqr_bin = ""
if "PDB2PQR_BIN" in config["ThirdParty"]:
    pdb2pqr_bin = config["ThirdParty"]["PDB2PQR_BIN"]
else:
    print("ERROR: PDB2PQR_BIN not set. Variable should point to PDB2PQR_BIN program.")
    sys.exit(1)

apbs_bin = ""
if "APBS_BIN" in config["ThirdParty"]:
    apbs_bin = config["ThirdParty"]["APBS_BIN"]
else:
    print("ERROR: APBS_BIN not set. Variable should point to APBS program.")
    sys.exit(1)

multivalue_bin = ""
if "MULTIVALUE_BIN" in config["ThirdParty"]:
    multivalue_bin = config["ThirdParty"]["MULTIVALUE_BIN"]
else:
    print("ERROR: MULTIVALUE_BIN not set. Variable should point to MULTIVALUE program.")
    sys.exit(1)


class NoSolutionError(Exception):
    pass
