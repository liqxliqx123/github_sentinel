import os
from openai import OpenAI
from config import Config


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
        prompt = f"{markdown_content}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        return response.choices[0].message.content
