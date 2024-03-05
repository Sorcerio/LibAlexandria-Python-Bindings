# LibAlexandria: Version Data
# Interprets "Semantic Versioning 2.0.0" strings as code accessible parameters.

# Imports
import re

# Classes
class SemanticVersion:
    """
    Interprets "Semantic Versioning 2.0.0" strings as code accessible parameters.
    """
    # Constructor
    def __init__(self, s: str):
        """
        s: A Semantic Versioning version string like `1.0.0`.
        """
        # Record the basic string
        self.string = s # TODO: Trim "v" and such characters

        # Interpret the version
        self.isValid = True
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.preRelease = ""
        self.metaData = ""
        self._parse()

    # Python Functions
    def __str__(self) -> str:
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    # TODO: eq, ne, lt, le, gt, and ge functions

    # Private Functions
    def _parse(self):
        """
        Parses the version string.

        Regex from [Semantic Versioning 2.0.0](https://semver.org).
        """
        # Collect matches
        regex = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        matches = re.finditer(regex, self.string, re.MULTILINE)

        # Loop through matches
        for matchNum, match in enumerate(matches, start=1):
            # Only accept one version set
            if matchNum > 1:
                print(f"Multiple version code matches were found in: \"{self.string}\". Only the data from the first will be kept.")
                break

            # Get the major
            try:
                self.major = int(match.group(1))
            except ValueError:
                print(f"An invalid major version number was found in: \"{self.string}\". It will be recorded as `None`.")
                self.major = None
                self.isValid = False

            # Get the minor
            try:
                self.minor = int(match.group(2))
            except ValueError:
                print(f"An invalid minor version number was found in: \"{self.string}\". It will be recorded as `None`.")
                self.minor = None
                self.isValid = False

            # Get the patch
            try:
                self.patch = int(match.group(3))
            except ValueError:
                print(f"An invalid patch version number was found in: \"{self.string}\". It will be recorded as `None`.")
                self.patch = None
                self.isValid = False

            # Get the pre-release
            self.preRelease = match.group(4)

            # Get the build meta data
            self.metaData = match.group(5)

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
