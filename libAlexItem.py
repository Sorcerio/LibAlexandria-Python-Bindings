# LibAlexandria: LibAlexandria Item
# A standardized LibAlexandria item that can be used in other Python scripts.

# Imports
import os
import json
from typing import Optional, Any

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
        title: str = laShared.DEFAULT_TITLE,
        author: str = laShared.DEFAULT_AUTHOR,
        date: str = laShared.DEFAULT_DATE,
        description: str = laShared.DEFAULT_DESCRIPTION,
        directory: Optional[str] = laShared.DEFAULT_ITEM_DIRECTORY,
        sourceFile: Optional[str] = laShared.DEFAULT_SOURCEFILE,
        otherFiles: Optional[list[LibAlexRelatedFile]] = laShared.DEFAULT_OTHERFILES,
        metaFilepath: Optional[str] = laShared.DEFAULT_ITEM_METAFILEPATH,
        classification: Optional[str] = laShared.DEFAULT_CLASSIFICATION,
        flags: Optional[list[str]] = laShared.DEFAULT_FLAGS,
        resolvedFlags: Optional[list[str]] = laShared.DEFAULT_ITEM_RESOLVEDFLAGS
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
        otherFiles: A list of `LibAlexRelatedFile` objects or `None`.
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
        self.otherFiles = otherFiles
        self.metaFilepath = metaFilepath
        self.classification = classification
        self.flags = flags
        self.resolvedFlags = resolvedFlags

    @classmethod
    def fromMetaFile(cls, metaPath: str) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided `meta.json` format file.

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
        return cls.fromJson(metaJson, resolvedFlags=resolvedFlags)

    @classmethod
    def fromJson(cls,
        jsonData: dict[str, Any],
        resolvedFlags: Optional[list[str]] = laShared.DEFAULT_ITEM_RESOLVEDFLAGS
    ) -> 'LibAlexItem':
        """
        Loads a LibAlexandria Item from the provided JSON data.

        jsonData: The JSON data to load.
        resolvedFlags: Any additional resolved flags to add to the item.

        Returns a new LibAlexandria Item.
        """
        print(jsonData)
        print(resolvedFlags)
        exit()

    # Python Functions
    def __str__(self) -> str:
        if self.isLoaded:
            return f"{self.title} by {self.author} ({self.date})"
        else:
            return "Invalid LibAlexandria Item"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    # Loader Functions
    def loadMeta(self, dirpath: str, metaFilename: str = "meta.json"): # TODO: Should be a `@classmethod`
        """
        Loads this LibAlexandria Item from the given directory.

        dirpath: The path to a directory that conforms to Lib Alexandria standard.
        metaFilename: The filename and extension of the meta file to load within the provided `dirpath`.
        """
        # Check the directory path
        self.directory = laShared.fullpath(dirpath)
        if laShared.checkPath(self.directory):
            # Check the meta file path
            self.metaFilepath = os.path.join(self.directory, metaFilename)
            if os.path.isfile(self.metaFilepath):
                # TODO: Resolve additional flags from the directory structure to `resolvedFlags`

                # Read the meta file
                with open(self.metaFilepath, "r") as metaFile:
                    # Load the meta json data
                    # TODO: Add failure message for bad JSON load
                    metaJson = json.loads(metaFile.read())

                    # Verify the base level of the json
                    if isinstance(metaJson, dict):
                        # Assign values
                        self.isLoaded = self._assignMetadata(metaJson)
                    else:
                        # Failed
                        print(f"\"{self.metaFilepath}\" is not a valid Metadata file.")
            else:
                # Failed
                print(f"\"{self.metaFilepath}\" could not be found within the provided directory: {self.directory}")
        else:
            # Failed
            print(f"Provided directory does not exist: {self.directory}")

    # Private Functions
    def _assignMetadata(self, data: dict) -> bool:
        """
        Parses the provided Metadata JSON dictionary and assigns its values to this object.

        data: Metadata JSON dictionary.

        Returns True if the assigned metadata is valid.
        """
        # Get the version code
        dataVersion = data.get("_infover", None)

        # Check for validity
        if dataVersion != None:
            # Convert to a data version object
            dataVersion = SemanticVersion(dataVersion)

            # Check the version
            if dataVersion.major == 2:
                return self._parseVersionTwoData(data, dataVersion)
            elif dataVersion.major == 1:
                return self._parseVersionOneData(data, dataVersion)
            else:
                # Failed
                print(f"\"{dataVersion.string}\" is not a supported version of Meta file.")
        else:
            # Failed
            print(f"\"{self.metaFilepath}\" does not provide a Meta file version using the `_infover` key.")

        # Overall Failure
        return False

    def _parseVersionTwoData(self, data: dict, version: SemanticVersion) -> bool:
        """
        Parses the provided Metadata JSON dictionary as a `v2.*` LibAlex dataset and assigns its values to this object.

        data: Metadata JSON dictionary.
        version: A SemanticVersion object.

        Returns True if the assigned metadata is valid.
        """
        # Prepare flag
        isValid = True

        # Assign easy values
        self.infoVer = version
        self.classification = data.get("classification", laShared.DEFAULT_CLASSIFICATION)
        self.title = data.get("title", laShared.DEFAULT_TITLE)
        self.author = data.get("author", laShared.DEFAULT_AUTHOR)
        self.date = data.get("date", laShared.DEFAULT_DATE)
        self.flags = data.get("flags", laShared.DEFAULT_FLAGS)
        self.description = data.get("description", laShared.DEFAULT_DESCRIPTION)

        # Assign source file
        sourceFileRaw = data.get("sourceFile", laShared.DEFAULT_SOURCEFILE)
        if (sourceFileRaw != laShared.DEFAULT_SOURCEFILE) and isinstance(sourceFileRaw, str):
            sourceFileRaw = os.path.join(self.directory, sourceFileRaw)
            if os.path.isfile(sourceFileRaw):
                self.sourceFile = sourceFileRaw
            else:
                if self.isVerbose:
                    print(f"Provided source file path is invalid: {sourceFileRaw}")
                isValid = False
        else:
            if self.isVerbose:
                print(f"Provided source file path is invalid: {sourceFileRaw}")
            isValid = False

        # Assign other files
        otherFilesRaw = data.get("otherFiles", laShared.DEFAULT_OTHERFILES)
        if (otherFilesRaw != laShared.DEFAULT_OTHERFILES) and isinstance(otherFilesRaw, list):
            # Populate the other files list
            self.otherFiles = []
            for ofData in otherFilesRaw:
                # Resolve the full filepath
                otherFilePath = ofData.get("path", laShared.DEFUALT_OTHERFILE_PATH)
                if otherFilePath != laShared.DEFUALT_OTHERFILE_PATH:
                    otherFilePath = os.path.join(self.directory, otherFilePath)

                # Record the other file
                try:
                    otherFile = LibAlexRelatedFile(
                        ofData.get("label", laShared.DEFAULT_OTHERFILE_LABEL),
                        otherFilePath,
                        ofData.get("description", laShared.DEFAULT_OTHERFILE_DESCRIPTION),
                        ofData.get("id", laShared.DEFAULT_OTHERFILE_ID)
                    )
                    self.otherFiles.append(otherFile)
                except FileNotFoundError as e:
                    print("Failed to load a Related File because:\n", e)

        return isValid

    def _parseVersionOneData(self, data: dict, version: SemanticVersion) -> bool:
        """
        Parses the provided Metadata JSON dictionary as a `v1.*` LibAlex dataset and assigns its values to this object the best it can.

        *Some data will be filled with default values!*
        This is due to the fact that `v1.*` contains less information than `v2.*` data.

        data: Metadata JSON dictionary.
        version: A SemanticVersion object.

        Returns True if the assigned metadata is valid.
        """
        # Tell the user they're bad
        print("DEPRECATED: Version `1.*` Meta files should be converted to Version `2.*` for increased compatibility and functionality!")

        # Convert the data to 2.*
        translated = {
            "title": data.get("title", laShared.DEFAULT_TITLE),
            "author": data.get("author", laShared.DEFAULT_AUTHOR),
            "date": data.get("date", laShared.DEFAULT_DATE),
            "sourceFile": data.get("content", laShared.DEFAULT_SOURCEFILE),
            "flags": data.get("flags", laShared.DEFAULT_FLAGS),
            "description": data.get("description", laShared.DEFAULT_DESCRIPTION)
        }

        # Run through v2.* parser
        return self._parseVersionTwoData(translated, version)

    # Functions
    def getAllFlags(self) -> list:
        """
        Returns all flags including metadata specified, resolved from filepath, and metadata classification.
        """
        # Check if loaded
        if self.isLoaded:
            # Determine if the flag lists are valid
            flagsIsList = isinstance(self.flags, list)
            resolvedFlagsIsList = isinstance(self.resolvedFlags, list)

            if flagsIsList and resolvedFlagsIsList:
                # Both flags
                allFlags = self.flags + self.resolvedFlags
                allFlags.append(self.classification)
                return allFlags
            elif flagsIsList:
                # Only metadata flags
                allFlags = self.flags.copy()
                allFlags.append(self.classification)
                return allFlags
            else:
                # Only resolved flags
                allFlags = self.resolvedFlags.copy()
                allFlags.append(self.classification)
                return allFlags

    def getText(self) -> str:
        """
        Returns the full source file Markdown text.
        """
        # Check if loaded
        if self.isLoaded:
            # Open and read
            with open(self.sourceFile, 'r') as source:
                return source.read()

    # TODO: A `toJson` function

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
