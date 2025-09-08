## Page Analyzer (Hexlet Project 83)

[![Actions Status](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)
[![Quality Gate](https://sonarcloud.io/api/project_badges/quality_gate?project=vlrkors_python-project-83)](https://sonarcloud.io/summary/new_code?id=vlrkors_python-project-83)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=vlrkors_python-project-83&metric=coverage)](https://sonarcloud.io/summary/new_code?id=vlrkors_python-project-83)

Небольшое Flask‑приложение для анализа веб‑страниц (учебный проект Hexlet).

### Демо
- Продакшен: https://python-project-83.onrender.com
- Девелопмент: https://python-project-83-5kzt.onrender.com

### Установка и запуск (локально)
- Требования: Python 3.12+, установленный `uv` (https://docs.astral.sh/uv/)
- Установка зависимостей: `make install`
- Запуск dev‑сервера: `make dev` (по умолчанию http://localhost:8000)

### Проверки
- Линтер: `make lint`
- Форматирование: `make fmt`
- Тесты: `uv run pytest`
- Healthcheck: `GET /health` — проверяет доступность БД (если настроена `DATABASE_URL`)

### Конфигурация
- Переменные окружения подхватываются из системы и файла `.env` (локально)
- Пример: `.env.example` (`SECRET_KEY`, `DATABASE_URL`)

### Деплой на Render
1. Подключите репозиторий GitHub к Render (через Blueprint).
2. В Render: New → Blueprint → укажите репозиторий с `render.yaml` (ветка `main`).
3. Примените конфигурацию (создастся Web‑сервис и PostgreSQL).
4. Сборка выполняет `uv sync`, запуск — `make render-start`.

Параметры (из `render.yaml`):
- Build Command: `uv sync`
- Start Command: `make render-start`
- Переменные окружения: `SECRET_KEY` (генерируется), `DATABASE_URL` (из базы)

