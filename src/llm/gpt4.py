import os
from openai import OpenAI
from config import Config
from utils.logger import LogManager
from utils.path import get_gpt_4o_mini_prompt_path
from utils.token_counter import TokenCounter


class GPT4Module:
    def __init__(self):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.conf = Config().config
        self.model = self.conf["model"]["gpt"]["name"]

    def generate_daily_report(self, system_prompt, markdown_content):
        logger = LogManager().logger
        prompt = f"{markdown_content}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        logger.debug(f"message costs tokens: {TokenCounter().count_message_tokens(messages)}")
        if not self.conf["dry_run"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            logger.debug(response)
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
