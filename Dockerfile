FROM python:3.12-slim

WORKDIR /code

COPY . /code/

RUN  apt update && apt install -y --no-install-recommends build-essential git gcc

RUN pip install -r /code/requirements.txt

RUN poetry build --format=wheel --no-interaction --no-ansi

RUN pip install /code/dist/*.whl

RUN huggingface-cli download colbert-ir/colbertv2.0

CMD  ["fastapi", "run", "src/edge_ai/main.py", "--port", "80"]
