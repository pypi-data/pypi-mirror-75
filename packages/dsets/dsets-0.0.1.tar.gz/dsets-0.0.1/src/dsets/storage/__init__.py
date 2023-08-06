from abc import ABC, abstractmethod
from typing import Optional

from dsets.dataset import DatasetCollection
from dsets.downloader import KNOWN_DATASETS


class DatasetCollectionStorage(ABC):
    def get(self, name) -> DatasetCollection:
        ds = self._load(name)
        if ds is not None:
            return ds

        if name in KNOWN_DATASETS:
            return self._download(name)

        raise ValueError(f'Couldnt retrieve unknown dataset "{name}"')

    @abstractmethod
    def _load(self, name) -> Optional[DatasetCollection]:
        """Returns None if dataset couldn't be found in storage"""
        pass

    @abstractmethod
    def add(self, name, ds: DatasetCollection) -> None:
        pass

    def _download(self, name) -> DatasetCollection:
        downloader = KNOWN_DATASETS.get(name)
        if name is None:
            raise ValueError(f'Cannot download unknown dataset "{name}"."')

        dataset = downloader()
        self.add(name, dataset)

        return dataset
