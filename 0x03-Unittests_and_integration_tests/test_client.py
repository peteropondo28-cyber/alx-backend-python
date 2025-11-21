#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

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

        # Patch get_json inside client module
        with patch("client.get_json") as mock_get_json:
            mock_get_json.return_value = expected_payload

            client = GithubOrgClient(org_name)
            result = client.org

            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )
            self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL based on
        the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        # Patch GithubOrgClient.org as a property (memoize turned it into one)
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:

            mock_org.return_value = mock_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)
            
