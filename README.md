# edge-ai

## Local .env File
To run the Edge-AI module with its API, you'll need to create a local `.env` in
your local directory with the following values for the Generative AI services you
intend to use and the FOLIO environment (the example below uses the Bugfest
Quesnelia environment):

```
export ANTHROPIC_API_KEY={your-claude-ai-key}
export GOOGLE_API_KEY={google-gemini-key}
export OPENAI_API_KEY={your-openai-key}
export OPENAI_MODEL=gpt-3.5-turbo
export OKAPI_URL=https://okapi-bugfest-quesnelia.int.aws.folio.org
export TENANT_ID=fs09000000
export ADMIN_USER=folio
export ADMIN_PASSWORD=folio
```

## Developing
1. Install [poetry][poetry] 
1. Clone the repository `git clone --depth=5 https://github.com/folio-labs/edge-ai.git`
1. Change to the primary directory `cd edge-ai/` 
1. Run dependency installation `poetry install`
1. Source local environmental .env file `source .env`
1. Run fastapi in local dev mode `poetry run fastapi dev src/edge_ai/main.py`


## Running in a Docker container
To run the `edge-ai` in Docker, you'll need to adjust your `.env` file to follow the
Docker format of KEY=VALUE like:

```
ANTHROPIC_API_KEY={your-claude-ai-key}
GOOGLE_API_KEY={google-gemini-key}
OKAPI_URL=https://okapi-bugfest-quesnelia.int.aws.folio.org
TENANT_ID=fs09000000
ADMIN_USER=folio
ADMIN_PASSWORD=folio
```

Then to run use the `--env-file` parameter along with the `--expose` the API port 80 and then to 
allow the docker host to connect to the container on the host's port 8004 (or another host port) use
the `-p 8004:80` parameter:

`docker run --env-file .env --expose 80 -p 8004:80 folio-labs/edge-ai:latest`

[poetry]: https://python-poetry.org/
