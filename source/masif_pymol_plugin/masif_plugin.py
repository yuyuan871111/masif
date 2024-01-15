# Pablo Gainza Cirauqui 2016 LPDI IBI STI EPFL
# This pymol plugin for Masif just enables the load ply functions.

import sys

from loadDOTS import *
from loadPLY import *
from pymol import cmd

cmd.extend("loadply", load_ply)
cmd.extend("loaddots", load_dots)
cmd.extend("loadgiface", load_giface)
