# 调用ollama接口，实现模型私有化
import json
import os

import requests

from config import Config
from utils.logger import LogManager
from utils.path import get_gpt_4o_mini_prompt_path


class Gemma2Model:
    def __init__(self):
        self.conf = Config().config
        self.model_name = self.conf["model"]["gemma2"]["name"]
        self.model_url = self.conf["model"]["gemma2"]["url"]

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
            response = requests.post(self.model_url,
                                     json={"model": self.model_name, "messages": messages, "stream": False}, timeout=300)
            if response.status_code == 200:
                content = response.content
                content = json.loads(content.decode())
                return content["message"]["content"]
            else:
                logger.error(f"调用gemma2接口失败，错误信息：{response.text}")

        return ""

    def generate_report(self, report_type: str, markdown_content):
        if report_type == "github":
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "github_prompt.txt")
        else:
            file_path = os.path.join(get_gpt_4o_mini_prompt_path(), "hacker_news_prompt.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            return self.generate_daily_report(system_prompt, markdown_content)
