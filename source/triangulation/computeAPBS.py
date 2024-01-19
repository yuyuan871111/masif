import os
from subprocess import PIPE, Popen

import numpy

from ..default_config.global_vars import apbs_bin, multivalue_bin, pdb2pqr_bin

"""
computeAPBS.py: Wrapper function to compute the Poisson Boltzmann electrostatics for a surface using APBS.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""


def computeAPBS(vertices, pdb_file, tmp_file_base, pdb2pqr_skip=False):
    """
    Calls APBS, pdb2pqr, and multivalue and returns the charges per vertex
    """
    fields = tmp_file_base.split("/")[0:-1]
    directory = "/".join(fields) + "/"
    filename_base = tmp_file_base.split("/")[-1]
    pdbname = pdb_file.split("/")[-1]

    # Prepare the APBS input file with pdb2pqr
    if not pdb2pqr_skip:
        args = [
            pdb2pqr_bin,
            "--ff=PARSE",
            "--whitespace",
            "--noopt",
            "--apbs-input",
            f"{filename_base}.in",
            pdbname,  # input: PDB file
            filename_base,  # output: PQR formated file
        ]
        p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
        stdout, stderr = p2.communicate()

    # Calculate potentials with APBS
    args = [apbs_bin, filename_base + ".in"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
    stdout, stderr = p2.communicate()

    vertfile = open(directory + "/" + filename_base + ".csv", "w")
    for vert in vertices:
        vertfile.write("{},{},{}\n".format(vert[0], vert[1], vert[2]))
    vertfile.close()

    # Access the potential for each vertex with multivalue
    args = [
        multivalue_bin,
        filename_base + ".csv",
        filename_base + ".dx",
        filename_base + "_out.csv",
    ]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE, cwd=directory)
    stdout, stderr = p2.communicate()

    # Read the charge file
    chargefile = open(tmp_file_base + "_out.csv")
    charges = numpy.array([0.0] * len(vertices))
    for ix, line in enumerate(chargefile.readlines()):
        charges[ix] = float(line.split(",")[3])

    remove_fn = os.path.join(directory, filename_base)
    os.remove(remove_fn)
    os.remove(remove_fn + ".csv")
    os.remove(remove_fn + ".dx")
    os.remove(remove_fn + ".in")
    os.remove(os.path.join(directory, "io.mc"))
    os.remove(remove_fn + "_out.csv")

    return charges
