import logging
import os

from dataclasses import dataclass
from typing import Optional, Union


from folioclient import FolioClient
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


logger = logging.getLogger(__name__)

class FOLIOInstance(BaseModel):
    record: Union[str,dict]


@dataclass
class Dependencies:
    type_of: Optional[str] = None
    examples: str = ''.join([
        'Question: Parable of the Sower by Octiva Butler, published in 1993 by Four Walls Eight Windows in New York\n\n',
        'Answer: {"title": "Parable of the Sower", "source": "AIModel", "instanceTypeText": "text", ',
        '        "contributors": [{"name": "Octiva Butler", "contributorTypeText": "Author"}], ',
        '        "publication": [{"publisher": "Four Walls Eight Windows", "dateOfPublication": "1993", "place": "New York"}] }}"""'
    ])


agent = Agent(deps_type=Dependencies, result_type=FOLIOInstance)


@agent.tool
async def retrieve_reference_data(ctx: RunContext[str], lookup_type: str, value: str) -> str:
    folio_client = FolioClient(
        os.environ.get("GATEWAY_URL"),
        os.environ.get("TENANT_ID"),
        os.environ.get("ADMIN_USER"),
        os.environ.get("ADMIN_PASSWORD"),
    )
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

@agent.tool
async def new_folio_instance(ctx: RunContext[str], record: dict) -> dict:
    folio_client = FolioClient(
        os.environ.get("GATEWAY_URL"),
        os.environ.get("TENANT_ID"),
        os.environ.get("ADMIN_USER"),
        os.environ.get("ADMIN_PASSWORD"),
    )
    post_result = folio_client.folio_post("/inventory/instances",
                                          payload=record)
    post_result.rasie_for_status()
    return post_result.json()


@agent.system_prompt
async def expert_cataloger(ctx: RunContext[str]):
    prompt = """You are an expert cataloger. Please be accurate as possible and not hallucinate
    any extra fields when cataloging material.\n\n"""

    match ctx.deps.type_of:
        case "image_upload":
            prompt += """Given an image, construct a FOLIO Inventory Instance record.\n"""

        case _:
            prompt += """Given a sentence, construct a FOLIO Inventory Instance record.\n"""

    prompt += f"""Use the `retrieve_reference_data` function to determine the id for contributorTypeId,
    Use the `retrieve_reference_data` function to determine the id for contributorTypeId,
    contributorNameTypeId, and instanceTypeId. After creating an instance record, use the 
    `new_folio_instance` function to post the record to the FOLIO Inventory API.\n\n
    
    Here are some examples:
    {ctx.deps.examples}"""
    return prompt
