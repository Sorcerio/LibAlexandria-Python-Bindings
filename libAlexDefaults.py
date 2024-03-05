# LibAlexandria: Defaults
# The default values for various components of the Python 3 bindings.

# Imports
import os
import re
from unicodedata import normalize

# Variables
VER_LIBALEX = "2.0.0"

DEF_ITEM_DIR = None
DEF_ITEM_META_PATH = None
DEF_ITEM_RES_FLAGS = None

DEF_REL_FILE_LABEL = "Untitled"
DEF_REL_FILE_PATH = None
DEF_REL_FILE_DESC = ""
DEF_REL_FILE_ID = None

DEF_CLASSIFICATION = None
DEF_TITLE = "Untitled"
DEF_AUTHOR = "Anonymous"
DEF_DATE = "Undated"
DEF_SRC_FILE = None
DEF_REL_FILES = None
DEF_FLAGS = None
DEF_DESC = "An empty LibAlexandria Item."

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
