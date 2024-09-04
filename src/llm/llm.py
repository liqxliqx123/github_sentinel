from config import Config
from llm.gemma2 import Gemma2Model
from llm.gpt4 import GPT4Module
from llm.zhipu import ZhipuAIModule

from const import LLMModuleType


class LLM:
    def __init__(self):
        conf = Config().config
        model_key = conf["model_key"]
        if model_key == LLMModuleType.GPT.value:
            self._model = GPT4Module()
        elif model_key == LLMModuleType.OLLAMA.value:
            self._model = Gemma2Model()
        elif model_key == LLMModuleType.GLM.value:
            self._model = ZhipuAIModule()
        else:
            raise ValueError("Invalid model key")

    @property
    def model(self):
        return self._model
