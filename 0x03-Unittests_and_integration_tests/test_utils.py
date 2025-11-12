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
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests the access_nested_map function with various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
