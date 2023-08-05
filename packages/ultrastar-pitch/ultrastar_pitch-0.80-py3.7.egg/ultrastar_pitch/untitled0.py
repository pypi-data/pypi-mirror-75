#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:35:58 2020

@author: ruben
"""

import os
import sys
import tensorflow as tf
import onnxruntime as rt
from tf2onnx.tfonnx import process_tf_graph
from tf2onnx import constants, logging, utils, optimizer
from tf2onnx import tf_loader

MODEL = "/home/ruben/pCloudDrive/Eclipse Projects/ultrastar_pitch/ultrastar_pitch/binaries/tf2_256_96_12_stft_pca_median.model/"
OUT = "/home/ruben/pCloudDrive/Eclipse Projects/ultrastar_pitch/ultrastar_pitch/binaries/test.onnx"
OPT = "/home/ruben/pCloudDrive/Eclipse Projects/ultrastar_pitch/ultrastar_pitch/binaries/test.onnx"


graph_def, inputs, outputs = tf_loader.from_saved_model(MODEL, input_names=None, output_names=None)
with tf.Graph().as_default() as tf_graph:
    tf.import_graph_def(graph_def, name='')
with tf_loader.tf_session(graph=tf_graph):
    g = process_tf_graph(tf_graph, input_names=inputs, output_names=outputs)
    
onnx_graph = optimizer.optimize_graph(g)
model_proto = onnx_graph.make_model("converted from {}".format(MODEL))
utils.save_protobuf(OUT, model_proto)

sess_options = rt.SessionOptions()
sess_options.execution_mode = rt.ExecutionMode.ORT_PARALLEL
sess_options.inter_op_num_threads = 2
# Set graph optimization level
print(sess_options.inter_op_num_threads)
sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL

# To enable model serialization after graph optimization set this
sess_options.optimized_model_filepath = OPT
session = rt.InferenceSession(OUT, sess_options)