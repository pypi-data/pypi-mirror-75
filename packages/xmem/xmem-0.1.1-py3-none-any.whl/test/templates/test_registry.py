import json
import pickle
import unittest
import winreg
from pathlib import Path

from xmem import MemoryEngine
from xmem.templates import RegistryTemplate

TEST_PATH = 'pickletest'
DUMMY_DATA = {f'test {i}': i for i in range(10)}


class RegistryTemplateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.memory = MemoryEngine(TEST_PATH, RegistryTemplate())

    def tearDown(self) -> None:
        self.memory._data.clear()

    def test_save(self):
        self.memory._data = DUMMY_DATA

        self.memory.save()

        self.assertEqual(self.memory.template.load(), DUMMY_DATA)

    def test_load(self):
        self.memory.load()

        self.assertEqual(self.memory._data, DUMMY_DATA)
