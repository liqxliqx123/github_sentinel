import os
from openai import OpenAI
from src.config import Config
from src.utils.logger import LogManager
from src.utils.path import get_prompt_path
from src.utils.token_counter import TokenCounter


class LLMModule:
    def __init__(self):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        file_path = os.path.join(get_prompt_path(), "system_prompt.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        self.conf = Config().config
        self.model = self.conf["model_name"]

    def generate_daily_report(self, markdown_content):
        logger = LogManager().logger
        prompt = f"{markdown_content}"
        messages = [
            {"role": "system", "content": self.system_prompt},
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
        return None
