# LibAlexandria: Senamtic Versioning Tests
# Tests for the `SemanticVersion` class.

# Imports
import unittest

from libAlexSemanticVersion import SemanticVersion

# Classes
class TestSemanticVersion(unittest.TestCase):
    def test_init1(self):
        v = SemanticVersion("v1.0.3")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 3)
        self.assertEqual(v.preRelease, "")
        self.assertEqual(v.metaData, "")
        self.assertTrue(v.isValid)

    def test_init2(self):
        v = SemanticVersion("2.1.5-rc.1+build.123")
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.patch, 5)
        self.assertEqual(v.preRelease, "rc.1")
        self.assertEqual(v.metaData, "build.123")
        self.assertTrue(v.isValid)

    def test_init3(self):
        v = SemanticVersion("2.1.5-rc.1")
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 1)
        self.assertEqual(v.patch, 5)
        self.assertEqual(v.preRelease, "rc.1")
        self.assertEqual(v.metaData, "")
        self.assertTrue(v.isValid)

    def test_init4(self):
        v = SemanticVersion("2.10.5")
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 10)
        self.assertEqual(v.patch, 5)
        self.assertEqual(v.preRelease, "")
        self.assertEqual(v.metaData, "")
        self.assertTrue(v.isValid)

    def test_init5(self):
        v = SemanticVersion("a.1.5")
        self.assertFalse(v.isValid)

    def test_init6(self):
        v = SemanticVersion("10.6.5+build.123")
        self.assertEqual(v.major, 10)
        self.assertEqual(v.minor, 6)
        self.assertEqual(v.patch, 5)
        self.assertEqual(v.preRelease, "")
        self.assertEqual(v.metaData, "build.123")
        self.assertTrue(v.isValid)

    def test_init6(self):
        v = SemanticVersion("invalid.version")
        self.assertFalse(v.isValid)

    def test_str(self):
        v = SemanticVersion("1.2.3")
        self.assertTrue(isinstance(str(v), str))

    def test_repr(self):
        v = SemanticVersion("1.2.3")
        self.assertTrue(isinstance(repr(v), str))

    def test_eq(self):
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.3")
        self.assertTrue(v1 == v2)

    def test_ne(self):
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.4")
        self.assertTrue(v1 != v2)

    def test_lt(self):
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.4")
        self.assertTrue(v1 < v2)

    def test_le(self):
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.4")
        self.assertTrue(v1 <= v2)

    def test_gt(self):
        v1 = SemanticVersion("1.2.4")
        v2 = SemanticVersion("1.2.3")
        self.assertTrue(v1 > v2)

    def test_ge(self):
        v1 = SemanticVersion("1.2.4")
        v2 = SemanticVersion("1.2.3")
        self.assertTrue(v1 >= v2)

if __name__ == "__main__":
    unittest.main()
