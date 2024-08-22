FROM python:3.12-slim

WORKDIR /code

COPY . /code/

RUN pip install -r /code/requirements.txt

RUN poetry build --format=wheel --no-interaction --no-ansi

RUN pip install /code/dist/*.whl

CMD  ["fastapi", "run", "src/edge_ai/main.py", "--port", "80"]
