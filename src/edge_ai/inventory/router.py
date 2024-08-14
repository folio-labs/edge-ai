import json
import os

import dspy
import httpx

from dspy import ChainOfThought, OpenAI
from fastapi import APIRouter, HTTPException
from folioclient import FolioClient
from pydantic import BaseModel

from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import (
    InstancePromptGeneration,
    InstanceSimilarity,
)
from edge_ai.inventory.signatures.item import ItemSimilarity

router = APIRouter()

folio_client = FolioClient(
    os.environ.get("OKAPI_URL"),
    os.environ.get("TENANT_ID"),
    os.environ.get("ADMIN_USER"),
    os.environ.get("ADMIN_PASSWORD"),
)

chatgpt = OpenAI(model="gpt-3.5-turbo")


class SimilarityBody(BaseModel):
    text: dict
    uuid: str | None = None


class PromptGeneration(BaseModel):
    text: str


@router.post("/inventory/{type_of}/generate")
async def generate_inventory_record(type_of: str, prompt: PromptGeneration):

    match type_of:

        case "instance":
            with dspy.context(lm=chatgpt):
                cot = ChainOfThought(InstancePromptGeneration)
                predication = cot(prompt=prompt.text)
    return {"rationale": predication.rationale, "instance": predication.instance}


@router.post("/inventory/{type_of}/similarity")
async def check_inventory_record(type_of: str, similarity: SimilarityBody):
    text = json.dumps(similarity.text)
    uuid = similarity.uuid

    match type_of:

        case "holdings":
            try:
                if uuid:
                    holdings = folio_client.folio_get(
                        f"/holdings-storage/holdings/{uuid}"
                    )
                else:
                    # Use RAG module
                    holdings = []

            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"holdings {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                if uuid:
                    cot = ChainOfThought(HoldingsSimilarity)
                    predication = cot(context=json.dumps(holdings), holdings=text)
                # else: Holdings RAG

        case "instance":
            try:
                if uuid:
                    instance = folio_client.folio_get(f"/inventory/instances/{uuid}")
                else:
                    instance = []

            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"instance {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                if uuid:
                    cot = ChainOfThought(InstanceSimilarity)
                    predication = cot(context=json.dumps(instance), instance=text)
                # else: Instance RAG

        case "item":
            try:
                if uuid:
                    item = folio_client.folio_get(f"/item-storage/items/{uuid}")
                else:
                    item = []

            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"item {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                if uuid:
                    cot = ChainOfThought(ItemSimilarity)
                    predication = cot(item=item, text=text)
                # else: Item RAG

        case _:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown inventory record: {type_of} with {uuid} not found",
            )

    return {"rationale": predication.rationale, "verifies": predication.verifies}
