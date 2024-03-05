# LibAlexandria: Defaults
# The default values for various components of the Python 3 bindings.

# Imports
import os
import re
from unicodedata import normalize

# Variables
VER_LIBALEX = "2.0.0"

DEFAULT_ITEM_DIRECTORY = None
DEFAULT_ITEM_METAFILEPATH = None
DEFAULT_ITEM_RESOLVEDFLAGS = None

DEFAULT_OTHERFILE_LABEL = "Untitled"
DEFUALT_OTHERFILE_PATH = None
DEFAULT_OTHERFILE_DESCRIPTION = ""
DEFAULT_OTHERFILE_ID = None

DEFAULT_CLASSIFICATION = None
DEFAULT_TITLE = "Untitled"
DEFAULT_AUTHOR = "Anonymous"
DEFAULT_DATE = "Undated" # NOTE: This is normally a year in 'YYYY-MM-DD' format.
DEFAULT_SOURCEFILE = None
DEFAULT_OTHERFILES = None
DEFAULT_FLAGS = None
DEFAULT_DESCRIPTION = "An empty LibAlexandria Item."

# Functions
def fullpath(path: str) -> str:
    """
    Returns the full path of the provided path.

    path: The path to resolve.

    Returns the full path.
    """
    return os.path.abspath(os.path.expanduser(path))

def checkPath(path: str, createPath: bool = False) -> bool:
    """
    Checks if the provided path exists; and creates it if specified.

    path: The string path to clean.
    createPath: Boolean indicating if the path should be created if it doesn't exist.

    Returns if the path exists.
    """
    # Get the full path
    path = fullpath(path)

    # Check if the path exists
    if not os.path.exists(path):
        if createPath:
            # Build the desired path
            os.makedirs(path)
        else:
            # Fail
            return False

    # Success
    return True

def slugify(s: str) -> str:
    """
    Converts the provided string into a slugified version
    Modified from [Django](https://github.com/django/django/blob/d3f4c2b95d2a13a5d9bc0e6413dfdbab21388822/django/utils/text.py#L385).

    s: String to slugify.

    Returns the string slugified.
    """
    s = str(s)
    s = normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower())
    s = re.sub(r"[-\s]+", "-", s).strip("-_")
    return s

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
