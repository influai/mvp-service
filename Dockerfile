FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY . /app/

RUN poetry install

EXPOSE 8000

ARG DATABASE_URL
ARG RANK_MODEL_PATH

ENV DATABASE_URL=${DATABASE_URL}
ENV RANK_MODEL_PATH=${RANK_MODEL_PATH}

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]