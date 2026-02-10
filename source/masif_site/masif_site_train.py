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


# Header variables and parameters.
import importlib
import os
import sys

import numpy as np
from IPython.core.debugger import set_trace

from ..default_config.masif_opts import masif_opts

"""
masif_site_train.py: Entry function to train MaSIF-site.
Pablo Gainza - LPDI STI EPFL 2019
This file is part of MaSIF.
Released under an Apache License 2.0
"""

params = masif_opts["site"]

if len(sys.argv) > 0:
    custom_params_file = sys.argv[1]
    custom_params = importlib.import_module(custom_params_file, package=None)
    custom_params = custom_params.custom_params

    for key in custom_params:
        print("Setting {} to {} ".format(key, custom_params[key]))
        params[key] = custom_params[key]


# Apply mask to input_feat
def mask_input_feat(input_feat, mask):
    mymask = np.where(np.array(mask) == 0.0)[0]
    return np.delete(input_feat, mymask, axis=2)


if "pids" not in params:
    params["pids"] = ["p1", "p2"]

# Build the neural network model
from masif_modules.MaSIF_site import MaSIF_site

if "n_theta" in params:
    learning_obj = MaSIF_site(
        params["max_distance"],
        n_thetas=params["n_theta"],
        n_rhos=params["n_rho"],
        n_rotations=params["n_rotations"],
        idx_gpu="/gpu:1",
        feat_mask=params["feat_mask"],
        n_conv_layers=params["n_conv_layers"],
    )
else:
    learning_obj = MaSIF_site(
        params["max_distance"],
        n_thetas=4,
        n_rhos=3,
        n_rotations=4,
        idx_gpu="/gpu:1",
        feat_mask=params["feat_mask"],
        n_conv_layers=params["n_conv_layers"],
    )

# train
from masif_modules.train_masif_site import train_masif_site

print(params["feat_mask"])
if not os.path.exists(params["model_dir"]):
    os.makedirs(params["model_dir"])
else:
    # Load existing network.
    print("Reading pre-trained network")
    learning_obj.saver.restore(learning_obj.session, params["model_dir"] + "model")

train_masif_site(learning_obj, params)
