#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
Tests include:
- org property
- _public_repos_url property
- public_repos method
- has_license method
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
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            fake_url = "https://api.github.com/orgs/google/repos"
            mock_url.return_value = fake_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(fake_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),  # Edge case: no license key
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if the repo license key matches
        the given license_key, and False otherwise.

        Args:
            repo (dict): Repository dictionary containing license info.
            license_key (str): The license key to check.
            expected (bool): Expected return value.
        """
        client = GithubOrgClient("google")  # org name irrelevant here
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
