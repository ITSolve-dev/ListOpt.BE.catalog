FROM python:3.13.1-slim AS builder

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN pip install 'poetry==2.1.4'

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-root --no-ansi --no-interaction \
    && pip cache purge \
    && rm -rf ~/.cache/pypoetry/{cache,artifacts}


FROM python:3.13.1-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv


ENV PATH=/app/.venv/bin:$PATH

COPY . /app
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--no-reload"]
