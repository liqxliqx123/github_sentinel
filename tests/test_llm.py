import unittest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from config import Config

from llm.gpt4 import GPT4Module




class TestLLM(unittest.TestCase):
    def setUp(self):
        self.config = Config().config
        self.llm = GPT4Module()
        # 设置示例的系统提示信息
        self.system_prompt = "Your specific system prompt for GitHub report generation"

        # 准备用于测试的 GitHub 内容字符串
        self.github_content = """
                # Progress for langchain-ai/langchain (2024-08-20 to 2024-08-21)

                ## Issues Closed in the Last 1 Days
                - partners/chroma: release 0.1.3 #25599
                - docs: few-shot conceptual guide #25596
                - docs: update examples in api ref #25589
                """
    @patch('utils.logger.LogManager')
    @patch('llm.gpt4.OpenAI')
    def test_openai_exception_handling(self, mock_openai, mock_logger):
        """
        测试调用 OpenAI 模型时发生异常的错误处理路径。
        """
        # 模拟 OpenAI 客户端抛出异常
        mock_openai().chat.completions.create.side_effect = Exception("OpenAI API error")

        self.assertEqual(self.llm.generate_daily_report(self.system_prompt, self.github_content), "")

        # 检查是否记录了预期的错误日志
        # mock_logger._logger.error.assert_called_with("调用openAI接口失败：OpenAI API error")
