# Minimal makefile for Sphinx documentation
#

# Кроссплатформенное определение папки бинарников виртуального окружения
ifeq ($(OS),Windows_NT)
    VENV_BIN = ../.venv/Scripts
else
    VENV_BIN = ../.venv/bin
endif

SPHINXOPTS    ?=
SPHINXBUILD   ?= $(VENV_BIN)/sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
