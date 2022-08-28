# LibAlexandria: LibAlexandria Item
# A standardized LibAlexandria item that can be used in other Python scripts.

# Imports
import os
import json

import libAlexDefaults as laShared

# Defaults

# Classes
class LibAlexItem():
    """
    A LibAlexandria item representing the information for the provided directory's meta file and content.
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
                        # self.classification = metaJson.get()
                        pass
                    else:
                        # Failed
                        print(f"\"{self.metaFilepath}\" is not a valid Metadata file.")

                # TODO: Validation check assigned values
            else:
                # Failed
                print(f"\"{self.metaFilepath}\" could not be found within the provided directory: {self.directory}")
        else:
            # Failed
            print(f"Provided directory does not exist: {self.directory}")

    # Private Functions
    # TODO: Value assignment function
    # TODO: Value validation function (together with above?)

    # Functions
    # TODO: Add function to get all flags from `flags`, `resolvedFlags`, and `classification`
