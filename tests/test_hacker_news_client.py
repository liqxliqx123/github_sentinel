import unittest
from unittest.mock import patch, MagicMock
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fetcher.hacker_news import fetch_hackernews_top_stories


class TestHackerNews(unittest.TestCase):

    @patch("fetcher.hacker_news.requests.get")
    def test_fetch_hackernews_top_stories(self, mock_get):
        # 模拟爬虫响应
        mock_response = MagicMock()
        mock_response.text = '''
        <tr class="athing">
            <td class="title">
                <span class="titleline">
                    <a href="https://news.ycombinator.com/">Story 1</a>
                </span>
            </td>
        </tr>
        '''
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        """Test that the fetch_hackernews_top_stories function returns a list of story IDs."""
        top_stories = fetch_hackernews_top_stories()
        self.assertEqual(len(top_stories), 1)
        self.assertEqual(top_stories[0]['title'], 'Story 1')
        self.assertEqual(top_stories[0]['link'], 'https://news.ycombinator.com/')

    @patch("fetcher.hacker_news.requests.get")
    def test_fetch_hackernews_top_stories_exception(self, mock_get):
        # 模拟爬虫响应
        mock_get.side_effect = Exception("An error occurred")

        """Test that the fetch_hackernews_top_stories function returns a list of story IDs."""
        top_stories = fetch_hackernews_top_stories()
        self.assertEqual(len(top_stories), 0)