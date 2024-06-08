import json
import tomllib

from datetime import datetime
from pathlib import Path
from typing import Annotated, Union

from fastapi import FastAPI, Body
from jinja2 import Template
from pydantic import BaseModel

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from langserve import add_routes


with (Path(__file__).parents[2] / "pyproject.toml").open('rb') as fo:
        pyproject = tomllib.load(fo)

class Project(BaseModel):
    toml: dict = pyproject
     
    @property
    def description(self):
        return self.toml['tool']['poetry']['description']
    

    @property
    def name(self):
          return self.toml['tool']['poetry']['name']
     
    @property
    def version(self):
          return self.toml['tool']['poetry']['version']

project = Project()

app = FastAPI(
     title=project.name,
     version=project.version,
     description=project.description
)

# add_routes(
#      app,
#      ChatOpenAI(model="gpt-3.5-turbo-0125"),
#      path="/openai"
# )

# add_routes(
#      app,
#      ChatAnthropic(model="claude-3-haiku-20240307"),
#      path="/anthropic"
# )


class QueryData(BaseModel):
    prompt: str
    model: str


@app.post("/conversation")
async def conversation(prompt: str):
     pass

@app.get("/moduleDescriptor.json")
async def moduleDescriptor():
    module_descriptor = Template("""{
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
}""").render(project=project, handlers=['"query"', '"conversation"'])
    return json.loads(module_descriptor)

@app.get("/")
async def about():
    return {
        "name": project.name,
        "version": project.version
    }
