# edge-ai

## Developing
1. Install [poetry][poetry] 
1. Clone the repository `git clone --depth=5 https://github.com/folio-labs/edge-ai.git`
1. Change to the primary directory `cd edge-ai/` 
1. Run dependency installation `poetry install`
1. Source local environmental .env file `source .env`
1. Run fastapi in local dev mode `poetry run fastapi src/edge_ai/main.py`

[poetry]: https://python-poetry.org/
