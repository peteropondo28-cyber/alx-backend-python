#!/usr/bin/env python3
import unittest
from parameterized import parameterized
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
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests the access_nested_map function with various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "KeyError: 'a'"),
        ({"a": 1}, ("a", "b"), "KeyError: 'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """
        Tests that access_nested_map raises a KeyError with the correct message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)
        #!/usr/bin/env python3
"""
Unit tests for the get_json function.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Dict
from your_module import get_json  # Replace your_module

class TestGetJson(unittest.TestCase):
    """
    Unit tests for the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("your_module.requests.get")  # Replace your_module
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict,
        mock_get: Mock,
    ) -> None:
        """
        Tests that get_json returns the expected result.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
