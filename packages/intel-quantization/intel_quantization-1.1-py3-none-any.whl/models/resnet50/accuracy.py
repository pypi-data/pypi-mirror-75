#
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2019 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from google.protobuf import text_format
import tensorflow as tf
import preprocessing
import datasets

NUM_TEST_IMAGES = 50000


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    import os
    file_ext = os.path.splitext(model_file)[1]

    with open(model_file, "rb") as f:
        if file_ext == '.pbtxt':
            text_format.Merge(f.read(), graph_def)
        else:
            graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')

    return graph


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_graph", default=None,
                        help="graph/model to be executed")
    parser.add_argument("--data_location", default=None,
                        help="full path to the validation data")
    parser.add_argument("--input_height", default=None,
                        type=int, help="input height")
    parser.add_argument("--input_width", default=None,
                        type=int, help="input width")
    parser.add_argument("--batch_size", default=32,
                        type=int, help="batch size")
    parser.add_argument("--input_layer", default="input",
                        help="name of input layer")
    parser.add_argument("--output_layer", default="predict",
                        help="name of output layer")
    parser.add_argument(
        '--num_inter_threads',
        help='number threads across operators',
        type=int, default=1)
    parser.add_argument(
        '--num_intra_threads',
        help='number threads for an operator',
        type=int, default=1)
    parser.add_argument(
        '--num_batches',
        help='num of batch to run.',
        type=int, default=0)
    args = parser.parse_args()

    if args.input_graph:
        model_file = args.input_graph
    else:
        sys.exit("Please provide a graph file.")
    if args.input_height:
        input_height = args.input_height
    else:
        input_height = 224
    if args.input_width:
        input_width = args.input_width
    else:
        input_width = 224
    batch_size = args.batch_size
    input_layer = args.input_layer
    output_layer = args.output_layer
    num_inter_threads = args.num_inter_threads
    num_intra_threads = args.num_intra_threads
    data_location = args.data_location
    dataset = datasets.ImagenetData(data_location)
    preprocessor = preprocessing.ImagePreprocessor(
        input_height, input_width, batch_size,
        1,  # device count
        tf.float32,  # data_type for input fed to the graph
        train=False,  # doing inference
        resize_method='crop')
    images, labels = preprocessor.minibatch(dataset, subset='validation')
    graph = load_graph(model_file)
    input_tensor = graph.get_tensor_by_name(input_layer + ":0")
    output_tensor = graph.get_tensor_by_name(output_layer + ":0")

    config = tf.ConfigProto()
    config.inter_op_parallelism_threads = num_inter_threads
    config.intra_op_parallelism_threads = num_intra_threads

    total_accuracy1, total_accuracy5 = (0.0, 0.0)
    num_processed_images = 0
    num_remaining_images = dataset.num_examples_per_epoch(subset='validation') \
                           - num_processed_images
    if args.num_batches > 0:
        num_remaining_images = batch_size * args.num_batches
    with tf.Session() as sess:
        sess_graph = tf.Session(graph=graph, config=config)
        while num_remaining_images >= batch_size:
            # Reads and preprocess data
            np_images, np_labels = sess.run([images[0], labels[0]])
            num_processed_images += batch_size
            num_remaining_images -= batch_size
            # Compute inference on the preprocessed data
            predictions = sess_graph.run(output_tensor,
                                         {input_tensor: np_images})
            accuracy1 = tf.reduce_sum(
                tf.cast(tf.nn.in_top_k(tf.constant(predictions),
                                       tf.constant(np_labels), 1), tf.float32))

            accuracy5 = tf.reduce_sum(
                tf.cast(tf.nn.in_top_k(tf.constant(predictions),
                                       tf.constant(np_labels), 5), tf.float32))
            np_accuracy1, np_accuracy5 = sess.run([accuracy1, accuracy5])
            total_accuracy1 += np_accuracy1
            total_accuracy5 += np_accuracy5
            print("Processed %d images. (Top1 accuracy, Top5 accuracy) = (%0.4f, %0.4f)" \
                  % (num_processed_images, total_accuracy1 / num_processed_images,
                     total_accuracy5 / num_processed_images))
