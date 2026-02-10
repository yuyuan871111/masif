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

import os
import sys

from SBI.structure import PDB

from ..default_config.masif_opts import masif_opts

ligands = ["ADP", "COA", "FAD", "HEM", "NAD", "NAP", "SAM"]

if not os.path.exists(masif_opts["ligand"]["assembly_dir"]):
    os.mkdir(masif_opts["ligand"]["assembly_dir"])


def assemble(pdb_id):
    # Reads and builds the biological assembly of a structure
    struct = PDB(
        os.path.join(masif_opts["raw_pdb_dir"], "{}.pdb".format(pdb_id)), header=True
    )
    try:
        struct_assembly = struct.apply_biomolecule_matrices()[0]
    except:
        return 0
    struct_assembly.write(
        os.path.join(masif_opts["ligand"]["assembly_dir"], "{}.pdb".format(pdb_id))
    )
    return 1


in_fields = sys.argv[1].split("_")
pdb_id = in_fields[0]

res = assemble(pdb_id)
if res:
    print("Building assembly was successfull for {}".format(pdb_id))
else:
    print("Building assembly was not successfull for {}".format(pdb_id))
