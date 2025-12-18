# Go Out Today (Telegram Mini App)

## ✨ Что умеет

- «Tinder для мест»: бары/кафе/события по городу, свайпы, матчи для пары/группы.
- Фильтры по категориям, цене, времени работы, «рядом со мной»; таймер «свободен через X минут».
- Совместный выбор: пригласить друзей, общий матч, уведомления через бота.

## 🧠 Технологии

- Bot: Aiogram 3.x для инвайтов/уведомлений.
- Mini App: React/Vite + Telegram WebApps SDK.
- API: FastAPI proxy 2GIS/Google Places, кеш (Redis), rate limits.
- Безопасность: API ключи через ENV, gitleaks/pre-commit, minimal Actions permissions.

## 🖼️ Демо

- TODO: добавить скрин/видео mini app и ссылку на стенд.

## Архитектура

- `api/` — FastAPI proxy к 2GIS/Google Places, кеширование, фильтры, матчи.
- `miniapp/` — WebApp UI со свайпами и матчами.
- `bot/` — aiogram: /start, приглашения, нотификации.
- `docs/` — overview, ci badge snippet; `assets/` — social preview.

## Конфигурация

- `.env.example`: `BOT_TOKEN`, `PLACES_API_KEY`, `PLACES_PROVIDER` (2gis/google), `BACKEND_URL`, `WEBAPP_ORIGIN`, `REDIS_URL`.
- Секреты не коммитим; gitleaks в pre-commit/CI.

### Локальный запуск

```bash
pip install -r requirements.txt
python -m bot.main  # telegram bot stub
```

API:

```bash
cd api
pip install -e .[dev]
uvicorn app.main:app --reload
```

Docker Compose:

```bash
cd infra
docker compose up --build
```

## Тесты

- План: `ruff check . && black --check . && mypy . && pytest` для api/bot; miniapp — `npm run lint && npm test` после scaffold.

## Roadmap

- Инициализировать api (FastAPI) и miniapp (React/Vite + TWA SDK).
- Добавить поиск/свайпы по 2GIS, кеш Redis, матчи для группы.
- Подключить бот-инвайты/нотификации, deep-link miniapp.
- Добавить e2e smoke (Playwright) и CI матрицу.
