# LibAlexandria: Senamtic Versioning Tests
# Tests for the `SemanticVersion` class.

# Imports
import unittest
import os
import tempfile

from libAlexDefaults import fullpath, checkPath, slugify

# Classes
class TestFullPath(unittest.TestCase):
    def test_fullpath(self):
        # This is a shit test, but it works
        relPath = "relative/path/to/file"
        absPath = os.path.abspath(os.path.expanduser(relPath))
        self.assertEqual(fullpath(relPath), absPath)

class TestCheckPath(unittest.TestCase):
    def setUp(self):
        self.existingPath = tempfile.gettempdir()
        self.nonexistingPath = os.path.join(tempfile.gettempdir(), "non_existing_path")
        self.path_to_create = os.path.join(tempfile.gettempdir(), "path_to_create")

    def tearDown(self):
        if os.path.exists(self.path_to_create):
            os.rmdir(self.path_to_create)

    def test_existingPath(self):
        self.assertTrue(checkPath(self.existingPath))

    def test_nonexistingPath(self):
        self.assertFalse(checkPath(self.nonexistingPath))

    def test_createPath(self):
        self.assertFalse(os.path.exists(self.path_to_create))
        self.assertTrue(checkPath(self.path_to_create, createPath=True))
        self.assertTrue(os.path.exists(self.path_to_create))

class TestSlugify(unittest.TestCase):
    def test_slugify(self):
        string = "Hëllö 🌍! Ç'est ün ẞtrïng. bruh 🐱‍👤🐱‍🚀🐱‍💻🐱‍🐉🐱‍👓🐱‍🐾 meow"
        slug = "hello-cest-un-tring-bruh-meow"
        self.assertEqual(slugify(string), slug)

if __name__ == '__main__':
    unittest.main()
