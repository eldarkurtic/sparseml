# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest
import tensorflow
from packaging import version

from sparseml.tensorflow_v1.datasets import (
    DatasetRegistry,
    ImageFolderDataset,
    ImagenetteDataset,
    ImagewoofDataset,
    create_split_iterators_handle,
)
from sparseml.tensorflow_v1.utils import tf_compat


def _validate(dataset: ImageFolderDataset, size: int):
    with tf_compat.Graph().as_default():
        batch_size = 16

        with tf_compat.device("/cpu:0"):
            print("loading datasets")
            dataset_len = len(dataset)
            assert dataset_len > 0
            tf_dataset = dataset.build(
                batch_size,
                repeat_count=2,
                shuffle_buffer_size=10,
                prefetch_buffer_size=batch_size,
                num_parallel_calls=4,
            )

        handle, iterator, (tf_iter,) = create_split_iterators_handle([tf_dataset])
        images, labels = iterator.get_next()

        with tf_compat.Session() as sess:
            sess.run(
                [
                    tf_compat.global_variables_initializer(),
                    tf_compat.local_variables_initializer(),
                ]
            )
            iter_handle = sess.run(tf_iter.string_handle())
            sess.run(tf_iter.initializer)

            for _ in range(5):
                batch_x, batch_lab = sess.run(
                    [images, labels], feed_dict={handle: iter_handle}
                )
                assert batch_x.shape[0] == 16
                assert batch_x.shape[1] == size
                assert batch_x.shape[2] == size
                assert batch_x.shape[3] == 3
                assert batch_lab.shape[0] == 16
                assert batch_lab.shape[1] == 10


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False),
    reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    version.parse(tensorflow.__version__) < version.parse("1.3"),
    reason="Must install tensorflow_v1 version 1.3 or greater",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_DATASET_TESTS", False),
    reason="Skipping dataset tests",
)
def test_imagenette_160():
    train_dataset = ImagenetteDataset(train=True)
    _validate(train_dataset, 160)

    val_dataset = ImagenetteDataset(train=False)
    _validate(val_dataset, 160)

    reg_dataset = DatasetRegistry.create("imagenette", train=False)
    _validate(reg_dataset, 160)


@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_TENSORFLOW_TESTS", False),
    reason="Skipping tensorflow_v1 tests",
)
@pytest.mark.skipif(
    version.parse(tensorflow.__version__) < version.parse("1.3"),
    reason="Must install tensorflow_v1 version 1.3 or greater",
)
@pytest.mark.skipif(
    os.getenv("NM_ML_SKIP_DATASET_TESTS", False),
    reason="Skipping dataset tests",
)
def test_imagewoof_160():
    train_dataset = ImagewoofDataset(train=True)
    _validate(train_dataset, 160)

    val_dataset = ImagewoofDataset(train=False)
    _validate(val_dataset, 160)

    reg_dataset = DatasetRegistry.create("imagewoof", train=False)
    _validate(reg_dataset, 160)
