#!/usr/bin/env python3
""" Unit Test and Integration Test"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock


GithubOrgClient = __import__("client").GithubOrgClient
TEST_PAYLOAD = __import__("fixtures").TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org method"""
        dict_ = {"payload": True}
        mock_get_json.return_value = dict_
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, dict_)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
