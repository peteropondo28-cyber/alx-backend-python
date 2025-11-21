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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the correct list of
        repository names and calls the mocked properties exactly once.
        """
        payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = payload
        fake_url = "https://api.github.com/orgs/google/repos"

        # Patch _public_repos_url property
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = fake_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Check the result is just the repo names
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Ensure _public_repos_url property was accessed once
            mock_url.assert_called_once()

            # Ensure get_json was called once with the fake URL
            mock_get_json.assert_called_once_with(fake_url)
