from enum import Enum


class LLMModuleType(Enum):
    GPT = "gpt"
    GLM = "glm"
    OLLAMA = "ollama"
