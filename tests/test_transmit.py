"""The test_transmit module is used to test the rifs.transmit module.
"""

import pytest

import rifs.core
import rifs.transmit
from rifs.core.soumission import standard_job


class NonInheritedOperation:
    """A non-inherited operation class."""

    def __init__(self, name: str = "non-inherited", notes: str = "Non-Inherited Operation"):
        """Initialize the NonInheritedOperation class."""
        self.name = name
        self.notes = notes

    def __call__(self):
        """Print the operation name and notes."""
        print(f"{self.name}: {self.notes}")


def test_instance_skip():
    """Test the instance skip."""
    operation = NonInheritedOperation()
    created_standard_job = standard_job()

    constructor = rifs.transmit.Constructor([operation, created_standard_job])

    assert constructor

    assert constructor.build()


def test_no_operations():
    """Test the constuctor doesnt process any bad operations."""
    constructor = rifs.transmit.Constructor([])
    constructor_resolver = constructor.build()

    assert constructor, "The constructor is not created."

    assert len(constructor_resolver) == 0, "The resolver has grouping, we want it to be empty."


def test_raise_only_one():
    """Test the raise only one."""
    with pytest.raises(TypeError):
        rifs.transmit.only_one(NonInheritedOperation())


if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
