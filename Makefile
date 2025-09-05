SHELL := /bin/bash
PORT ?= 8000

.PHONY: install dev start lint fmt build render-start

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run --port $(PORT)

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run ruff check .

fmt:
	uv run ruff format .

build:
	bash ./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

