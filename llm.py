import os
from openai import OpenAI


class LLMModule:
    def __init__(self):
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def generate_daily_report(self, markdown_content):
        prompt = f"Please summarize the following project updates into a formal daily report:\n\n{markdown_content}"
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        return response.choices[0].message.content
