### Hexlet tests and linter status:
[![Actions Status](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)

[![Quality Gate](https://sonarcloud.io/api/project_badges/quality_gate?project=vlrkors_python-project-83)](https://sonarcloud.io/summary/new_code?id=vlrkors_python-project-83)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=vlrkors_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=vlrkors_python-project-83)


## Разворачивание окружения (Render)

Базовый Flask-проект подготовлен для деплоя на Render (PaaS) с PostgreSQL.

Что внутри:
- Flask-приложение: `app/__init__.py`, маршруты в `app/routes.py`
- WSGI-точка входа: `wsgi.py`
- Gunicorn запускается через `Procfile`
- Зависимости: `requirements.txt`
- Blueprint-файл для Render: `render.yaml` (включает Web-сервис и PostgreSQL)
- Пример переменных окружения: `.env.example`
 - Поддержка `.env` через `python-dotenv` (12‑Factor для локалки)

Локальный запуск (через uv):
```bash
# Установите uv локально (https://docs.astral.sh/uv/)
make install
make dev  # http://localhost:8000
```

Деплой на Render через Blueprint:
1. Создайте приватный форк/репозиторий с этим кодом и подключите его к Render.
2. В Render: New + → Blueprint → укажите ссылку на репозиторий с `render.yaml`.
3. Подтвердите создание сервисов: Web `python-project-83` и Postgres `python-project-83-db` (оба на Free плане).
4. Дождитесь сборки и запуска. Приложение будет доступно по URL сервиса.

Проверки:
- Healthcheck: `GET /health` — проверяет соединение с БД (если настроена переменная `DATABASE_URL`).

Переменные окружения:
- `SECRET_KEY` — генерируется автоматически (см. `render.yaml`).
- `DATABASE_URL` — автоматически прокинется из PostgreSQL-инстанса в Render.

Принципы 12‑Factor:
- Конфигурация через переменные окружения (см. `SECRET_KEY`, `DATABASE_URL`).
- Порт берётся из `PORT` (см. `Procfile`/`render.yaml`).
- Зависимости фиксируются в `requirements.txt`.
- Локально можно использовать `.env` (загружается автоматически, не влияет на прод).

## Структура проекта
- Пакет приложения: `page_analyzer` — экспортирует переменную `app` на уровне пакета.
- Основной модуль Flask: `page_analyzer/app.py`
- Пакетное имя проекта: задаётся в `pyproject.toml` как `hexlet-code`.

## Makefile команды
- `make install` — установка зависимостей через `uv sync`
- `make dev` — запуск Flask в debug (`flask --app page_analyzer:app`)
- `make start` — запуск в проде через Gunicorn на `$(PORT)`
- `make lint` / `make fmt` — проверка/форматирование ruff
- `make build` — скрипт сборки для Render (`build.sh`)
- `make render-start` — кроссплатформенный старт в проде:
  - Windows: `waitress-serve` (Gunicorn не работает на Windows)
  - Linux/macOS/Render: `gunicorn`

## CI / Линтер
Настроен GitHub Actions (`.github/workflows/ci.yml`) с установкой `uv` и проверкой `ruff`.

## Деплой (Render)
В настройках web‑сервиса:
- Build Command: `make build`
- Start Command: `make render-start`

Продакшен URL: заполните ссылку на ваш домен Render здесь.
