SHELL := /bin/bash
PORT ?= 8000

# Choose production server depending on OS
ifeq ($(OS),Windows_NT)
RENDER_CMD = uv run waitress-serve --host=0.0.0.0 --port=$(PORT) page_analyzer:app
else
RENDER_CMD = gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
endif

.PHONY: install dev start lint fmt build render-start

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run --port $(PORT)

start:
	$(RENDER_CMD)

lint:
	uv run ruff check .

fmt:
	uv run ruff format .

build:
	bash ./build.sh

render-start:
	$(RENDER_CMD)
