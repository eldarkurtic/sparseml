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

"""
Imagenette and Imagewoof dataset implementations for the image classification field in
computer vision.
More info for the dataset can be found `here <https://github.com/fastai/imagenette>`__.
"""

from typing import Union

from sparseml.keras.datasets.classification.imagefolder import ImageFolderDataset
from sparseml.keras.datasets.registry import DatasetRegistry
from sparseml.utils.datasets import (
    IMAGENET_RGB_MEANS,
    IMAGENET_RGB_STDS,
    ImagenetteDownloader,
    ImagenetteSize,
    default_dataset_path,
)


__all__ = ["ImagenetteDataset"]


@DatasetRegistry.register(
    key=["imagenette"],
    attributes={
        "num_classes": 10,
        "transform_means": IMAGENET_RGB_MEANS,
        "transform_stds": IMAGENET_RGB_STDS,
    },
)
class ImagenetteDataset(ImageFolderDataset, ImagenetteDownloader):
    """
    Wrapper for the imagenette (10 class) dataset that fastai created.
    Handles downloading and applying standard transforms.
    :param root: The root folder to find the dataset at,
        if not found will download here if download=True
    :param train: True if this is for the training distribution,
        False for the validation
    :param dataset_size: The size of the dataset to use and download:
        See ImagenetteSize for options
    :param image_size: The image size to output from the dataset
    :param download: True to download the dataset, False otherwise
    """

    def __init__(
        self,
        root: str = default_dataset_path("imagenette"),
        train: bool = True,
        dataset_size: ImagenetteSize = ImagenetteSize.s320,
        image_size: Union[int, None] = None,
        download: bool = True,
    ):
        ImagenetteDownloader.__init__(self, root, dataset_size, download)
        self._train = train

        if image_size is None:
            if dataset_size == ImagenetteSize.s160:
                image_size = 160
            elif dataset_size == ImagenetteSize.s320:
                image_size = 320
            else:
                image_size = 224

        super().__init__(self.extracted_root, train, image_size)
