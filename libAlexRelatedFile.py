# LibAlexandria: LibAlexandria Related File Object
# A utility object for defining an additional file generally associated with a LibAlexandria Item.

# Imports
import json
from typing import Optional

import libAlexDefaults as laShared

# Classes
class LibAlexRelatedFile:
    """
    A utility object for defining an additional file generally associated with a LibAlexandria Item.
    """
    # Constructors
    def __init__(self, label: str, path: str, description: str, id: Optional[str] = None):
        """
        label: Title or generic label for the referenced file.
        path: A full filepath to the referenced file.
        description: A description of the referenced file.
        id: A string identifier for the referenced file or `None`.
        """
        # Assign values
        self.label = label
        self.path = path
        self.description = description
        self.id = id

        # Validate the path
        self.path = laShared.fullpath(self.path)

        if not laShared.checkPath(self.path):
            raise FileNotFoundError(f"Related File called \"{self.label}\" could not be found at: {self.path}")

    # Python Functions
    def __str__(self) -> str:
        return f"{self.label} at {self.path}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    # Functions
    def toJson(self) -> dict:
        """
        Returns a dictionary representation of the object.
        """
        return {
            "label": self.label,
            "path": self.path,
            "description": self.description,
            "id": self.id
        }

    def toJsonStr(self) -> str:
        """
        Returns a JSON string representation of the object.
        """
        return json.dumps(self.toJson())

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
