VENV = .venv

ifeq ($(OS),Windows_NT)
    VENV_BIN = $(VENV)/Scripts
    PYTHON_SYS = python
else
    VENV_BIN = $(VENV)/bin
    PYTHON_SYS = python3
endif

PYTHON = $(VENV_BIN)/python
PIP = $(VENV_BIN)/pip
POETRY = $(VENV_BIN)/poetry

.PHONY: help setup run test coverage build-lib install-lib-local docs compose-up compose-down check clean

.DEFAULT_GOAL := help

help:
	@echo "Доступные команды:"
	@echo "  setup              Подготовить виртуальное окружение и установить зависимости"
	@echo "  run                Запустить сервер API"
	@echo "  test               Запустить тесты"
	@echo "  coverage           Запустить тесты с отчетом покрытия"
	@echo "  build-lib          Собрать wheel-пакет библиотеки recipe_core"
	@echo "  install-lib-local  Переустановить локальную библиотеку recipe_core"
	@echo "  docs               Сгенерировать HTML-документацию Sphinx"
	@echo "  compose-up         Запустить контейнеры приложения и БД в Docker"
	@echo "  compose-down       Остановить контейнеры Docker"
	@echo "  check              Запустить полную проверку (тесты, сборка либы, сборка доков)"
	@echo "  clean              Очистить кэши и временные файлы"

$(VENV):
	$(PYTHON_SYS) -m venv $(VENV)
	$(VENV_BIN)/pip install poetry

setup: $(VENV)
	$(POETRY) install

run: setup
	$(VENV_BIN)/uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

test: setup
	$(VENV_BIN)/pytest

coverage:
	@echo "Coverage tool is disabled"

build-lib: setup
	cd packages/recipe_core && ../../$(POETRY) build

install-lib-local: setup
	$(POETRY) install

docs: setup
	$(VENV_BIN)/sphinx-apidoc -f -o docs/source/api packages/recipe_core/src/recipe_core
	cd docs && ../$(VENV_BIN)/sphinx-build -b html source _build/html

compose-up:
	docker compose -f infra/compose.yaml up --build -d

compose-down:
	docker compose -f infra/compose.yaml down -v

check: test build-lib docs
	@echo "All checks passed successfully!"

clean:
	rm -rf $(VENV) .pytest_cache .coverage htmlcov docs/build build dist packages/recipe_core/dist packages/recipe_core/build docs/_build
