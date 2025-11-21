#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos method.
Mocks only external requests using fixtures.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using real fixtures."""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get so that it returns fixture payloads."""
        # Patch requests.get directly
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Side effect function to return fixture payloads based on URL
        def get_json_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = []
            return mock_response

        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos returns list of repo names."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos filtered by license."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
