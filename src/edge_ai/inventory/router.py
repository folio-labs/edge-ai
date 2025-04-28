import json
import logging
import os

from typing import Union
from uuid import uuid4

import httpx

from fastapi import APIRouter, File, UploadFile, Response
from pydantic import BaseModel
from pydantic_ai import BinaryContent

from edge_ai.utils.messages import filter_messages
from edge_ai.inventory.agents.instance import (
    folio_client,
    Dependencies as InstanceDependencies,
    agent as instance_agent,
    AIModelInfo,
)


logger = logging.getLogger(__name__)

router = APIRouter()

# Defaults are when running AI Workflows Airflow locally
airflow = {
    "host": os.environ.get("AIRFLOW_HOST", "http://localhost"),
    "port": os.environ.get("AIRFLOW_PORT", 8080),
    "user": os.environ.get("AIRFLOW_USER", "airflow"),
    "password": os.environ.get("AIRFLOW_PASSWORD", "airflow"),
}


jobs: dict = {}


class PromptGeneration(BaseModel):
    text: str
    model: str = "openai"


def _set_model(model_name: str):
    model = None
    match model_name.lower():
        case "openai":
            from pydantic_ai.models.openai import OpenAIModel

            model = OpenAIModel("gpt-4o")

    return model


@router.post("/inventory/{type_of}/generate")
async def generate_inventory_record(type_of: str, prompt: PromptGeneration):
    response = {}
    match type_of:
        case "instance":
            instance_agent.model = _set_model(prompt.model)
            try:
                result = await instance_agent.run(
                    prompt.text, deps=InstanceDependencies()
                )
                response["record"] = json.loads(result.data.record)
                ai_model_info = AIModelInfo(
                    model_name=prompt.model,
                    usage=result.usage(),
                    messages=filter_messages(result.all_messages()),
                )
                response["usage"] = ai_model_info
                new_instance_result = folio_client.folio_post(
                    "/instance-storage/instances", payload=response["record"]
                )
                response["folio_response"] = new_instance_result
            except Exception as error:
                response["error"] = str(error)

        case _:
            response["error"] = f"{type_of} not supported or unknown to FOLIO"

    return response


@router.post("/inventory/{type_of}/generate_from_image")
async def generate_instance_from_image(type_of: str, image: UploadFile = File(...)):
    raw_image = image.file.read()
    response = {}
    match type_of:
        case "instance":
            # Hardcode the model for now
            model = "openai"
            instance_agent.model = _set_model(model)
            try:
                result = await instance_agent.run(
                    [BinaryContent(data=raw_image, media_type=image.content_type)],
                    deps=InstanceDependencies(type_of="image_upload"),
                )
                response["record"] = json.loads(result.data.record)
                ai_model_info = AIModelInfo(
                    model_name=model,
                    usage=result.usage(),
                    messages=filter_messages(result.all_messages()),
                )
                response["usage"] = ai_model_info
                new_instance_result = folio_client.folio_post(
                    "/instance-storage/instances", payload=response["record"]
                )
                response["folio_response"] = new_instance_result
            except Exception as error:
                response["error"] = str(error)

        case _:
            response["error"] = f"{type_of} not supported or unknown to FOLIO"

    return response
