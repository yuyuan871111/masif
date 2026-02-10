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
from subprocess import PIPE, Popen
from time import strftime

import numpy

from ..default_config.global_vars import apbs_bin, multivalue_bin, pdb2pqr_bin

"""
Modified by Yu-Yuan (Stuart) Yang - 2024

computeAPBS.py: Wrapper function to compute the Poisson Boltzmann electrostatics for a surface using APBS.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""


def computeAPBS(
    vertices, pdb_file, tmp_file_base=None, pdb2pqr_skip=False, keep_logfile=False
):
    """
    Calls APBS, pdb2pqr, and multivalue and returns the charges per vertex
    """
    # Set up
    pdbname = pdb_file.split("/")[-1]
    filename_base = pdbname.replace(".pdb", "")
    if tmp_file_base is None:
        now = strftime("%y%m%d%H%M%S")
        tmp_file_base = f"{pdb_file.replace('.pdb', '')}_temp_{now}"
        os.makedirs(tmp_file_base, exist_ok=True)

    # Prepare the APBS input file with pdb2pqr
    if not pdb2pqr_skip:
        args = [
            pdb2pqr_bin,
            "--ff=PARSE",
            "--whitespace",
            "--noopt",
            "--apbs-input",
            f"{filename_base}.in",
            pdb_file,  # input: PDB file
            f"{filename_base}",  # output: PQR formated file
        ]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=tmp_file_base)
        stdout, stderr = p2.communicate()

    # Calculate potentials with APBS
    args = [apbs_bin, f"{filename_base}.in"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=tmp_file_base)
    stdout, stderr = p2.communicate()

    vertfile = open(f"{tmp_file_base}/{filename_base}.csv", "w")
    for vert in vertices:
        vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))
    vertfile.close()

    # Access the potential for each vertex with multivalue
    args = [
        multivalue_bin,
        f"{filename_base}.csv",
        f"{filename_base}.dx",
        f"{filename_base}_out.csv",
    ]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=tmp_file_base)
    stdout, stderr = p2.communicate()

    # Read the charge file
    chargefile = open(f"{tmp_file_base}/{filename_base}_out.csv")
    charges = numpy.array([0.0] * len(vertices))
    for ix, line in enumerate(chargefile.readlines()):
        charges[ix] = float(line.split(",")[3])
    chargefile.close()

    # Clean up
    if not keep_logfile:
        os.remove(f"{tmp_file_base}/{filename_base}")
        os.remove(f"{tmp_file_base}/{filename_base}.in")
        os.remove(f"{tmp_file_base}/{filename_base}.csv")
        os.remove(f"{tmp_file_base}/{filename_base}.dx")
        os.remove(f"{tmp_file_base}/{filename_base}_out.csv")
        os.remove(f"{tmp_file_base}/{filename_base}.log")
        os.remove(f"{tmp_file_base}/io.mc")
        os.rmdir(tmp_file_base)

    return charges
