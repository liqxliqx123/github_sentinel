import json
import os

from src.utils.path import get_settings_json_path


def save(config, config_file="settings.json"):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)


class Config:
    _global_config = None

    def __init__(self):

        if Config._global_config:
            self.config = Config._global_config
            return

        file_path = get_settings_json_path()
        with open(file_path, 'r') as file:
            config = json.load(file)

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise Exception(
                "No GitHub token found. Please set the GITHUB_TOKEN environment variable or provide it in the config file.")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception(
                "No OpenAI API key found. Please set the OPENAI_API_KEY environment variable or provide it in the config file.")

        mail_password = os.getenv("EMAIL_PASSWORD")
        if not mail_password:
            raise Exception(
                "No EMAIL password found. Please set the MAIL_POP3_PASSWORD environment variable or provide it in the config file.")

        config['github_token'] = token
        self.config = config
        Config._global_config = config
