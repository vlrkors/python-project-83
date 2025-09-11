## Page Analyzer (Hexlet Project 83)

[![Hexlet check](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/hexlet-check.yml)
[![CI](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml/badge.svg)](https://github.com/vlrkors/python-project-83/actions/workflows/ci.yml)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-46a2f1.svg)](https://docs.astral.sh/ruff/)

Веб‑приложение на Flask для анализа страниц сайтов и базовых SEO‑метрик. Учебный проект Hexlet (№83).

### Требования
- Python 3.12+
- Менеджер пакетов `uv` (https://docs.astral.sh/uv/)
- PostgreSQL (строка подключения в переменной окружения)

### Локальный запуск (dev)
1. Установить зависимости: `make install`
2. Создать файл `.env` (можно скопировать из `.env.example`) и задать переменные:
   - `SECRET_KEY` — секретный ключ Flask
   - `DATABASE_URL` — строка подключения к PostgreSQL
3. Инициализировать БД: `make db-init` (использует `DATABASE_URL` и схему из `database.sql`)
4. Запустить dev‑сервер: `make dev` (приложение доступно на http://localhost:8000)

### Полезные команды
- `make install` — установка зависимостей
- `make dev` — запуск dev‑сервера Flask
- `make start` — запуск прод‑сервера (Gunicorn/Waitress)
- `make lint` — проверка кода ruff
- `make fmt` — автоформатирование ruff
- `make render-start` — команда старта для Render
- `make db-init` — применить `database.sql` к `DATABASE_URL`
- `make test-db-init` — применить `database.sql` к `TEST_DATABASE_URL`
- `make db-reset-test` — очистка таблиц в тестовой БД

### Тесты
- Запуск: `uv run pytest`
- Для тестов работы с БД требуется `TEST_DATABASE_URL`. Если подключения нет, тесты будут пропущены.

### Деплой на Render
1. Подключить репозиторий GitHub к Render через Blueprint.
2. Создать приложение по `render.yaml` (ветка `main`).
3. Выбрать типы сервисов (Web и PostgreSQL).
4. Build: `uv sync`, Start: `make render-start`.

Необходимые переменные окружения: `SECRET_KEY`, `DATABASE_URL`.

### UI / Bootstrap
- Bootstrap 5 подключён через CDN в базовом шаблоне.
- Файл: `page_analyzer/templates/base.html`
- Подключения:
  - CSS: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css`
  - JS:  `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js`

