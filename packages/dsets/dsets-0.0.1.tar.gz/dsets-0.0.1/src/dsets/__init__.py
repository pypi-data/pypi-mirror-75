from dsets.storage.local import LocalStorage


def connect_local() -> LocalStorage:
    return LocalStorage()
