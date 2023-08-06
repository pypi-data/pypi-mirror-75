import unittest
from pathlib import Path

from xmem import MemoryEngine, MemoryTemplate


class MemoryEngineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # template left as EmptyTemplate, as data wont be written to disk
        # auto_load disabled since template left empty
        self.memory = MemoryEngine('testdata', MemoryTemplate(), auto_load=False)

    def tearDown(self) -> None:
        self.memory._data.clear()

    def test_string_location_to_path(self):
        LOCATION = 'memorychanged'
        PATH = Path(LOCATION)

        self.memory.path = LOCATION

        self.assertEqual(self.memory._path, PATH)
        self.assertEqual(self.memory._template.path, PATH)

    def test_put(self):
        KEY = 'put'
        VALUE = 'PVALUE'

        self.memory.put(KEY, VALUE)

        self.assertEqual(self.memory._data[KEY], VALUE)

    def test_putall(self):
        DATA = {str(i): i for i in range(5)}

        self.memory.putall(DATA)

        for key, value in DATA.items():
            self.assertEqual(self.memory._data[key], value)

    def test_get(self):
        KEY = 'get'
        VALUE = 'GVALUE'

        self.memory._data[KEY] = VALUE

        self.assertEqual(self.memory.get(KEY), VALUE)

    def test_delete(self):
        KEY = 'delete'
        VALUE = 'DVALUE'

        self.memory._data[KEY] = VALUE

        self.memory.delete(KEY)

        with self.assertRaises(KeyError):
            _ = self.memory._data[KEY]