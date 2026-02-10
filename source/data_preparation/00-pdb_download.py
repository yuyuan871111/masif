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

#!/usr/bin/python
import importlib
import os
import sys

import Bio
from Bio.PDB import *

# Local includes
from ..default_config.masif_opts import masif_opts
from ..input_output.protonate import protonate

if len(sys.argv) <= 1:
    print("Usage: " + sys.argv[0] + " PDBID_A_B")
    print("A or B are the chains to include in this pdb.")
    sys.exit(1)

if not os.path.exists(masif_opts["raw_pdb_dir"]):
    os.makedirs(masif_opts["raw_pdb_dir"])

if not os.path.exists(masif_opts["tmp_dir"]):
    os.mkdir(masif_opts["tmp_dir"])

in_fields = sys.argv[1].split("_")
pdb_id = in_fields[0]

# Download pdb
pdbl = PDBList(server="http://ftp.wwpdb.org")
pdb_filename = pdbl.retrieve_pdb_file(
    pdb_id, pdir=masif_opts["tmp_dir"], file_format="pdb"
)

##### Protonate with reduce, if hydrogens included.
# - Always protonate as this is useful for charges. If necessary ignore hydrogens later.
protonated_file = masif_opts["raw_pdb_dir"] + "/" + pdb_id + ".pdb"
protonate(pdb_filename, protonated_file)
pdb_filename = protonated_file
