#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
Tests include:
- org property
- _public_repos_url property
- public_repos method
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

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
        Test that _public_repos_url returns the expected URL extracted
        from the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/google/repos"
        mock_payload = {"repos_url": expected_url}

        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns a list of repository names
        based on the mocked payload. Also test that _public_repos_url
        property and get_json function are called exactly once.
        """
        # Mocked list of repos returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Mock the _public_repos_url property to return a fake URL
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            fake_url = "https://api.github.com/orgs/google/repos"
            mock_url.return_value = fake_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected list of repository names
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Ensure the property was accessed exactly once
            mock_url.assert_called_once()

            # Ensure get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(fake_url)
