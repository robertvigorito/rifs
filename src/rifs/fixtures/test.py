"""The rifs fixtures for testing.
"""

from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path, PosixPath

# Package imports
import rifs.core
import rifs.transmit


@dataclass(eq=True, order=True)
class EchoOperation(rifs.core.AbstractRif):
    """Echo operation for testing."""

    notes: str = "Echo Operation"

    def __call__(self):
        """Echo the notes."""
        print("Echo:", self.notes)


@dataclass(eq=True, order=True)
class PathPrinter(rifs.core.AbstractRif):
    """Path printer for testing."""

    path_one: Path = field(default_factory=Path)
    path_two: Path = field(default_factory=Path)

    def __call__(self):
        """Print the paths."""

        # Check the paths and raise an error if they are not valid
        if not isinstance(self.path_one, (Path, PosixPath)) or not isinstance(self.path_two, (Path, PosixPath)):
            raise TypeError("The paths are not valid pathlib.Path objects.")

        print("Path One:", self.path_one)
        print("Path Two:", self.path_two)


TestTuple = namedtuple("TestTuple", ["a", "b"])
