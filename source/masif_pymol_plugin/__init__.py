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

# Pablo Gainza Cirauqui 2016 LPDI IBI STI EPFL
# This pymol plugin for Masif just enables the load ply functions.

import sys

from pymol import cmd

from .loadDOTS import *
from .loadPLY import *
from .simple_mesh import *


def __init_plugin__(app):
    cmd.extend("loadply", load_ply)
    cmd.extend("loaddots", load_dots)
    cmd.extend("loadgiface", load_giface)
    cmd.extend("loadply_interest", load_ply_interest)
