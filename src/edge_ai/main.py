import json
import os
import tomllib

from datetime import datetime, UTC
from pathlib import Path

from dspy import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from folioclient import FolioClient
from jinja2 import Template
from pydantic import BaseModel


from edge_ai.inventory.router import router as inventory_router


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router)

chatgpt = OpenAI(model="gpt-3.5-turbo")

folio_client = FolioClient(
    os.environ.get("OKAPI_URL"),
    os.environ.get("TENANT_ID"),
    os.environ.get("ADMIN_USER"),
    os.environ.get("ADMIN_PASSWORD"),
)


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
    ).render(
        project=project,
        handlers=[
            {
                "methods": ["POST"],
                "pathPattern": "/inventory/holdings/similiarity",
                "permissionsRequired": ["edge-ai.post.similiarity"],
            },
            {
                "methods": ["POST"],
                "pathPattern": "/inventory/instance/similiarity",
                "permissionsRequired": ["edge-ai.post.similiarity"],
            },
            {
                "methods": ["POST"],
                "pathPattern": "/inventory/item/similiarity",
                "permissionsRequired": ["edge-ai.post.similiarity"],
            },
        ],
    )
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
        "models": {"chatgpt": chatgpt.kwargs["model"]},
    }
