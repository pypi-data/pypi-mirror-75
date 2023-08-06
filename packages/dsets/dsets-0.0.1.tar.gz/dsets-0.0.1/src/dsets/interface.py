import abc
import json
from uuid import UUID, uuid4
from typing import *

import numpy as np

Json = NewType('Json', str)

SerializedSample = NewType('SerializedSample', Tuple[Json, np.ndarray])
SerializedDataset = NewType('SerializedDataset', Tuple[Json, np.ndarray])
SerializedDatasetCollection = NewType('SerializedDatasetCollection', Tuple[Json, Dict[str, np.ndarray]])


class Sample(metaclass=abc.ABCMeta):
    IMPLEMENTATIONS: Dict[str, Type['Sample']] = dict()

    type = None

    def __init__(self):
        self.uuid = uuid4()

    @abc.abstractmethod
    def serialize(self) -> SerializedSample:
        """
        Return the sample serialized to a numpy array.

        An additional string can be returned to store metadata. However, make sure the metadata is identical for every
        sample in a dataset, otherwise serialization will fail
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_serialized(cls, uuid: UUID, data: SerializedSample) -> 'Sample':
        pass


class Dataset(Sized, metaclass=abc.ABCMeta):
    """Expected to hold a large set of identical-typed samples"""
    IMPLEMENTATIONS: Dict[str, Type['Dataset']] = dict()

    type = None

    @abc.abstractmethod
    def add(self, sample: Sample) -> None:
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Sample]:
        pass

    @classmethod
    def from_serialized(cls, serialized: SerializedDataset) -> 'Dataset':
        metadata, data = serialized

        sample_implementation = Sample.IMPLEMENTATIONS[metadata.pop('sample_type')]

        sample_metadata = metadata['sample_metadata']
        sample_ids = metadata['sample_ids']

        dataset = cls()
        for uuid, sample_data in zip(sample_ids, data):
            dataset.add(sample_implementation.from_serialized(uuid, (sample_metadata, sample_data)))

        return dataset

    def serialize(self) -> SerializedDataset:
        metadata = {
            'sample_metadata': None,
            'sample_type': None,
            'sample_ids': []
        }

        # optimization: pre-allocate the final data array based on a random sample size
        sample = self.take(1)[0]
        metadata['sample_type'] = sample.__class__.type

        if metadata['sample_type'] not in Sample.IMPLEMENTATIONS:
            raise ValueError('sample type could not be serialized')

        sample_metadata, sample_data = sample.serialize()

        metadata['sample_metadata'] = sample_metadata
        data = np.zeros((len(self), sample_data.shape[0]), dtype=sample_data.dtype)

        for i, sample in enumerate(self):
            sample_metadata, sample_data = sample.serialize()

            if sample_metadata != metadata['sample_metadata']:
                raise Exception('could not serialize dataset because sample metadata were not idential')

            data[i] = sample_data
            metadata['sample_ids'].append(str(sample.uuid))

        metadata['sample_metadata'] = json.loads(metadata['sample_metadata'])
        return json.dumps(metadata), data

    def take(self, max_samples: Optional[int] = None) -> List[Sample]:
        result = list()

        for i, sample in enumerate(self):
            if max_samples is not None and i >= max_samples:
                break

            result.append(sample)

        return result


class DatasetCollection(metaclass=abc.ABCMeta):
    """Expected to hold a small set of Datasets"""
    @abc.abstractmethod
    def add(self, name: str, dataset: Dataset) -> None:
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[Tuple[str, Dataset]]:
        pass

    @classmethod
    def from_serialized(cls, serialized_data: SerializedDatasetCollection) -> 'DatasetCollection':
        metadata = json.loads(serialized_data[0])
        data = serialized_data[1]

        dataset_collection = cls()
        for name, serialized_dataset in data.items():
            dataset_metadata = metadata['dataset_metadata'][name]
            dataset_implementation = Dataset.IMPLEMENTATIONS[dataset_metadata.pop('type')]

            dataset = dataset_implementation.from_serialized((dataset_metadata, serialized_dataset))
            dataset_collection.add(name, dataset)

        return dataset_collection

    def serialize(self) -> SerializedDatasetCollection:
        metadata = {
            'dataset_metadata': dict()
        }
        data = dict()

        for name, dataset in self:
            dataset_metadata, dataset_data = dataset.serialize()

            metadata['dataset_metadata'][name] = json.loads(dataset_metadata)
            metadata['dataset_metadata'][name]['type'] = dataset.type
            data[name] = dataset_data

        return json.dumps(metadata), data
