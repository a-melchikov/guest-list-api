FROM python:3.12-slim

ENV POETRY_VERSION=1.6.1

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
