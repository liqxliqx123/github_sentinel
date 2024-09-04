# 调用ollama接口，实现模型私有化
import datetime
import json
import os

import requests

from config import Config
from utils.logger import LogManager
from utils.path import get_prompt_path


class Gemma2Model:
    def __init__(self):
        self.conf = Config().config
        self.model_name = self.conf["model"]["ollama"]["name"]
        self.model_url = self.conf["model"]["ollama"]["url"]
        self.logger = LogManager().logger

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
            options = {
                "temperature": 0.1,
                "num_ctx": 8192  # 设置太小可能导致模型不听prompt的话
            }
            self.logger.debug(f"调用ollama接口")
            # self.logger.debug(f"messages: {messages}")
            # todo 通过tools进行联网
            response = requests.post(self.model_url,
                                     json={"model": self.model_name, "messages": messages, "stream": False,
                                           "options": options},
                                     timeout=300)
            if response.status_code == 200:
                self.logger.debug("调用ollama接口成功")
                content = response.content
                content = json.loads(content.decode())
                return content["message"]["content"]
            else:
                self.logger.error(f"调用gemma2接口失败，错误信息：{response.text}")

        return ""

    def generate_report(self, report_type: str, markdown_content):
        model_type = self.conf["model_key"]
        time_now = datetime.datetime.now().strftime("%Y%m%d")
        if report_type == "github":
            file_path = os.path.join(get_prompt_path(), f"{model_type}/github_prompt.txt")
        elif report_type == "hacker_news_hours":
            file_path = os.path.join(get_prompt_path(), f"{model_type}/hacker_news_hours_prompt.txt")
        elif report_type == "hacker_news_daily_report":
            file_path = os.path.join(get_prompt_path(), f"{model_type}/hacker_news_daily_report_prompt.txt")
        else:
            raise ValueError(f"Invalid report type: {report_type}")
        self.logger.debug(f"读取prompt文件：{file_path}")
        self.logger.debug(f"调用模型： [{self.model_name}]")
        with open(file_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            return self.generate_daily_report(system_prompt.format(time_now=time_now),
                                              markdown_content)
