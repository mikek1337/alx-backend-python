#!/usr/bin/env python3
"""test_client module"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """test class GithubOrgClient"""

    def test_org(self):
        """test_org method"""
        @parameterized.expand([
            ("google"),
            ("abc"),
        ])
        @patch('client.get_json')
        def test_org(self, org_name, mock_get_json):
            """test_org method"""
            test_class = GithubOrgClient(org_name)
            test_class.org()
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_public_repos_url(self):
        """test_public_repos_url method"""
        with patch('client.GithubOrgClient.org',
                   PropertyMock(return_value={"repos_url": "twitter"})):
            """test_public_repos_url method"""
            test_class = GithubOrgClient("twitter")
            self.assertEqual(test_class._public_repos_url, "twitter")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test_public_repos method"""
        json_payload = [{"name": "google"}, {"name": "abc"}]
        mock_get_json.return_value = json_payload
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock(return_value="test")):
            test_class = GithubOrgClient("test")
            self.assertEqual(test_class.public_repos(), ["google", "abc"])
            mock_get_json.assert_called_once_with("test")
