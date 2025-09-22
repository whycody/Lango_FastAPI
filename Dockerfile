FROM python:3.10-slim AS builder

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN pip install --no-cache-dir poetry

RUN pip install watchgod

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

RUN python -m spacy download en_core_web_sm \
    && python -m spacy download es_core_news_sm \
    && python -m spacy download it_core_news_sm


FROM python:3.10-slim AS runtime

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app/src"]