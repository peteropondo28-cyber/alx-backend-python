#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function.
"""
import unittest
from parameterized import parameterized
from typing import (
    Mapping,
    Sequence,
    Any,
)
from your_module import access_nested_map  # Replace your_module

class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": 0}}, ("a", "b"), 0),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any,
    ) -> None:
        """
        Tests the access_nested_map function with various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "KeyError: 'a'"),
        ({"a": 1}, ("a", "b"), "KeyError: 'b'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_message: str,
    ) -> None:
        """
        Tests that access_nested_map raises a KeyError with the correct message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)

