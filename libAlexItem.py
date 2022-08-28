# LibAlexandria: LibAlexandria Item
# A standardized LibAlexandria item that can be used in other Python scripts.

# Imports
import os
import json

import libAlexDefaults as laShared
from libAlexOtherFile import LibAlexOtherFile

# Defaults

# Classes
class LibAlexItem:
    """
    A LibAlexandria Item representing the information for the provided directory's meta file and content.
    """
    # Constructor
    def __init__(self, verbose = False):
        """
        verbose: If verbose logging should be enabled.
        """
        # Assign variables
        self.isLoaded = False
        self.directory = laShared.DEFAULT_ITEM_DIRECTORY
        self.metaFilepath = laShared.DEFAULT_ITEM_METAFILEPATH
        self.resolvedFlags = laShared.DEFAULT_ITEM_RESOLVEDFLAGS
        self.isVerbose = verbose

        # Prepare default values
        self.classification = laShared.DEFAULT_CLASSIFICATION
        self.title = laShared.DEFAULT_TITLE
        self.author = laShared.DEFAULT_AUTHOR
        self.date = laShared.DEFAULT_DATE
        self.sourceFile = laShared.DEFAULT_SOURCEFILE
        self.otherFiles = laShared.DEFAULT_OTHERFILES
        self.flags = laShared.DEFAULT_FLAGS
        self.description = laShared.DEFAULT_DESCRIPTION

    # Loader Functions
    def loadMeta(self, dirpath: str, metaFilename = "meta.json"):
        """
        Loads this LibAlexandria Item from the given directory.

        dirpath: The path to a directory that conforms to Lib Alexandria standard.
        metaFilename: The filename and extension of the meta file to load within the provided `dirpath`.
        """
        # Check the directory path
        dirIsValid, self.directory = laShared.checkPath(dirpath, verbose=self.isVerbose)
        if dirIsValid:
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
                        self._assignMetadata(metaJson)
                        self.isLoaded = True
                    else:
                        # Failed
                        print(f"\"{self.metaFilepath}\" is not a valid Metadata file.")
            else:
                # Failed
                print(f"\"{self.metaFilepath}\" could not be found within the provided directory: {self.directory}")
        else:
            # Failed
            print(f"Provided directory does not exist: {self.directory}")

    ## Core Functions
    def __str__(self) -> str:
        if self.isLoaded:
            return f"{self.title} by {self.author} ({self.date})"
        else:
            return "Invalid LibAlexandria Item"

    # Private Functions
    def _assignMetadata(self, data: dict) -> bool:
        """
        Parses the provided Metadata JSON dictionary and assigns its values to this object.
        Be sure to run `validate()` after assigning these values.

        data: Metadata JSON dictionary.
        """
        # Assign easy values
        self.classification = data.get("classification", laShared.DEFAULT_CLASSIFICATION)
        self.title = data.get("title", laShared.DEFAULT_TITLE)
        self.author = data.get("author", laShared.DEFAULT_AUTHOR)
        self.date = data.get("date", laShared.DEFAULT_DATE)
        self.sourceFile = data.get("sourceFile", laShared.DEFAULT_SOURCEFILE)
        self.flags = data.get("flags", laShared.DEFAULT_FLAGS)
        self.description = data.get("description", laShared.DEFAULT_DESCRIPTION)

        # Assign other files
        otherFilesRaw = data.get("otherFiles", laShared.DEFAULT_OTHERFILES)
        if (otherFilesRaw != laShared.DEFAULT_OTHERFILES) and (otherFilesRaw != None) and isinstance(otherFilesRaw, list):
            # Populate the other files list
            self.otherFiles = []
            for ofData in otherFilesRaw:
                # Resolve the full filepath
                otherFilePath = ofData.get("path", laShared.DEFUALT_OTHERFILE_PATH)
                if otherFilePath != laShared.DEFUALT_OTHERFILE_PATH:
                    otherFilePath = os.path.join(self.directory, otherFilePath)

                # Record the other file
                otherFile = LibAlexOtherFile(
                    ofData.get("label", laShared.DEFAULT_OTHERFILE_LABEL),
                    otherFilePath,
                    ofData.get("description", laShared.DEFAULT_OTHERFILE_DESCRIPTION),
                    verbose=self.isVerbose
                )
                self.otherFiles.append(otherFile)

    # Functions
    # TODO: Add function to get all flags from `flags`, `resolvedFlags`, and `classification`
    def getAllFlags(self) -> list:
        """
        Returns all flags including metadata specified, resolved from filepath, and metadata classification.
        """
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

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")