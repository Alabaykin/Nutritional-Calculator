# Кроссплатформенное определение папки бинарников локального виртуального окружения
ifeq ($(OS),Windows_NT)
    VENV_BIN = .venv/Scripts
else
    VENV_BIN = .venv/bin
endif

.PHONY: help setup run test coverage build-lib install-lib-local docs compose-up compose-down check clean

.DEFAULT_GOAL := help