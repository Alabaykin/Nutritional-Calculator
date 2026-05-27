# Кроссплатформенное определение папки бинарников локального виртуального окружения
ifeq ($(OS),Windows_NT)
    VENV_BIN = .venv/Scripts
else
    VENV_BIN = .venv/bin
endif

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

setup:
	python -m poetry install

run:
	$(VENV_BIN)/uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

test:
	$(VENV_BIN)/pytest

coverage:
	@echo "Coverage tool is disabled"

build-lib:
	cd packages/recipe_core && python -m poetry build

install-lib-local:
	python -m poetry install

docs:
	$(VENV_BIN)/sphinx-apidoc -f -o docs/source/api packages/recipe_core/src/recipe_core
	cd docs && $(VENV_BIN)/sphinx-build -b html source _build/html

compose-up:
	docker compose -f infra/compose.yaml up --build -d
