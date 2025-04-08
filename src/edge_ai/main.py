import json
import os
import tomllib

from datetime import datetime, UTC
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Template
from pydantic import BaseModel


from edge_ai.inventory.router import router as inventory_router


with (Path(__file__).parents[2] / "pyproject.toml").open("rb") as fo:
    pyproject = tomllib.load(fo)


class Project(BaseModel):
    toml: dict = pyproject

    @property
    def description(self):
        return self.toml["project"]["description"]

    @property
    def name(self):
        return self.toml["project"]["name"]

    @property
    def version(self):
        return self.toml["project"]["version"]


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

# chatgpt = OpenAI(model="gpt-3.5-turbo")


@app.post("/conversation")
async def conversation(prompt: str):
    return {"message": "Not implemented"}


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
            "exec": "uv run fastapi dev src/edge_ai/main.py"
          }
}"""
    ).render(
        project=project,
        handlers=[
            {
                "methods": ["POST"],
                "pathPattern": "/inventory/instance/generate",
                "permissionsRequired": ["edge-ai.post.generate"],
            },
            {
                "methods": ["POST"],
                "pathPattern": "/inventory/instance/generate_from_image",
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
            "gateway_url": os.environ.get("GATEWAY_URL"),
            "tenant": os.environ.get("TENANT_ID"),
            "user": os.environ.get("ADMIN_USER"),
        },
        "date": datetime.now(UTC),
        "models": {},
    }
