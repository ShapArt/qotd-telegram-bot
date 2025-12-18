# QOTD Telegram Bot

## ✨ Что умеет
- Шлёт «вопрос/цитату/слово дня» в Telegram по расписанию GitHub Actions (cron) или руками через `workflow_dispatch`.
- Источники: Open Trivia DB и The Trivia API (регион RU), варианты/ответ перемешаны, ответ пишет только в логи.
- CLI/cron без long-polling: `python bot/main.py --source opentdb --locale ru`.
- Локализация в RU/EN: заголовки/подсказки подстраиваются по `LOCALE`.
- Секреты только из GitHub Secrets (`BOT_TOKEN`, `CHAT_ID`), без .env в коммитах.

## 🧠 Технологии
- Python 3.11+, requests.
- GitHub Actions: матрица CI (lint/test), отдельный scheduler для рассылки.
- pre-commit + gitleaks (--redact) для локальной и CI-проверки.

## 🖼️ Демо
- Actions: `QOTD Scheduler` запускается раз в день (`cron: 0 7 * * *`) либо по кнопке.
- Локально: `BOT_TOKEN=xxx CHAT_ID=yyy python bot/main.py --source trivia --locale en`.

## 🏗️ Архитектура
- Fetcher (`fetch_opentdb` / `fetch_trivia_api`) → message builder → `sendMessage` в Bot API.
- Scheduler в Actions → `python bot/main.py` на чистом окружении → логирует правильный ответ в job output.
- Секреты/vars: `BOT_TOKEN`/`CHAT_ID` в secrets, `SOURCE`/`LOCALE` в Actions vars.

## ⚙️ Конфигурация
- `.env.example`: BOT_TOKEN, CHAT_ID, SOURCE (opentdb|trivia), LOCALE (ru|en).
- Secrets: `BOT_TOKEN`, `CHAT_ID`.
- Vars (optional): `SOURCE`, `LOCALE`.

## 🧪 Тесты
- Запланированы юниты для форматирования сообщений и fallback при пустом API.
- CI: pre-commit run --all-files (ruff/black/isort/prettier) + gitleaks detect.

## 🗺️ Roadmap
- [ ] Кешировать вопросы, чтобы не повторялись подряд.
- [ ] Добавить режим «цитата дня» из публичного API.
- [ ] Поддержать MarkdownV2/HTML выбор.
- [ ] Добавить health-check в Actions и алерт в чат при ошибке.
