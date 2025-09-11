SHELL := /bin/bash
PORT ?= 8000

# Load .env if present (does not override env)
-include .env
export

# Cross-platform start command (Render/local)
ifeq ($(OS),Windows_NT)
RENDER_CMD = uv run waitress-serve --host=0.0.0.0 --port=$(PORT) page_analyzer:app
else
RENDER_CMD = gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
endif

.PHONY: install dev start lint fmt lint-imports fmt-imports build render-start record play upload db-init test-db-init db-reset-test

# Install dependencies
install:
	uv sync

# Dev server
dev:
	uv run flask --debug --app page_analyzer:app run --port $(PORT)

# Start production server locally
start:
	$(RENDER_CMD)

# Lint
lint:
	uv run ruff check .

# Format code
fmt:
	uv run ruff format .

# Imports check only (isort via ruff)
lint-imports:
	uv run ruff check --select I .

# Auto-fix imports (sort/group)
fmt-imports:
	uv run ruff check --select I --fix .

# Build assets/bundle
build:
	bash ./build.sh

# Start command for Render
render-start:
	$(RENDER_CMD)

# Asciinema helpers
record:
	asciinema rec page_analizer.cast
play:
	asciinema play page_analizer.cast
upload:
	asciinema upload page_analizer.cast

# Apply schema to DATABASE_URL
db-init:
	@test -n "$(DATABASE_URL)" || (echo "DATABASE_URL is not set" && exit 1)
	psql "$(DATABASE_URL)" -f database.sql

# Apply schema to TEST_DATABASE_URL
test-db-init:
	@test -n "$(TEST_DATABASE_URL)" || (echo "TEST_DATABASE_URL is not set" && exit 1)
	psql "$(TEST_DATABASE_URL)" -f database.sql

# Truncate test DB tables
db-reset-test:
	@test -n "$(TEST_DATABASE_URL)" || (echo "TEST_DATABASE_URL is not set" && exit 1)
	psql "$(TEST_DATABASE_URL)" -c "TRUNCATE url_checks RESTART IDENTITY CASCADE; TRUNCATE urls RESTART IDENTITY CASCADE;"

