import unittest
from unittest.mock import patch, MagicMock
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fetcher.github import GithubFetcher


class TestGithubClient(unittest.TestCase):
    def setUp(self):
        # 初始化测试环境
        self.token = "fake_token"
        self.client = GithubFetcher()
        self.repo = "fake_repo"

    @patch("fetcher.github.requests.get")
    def test_fetch_issue(self, mock_get):
        # 模拟api响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"number": 1, "title": "Fix bug", "created_at": "2024-09-09T00:00:00Z"}]
        mock_get.return_value = mock_response

        # 调用fetch_issue方法并进行断言
        issues = self.client.fetch_issues(self.repo)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["number"], 1)
        self.assertEqual(issues[0]["title"], "Fix bug")

    @patch("fetcher.github.requests.get")
    def test_fetch_pull_requests(self, mock_get):
        # 模拟api响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"number": 42, "title": "Add new feature", "created_at": "2024-09-09T00:00:00Z"},
            {"number": 43, "title": "Add another new feature", "created_at": "2024-09-08T00:00:00Z"}]
        mock_get.return_value = mock_response

        # 调用fetch_issue方法并进行断言
        pr = self.client.fetch_pull_requests(self.repo)
        self.assertEqual(len(pr), 2)
        self.assertEqual(pr[0]["number"], 42)
        self.assertEqual(pr[0]["title"], "Add new feature")

    @patch("fetcher.github.requests.get")
    def test_fetch_pull_requests_by_empty(self, mock_get):
        # 模拟api响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # 调用fetch_issue方法并进行断言
        pr = self.client.fetch_pull_requests(self.repo)
        self.assertEqual(len(pr), 0)

if __name__ == "__main__":
    unittest.main()
