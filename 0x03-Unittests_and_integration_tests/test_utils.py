#!/usr/bin/env python3
import pytest
from utils import add_one_and_two

@pytest.mark.parametrize(
    "input_a, input_b, expected_result",
    [
        (1, 2, 4),
        (0, 0, 1),
        (-1, 1, 1),
        (10, 20, 31),
        (1.5, 2.5, 5.0),
    ]
)
def test_add_one_and_two(input_a, input_b, expected_result):
    """
    Tests the add_one_and_two function with various valid inputs.
    """
    assert add_one_and_two(input_a, input_b) == expected_result

@pytest.mark.parametrize(
    "input_a, input_b, expected_error_message",
    [
        ("a", 2, "Inputs must be numbers"),
        (1, "b", "Inputs must be numbers"),
        (None, 5, "Inputs must be numbers"),
    ]
)
def test_add_one_and_two_exceptions(input_a, input_b, expected_error_message):
    """
    Tests the add_one_and_two function for expected exceptions.
    """
    with pytest.raises(TypeError) as excinfo:
        add_one_and_two(input_a, input_b)
    assert str(excinfo.value) == expected_error_message
