from typing import Annotated

from fastapi import FastAPI, Body
from llms.base import LargeLanguageModels


app = FastAPI()


@app.get("/llms/{model_name}")
async def llm_models(model_name: LargeLanguageModels):
    match model_name:

        case LargeLanguageModels.chatgpt:
            return { "model_name": model_name, "description": "OpenAI's ChatGPT" }

        case LargeLanguageModels.claude:
            return { "model_name": model_name, "description": "Anthropic's Claude" }

        case LargeLanguageModels.gemini:
            return { "model_name": model_name, "description": "Google's Gemini" }

        case LargeLanguageModels.llama:
            return { "model_name": model_name, "description": "Meta's Llama" }

@app.post("/llms/{model_name}/query")
async def llm_query(model_name: LargeLanguageModels, query: Annotated[str, Body()]):
    return { "model_name": model_name, "query": query }

@app.get("/")
async def about():
    return { "about": "Edge AI for FOLIO" }
