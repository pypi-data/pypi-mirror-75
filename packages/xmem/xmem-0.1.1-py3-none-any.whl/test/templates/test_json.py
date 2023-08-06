import json
import unittest
from pathlib import Path

from xmem import MemoryEngine
from xmem.templates import JsonTemplate

TEST_PATH = 'jsontest'
DUMMY_DATA = {f'test {i}': i for i in range(10)}


class JsonTemplateTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.memory = MemoryEngine(TEST_PATH, JsonTemplate())

    def tearDown(self) -> None:
        self.memory._data.clear()
        self.memory._path.unlink()

    def test_save(self):
        self.memory._data = DUMMY_DATA

        self.memory.save()

        with Path(TEST_PATH).open('r') as f:
            self.assertEqual(json.load(f), DUMMY_DATA)

    def test_load(self):
        with Path(TEST_PATH).open('w') as f:
            json.dump(DUMMY_DATA, f)

        self.memory.load()

        self.assertEqual(self.memory._data, DUMMY_DATA)
