# LibAlexandria: LibAlexandria Related File Object Tests
# Tests for the LibAlexandria Related File Object.

# Imports
import os
import unittest

from libAlexRelatedFile import LibAlexRelatedFile

# Classes
class TestLibAlexRelatedFile(unittest.TestCase):
    def setUp(self):
        self.label = "Test File"
        self.path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets", "relatedFile.txt"))
        self.desc = "This is a test file"
        self.ident = "test1"
        self.file = LibAlexRelatedFile(self.label, self.path, self.desc, self.ident)

    def test_init(self):
        self.assertEqual(self.file.label, self.label)
        self.assertEqual(self.file.path, self.path)
        self.assertEqual(self.file.description, self.desc)
        self.assertEqual(self.file.id, self.ident)

    def test_str(self):
        self.assertTrue(isinstance(str(self.file), str))

    def test_repr(self):
        self.assertTrue(isinstance(repr(self.file), str))

    def test_toJson(self):
        expectedJson = {
            "label": self.label,
            "path": self.path,
            "description": self.desc,
            "id": self.ident
        }
        self.assertEqual(self.file.toJson(), expectedJson)

    def test_failedInit(self):
        with self.assertRaises(FileNotFoundError):
            LibAlexRelatedFile(self.label, "bad/path/to/file.txt", self.desc)

if __name__ == '__main__':
    unittest.main()
