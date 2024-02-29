"""
protonate.py: Wrapper method for the reduce program: protonate (i.e., add hydrogens) a pdb using reduce 
                and save to an output file.
Pablo Gainza - LPDI STI EPFL 2019
Released under an Apache License 2.0
Modified by Yu-Yuan Yang (2024)
"""

from subprocess import PIPE, Popen

from ..default_config.global_vars import pdb2pqr_bin, reduce_bin


def protonate(in_pdb_file, out_pdb_file, method="reduce"):
    """
    protonate (i.e., add hydrogens) a pdb using reduce and save to an output file.
    in_pdb_file: file to protonate.
    out_pdb_file: output file where to save the protonated pdb file.
    """
    if method == None:
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
        pqr_out_file = out_pdb_file.replace(".pdb", "")
        apbs_in_file = out_pdb_file.replace(".pdb", ".in")
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

    else:
        raise ValueError(f"Unknown protonation method: {method}")

    return None
