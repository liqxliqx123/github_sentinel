import json

class Config:
    @staticmethod
    def load(config_file="config.json"):
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config

    @staticmethod
    def save(config, config_file="config.json"):
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
