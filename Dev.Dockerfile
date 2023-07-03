ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

WORKDIR /uploader

RUN pip install --upgrade --no-cache pip
RUN pip install poetry

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry export -f requirements.txt --output ./requirements.txt --without-hashes
RUN pip install --no-cache -r ./requirements.txt

ENTRYPOINT uvicorn file_uploader.main:app --host 0.0.0.0 --port 3457 --reload