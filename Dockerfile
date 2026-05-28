FROM python:3.11-slim AS builder

WORKDIR /build
ENV POETRY_HTTP_TIMEOUT=120
RUN pip install poetry

COPY packages/recipe_core/ /build/packages/recipe_core/
WORKDIR /build/packages/recipe_core
RUN poetry build -f wheel

FROM python:3.11-slim

WORKDIR /app
ENV POETRY_HTTP_TIMEOUT=120
RUN pip install poetry

COPY --from=builder /build/packages/recipe_core/dist/*.whl /app/
COPY pyproject.toml poetry.lock* README.md* /app/
COPY packages/recipe_core/ /app/packages/recipe_core/

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root --no-interaction --no-ansi

COPY app/ /app/app/
COPY sample_recipe.json /app/

EXPOSE 8000
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
