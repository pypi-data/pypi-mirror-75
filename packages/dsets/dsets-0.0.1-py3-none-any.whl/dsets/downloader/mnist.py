import gzip
from urllib import request

import numpy as np

from dsets.dataset import BasicDatasetCollection, BasicDataset, GroupedSample


def download() -> BasicDatasetCollection:
    url_train_images = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'
    url_train_labels = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'
    url_test_images = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'
    url_test_labels = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'

    mnist = BasicDatasetCollection()
    mnist.add('train', download_dataset(url_train_images, url_train_labels))
    mnist.add('test', download_dataset(url_test_images, url_test_labels))

    return mnist


def download_dataset(url_images: str, url_labels: str) -> BasicDataset:
    with request.urlopen(url_images) as req:
        data_image = gzip.decompress(req.read())
    with request.urlopen(url_labels) as req:
        data_labels = gzip.decompress(req.read())

    # data file
    magic_number = int.from_bytes(data_image[0:4], byteorder='big', signed=False)
    if magic_number != 2051:
        raise ValueError('Received unexpected magic number', magic_number)

    num_images = int.from_bytes(data_image[4:8], byteorder='big', signed=False)
    num_rows = int.from_bytes(data_image[8:12], byteorder='big', signed=False)
    num_columns = int.from_bytes(data_image[12:16], byteorder='big', signed=False)

    num_pixels = num_columns * num_rows
    if len(data_image) != 4*4 + num_images * num_pixels:
        raise ValueError('Downloaded data corrupted. Length doesnt match expected value.')

    # label file
    magic_number = int.from_bytes(data_labels[0:4], byteorder='big', signed=False)
    if magic_number != 2049:
        raise ValueError('Received unexpected magic number', magic_number)

    num_labels = int.from_bytes(data_labels[4:8], byteorder='big', signed=False)
    if len(data_labels) != 2*4 + num_labels:
        raise ValueError('Downloaded data corrupted. Length doesnt match expected value.')

    # combine data into samples
    ds = BasicDataset()
    for i in range(num_images):
        image = np.frombuffer(data_image, dtype=np.uint8, count=num_pixels, offset=4*4 + i*num_pixels)
        label = np.frombuffer(data_labels, dtype=np.uint8, count=1, offset=2*4 + i)

        ds.add(GroupedSample(
            image=image,
            label=label
        ))

    return ds
