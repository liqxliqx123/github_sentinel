import os

from zhipuai import ZhipuAI

from utils.logger import LogManager

from config import Config
from utils.path import get_gpt_4o_mini_prompt_path


class ZhipuAIModule:

    def __init__(self):
        api_key = os.getenv("ZHIPU_API_KEY")
        self.conf = Config().config
        self.model = self.conf["model"]["glm"]["name"]
        self.client = ZhipuAI(api_key=api_key)

    def generate_daily_report(self, system_prompt, markdown_content):
        logger = LogManager().logger
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
            response = self.client.chat.completions.create(
                model=self.model,  # 填写需要调用的模型编码
                messages=messages,
                stream=False,
            )
            return response.choices[0].message.content
        return ""

    def generate_report(self, report_type: str, markdown_content):
        if report_type == "github":
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "github_prompt.txt")
        else:
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "hacker_news_prompt.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            return self.generate_daily_report(system_prompt, markdown_content)
