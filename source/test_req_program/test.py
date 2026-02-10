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
