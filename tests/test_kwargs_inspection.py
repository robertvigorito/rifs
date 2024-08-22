"""Test the kwargs inspection for the rifs module.
"""

from collections import namedtuple
from pathlib import Path

import pytest

from rifs.core import inspection
from rifs.core import inspection as inspection
from rifs.fixtures.test import TestTuple

# Example namedtuple for testing


@pytest.fixture
def sample_kwargs() -> dict[str, object]:
    """Return a sample kwargs dictionary for testing."""

    return {
        "int_value": 42,
        "str_value": "example",
        "named_tuple_value": TestTuple(a=1, b=2),
        "list_value": [1, 2, 3],
        "dict_value": {"key": TestTuple(a=3, b=4), "path": Path("/vfx/wgid/test/one")},
    }


def test_define_namedtuple():
    """Test the define_namedtuple function."""
    value = TestTuple(a=1, b=2)
    expected = "TestTuple = namedtuple('TestTuple', ('a', 'b'))"
    assert inspection.define_namedtuple(value) == expected


def test_find_import():
    """Test the find_import function."""
    value = TestTuple(a=1, b=2)
    expected = "from rifs.fixtures.test import TestTuple"

    assert inspection.find_import(value, "rifs.core") == expected

    # Test with a built-in type
    value = 42
    expected = ""
    assert inspection.find_import(value, "rifs.core") == expected


def test_recursive_inspect_generator(sample_kwargs):
    """Test the recursive_inspect_generator function."""

    result = list(inspection.recursive_inspect_generator(sample_kwargs, "rifs.core"))

    expected = [
        "from rifs.core import TestTuple",
        "TestTuple = namedtuple('TestTuple', ('a', 'b'))",
        "from rifs.core import TestTuple",
    ]
    assert [item for item in result if item in expected]


def test_base(sample_kwargs: dict[str, object]):
    """Test the base function."""
    result = inspection.base(sample_kwargs)

    expected = [
        "from collections import namedtuple",
        "from pathlib import PosixPath",
        "TestTuple = namedtuple('TestTuple', ('a', 'b'))",
    ]
    assert result == expected


def test_formatted_base(sample_kwargs):
    """Test the formatted_base function."""
    result = inspection.formatted_base(sample_kwargs, "rifs.core")
    expected = """\
from collections import namedtuple
from pathlib import PosixPath
TestTuple = namedtuple('TestTuple', ('a', 'b'))"""
    assert result == expected
