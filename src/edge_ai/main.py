import json
import os
import tomllib

from datetime import datetime, UTC
from pathlib import Path
from typing import Union

import dspy
import httpx

from dspy import ChainOfThought, OpenAI
from fastapi import FastAPI, HTTPException
from folioclient import FolioClient
from jinja2 import Template
from pydantic import BaseModel


from edge_ai.inventory.signatures.holdings import HoldingsSimilarity
from edge_ai.inventory.signatures.instance import InstanceSimilarity
from edge_ai.inventory.signatures.item import ItemSimilarity

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

@app.post("/inventory/{type_of}/similarity")
async def check_inventory_record(type_of: str, text: str, uuid: Union[str, None]):

    match type_of:

        case "holdings":
            try:
                if uuid:
                    holdings = folio_client.folio_get(f"/holdings-storage/holdings/{uuid}")
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
                    predication = cot(holdings=holdings, text=text)
                #else: Holdings RAG

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
                #else: Instance RAG

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
                #else: Item RAG

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
                  {
                     "methods": [
                     {% for method in handler.methods %}
                       "{{ method }}"
                      {% if not loop.last %},{% endif %}
                      {% endfor %} 
                     ],
                     "pathPattern": "{{ handler.pathPattern }}",
                     "permissionsRequired": [
                      {% for permission in handler.permissionsRequired %}
                      "{{ permission }}"
                      {% if not loop.last %},{% endif %}
                      {% endfor %}
                     ]
                  }
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
    ).render(project=project, handlers=[
        {
            "methods": [
                "POST"
            ],
            "pathPattern": "/inventory/holdings/similiarity",
            "permissionsRequired": [
                "edge-ai.post.similiarity"
            ]
        },
        {
            "methods": [
                "POST"
            ],
            "pathPattern": "/inventory/instance/similiarity",
            "permissionsRequired": [
                "edge-ai.post.similiarity"
            ]
        },
        {
            "methods": [
                "POST"
            ],
            "pathPattern": "/inventory/item/similiarity",
            "permissionsRequired": [
                "edge-ai.post.similiarity"
            ]
        }
    ])
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
