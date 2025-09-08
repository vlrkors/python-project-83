SHELL := /bin/bash
PORT ?= 8000

# Выбор сервера для продакшена в зависимости от ОС
ifeq ($(OS),Windows_NT)
RENDER_CMD = uv run waitress-serve --host=0.0.0.0 --port=$(PORT) page_analyzer:app
else
RENDER_CMD = gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
endif

.PHONY: install dev start lint fmt build render-start

# Установка зависимостей
install:
	uv sync

# Запуск в режиме разработки
dev:
	uv run flask --debug --app page_analyzer:app run --port $(PORT)

# Запуск приложения (продакшен)
start:
	$(RENDER_CMD)

# Проверка кода с помощью ruff
lint:
	uv run ruff check .

# Форматирование кода с помощью ruff
fmt:
	uv run ruff format .

# Сборка проекта
build:
	bash ./build.sh

# Запуск продакшен сервера
render-start:
	$(RENDER_CMD)

# Запись терминальной сессии с помощью asciinema
record:
	asciinema rec page_analizer.cast

# Воспроизведение записанной сессии
play:
	asciinema play page_analizer.cast

# Загрузка записанной сессии на asciinema.org
upload:
	asciinema upload page_analizer.cast