import os

from zhipuai import ZhipuAI

from utils.logger import LogManager

from config import Config
from utils.path import get_gpt_4o_mini_prompt_path


class ZhipuAIModule:

    def __init__(self):
        api_key = os.getenv("ZHIPU_API_KEY")
        self.conf = Config().config
        self.model = self.conf["model"]["ollama"]["name"]
        self.client = ZhipuAI(api_key=api_key)
        self.logger = LogManager().logger

    def generate_daily_report(self, system_prompt, markdown_content):
        prompt = f"{markdown_content}"
        if not self.conf["dry_run"]:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            self.logger.info("Sending request to ZhipuAI")
            response = self.client.chat.completions.create(
                model=self.model,  # 填写需要调用的模型编码
                messages=messages,
                stream=False,
            )
            self.logger.info(f"Response received from ZhipuAI")
            return response.choices[0].message.content
        return ""

    def generate_report(self, report_type: str, markdown_content):
        if report_type == "github":
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "github_prompt.txt")
        elif report_type == "hacker_news_hours":
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "hacker_news_hours_prompt.txt")
        elif report_type == "hacker_news_daily_report":
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "hacker_news_daily_report_prompt.txt")
        else:
            raise ValueError(f"Invalid report type: {report_type}")
        print(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            return self.generate_daily_report(system_prompt, markdown_content)
