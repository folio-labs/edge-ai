import json
import logging
import os


from fastapi import APIRouter, File, UploadFile
from folioclient import FolioClient

from pydantic import BaseModel
from pydantic_ai import BinaryContent

from edge_ai.utils.messages import filter_messages
from edge_ai.inventory.agents.instance import (
    Dependencies as InstanceDependencies,
    agent as instance_agent,
    AIModelInfo,
)


logger = logging.getLogger(__name__)

folio_client = FolioClient(
    os.environ.get("GATEWAY_URL"),
    os.environ.get("TENANT_ID"),
    os.environ.get("ADMIN_USER"),
    os.environ.get("ADMIN_PASSWORD"),
)

router = APIRouter()


class PromptGeneration(BaseModel):
    text: str
    model: str = "openai"


def _set_model(model_name: str):
    model = None
    api_key = os.environ.get("PROVIDER_API_KEY")
    provider_url = os.environ.get("PROVIDER_URL")

    match model_name.lower():
        case "openai":
            from pydantic_ai.models.openai import OpenAIChatModel
            from pydantic_ai.providers.openai import OpenAIProvider

            if provider_url is None:
                provider = OpenAIProvider(api_key=api_key)
            else:
                # For external services that provide OpenAI API compatiblity
                provider = OpenAIProvider(base_url=provider_url, api_key=api_key)

            model = OpenAIChatModel("gpt-4o", provider=provider)

    return model


@router.post("/inventory/{type_of}/generate", operation_id="make_inventory_record")
async def generate_inventory_record(type_of: str, prompt: PromptGeneration):
    response = {}
    match type_of:
        case "instance":
            instance_agent.model = _set_model(prompt.model)
            try:
                result = await instance_agent.run(
                    prompt.text, deps=InstanceDependencies()
                )
                response["record"] = json.loads(result.output.record)
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


@router.post(
    "/inventory/{type_of}/generate_from_image", operation_id="make_record_from_image"
)
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
                response["record"] = json.loads(result.output.record)
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
