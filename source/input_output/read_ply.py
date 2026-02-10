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


import numpy
import pymesh

"""
read_ply.py: Read a ply file from disk using pymesh and load the attributes used by MaSIF.
Pablo Gainza - LPDI STI EPFL 2019
Released under an Apache License 2.0
"""


def read_ply(filename):
    # Read a ply file from disk using pymesh and load the attributes used by MaSIF.
    # filename: the input ply file.
    # returns data as tuple.
    mesh = pymesh.load_mesh(filename)

    attributes = mesh.get_attribute_names()
    if "vertex_nx" in attributes:
        nx = mesh.get_attribute("vertex_nx")
        ny = mesh.get_attribute("vertex_ny")
        nz = mesh.get_attribute("vertex_nz")

        normals = numpy.column_stack((nx, ny, nz))
    else:
        normals = None
    if "vertex_charge" in attributes:
        charge = mesh.get_attribute("vertex_charge")
    else:
        charge = numpy.array([0.0] * len(mesh.vertices))

    if "vertex_cb" in attributes:
        vertex_cb = mesh.get_attribute("vertex_cb")
    else:
        vertex_cb = numpy.array([0.0] * len(mesh.vertices))

    if "vertex_hbond" in attributes:
        vertex_hbond = mesh.get_attribute("vertex_hbond")
    else:
        vertex_hbond = numpy.array([0.0] * len(mesh.vertices))

    if "vertex_hphob" in attributes:
        vertex_hphob = mesh.get_attribute("vertex_hphob")
    else:
        vertex_hphob = numpy.array([0.0] * len(mesh.vertices))

    return (
        mesh.vertices,
        mesh.faces,
        normals,
        charge,
        vertex_cb,
        vertex_hbond,
        vertex_hphob,
    )
