#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient.org method."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name):
        """
        Test that GithubOrgClient.org returns the correct payload and that
        get_json is called exactly once with the expected URL.
        """
        expected_payload = {"login": org_name}
        # Use context manager to avoid decorator ordering issues
        with patch("client.get_json") as mock_get_json:
            mock_get_json.return_value = expected_payload

            client = GithubOrgClient(org_name)
            result = client.org

            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )
            self.assertEqual(result, expected_payload)
