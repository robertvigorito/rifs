"""Test that the rifs module can import kwargs outside the normal standard library types.
"""

from pathlib import Path

import pytest

import rifs.transmit
from rifs.fixtures.test import PathPrinter


@pytest.fixture(name="pathlib_one")
def path_one_fixture() -> Path:
    """Return a pathlib.Path object."""
    return Path("/vfx/wgid/test/one")


@pytest.fixture(name="pathlib_two")
def path_two_fixture() -> Path:
    """Return a pathlib.Path object."""
    return Path("/vfx/wgid/test/two")


def test_passover_kwarg_object(pathlib_one: Path, pathlib_two: Path):
    """Test that the rifs module can import kwargs outside the normal standard library types."""
    path_printer = PathPrinter(path_one=pathlib_one, path_two=pathlib_two)
    assert path_printer.path_one == pathlib_one, "The path is not correct."

    assert path_printer.path_two == pathlib_two, "The path is not correct."

    returncode, output = rifs.transmit.only_one(path_printer)

    assert returncode == 0, f"The process failed!\n{output}"
    assert output == f"Path One: {pathlib_one}\nPath Two: {pathlib_two}\n", "The output is not correct."
