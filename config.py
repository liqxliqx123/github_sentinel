import json
import os

global_config = {}


class Config:

    @staticmethod
    def get_config():
        global global_config
        return global_config

    @staticmethod
    def load(config_file="config.json"):
        with open(config_file, 'r') as file:
            config = json.load(file)

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise Exception(
                "No GitHub token found. Please set the GITHUB_TOKEN environment variable or provide it in the config file.")

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception(
                "No OpenAI API key found. Please set the OPENAI_API_KEY environment variable or provide it in the config file.")
        config['github_token'] = token
        global global_config
        global_config = config

    @staticmethod
    def save(config, config_file="config.json"):
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
