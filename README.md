## Page Analyzer (Hexlet Project 83)

[![Hexlet check](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Quality Gate](https://sonarcloud.io/api/project_badges/quality_gate?
project=vlrkors_python-project-83)](https://sonarcloud.io/summary/new_code?
id=vlrkors_python-project-83)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)

Веб‑приложение на Flask для анализа страниц сайтов (h1, title, description) 
и базовых SEO‑метрик. Учебный проект Hexlet (№83).

### Быстрый старт
- `make install` — установить зависимости
- создать `.env` (см. ниже) и задать `DATABASE_URL`
- `make db-init` — применить миграции (`database.sql`)
- `make dev` — запустить на http://localhost:8000

### Требования
- Python 3.12+
- Менеджер пакетов `uv`
- PostgreSQL (строка подключения)

### Переменные окружения
- `SECRET_KEY` — секретный ключ Flask
- `DATABASE_URL` — строка подключения к PostgreSQL
- `TEST_DATABASE_URL` — строка подключения к тестовой БД
- `FLASK_DEBUG` — включает режим отладки при локальной разработке

Файл примера: `.env.example`.

### Локальная разработка
- Установка: `make install`
- Инициализация БД: `make db-init` (использует `DATABASE_URL` и `database.sql`)
- Запуск dev: `make dev` (http://localhost:8000)
- Здоровье сервиса: `GET /health` возвращает `{ "status": "ok" }` при доступной БД

### Работа с БД на Render
- Создать PostgreSQL в Render (Blueprint из `render.yaml` уже описывает сервис).
- Взять External Connection string на странице базы (вкладка Connect) — обычно `...<region>-postgres.render.com...?sslmode=require`.
- Поместить строку в `DATABASE_URL` и выполнить локально: `make db-init`.

Подсказки:
- Для подключения извне нужен External URL и `sslmode=require`.
- Проверка: `psql "$env:DATABASE_URL" -c "SELECT 1;"` (Windows PowerShell) / `psql "$DATABASE_URL" -c "SELECT 1;"` (Linux/macOS).

### Тесты
- Запуск: `uv run pytest`
- Для DB‑тестов требуется `TEST_DATABASE_URL`. Без него тесты с БД будут пропущены.

### Деплой на Render
- Через Blueprint из `render.yaml`: создаст Web и PostgreSQL‑сервисы.
- Build: `uv sync`, Start: `make render-start`.
- Procfile запускает `gunicorn page_analyzer.app:app`, поэтому Render и 
  Heroku используют один и тот же вход.
- Переменные окружения Web‑сервиса: `SECRET_KEY`, `DATABASE_URL`.

### Полезные команды
- `make install` — установка зависимостей
- `make dev` — запуск dev‑сервера
- `make start` — локальный прод‑старт (Gunicorn/Waitress)
- `make lint` — проверка ruff
- `make fmt` — форматирование ruff
- `make lint-imports` / `make fmt-imports` — проверка/сортировка импортов
- `make db-init` / `make test-db-init` — применить `database.sql` к БД/тестовой БД
- `make db-reset-test` — очистить таблицы в тестовой БД
- `make render-start` — стартовая команда для Render

### UI / Bootstrap
- Bootstrap 5 подключён через CDN в `page_analyzer/templates/base.html`:
  - CSS: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css`
  - JS:  `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js`

###  Запуск на Render
- https://python-project-83-5kzt.onrender.com
