import tempfile
from pathlib import Path
from typing import *

import numpy as np

from dsets.dataset import BasicDatasetCollection
from dsets.interface import DatasetCollection
from dsets.storage import DatasetCollectionStorage


class LocalStorage(DatasetCollectionStorage):
    def __init__(self, location: Optional[str] = None):
        if location is None:
            location = Path(tempfile.gettempdir()) / 'dsets_localstore'
            if not location.exists():
                location.mkdir()
        else:
            location = Path(location)
            if not location.is_dir():
                raise ValueError(f'The provided location {location} is not a valid directory')

        print(f'using local storage at {location}')
        self.location = location

    def add(self, name, collection: DatasetCollection) -> None:
        location = self._get_location(name)
        if not location.exists():
            location.mkdir()

        metadata, data = collection.serialize()

        location_metadata = location / 'metadata.json'
        location_metadata.write_text(metadata, encoding='ascii')

        location_data = location / 'data.npz'
        np.savez_compressed(str(location_data), **data)

    def _load(self, name) -> Optional[BasicDatasetCollection]:
        location = self._get_location(name)
        if not location.exists():
            return None

        location_metadata = location / f'metadata.json'
        location_data = location / f'data.npz'

        metadata = location_metadata.read_text(encoding='ascii')
        data = np.load(str(location_data), allow_pickle=False)

        return BasicDatasetCollection.from_serialized((metadata, data))

    def _get_location(self, name) -> Path:
        return self.location / name
