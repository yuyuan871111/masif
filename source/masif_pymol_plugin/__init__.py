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
