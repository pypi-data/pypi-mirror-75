from pathlib import Path


class MemoryTemplate:
    _path: Path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        # making sure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        self._path = path

    def save(self, data: dict):
        """
        write the given dictionary to :path:

        :param data: item to save
        """
        raise NotImplementedError

    def load(self) -> dict:
        """
        :return: content read from disk
        """
        raise NotImplementedError
