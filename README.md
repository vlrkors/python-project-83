## Page Analyzer (Hexlet Project 83)

[![Actions Status](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)
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

### Тестовая БД
- Для unit‑тестов репозитория используется переменная `TEST_DATABASE_URL`.
- Если `TEST_DATABASE_URL` не задан или БД недоступна — тесты с БД будут пропущены.

Примеры задания переменных окружения:
- PowerShell: ``$env:TEST_DATABASE_URL = 'postgresql://USER:PASSWORD@localhost:5432/db_test'``
- Bash: ``export TEST_DATABASE_URL='postgresql://USER:PASSWORD@localhost:5432/db_test'``

Инициализация схемы (в том числе для локальной `DATABASE_URL`):
- PowerShell: ``psql "$env:TEST_DATABASE_URL" -f database.sql``
- Bash: ``psql "$TEST_DATABASE_URL" -f database.sql``

Быстрые команды Makefile:
- `make db-init` — применить `database.sql` к `DATABASE_URL`.
- `make test-db-init` — применить `database.sql` к `TEST_DATABASE_URL`.
- `make db-reset-test` — очистить таблицы (`TRUNCATE ... RESTART IDENTITY`) в тестовой БД.

### Деплой на Render
1. Подключите репозиторий GitHub к Render (через Blueprint).
2. В Render: New → Blueprint → укажите репозиторий с `render.yaml` (ветка `main`).
3. Примените конфигурацию (создастся Web‑сервис и PostgreSQL).
4. Сборка выполняет `uv sync`, запуск — `make render-start`.

Параметры (из `render.yaml`):
- Build Command: `uv sync`
- Start Command: `make render-start`
- Переменные окружения: `SECRET_KEY` (генерируется), `DATABASE_URL` (из базы)
