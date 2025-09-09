## Page Analyzer (Hexlet Project 83)

[![Hexlet check](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)

Небольшое Flask‑приложение для анализа веб‑страниц на SEO‑пригодность. Учебный проект Hexlet (№83).

### Требования
- Python 3.12+
- Установленный `uv` (https://docs.astral.sh/uv/)
- PostgreSQL (для хранения URL и результатов проверок)

### Установка и запуск (локально)
1. Установить зависимости: `make install`
2. Создать `.env` (можно скопировать из `.env.example`) и задать переменные:
   - `SECRET_KEY` — произвольная строка
   - `DATABASE_URL` — строка подключения к PostgreSQL
3. Инициализировать БД: `make db-init` (использует `DATABASE_URL` и `database.sql`)
4. Запустить dev‑сервер: `make dev` (по умолчанию http://localhost:8000)

### Команды
- `make install` — установка зависимостей
- `make dev` — запуск dev‑сервера Flask
- `make start` — запуск приложения (продакшен)
- `make lint` — проверка кода ruff
- `make fmt` — форматирование кода ruff
- `make render-start` — запуск для Render
- `make db-init` — применить `database.sql` к `DATABASE_URL`
- `make test-db-init` — применить `database.sql` к `TEST_DATABASE_URL`
- `make db-reset-test` — очистить таблицы в тестовой БД

### Тесты
- Запуск: `uv run pytest`
- DB‑тесты используют `TEST_DATABASE_URL`. Если переменная не задана или БД недоступна — эти тесты пропускаются.

### Деплой на Render
1. Подключите репозиторий GitHub к Render через Blueprint.
2. В Render: New → Blueprint → выберите репозиторий с `render.yaml` (ветка `main`).
3. Примените конфигурацию (создастся Web‑сервис и PostgreSQL).
4. Сборка: `uv sync`, запуск: `make render-start`.

Параметры (из `render.yaml`):
- Build Command: `uv sync`
- Start Command: `make render-start`
- Переменные окружения: `SECRET_KEY`, `DATABASE_URL`

### Демо
- Продакшен: https://python-project-83.onrender.com
- Девелопмент: https://python-project-83-5kzt.onrender.com

