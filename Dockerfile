FROM python:3.11-slim AS builder

WORKDIR /build
RUN pip install poetry

COPY packages/recipe_core/ /build/packages/recipe_core/
WORKDIR /build/packages/recipe_core
RUN poetry build -f wheel

FROM python:3.11-slim

WORKDIR /app
RUN pip install poetry

COPY --from=builder /build/packages/recipe_core/dist/*.whl /app/
COPY pyproject.toml poetry.lock* /app/
COPY packages/recipe_core/ /app/packages/recipe_core/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY app/ /app/app/
COPY sample_recipe.json /app/

EXPOSE 8000
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
