from enum import Enum

class LargeLanguageModels(str, Enum):
    chatgpt = "ChatGPT"
    claude = "Claude"
    gemini = "Gemini"
    llama = "Llama"
