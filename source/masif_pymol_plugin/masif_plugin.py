# Pablo Gainza Cirauqui 2016 LPDI IBI STI EPFL
# This pymol plugin for Masif just enables the load ply functions.

import sys

from pymol import cmd

from .loadDOTS import *
from .loadPLY import *

cmd.extend("loadply", load_ply)
cmd.extend("loaddots", load_dots)
cmd.extend("loadgiface", load_giface)
