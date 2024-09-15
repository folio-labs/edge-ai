import asyncio
import json
import logging
import os
import pathlib

from http import HTTPStatus
from typing import Dict
from uuid import UUID, uuid4

import dspy
import httpx

from dsp import Claude
from dspy import ChainOfThought, OpenAI
from fastapi import APIRouter, BackgroundTasks, HTTPException
from folioclient import FolioClient
from pydantic import BaseModel

from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import (
    InstancePromptGeneration,
    InstanceSimilarity,
)
from edge_ai.inventory.signatures.item import ItemSimilarity
from edge_ai.inventory.rag import (
    Instances as InstancesRAG,
    new_rag_index,
    update_rag_index,
)

logger = logging.getLogger(__name__)

router = APIRouter()

folio_client = FolioClient(
    os.environ.get("OKAPI_URL"),
    os.environ.get("TENANT_ID"),
    os.environ.get("ADMIN_USER"),
    os.environ.get("ADMIN_PASSWORD"),
)

# Defaults are when running AI Workflows Airflow locally
airflow = {
    "host": os.environ.get("AIRFLOW_HOST", "http://localhost"),
    "port": os.environ.get("AIRFLOW_PORT", 8080),
    "user": os.environ.get("AIRFLOW_USER", "airflow"),
    "password": os.environ.get("AIRFLOW_PASSWORD", "airflow"),
}

chatgpt = OpenAI(model=os.environ.get("OPENAI_MODEL"))
claude = Claude()
try:
    instance_rag = InstancesRAG(index_root=".ragatouille/colbert/indexes")
except FileNotFoundError as e:
    logger.info(f"No Instance Index Exists")


class PromptGeneration(BaseModel):
    text: str


class SimilarityBody(BaseModel):
    text: dict
    uuid: str | None = None


class RAGIndexerBody(BaseModel):
    source: str


@router.post("/inventory/{type_of}/generate")
async def generate_inventory_record(type_of: str, prompt: PromptGeneration):

    match type_of:

        case "instance":
            with dspy.context(lm=chatgpt):
                cot = ChainOfThought(InstancePromptGeneration)
                predication = cot(prompt=prompt.text)
    return {"rationale": predication.rationale, "instance": predication.instance}


@router.post("/inventory/{type_of}/index", status_code=HTTPStatus.ACCEPTED)
async def index_inventory_records(
    type_of: str, records_file: RAGIndexerBody, background_tasks: BackgroundTasks
):

    records_path = pathlib.Path(records_file.source)

    with records_path.open() as fo:
        records = [json.loads(line) for line in fo.readlines()]

    index_name = f"{type_of.capitalize()}s"

    index_path = pathlib.Path(f".ragatouille/colbert/indexes/{index_name}")

    if index_path.exists():
        msg = f"Updating existing {index_path} with {len(records):,} records"
        background_tasks.add_task(
            update_rag_index, records=records, index_path=str(index_path.absolute())
        )
    else:
        msg = f"Creating new index for {len(records)} records"
        background_tasks.add_task(new_rag_index, records=records, index_name=index_name)
    logger.info(msg)

    return {"message": msg}


@router.post("/inventory/{type_of}/index/start")
async def start_instance_embedding_dag(type_of: str, limit: int, offset: int):

    match type_of:

        case "instance":
            dag_run_url = f"""{airflow["host"]}:{airflow["port"]}/api/v1/dags/instance_embedding/dagRuns"""

        case _:
            msg = f"{type_of} not implemented for starting RAG DAG run"
            logger.info(msg)
            return {"message": msg}

    async with httpx.AsyncClient(
        auth=httpx.BasicAuth(username=airflow["user"], password=airflow["password"])
    ) as client:
        result = await client.post(
            dag_run_url,
            json={
                "conf": {"limit": limit, "offset": offset},
            },
        )

        return result.json()


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
                else:
                    predication = instance_rag.forward(
                        operation="verify", instance=text
                    )

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
