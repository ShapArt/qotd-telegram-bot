import argparse
import html
import os
import random
import sys
from typing import Dict, List

import requests

OPENTDB_URL = "https://opentdb.com/api.php?amount=1&type=multiple"
TRIVIA_API_URL = "https://the-trivia-api.com/api/questions?limit=1&region=RU"


def fetch_opentdb() -> Dict:
    response = requests.get(OPENTDB_URL, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if payload.get("response_code") != 0:
        raise RuntimeError(f"OpenTDB error: {payload.get('response_code')}")
    item = payload["results"][0]
    answers: List[str] = item.get("incorrect_answers", []) + [item.get("correct_answer", "")]
    random.shuffle(answers)
    return {
        "source": "Open Trivia DB",
        "category": html.unescape(item.get("category", "")),
        "difficulty": item.get("difficulty", ""),
        "question": html.unescape(item.get("question", "")),
        "answers": [html.unescape(a) for a in answers],
        "correct": html.unescape(item.get("correct_answer", "")),
    }


def fetch_trivia_api() -> Dict:
    response = requests.get(TRIVIA_API_URL, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if not payload:
        raise RuntimeError("Trivia API returned empty payload")
    item = payload[0]
    answers: List[str] = item.get("incorrectAnswers", []) + [item.get("correctAnswer", "")]
    random.shuffle(answers)
    return {
        "source": "The Trivia API",
        "category": item.get("category", ""),
        "difficulty": item.get("difficulty", ""),
        "question": item.get("question", ""),
        "answers": answers,
        "correct": item.get("correctAnswer", ""),
    }


def build_message(card: Dict, locale: str = "ru") -> str:
    prefix = "🧠 Вопрос дня" if locale.startswith("ru") else "🧠 Question of the day"
    question_block = f"{prefix}\n\n{card['question']}"
    options = "\n".join([f"• {opt}" for opt in card["answers"]])
    answer_hint = "✅ Ответ позже" if locale.startswith("ru") else "✅ Answer will follow"
    meta = f"Категория: {card['category']} | Сложность: {card['difficulty']} | Источник: {card['source']}"
    if not locale.startswith("ru"):
        meta = f"Category: {card['category']} | Difficulty: {card['difficulty']} | Source: {card['source']}"
    return f"{question_block}\n\n{options}\n\n{answer_hint}\n{meta}"


def send_message(token: str, chat_id: str, text: str) -> None:
    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=10,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Telegram sendMessage failed: {resp.status_code} {resp.text}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send QOTD to Telegram chat")
    parser.add_argument("--source", default=os.getenv("SOURCE", "opentdb"), choices=["opentdb", "trivia"], help="Question source")
    parser.add_argument("--locale", default=os.getenv("LOCALE", "ru"), help="Locale for labels")
    args = parser.parse_args()

    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        sys.exit("BOT_TOKEN and CHAT_ID must be provided via environment")

    fetcher = fetch_opentdb if args.source == "opentdb" else fetch_trivia_api
    card = fetcher()
    message = build_message(card, locale=args.locale)
    send_message(token, chat_id, message)

    # return the correct answer in logs only, not to chat
    print(f"Sent QOTD from {card['source']} to chat {chat_id}. Correct: {card['correct']}")


if __name__ == "__main__":
    main()
