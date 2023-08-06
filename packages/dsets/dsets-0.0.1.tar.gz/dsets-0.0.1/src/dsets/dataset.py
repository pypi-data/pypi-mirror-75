import json
from typing import *
from uuid import UUID

import numpy as np

from dsets.interface import Sample, Dataset, SerializedSample, DatasetCollection


class GroupedSample(Sample):
    type = 'grouped'

    featuregroups: Dict[str, np.ndarray]

    @classmethod
    def from_serialized(cls, uuid: UUID, serialized_data: SerializedSample) -> 'Sample':
        metadata, data = serialized_data

        sample = cls()
        sample.uuid = uuid

        current_start_index = 0
        for group_metadata in metadata:
            end_index = int(group_metadata['end_index'])
            group_name = group_metadata['group']

            sample.featuregroups[group_name] = np.copy(data[current_start_index:end_index])

            current_start_index = end_index

        return sample

    def serialize(self) -> SerializedSample:
        metadata = list()
        result_data = None

        current_end_index = 0
        for name, data in self.featuregroups.items():
            if not len(data.shape) == 1:
                raise Exception('featuregroup data must be a 1-dim array')

            current_end_index += data.shape[0]
            metadata.append({'group': name, 'end_index': current_end_index})
            if result_data is None:
                result_data = data
            else:
                result_data = np.hstack((result_data, data))


        return json.dumps(metadata), result_data

    def __init__(self, **kwargs):
        super().__init__()

        self.featuregroups = kwargs

    def __getattr__(self, item):
        if item in self.featuregroups:
            return self.featuregroups[item]

        raise AttributeError


class BasicDataset(Dataset):
    type = 'basic'

    def add(self, sample: Sample) -> None:
        self.samples.append(sample)

    def __len__(self) -> int:
        return len(self.samples)

    def __iter__(self) -> Iterator[Sample]:
        return iter(self.samples)

    def __init__(self):
        self.samples = []


class BasicDatasetCollection(DatasetCollection):
    def __iter__(self) -> Iterator[Tuple[str, Dataset]]:
        return iter(self.collection.items())

    def __init__(self):
        self.collection: Dict[str, Dataset] = dict()

    def add(self, name: str, dataset: Dataset):
        self.collection[name] = dataset

    def __getattr__(self, item):
        if item in self.collection:
            return self.collection[item]

        raise AttributeError


Sample.IMPLEMENTATIONS[GroupedSample.type] = GroupedSample
Dataset.IMPLEMENTATIONS[BasicDataset.type] = BasicDataset
