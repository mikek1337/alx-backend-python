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

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """test_has_license method"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            {"repos_url": "http://test.com"},
            [{"name": "google"}, {"name": "abc"}],
            ["google", "abc"],
            ["google"]
        ),
        (
            {"repos_url": "http://test.com"},
            [{"name": "google"}, {"name": "abc", "license": {"key": "apache2"}}],
            ["google", "abc"],
            ["abc"]
        )
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """TestIntegrationGithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """setUpClass method"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """tearDownClass method"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """test_public_repos method"""
        test_class = GithubOrgClient("test")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos(
            "apache2"), self.apache2_repos)
        self.mock_get.assert_called()
