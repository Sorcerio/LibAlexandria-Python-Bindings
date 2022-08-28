# LibAlexandria: LibAlexandria Other File Object
# A utility object for defining Other Files for a LibAlexandria Item.

# Imports
import libAlexDefaults as laShared

# Classes
class LibAlexOtherFile:
    """
    An additional file generally associated with a LibAlexandria Item.
    """
    # Constructor
    def __init__(self, label: str, path: str, description: str, id: str, verbose = False):
        """
        label: Title or generic label for the referenced file.
        path: A full filepath to the referenced file.
        description: A description of the referenced file.
        id: A string identifier for the referenced file or `None`.
        """
        # Assign values
        self.isVerbose = verbose
        self.label = label
        self.path = path
        self.description = description
        self.id = id

        # Validate the path
        isValidPath, self.path = laShared.checkPath(self.path)
        if not isValidPath:
            if self.isVerbose:
                print(f"An invalid path was provided for \"{self.label}\": {self.path}")
            self.path = laShared.DEFUALT_OTHERFILE_PATH

    # Core Functions
    def __str__(self) -> str:
        return f"{self.label} at {self.path}"

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
