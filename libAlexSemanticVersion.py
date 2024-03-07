# LibAlexandria: Senamtic Versioning
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
        self.string = s

        # Check for leading version character
        if self.string[0].lower() == "v":
            self.string = self.string[1:]

        # Assign initial values
        self.isValid = True
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.preRelease = ""
        self.metaData = ""

        # Interpret the version
        self._parse()

    # Python Functions
    def __str__(self) -> str:
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __eq__(self, other: 'SemanticVersion') -> bool:
        return self.string == other.string

    def __ne__(self, other: 'SemanticVersion') -> bool:
        return self.string != other.string

    def __lt__(self, other: 'SemanticVersion') -> bool:
        return self._versionTuple() < other._versionTuple()

    def __le__(self, other: 'SemanticVersion') -> bool:
        return self._versionTuple() <= other._versionTuple()

    def __gt__(self, other: 'SemanticVersion') -> bool:
        return self._versionTuple() > other._versionTuple()

    def __ge__(self, other: 'SemanticVersion') -> bool:
        return self._versionTuple() >= other._versionTuple()

    # Private Functions
    def _parse(self):
        """
        Parses the version string.

        Regex from [Semantic Versioning 2.0.0](https://semver.org).
        """
        # Check if the string is valid
        if not isinstance(self.string, str):
            print(f"An invalid type (\"{type(self.string)}\") of version string was provided: {self.string}.")
            self.isValid = False
            return

        # Check if a number is actually present
        if (len(self.string.strip()) == 0) or not (any(i.isdigit() for i in self.string)):
            print(f"No numbers were provided in the version string: \"{self.string}\".")
            self.isValid = False
            return

        # Collect matches
        regex = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        matches = re.finditer(regex, self.string, re.MULTILINE)

        # Loop through matches
        matchNum = -1
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
            if self.preRelease is None:
                self.preRelease = ""

            # Get the build meta data
            self.metaData = match.group(5)
            if self.metaData is None:
                self.metaData = ""

        # Check if any matches were even found
        if matchNum < 1:
            print(f"No valid version code matches were found in: \"{self.string}\".")
            self.isValid = False

    def _versionTuple(self) -> tuple[int, int, int]:
        """
        Returns the version values as a tuple.
        """
        return (self.major, self.minor, self.patch)

# Console Execution
if __name__ == "__main__":
    print("This file cannot be run from the command line.")
