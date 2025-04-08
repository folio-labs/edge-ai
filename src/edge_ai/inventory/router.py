import logging
import os

from typing import Union
from uuid import uuid4

import httpx

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from pydantic_ai import BinaryContent

from edge_ai.inventory.agents.instance import (
    Dependencies as InstanceDependencies, 
    agent as instance_agent
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


async def _trigger_instance_generation(instance: Union[str,dict], job_id: str) -> str:
    async with httpx.AsyncClient(
        auth=httpx.BasicAuth(
            username=airflow["user"], password=airflow["password"]
        )
    ) as client:
        result = client.post(
            f"""{airflow["host"]}:{airflow["port"]}/api/v1/dags/instance_generation/dagRuns""",
            json={
                "conf": {"instance": instance, "jobId": job_id},
            },
        )
        result.raise_for_status()
        dag_run_id = result.json().get("dag_run_id")
    return dag_run_id


@router.post("/inventory/{type_of}/generate")
async def generate_inventory_record(type_of: str, prompt: PromptGeneration):
    job_id = str(uuid4())
    jobs[job_id] = "started"
    response = {"job_id": job_id}

    match type_of:

        case "instance":
            result = await instance_agent.run(prompt.text, deps=InstanceDependencies())

            response["dag_run_id"] = await _trigger_instance_generation(
                result.data.record, 
                job_id
            )

        case _:
            jobs.pop(job_id)
            response = {"error": f"{type_of} not supported or unknown to FOLIO"}

    return response


@router.post("/inventory/{type_of}/generate_from_image")
async def generate_instance_from_image(type_of: str, image: UploadFile = File(...)):
    raw_image = image.file.read()
    job_id = str(uuid4())
    jobs[job_id] = "started"
    response = {"job_id": job_id }

    match type_of:
        case "instance":
            result = await instance_agent.run(
                [BinaryContent(data=raw_image, media_type=image.content_type)],
                deps=InstanceDependencies(type_of="image_upload")
            )

            response["dag_run_id"] = await _trigger_instance_generation(
                result.data.record, 
                job_id
            )

        case _:
            jobs.pop(job_id)
            response = {"error": f"{type_of} not supported or unknown to FOLIO"}

    return response