import os
from openai import OpenAI
from src.config import Config
from utils.logger import LogManager
from utils.token_counter import TokenCounter


class LLMModule:
    def __init__(self):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        with open("prompt/system_prompt.txt", "r") as f:
            self.system_prompt = f.read()
        conf = Config.get_config()
        self.model = conf["model_name"]

    def generate_daily_report(self, markdown_content):
        conf = Config.get_config()
        logger = LogManager.get_logger()
        prompt = f"{markdown_content}"
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        logger.debug(f"message costs tokens: {TokenCounter().count_message_tokens(messages)}")
        if not conf["dry_run"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            logger.debug(response)
            return response.choices[0].message.content
        return None
