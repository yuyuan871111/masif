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


"""
protonate.py: Wrapper method for the reduce program: protonate (i.e., add hydrogens) a pdb using reduce 
                and save to an output file.
Pablo Gainza - LPDI STI EPFL 2019
Released under an Apache License 2.0
Modified by Yu-Yuan Yang (2025)
"""

import os
import random
from subprocess import PIPE, Popen
from time import strftime

from ..default_config.global_vars import pdb2pqr_bin, reduce_bin


def protonate(in_pdb_file, out_pdb_file, method="reduce", keep_tempfiles=False):
    """
    protonate (i.e., add hydrogens) a pdb using reduce and save to an output file.
    in_pdb_file: file to protonate.
    out_pdb_file: output file where to save the protonated pdb file.
    """
    if method is None:
        pass
    elif method == "reduce":
        # Remove protons first, in case the structure is already protonated
        args = [reduce_bin, "-Trim", in_pdb_file]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()
        outfile = open(out_pdb_file, "w")
        outfile.write(stdout.decode("utf-8").rstrip())
        outfile.close()
        # Now add them again.
        args = [reduce_bin, "-HIS", out_pdb_file]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()
        # write the output to a file.
        outfile = open(out_pdb_file, "w")
        outfile.write(stdout.decode("utf-8"))
        outfile.close()

    elif method == "propka":
        # Create temporary directory
        now = strftime("%y%m%d%H%M%S")
        randnum = str(random.randint(1, 10000000))
        tmp_file_base = f"{in_pdb_file.replace('.pdb', '')}_temp_{now}_{randnum}"
        os.makedirs(tmp_file_base, exist_ok=False)

        filename = out_pdb_file.replace(".pdb", "").split("/")[-1]
        apbs_in_file = f"{tmp_file_base}/{filename}.in"
        pqr_out_file = f"{tmp_file_base}/{filename}"

        args = [
            pdb2pqr_bin,
            "--ff=CHARMM",
            "--pdb-output",
            out_pdb_file,
            "--whitespace",
            "--apbs-input",
            apbs_in_file,
            "--titration-state-method=propka",
            in_pdb_file,
            pqr_out_file,
        ]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p2.communicate()

        if os.path.exists(out_pdb_file):
            if keep_tempfiles:
                return tmp_file_base
            else:
                os.system(f"rm -r {tmp_file_base}")
        else:
            raise Exception(f"Error in protonation. Check log file in {tmp_file_base}")

    else:
        raise ValueError(f"Unknown protonation method: {method}")
