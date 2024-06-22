import json
import os
import tomllib

from datetime import datetime, UTC
from pathlib import Path
from typing import Annotated, Union

import dspy
import httpx

from dspy import configure, ChainOfThought, OpenAI, Predict
from fastapi import FastAPI, Body, HTTPException, Response
from folioclient import FolioClient
from jinja2 import Template
from pydantic import BaseModel


from edge_ai.inventory import rag
from edge_ai.inventory.signatures.holdings import CheckHoldings
from edge_ai.inventory.signatures.instance import CheckInstance
from edge_ai.inventory.signatures.items import CheckItem

with (Path(__file__).parents[2] / "pyproject.toml").open("rb") as fo:
    pyproject = tomllib.load(fo)


class Project(BaseModel):
    toml: dict = pyproject

    @property
    def description(self):
        return self.toml["tool"]["poetry"]["description"]

    @property
    def name(self):
        return self.toml["tool"]["poetry"]["name"]

    @property
    def version(self):
        return self.toml["tool"]["poetry"]["version"]


project = Project()

app = FastAPI(
    title=project.name, version=project.version, description=project.description
)

chatgpt = OpenAI(model="gpt-3.5-turbo")

folio_client = FolioClient(
    os.environ.get("OKAPI_URL"),
    os.environ.get("TENANT_ID"),
    os.environ.get("ADMIN_USER"),
    os.environ.get("ADMIN_PASSWORD"),
)

@app.post("/inventory/{type_of}/check")
async def check_inventory_record(type_of: str, text: str, uuid: str):

    match type_of:

        case "holdings":
            try:
                holdings = folio_client.folio_get(f"/inventory-storage/holdings/{uuid}")

            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"holdings {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                cot = ChainOfThought(CheckHoldings)
                predication = cot(holdings=holdings, text=text)

        case "instance":
            try:
                instance = folio_client.folio_get(f"/inventory/instances/{uuid}")
            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"instance {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                cot = ChainOfThought(CheckInstance)
                predication = cot(context=json.dumps(instance), instance=text)
                return predication

        case "item":
            try:
                item = folio_client.folio_get(f"/inventory/items/{uuid}")
            except httpx.HTTPStatusError as e:
                if "404 Not Found" in e.args[0]:
                    raise HTTPException(
                        status_code=404, detail=f"item {uuid} not Found"
                    )

            with dspy.context(lm=chatgpt):
                cot = ChainOfThought(CheckItem)
                predication = cot(item=item, text=text)

        case _:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown inventory record: {type_of} with {uuid} not found",
            )

    return {"rationale": predication.rationale, "verifies": predication.verifies}


@app.post("/conversation")
async def conversation(prompt: str):
    pass


@app.get("/moduleDescriptor.json")
async def moduleDescriptor():
    module_descriptor = Template(
        """{
          "id": "{{project.name}}-{{project.version}}",
          "name": "{{project.name}}",
          "provides": [
             {
              "id": "{{project.name|title }}",
              "version": "{{ project.version }}",
              "handlers": [
                {% for handler in handlers %}
                {{ handler }}
                {% if not loop.last %},{% endif %}
                {% endfor %}
              ]
            }
          ],
          "requires": [],
          "launchDescriptor": {
            "exec": "poetry run fastapi dev src/edge_ai/main.py"
          }
}"""
    ).render(project=project, handlers=['"query"', '"conversation"'])
    return json.loads(module_descriptor)


@app.get("/")
async def about():
    return {
        "name": project.name, 
        "version": project.version,
        "folio": {
            "okapi_url": os.environ.get("OKAPI_URL"),
            "tenant": os.environ.get("TENANT_ID"),
            "user": os.environ.get("ADMIN_USER"),
        },
        "date": datetime.now(UTC),
        "models": {
            "chatgpt": chatgpt.kwargs["model"]
        }
    }