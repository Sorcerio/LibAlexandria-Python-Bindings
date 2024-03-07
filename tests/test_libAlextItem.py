# LibAlexandria: LibAlexandria Item Object Tests
# Tests for the LibAlexandria Item Object.

# Imports
import os
import json
import unittest
from typing import Optional

from libAlexItem import LibAlexItem
from libAlexSemanticVersion import SemanticVersion
from libAlexRelatedFile import LibAlexRelatedFile

# Classes
class TestLibAlexItem(unittest.TestCase):
    # Tests
    def setUp(self):
        assetDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets"))

        self.metaPathV1 = os.path.join(assetDir, "metaV1.json")
        self.metaPathV2 = os.path.join(assetDir, "metaV2.json")

        self.version = SemanticVersion("1.0.0")
        self.title = "Lorem Ipsum"
        self.author = "John Doe"
        self.date = "1984-04-01"
        self.description = "A test LibAlexandria Item."
        self.directory = assetDir
        self.sourceFile = os.path.join(assetDir, "sourceFile.txt")
        self.classification = "AS"

        self.rf1 = LibAlexRelatedFile(
            label="A Limerick",
            path=os.path.join(assetDir, "relatedFile.txt"),
            description="A Limerick for testing purposes."
        )
        self.rf2 = LibAlexRelatedFile(
            label="A Haiku",
            path=os.path.join(assetDir, "relatedFile2.txt"),
            description="A Haiku for testing purposes.",
            id="haiku"
        )
        self.relatedFiles = [
            self.rf1,
            self.rf2
        ]

        self.flags = [
            "text",
            "prose",
            "example",
            "libalexandria",
            "test"
        ]

        self.resolvedFlags = [
            "test",
            "cat",
            "dog",
            "robot"
        ]

        self.flagDupeCount = 1 # Number of flags in `resolvedFlags` that are also in `flags`

        self.item = LibAlexItem(
            version=self.version,
            title=self.title,
            author=self.author,
            date=self.date,
            description=self.description,
            directory=self.directory,
            sourceFile=self.sourceFile,
            relatedFiles=self.relatedFiles,
            metaFilepath=self.metaPathV2,
            classification=self.classification,
            flags=self.flags,
            resolvedFlags=self.resolvedFlags
        )

    def test_init(self):
        self.assertEqual(self.item.version, self.version)
        self.assertEqual(self.item.title, self.title)
        self.assertEqual(self.item.author, self.author)
        self.assertEqual(self.item.date, self.date)
        self.assertEqual(self.item.description, self.description)
        self.assertEqual(self.item.directory, self.directory)
        self.assertEqual(self.item.sourceFile, self.sourceFile)
        self.assertEqual(self.item.metaFilepath, self.metaPathV2)
        self.assertEqual(self.item.classification, self.classification)
        self.assertEqual(self.item.flags, self.flags)
        self.assertEqual(self.item.resolvedFlags, self.resolvedFlags)

        for rf in self.item.relatedFiles:
            self.assertTrue(rf in self.relatedFiles)

    def test_fromMetaFile_v1(self): # This also tests the `fromJson` funcs
        with self.assertWarns(UserWarning):
            item = LibAlexItem.fromMetaFile(self.metaPathV1)

        self.assertEqual(item.version.major, SemanticVersion("1.0.0+mockedv2").major)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.author, self.author)
        self.assertEqual(item.date, self.date)
        self.assertEqual(item.description, self.description)
        self.assertEqual(item.directory, self.directory)
        self.assertEqual(item.sourceFile, self.sourceFile)
        self.assertEqual(item.metaFilepath, self.metaPathV1)
        self.assertEqual(item.flags, self.flags)
        self.assertEqual(item.classification, self.classification)

        self.assertIsNotNone(item.resolvedFlags) # These will change per user
        self.assertIsNone(item.relatedFiles)

    def test_fromMetaFile_v2(self): # This also tests the `fromJson` funcs
        item = LibAlexItem.fromMetaFile(self.metaPathV2)

        self.assertEqual(item.version.major, SemanticVersion("2.0.0").major)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.author, self.author)
        self.assertEqual(item.date, self.date)
        self.assertEqual(item.description, self.description)
        self.assertEqual(item.directory, self.directory)
        self.assertEqual(item.sourceFile, self.sourceFile)
        self.assertEqual(item.metaFilepath, self.metaPathV2)
        self.assertEqual(item.classification, self.classification)
        self.assertEqual(item.flags, self.flags)

        self.assertIsNotNone(item.resolvedFlags) # These will change per user

        for rf in self.item.relatedFiles:
            self.assertTrue(rf in self.relatedFiles)

    def test_versionFromJson_success(self):
        with open(self.metaPathV2, "r") as file:
            data = json.load(file)

        version = LibAlexItem.versionFromJson(data)
        self.assertEqual(version.major, 2)

    def test_versionFromJson_fail(self):
        with self.assertRaises(ValueError):
            k = LibAlexItem.versionFromJson({"should": "fail"})

    def test_str(self):
        self.assertTrue(isinstance(str(self.item), str))

    def test_repr(self):
        self.assertTrue(isinstance(repr(self.item), str))

    def test_getAllFlags(self):
        allFlags = self.item.getAllFlags()

        self.assertEqual(
            len(allFlags),
            (len(self.item.flags) + len(self.item.resolvedFlags) - self.flagDupeCount + 1) # +1 for classification!
        )

    def test_toJson_v1(self):
        item = LibAlexItem.fromMetaFile(self.metaPathV1)

        with open(self.metaPathV2, "r") as file:
            expectedJson = json.load(file)

        expectedJson["otherFiles"] = []

        self.assertEqual(item.toJson(), expectedJson)

    def test_toJson_v2(self):
        with open(self.metaPathV2, "r") as file:
            expectedJson = json.load(file)

        self.assertEqual(self.item.toJson(), expectedJson)

if __name__ == "__main__":
    unittest.main()
