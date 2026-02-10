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


import tensorflow as tf


def _parse_function(example_proto):
    keys_to_features = {
        "input_feat_shape": tf.FixedLenFeature([3], dtype=tf.int64),
        "input_feat": tf.VarLenFeature(dtype=tf.float32),
        "rho_wrt_center_shape": tf.FixedLenFeature([2], dtype=tf.int64),
        "rho_wrt_center": tf.VarLenFeature(dtype=tf.float32),
        "theta_wrt_center_shape": tf.FixedLenFeature([2], dtype=tf.int64),
        "theta_wrt_center": tf.VarLenFeature(dtype=tf.float32),
        "mask_shape": tf.FixedLenFeature([3], dtype=tf.int64),
        "mask": tf.VarLenFeature(dtype=tf.float32),
        "pdb": tf.FixedLenFeature([], dtype=tf.string),
        "pocket_labels_shape": tf.FixedLenFeature([2], dtype=tf.int64),
        "pocket_labels": tf.VarLenFeature(dtype=tf.int64),
    }
    parsed_features = tf.parse_single_example(example_proto, keys_to_features)
    input_feat = tf.sparse_tensor_to_dense(parsed_features["input_feat"])
    input_feat = tf.reshape(
        input_feat, tf.cast(parsed_features["input_feat_shape"], tf.int32)
    )
    rho_wrt_center = tf.sparse_tensor_to_dense(parsed_features["rho_wrt_center"])
    rho_wrt_center = tf.reshape(
        rho_wrt_center, tf.cast(parsed_features["rho_wrt_center_shape"], tf.int32)
    )
    theta_wrt_center = tf.sparse_tensor_to_dense(parsed_features["theta_wrt_center"])
    theta_wrt_center = tf.reshape(
        theta_wrt_center, tf.cast(parsed_features["theta_wrt_center_shape"], tf.int32)
    )
    mask = tf.sparse_tensor_to_dense(parsed_features["mask"])
    mask = tf.reshape(mask, tf.cast(parsed_features["mask_shape"], tf.int32))
    labels = tf.sparse_tensor_to_dense(parsed_features["pocket_labels"])
    labels = tf.reshape(
        labels, tf.cast(parsed_features["pocket_labels_shape"], tf.int32)
    )
    return (
        input_feat,
        rho_wrt_center,
        theta_wrt_center,
        mask,
        labels,
        parsed_features["pdb"],
    )
