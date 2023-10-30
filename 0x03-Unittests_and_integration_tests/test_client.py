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

    def test_public_repos_url(self):
        """Test public_repos_url method"""
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            dict_ = {"repos_url": "https://api.github.com/orgs/google/repos"}
            mock_org.return_value = dict_
            test_client = GithubOrgClient("google")
            self.assertEqual(test_client._public_repos_url, dict_["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """ set up mock_get_json """
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        # using context manager for the mock_repo_url
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = url

            # Create an instance of GithubOrgClient
            test_client = GithubOrgClient("google")

            # Call the method being tested
            repos = test_client.public_repos()

            # Assert the returned list of repos is what you expect
            self.assertEqual(repos, ["repo1", "repo2"])

            # Assert that the mocks were called exactly once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, linc_key, result):
        """Test has_license method"""
        test_client = GithubOrgClient("google")
        self.assertEqual(test_client.has_license(repo, linc_key), result)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    (TEST_PAYLOAD)
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """TestIntegrationGithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """set up class"""
        cls.get_patcher = patch("requests.get")
        cls.mock = cls.get_patcher.start()
        cls.mock.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """tear down class"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("TAVISH"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("TAVISH"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()


if __name__ == "__main__":
    unittest.main()
