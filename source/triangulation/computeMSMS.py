import os
import random
import sys
from subprocess import PIPE, Popen

from ..default_config.global_vars import msms_bin
from ..default_config.masif_opts import masif_opts
from ..input_output.read_msms import read_msms
from ..triangulation.xyzrn import output_pdb_as_xyzrn


# Pablo Gainza LPDI EPFL 2017-2019
# Calls MSMS and returns the vertices.
# Special atoms are atoms with a reduced radius.
def computeMSMS(pdb_file, protonate=True):
    randnum = random.randint(1, 10000000)
    file_base = masif_opts["tmp_dir"] + "/msms_" + str(randnum)
    out_xyzrn = file_base + ".xyzrn"

    if protonate:
        output_pdb_as_xyzrn(pdb_file, out_xyzrn)
    else:
        print("Error - pdb2xyzrn is deprecated.")
        sys.exit(1)

    # Now run MSMS on xyzrn file and Try to read ths msms file
    # if it fails, try again with a different probe radius.
    pr_dynamic_adjust = [1.5, 1.499, 1.501, 1.49, 1.51]
    for idx, probe_radius in enumerate(pr_dynamic_adjust):
        try:
            run_msms(out_xyzrn, file_base, probe_radius)
            vertices, faces, normals, names = read_msms(file_base)
        except Exception as e:
            print(f"[Warning]: {e}")
            print(
                f"[Warning]: running errors with probe radius {probe_radius} in MSMS.",
            )
            if idx < len(pr_dynamic_adjust):
                print(f"Trying another parameter = {pr_dynamic_adjust[idx+1]}.")
            else:
                print("Error - All candidate probe radius failed. Exiting.")
                sys.exit(1)
            continue
        else:
            break

    # Read the areas file
    areas = {}
    ses_file = open(file_base + ".area")
    next(ses_file)  # ignore header line
    for line in ses_file:
        fields = line.split()
        areas[fields[3]] = fields[1]

    # Remove temporary files.
    os.remove(file_base + ".area")
    os.remove(file_base + ".xyzrn")
    os.remove(file_base + ".vert")
    os.remove(file_base + ".face")

    return vertices, faces, normals, names, areas


def run_msms(out_xyzrn, file_base, probe_radius=1.5):
    FNULL = open(os.devnull, "w")
    # string with 3 digits after the decimal point.
    probe_radius = "{:.3f}".format(probe_radius)
    args = [
        msms_bin,
        "-density",
        "3.0",
        "-hdensity",
        "3.0",
        "-probe",
        probe_radius,
        "-if",
        out_xyzrn,
        "-of",
        file_base,
        "-af",
        file_base,
    ]
    # print msms_bin+" "+`args`
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()

    return None
