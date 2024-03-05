# LibAlexandria: LibAlexandria Item
# A standardized LibAlexandria item that can be used in other Python scripts.

# Imports
import os
import json
from typing import Optional, Any
from warnings import warn

import libAlexDefaults as laShared
from libAlexRelatedFile import LibAlexRelatedFile
from libAlexSemanticVersion import SemanticVersion

# TODO: Add tests.

# Classes
class LibAlexItem:
    """
    A LibAlexandria Item representing the information for the provided directory's meta file and content.
    """
    # Constructors
    def __init__(self,
        version: Optional[SemanticVersion] = None,
        title: str = laShared.DEF_TITLE,
        author: str = laShared.DEF_AUTHOR,
        date: str = laShared.DEF_DATE,
        description: str = laShared.DEF_DESC,
        directory: Optional[str] = laShared.DEF_ITEM_DIR,
        sourceFile: Optional[str] = laShared.DEF_SRC_FILE,
        relatedFiles: Optional[list[LibAlexRelatedFile]] = laShared.DEF_REL_FILES,
        metaFilepath: Optional[str] = laShared.DEF_ITEM_META_PATH,
        classification: Optional[str] = laShared.DEF_CLASSIFICATION,
        flags: Optional[list[str]] = laShared.DEF_FLAGS,
        resolvedFlags: Optional[list[str]] = laShared.DEF_ITEM_RES_FLAGS
    ):
        """
        Creates a new LibAlexandria Item.

        version: The version of the item.
        title: The title of the item.
        author: The author of the item.
        date: The date the item was originally written.
        description: A description of the item.
        directory: An absolute path to the directory where the item is located or `None`.
        sourceFile: An absolute path to the primary source file of the item or `None`.
        relatedFiles: A list of `LibAlexRelatedFile` objects or `None`.
        metaFilepath: An absolute path to the meta file of the item or `None`.
        classification: The Library of Congress classification of the item's content or `None`.
        flags: A list of flags for the item or `None`.
        resolvedFlags: A list of any additional resolved flags for the item or `None`.
        """
        self.version = version
        self.title = title
        self.author = author
        self.date = date # TODO: Parse dates in `YYYY-MM-DD`, `YYYY/MM/DD`, `MM-DD-YYYY`, and `MM/DD/YYYY` formats
        self.description = description
        self.directory = directory
        self.sourceFile = sourceFile
        self.relatedFiles = relatedFiles
        self.metaFilepath = metaFilepath
        self.classification = classification
        self.flags = flags
        self.resolvedFlags = resolvedFlags

    @classmethod
    def fromMetaFile(cls, metaPath: str) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided `meta.json` format file.
        If the operation fails, a `FileNotFoundError`, `json.JSONDecodeError`, or `ValueError` may be raised.

        metaPath: The path to the `meta.json` format file.
        """
        # Manage paths
        metaPath = laShared.fullpath(metaPath)
        dirPath = os.path.dirname(metaPath)

        # Verify the paths exist
        if not os.path.isdir(dirPath):
            # Fail
            raise FileNotFoundError(f"No directory present to load from at: {dirPath}")

        if not os.path.isfile(metaPath):
            # Check if the user doesn't read documentation
            if os.path.isfile(os.path.join(metaPath, "meta.json")):
                # Correct the meta path
                metaPath = os.path.join(metaPath, "meta.json")
                dirPath = os.path.dirname(metaPath)
            else:
                # Fail
                raise FileNotFoundError(f"No meta file was present at: {metaPath}")

        # Resolve additional flags from the directory structure
        resolvedFlags = [laShared.slugify(t) for t in (dirPath.split(os.sep)[1:])]

        # Read the meta file
        try:
            with open(metaPath, "r") as metaFile:
                # Load the meta json data
                metaJson: dict[str, Any] = json.load(metaFile)
        except json.JSONDecodeError as e:
            # Fail
            raise ValueError(f"Could not parse JSON from the provided meta file: {metaPath}\n\nCause: {e}")

        # Load from the JSON
        return cls.fromJson(
            metaJson,
            directory=dirPath,
            metaFilepath=metaPath,
            resolvedFlags=resolvedFlags
        )

    @classmethod
    def fromJson(cls,
        jsonData: dict[str, Any],
        directory: Optional[str] = laShared.DEF_ITEM_DIR,
        metaFilepath: Optional[str] = laShared.DEF_ITEM_META_PATH,
        resolvedFlags: Optional[list[str]] = laShared.DEF_ITEM_RES_FLAGS
    ) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided JSON data.
        If the operation fails, a `ValueError` or `FileNotFoundError` may be raised.

        jsonData: The JSON data to load.
        directory: An absolute path to the directory where the item is located.
        metaFilepath: An absolute path to the meta file of the item.
        resolvedFlags: Any additional resolved flags to add to the item.

        Returns a new LibAlexandria Item.
        """
        # Get the version or fail
        dataVersion = cls.versionFromJson(jsonData)

        # Pack the args
        packedArgs = {
            "jsonData": jsonData,
            "directory": directory,
            "metaFilepath": metaFilepath,
            "resolvedFlags": resolvedFlags
        }

        # Check the version
        if dataVersion.major == 2:
            return cls._fromV2Json(**packedArgs)
        elif dataVersion.major == 1:
            return cls._fromV1Json(**packedArgs)
        else:
            # Fail
            raise ValueError(f"\"{dataVersion.string}\" is not a supported version of LibAlexandria Metadata file.")

    @classmethod
    def versionFromJson(cls, jsonData: dict[str, Any]) -> SemanticVersion:
        """
        Extracts the version of the provided JSON data.
        If a version is not found, a `ValueError` may be raised.

        jsonData: The JSON data to extract the version from.

        Returns a SemanticVersion object.
        """
        # Extract the version code
        dataVersion = jsonData.get("_infover", None)

        # Check for validity
        if dataVersion != None:
            return SemanticVersion(dataVersion)
        else:
            # Fail
            raise ValueError(f"Provided LibAlexandria Metadata file does not provide a version using the `_infover` key.")

    @classmethod
    def _fromV1Json(cls,
        jsonData: dict[str, Any],
        directory: Optional[str] = laShared.DEF_ITEM_DIR,
        metaFilepath: Optional[str] = laShared.DEF_ITEM_META_PATH,
        resolvedFlags: Optional[list[str]] = laShared.DEF_ITEM_RES_FLAGS
    ) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided `v1.*` JSON data.
        If the operation fails, a `ValueError` may be raised.

        jsonData: The JSON data to load.
        directory: An absolute path to the directory where the item is located.
        metaFilepath: An absolute path to the meta file of the item.
        resolvedFlags: Any additional resolved flags to add to the item.

        Returns a new LibAlexandria Item.
        """
        # Tell them off
        # TODO: Make a script for converting v1.* to v2.*?
        warn("DEPRECATED: Version `1.*` Meta files should be converted to Version `2.*` for increased compatibility and functionality!")

        # Mock v2 style data
        return cls._fromV2Json(
            {
                "_infover": laShared.VER_LIBALEX,
                "title": jsonData.get("title", laShared.DEF_TITLE),
                "author": jsonData.get("author", laShared.DEF_AUTHOR),
                "date": jsonData.get("date", laShared.DEF_DATE),
                "sourceFile": jsonData.get("content", laShared.DEF_SRC_FILE),
                "flags": jsonData.get("flags", laShared.DEF_FLAGS),
                "description": jsonData.get("description", laShared.DEF_DESC)
            },
            directory=directory,
            metaFilepath=metaFilepath,
            resolvedFlags=resolvedFlags
        )

    @classmethod
    def _fromV2Json(cls,
        jsonData: dict[str, Any],
        directory: Optional[str] = laShared.DEF_ITEM_DIR,
        metaFilepath: Optional[str] = laShared.DEF_ITEM_META_PATH,
        resolvedFlags: Optional[list[str]] = laShared.DEF_ITEM_RES_FLAGS
    ) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided `v2.*` JSON data.
        If the operation fails, a `ValueError` or `FileNotFoundError` may be raised.

        jsonData: The JSON data to load.
        directory: An absolute path to the directory where the item is located.
        metaFilepath: An absolute path to the meta file of the item.
        resolvedFlags: Any additional resolved flags to add to the item.

        Returns a new LibAlexandria Item.
        """
        # Resolve the source file
        sourceFile = jsonData.get("sourceFile", laShared.DEF_SRC_FILE)
        if (sourceFile != laShared.DEF_SRC_FILE) and isinstance(sourceFile, str):
            # Build the full path
            sourceFile = os.path.join(directory, sourceFile)

            # Check if the source file exists
            if not os.path.isfile(sourceFile):
                # Fail
                raise FileNotFoundError(f"Provided source filepath could not be resolved: {sourceFile}")

        # Resolve related files
        relatedFilesData = jsonData.get("otherFiles", laShared.DEF_REL_FILES)
        if (relatedFilesData != laShared.DEF_REL_FILES) and isinstance(relatedFilesData, list):
            # Populate the related files list
            relatedFiles = []
            rfData: dict[str, Any]
            for rfData in relatedFilesData:
                # Resolve the full filepath
                relatedFilePath = rfData.get("path", laShared.DEF_REL_FILE_PATH)
                if relatedFilePath != laShared.DEF_REL_FILE_PATH:
                    relatedFilePath = os.path.join(directory, relatedFilePath)

                # Record the related file
                try:
                    relatedFile = LibAlexRelatedFile(
                        rfData.get("label", laShared.DEF_REL_FILE_LABEL),
                        relatedFilePath,
                        rfData.get("description", laShared.DEF_REL_FILE_DESC),
                        rfData.get("id", laShared.DEF_REL_FILE_ID)
                    )
                    relatedFiles.append(relatedFile)
                except FileNotFoundError as e:
                    raise FileNotFoundError(f"Failed to load a Related File because:\n{e}")
        else:
            # No data
            relatedFiles = relatedFilesData

        # Build the object
        return cls(
            version=cls.versionFromJson(jsonData),
            title=jsonData.get("title", laShared.DEF_TITLE),
            author=jsonData.get("author", laShared.DEF_AUTHOR),
            date=jsonData.get("date", laShared.DEF_DATE),
            description=jsonData.get("description", laShared.DEF_DESC),
            directory=directory,
            sourceFile=sourceFile,
            relatedFiles=relatedFiles,
            metaFilepath=metaFilepath,
            classification=jsonData.get("classification", laShared.DEF_CLASSIFICATION),
            flags=jsonData.get("flags", laShared.DEF_FLAGS),
            resolvedFlags=resolvedFlags
        )

    # Python Functions
    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.date})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    # Functions
    def getAllFlags(self) -> list:
        """
        Returns all flags including the specified flags, classification, and resolved flags.
        """
        # Create a copy of all present flags
        allFlags: list[str] = []

        if isinstance(self.flags, list):
            allFlags.extend(self.flags)

        if isinstance(self.resolvedFlags, list):
            allFlags.extend(self.resolvedFlags)

        if isinstance(self.classification, str):
            allFlags.append(self.classification)

        return sorted(tuple(set(allFlags)))

    def toJson(self) -> dict[str, Any]:
        """
        Returns the JSON representation of the item.
        """
        # Build the JSON
        jsonData = {
            "_infover": (self.version.string if isinstance(self.version, SemanticVersion) else laShared.VER_LIBALEX),
        }

        if isinstance(self.classification, str):
            jsonData["classification"] = self.classification

        jsonData["title"] = self.title
        jsonData["author"] = self.author
        jsonData["date"] = self.date

        if isinstance(self.sourceFile, str):
            jsonData["sourceFile"] = self.sourceFile

        if isinstance(self.relatedFiles, list):
            jsonData["otherFiles"] = [rf.toJson() for rf in self.relatedFiles]

        if isinstance(self.flags, list):
            jsonData["flags"] = self.flags

        jsonData["description"] = self.description

        return jsonData

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
