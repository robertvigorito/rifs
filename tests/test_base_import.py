"""Standard import test for the base package.
"""


def test_import():
    """Test the base import."""

    import rifs  # noqa: F401 # pylint: disable=unused-import,import-outside-toplevel

    assert rifs
    assert rifs.core
