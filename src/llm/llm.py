from config import Config
from llm.gemma2 import Gemma2Model
from llm.gpt4 import GPT4Module


class LLM:
    def __init__(self):
        conf = Config().config
        model_name = conf["model_name"]
        if model_name == "gpt_4o_mini":
            self._model = GPT4Module()
        elif model_name == "gemma2":
            self._model = Gemma2Model()

    @property
    def model(self):
        return self._model
