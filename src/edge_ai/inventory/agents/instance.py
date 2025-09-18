"""AI Agent for generating FOLIO Inventory Instance records from text or image upload"""

import logging
import os

from dataclasses import dataclass
from typing import Optional, Union


from folioclient import FolioClient
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


logger = logging.getLogger(__name__)


folio_client = None

def _folio_client():
    global folio_client

    if not folio_client:
        folio_client = FolioClient(
            os.environ.get("GATEWAY_URL"),
            os.environ.get("TENANT_ID"),
            os.environ.get("ADMIN_USER"),
            os.environ.get("ADMIN_PASSWORD"),
        )
    return folio_client


class AIModelInfo(BaseModel):
    model_name: str
    messages: list


class FOLIOInstance(BaseModel):
    model_info: AIModelInfo
    record: Union[str, dict]


@dataclass
class Dependencies:
    type_of: Optional[str] = None
    examples: str = "".join(
        [
            "Question: Parable of the Sower by Octiva Butler, published in 1993 by Four Walls Eight Windows in New York\n\n",
            'Answer: {"title": "Parable of the Sower", "source": "AIModel", "instanceTypeId": "text", ',
            '        "contributors": [{"name": "Octiva Butler", "contributorNameTypeId": "Personal name", "contributorTypeId": "Author"}], ',
            '        "publication": [{"publisher": "Four Walls Eight Windows", "dateOfPublication": "1993", "place": "New York"}] }}"""',
        ]
    )


agent = Agent(deps_type=Dependencies, output_type=FOLIOInstance, retries=3)


@agent.tool(retries=3)
async def retrieve_reference_data(
    ctx: RunContext[str], lookup_type: str, value: str
) -> str:
    """Retrieve reference data from FOLIO Inventory API based on lookup type and value."""
    folio_client = _folio_client()
    uuid = ""
    match lookup_type:
        case "contributorNameTypeId":
            for row in folio_client.contrib_name_types:
                if row["name"] == value:
                    uuid = row["id"]

        case "contributorTypeId":
            for row in folio_client.contributor_types:
                if row["name"] == value:
                    uuid = row["id"]

        case "instanceTypeId":
            for row in folio_client.instance_types:
                if row["name"] == value:
                    uuid = row["id"]
    return uuid


# @agent.tool
# async def new_folio_instance(ctx: RunContext[str], record: Union[dict,str]) -> dict:
#     """Post a new FOLIO Inventory Instance record."""
#     post_result = folio_client.folio_post("/inventory/instances", payload=record)
#     return post_result.json()


@agent.system_prompt
async def expert_cataloger(ctx: RunContext[str]):
    """System prompt for the AI Inventory Instance agent."""
    prompt = """You are an expert cataloger. Please be accurate as possible and not hallucinate
    any extra fields when cataloging material.\n\n"""

    match ctx.deps.type_of:
        case "image_upload":
            prompt += (
                """Given an image, construct a FOLIO Inventory Instance record.\n"""
            )

        case _:
            prompt += (
                """Given a sentence, construct a FOLIO Inventory Instance record.\n"""
            )

    prompt += f"""Use the `retrieve_reference_data` function to determine the id for contributorTypeId,
    contributorTypeId, contributorNameTypeId, and instanceTypeId from the values in those fields.\n\n
    
    Here are some examples:
    {ctx.deps.examples}"""
    return prompt
