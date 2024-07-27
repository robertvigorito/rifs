"""Standard import test for the base package.
"""

# Package imports
from rifs.fixtures.test import EchoOperation
import rifs.core
import rifs.transmit


def test_operation_output(capsys):
    """Test the operation output."""
    echo = EchoOperation()
    echo()
    captured = capsys.readouterr()
    assert captured.out == "Echo: Echo Operation\n", "The output is not correct."
    assert captured.err == ""


def test_operation_namespace():
    """Test the operation namespace."""

    echo = EchoOperation(name="namespace", notes="Namespace Operation", namespace="namespace")

    returncode, output = rifs.transmit.only_one(echo)

    assert "ModuleNotFoundError: No module named 'namespace'" in output, "The namespace failed to set."
    assert returncode == 1, f"The process didnt failed when it was meant too!\n{output}"


def test_operation_constructor():
    """Test the operation constructor."""
    echo = EchoOperation()
    returncode, output = rifs.transmit.only_one(echo)

    assert echo, "The operation is not created."
    assert returncode == 0, f"The process failed!\n{output}"
