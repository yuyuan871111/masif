"""
test.py: Test the third-party programe such as reduce, msms, etc.
Yu-Yuan Yang (2024)
Released under an Apache License 2.0
"""

from subprocess import PIPE, Popen

from ..default_config.global_vars import msms_bin, reduce_bin


def test_reduce():
    # Test reduce
    args = [reduce_bin, "-h"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"))


def test_msms():
    # Test msms
    args = [msms_bin, "-h"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"))


"""
def test_xyzrn():
    # Test xyzrn
    args = [xyzrn_bin, "-h"]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"))
"""
