import atexit
from pathlib import Path
from typing import Dict, Union

from .template import MemoryTemplate
from .exceptions import NotFoundError

class MemoryEngine(object):
    _data: Dict
    _path: Path
    _template: MemoryTemplate

    def __init__(self, path: Union[Path, str], template: MemoryTemplate, auto_load=True):
        """
        :param path: path to save file
        :param template: memory template
        """

        self._data = {}
        self._template = template

        # update path
        self.path = path

        # exposing dictionary methods
        self.clear = self._data.clear
        self.items = self._data.items

        # read the initial data
        if auto_load:
            self.load()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: Union[Path, str]):
        # conversion
        if type(value) != Path:
            self._path = Path(value)
        else:
            self._path = value

        # updating template path attribute
        self._template.path = self._path

    @property
    def template(self):
        return self._template

    def save(self):
        """
        write current data to disk
        """
        self._template.save(self._data)

    def load(self):
        """
        read data from disk
        """
        try:
            self._data = self._template.load()
        except NotFoundError:
            self.save()

    def get(self, key, default=None):
        """
        :param key: key used as identifier
        :param default: value to return is key not found

        :return: data corresponding to identifer(key)
        :returns: default if key not found
        """
        try:
            value = self._data[key]
        except KeyError:
            value = default

        return value

    def delete(self, *args):
        """
        removes the keys from memory

        :param args: keys to be removed
        """
        for key in args:
            try:
                del self._data[key]
            except KeyError:
                pass

    def put(self, key, value):
        """
        adds key-value pair to memory

        :param key: key used as identifier
        :param value: data to store
        :return: self, may be chained
        """
        self._data[key] = value

        return self

    def putall(self, d: dict):
        """
        adds all the key-value pairs in the map

        :param d: dictionary map to be stored
        """
        for key, value in d.items():
            self._data[key] = value

    def save_atexit(self, should_save=True):
        """
        register save function to atexit module

        :param should_save: whether to register or unregister
        """
        if should_save:
            atexit.register(self.save)
        else:
            atexit.unregister(self.save)
