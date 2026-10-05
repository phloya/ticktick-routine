#!/usr/bin/env python3
"""Календарь на N дней вперёд в часовом поясе пользователя.

Дни недели нужны в вариантах ответов («До вс 11.10») и в заголовках задач,
а считать их в уме легко ошибиться — этот скрипт печатает точную сетку.

Использование:
    python3 days.py                       # сегодня + 20 дней, системный часовой пояс
    python3 days.py 30 --tz Europe/Moscow # часовой пояс из карты
"""
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]


def main() -> None:
    args = sys.argv[1:]
    tz = None
    if "--tz" in args:
        i = args.index("--tz")
        tz = ZoneInfo(args[i + 1])
        del args[i : i + 2]
    days = int(args[0]) if args else 21

    now = datetime.now(tz) if tz else datetime.now().astimezone()
    tz_label = getattr(now.tzinfo, "key", None) or now.tzname()
    print(f"Сейчас: {now:%Y-%m-%d %H:%M} {WEEKDAYS[now.weekday()]} · {tz_label} (UTC{now:%z})")
    for k in range(days):
        d = (now + timedelta(days=k)).date()
        if k and d.weekday() == 0:
            print("—")
        mark = {0: "  ← сегодня", 1: "  ← завтра"}.get(k, "")
        print(f"{d.isoformat()}  {WEEKDAYS[d.weekday()]}  {d.day}.{d.month:02d}{mark}")


if __name__ == "__main__":
    main()
