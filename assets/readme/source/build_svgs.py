#!/usr/bin/env python3
"""Build the README illustrations (Russian + English) from one layout.

    python3 assets/readme/source/build_svgs.py

Writes assets/readme/{hero,workflow,one-map}.svg (Russian) and the same names
under assets/readme/en/ (English). Edit the copy in TEXT, the layout below it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent

BG, CARD, INK, MUTED, LINE = "#F6F7FB", "#FFFFFF", "#172033", "#5F6880", "#E2E6EF"
BLUE, BLUE_SOFT, BUSY = "#4772FA", "#E8EEFF", "#C9CFDC"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', 'DejaVu Sans', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

TEXT = {
    "ru": {
        "hero_title": "ticktick-routine — помощник, который сам разбирает дело на шаги и ставит их в твоё время в TickTick",
        "hero_desc": "Слева название и обещание; справа короткое сообщение о курсе испанского, выбранные срок и время и неделя, где курс разбит на занятия в обход занятого времени.",
        "promise": ["Одна строка от тебя —", "готовый план в TickTick"],
        "sub": ["Сам разберёт материал на шаги, подберёт свободное", "время и разложит по нужным спискам."],
        "bubble": ("курс испанского", " — на учёбу"),
        "blocks": ["1–4", "5–8"],
        "chip1": ("Срок", "до сб 31.10"),
        "chip2": ("Время", "11:00–12:30"),
        "days": ["пн", "вт", "ср", "чт", "пт", "сб", "вс"],
        "legend_new": "новые занятия",
        "legend_busy": "уже занято",
        "wf_title": "Как работает скилл: от одной строки до плана",
        "wf_desc": "Скинул материал; скилл понял, что это и сколько займёт, разбил на занятия, подобрал свободное время и разложил задачи по спискам.",
        "steps": [
            ("Скинул", ["Ссылка, файл, голос —", "без всякого формата"]),
            ("Разобрал", ["Понял объём и разбил", "на занятия по смыслу"]),
            ("Подобрал", ["Свободные окна —", "ответ в один клик"]),
            ("Разложил", ["Шаги по дням, списки,", "напоминания"]),
        ],
        "bubbles": ["курс испанского", "купить фильтр", "что на неделе?"],
        "parsed": ("Испанский A1", "курс · 20 уроков", "≈ 7 часов", "5 занятий"),
        "options": ["План до срока", "До сб 31.10", "11:00–12:30"],
        "dest": "Учёба → Сейчас",
        "plan": [("пн", "Уроки 1–4"), ("чт", "Уроки 5–8"), ("пн", "Уроки 9–12")],
        "map_title": "Одна карта на все агенты",
        "map_desc": "Claude Code, Codex, OpenCode и claude.ai читают одну карту аккаунта и работают с TickTick через официальный MCP-сервер.",
        "agents_note": ["~/.claude/skills", "~/.codex/skills", "читает ~/.claude/skills", "архив .skill + карта"],
        "map_lines": ["списки и колонки", "удобное время, ритм дня", "куда что класть", "секретные списки"],
        "map_foot": "создаётся при первом запуске",
        "reads": "читают карту",
        "calls": "через MCP",
        "account": ("Твой TickTick", "списки · задачи · привычки"),
    },
    "en": {
        "hero_title": "ticktick-routine — an assistant that breaks a task into steps and schedules them in your TickTick",
        "hero_desc": "Left: the name and promise. Right: a short message about a Spanish course, the chosen deadline and time, and a week where the course is split into sessions around busy time.",
        "promise": ["One line from you —", "a full plan in TickTick"],
        "sub": ["Breaks the material into steps, finds free time", "in your week and files it into your lists."],
        "bubble": ("Spanish course", " — to learn"),
        "blocks": ["1–4", "5–8"],
        "chip1": ("Due", "Sat, Oct 31"),
        "chip2": ("Time", "11:00–12:30"),
        "days": ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        "legend_new": "new sessions",
        "legend_busy": "already busy",
        "wf_title": "How the skill works: from one line to a plan",
        "wf_desc": "You drop material; the skill works out what it is and how long it takes, splits it into sessions, finds free time and files the tasks into your lists.",
        "steps": [
            ("Drop", ["Link, file or voice —", "no format needed"]),
            ("Break down", ["Sizes the work and", "splits it into steps"]),
            ("Schedule", ["Finds free slots,", "you answer in one tap"]),
            ("File", ["Steps by day, lists,", "reminders"]),
        ],
        "bubbles": ["Spanish course", "buy a filter", "what's this week?"],
        "parsed": ("Spanish A1", "course · 20 lessons", "≈ 7 hours", "5 sessions"),
        "options": ["Plan to deadline", "Due Sat, Oct 31", "11:00–12:30"],
        "dest": "Learning → Now",
        "plan": [("Mo", "Lessons 1–4"), ("Th", "Lessons 5–8"), ("Mo", "Lessons 9–12")],
        "map_title": "One map for every agent",
        "map_desc": "Claude Code, Codex, OpenCode and claude.ai read one account map and work with TickTick through the official MCP server.",
        "agents_note": ["~/.claude/skills", "~/.codex/skills", "reads ~/.claude/skills", ".skill archive + map"],
        "map_lines": ["lists and columns", "convenient hours, routine", "what goes where", "lists to keep private"],
        "map_foot": "built on the first run",
        "reads": "read the map",
        "calls": "via MCP",
        "account": ("Your TickTick", "lists · tasks · habits"),
    },
}


def t(x, y, s, size=20, fill=INK, weight=400, family=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def check(cx, cy, r=11, fill=BLUE, stroke="#FFFFFF"):
    k = r / 11
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            f'<path d="M{cx - 4.6 * k:.1f} {cy + 0.2 * k:.1f} l{3.2 * k:.1f} {3.2 * k:.1f} l{6 * k:.1f} -{6.4 * k:.1f}" '
            f'fill="none" stroke="{stroke}" stroke-width="{2.6 * k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def svg(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="title desc">\n'
            f'  <title id="title">{escape(title)}</title>\n  <desc id="desc">{escape(desc)}</desc>\n'
            f'  <defs><pattern id="busy" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="8" height="8" fill="#EEF0F5"/><rect width="3" height="8" fill="{BUSY}"/></pattern></defs>\n'
            f'  <rect width="{w}" height="{h}" rx="28" fill="{BG}"/>\n{body}\n</svg>\n')


def hero(L):
    out = []
    # Title block: category, name, promise, how, where it runs.
    out.append('<g id="title-block" transform="translate(64 0)">')
    out.append(t(0, 92, "AGENT SKILL  ·  TICKTICK MCP", 18, BLUE, 600, MONO, extra=' letter-spacing="1.5"'))
    out.append(t(0, 160, "ticktick-routine", 58, INK, 700, extra=' letter-spacing="-1"'))
    out.append(t(0, 214, L["promise"][0], 33, INK, 600))
    out.append(t(0, 254, L["promise"][1], 33, BLUE, 600))
    out.append(t(0, 302, L["sub"][0], 20, MUTED))
    out.append(t(0, 330, L["sub"][1], 20, MUTED))
    x = 0
    for name in ["Claude Code", "Codex", "OpenCode", "claude.ai"]:
        w = int(len(name) * 9.4) + 30
        out.append(f'<rect x="{x}" y="352" width="{w}" height="34" rx="17" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>')
        out.append(t(x + w / 2, 375, name, 17, MUTED, 500, anchor="middle"))
        x += w + 10
    out.append("</g>")

    # Proof: the conversation turned into a week.
    out.append('<g id="proof" transform="translate(640 36)">')
    out.append(f'<rect width="500" height="348" rx="22" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>')
    link, rest = L["bubble"]
    bw = 300
    out.append(f'<rect x="{476 - bw}" y="22" width="{bw}" height="48" rx="20" fill="{BLUE_SOFT}"/>')
    out.append(f'<text x="{476 - bw / 2}" y="53" font-family="{SANS}" font-size="20" fill="{INK}" text-anchor="middle">'
               f'<tspan font-weight="700" fill="{BLUE}">{escape(link)}</tspan>{escape(rest)}</text>')
    for i, (k, v) in enumerate([L["chip1"], L["chip2"]]):
        cx = 24 + i * 232
        out.append(f'<rect x="{cx}" y="88" width="220" height="44" rx="22" fill="{CARD}" stroke="{BLUE}" stroke-width="2"/>')
        out.append(check(cx + 24, 110))
        out.append(f'<text x="{cx + 44}" y="117" font-family="{SANS}" font-size="18" fill="{MUTED}">{escape(k)} '
                   f'<tspan fill="{INK}" font-weight="600">{escape(v)}</tspan></text>')
    gx, gy, col, ph = 70, 176, 58, 26.0  # grid origin, column width, units per hour (11:00 at gy+16)
    top = gy + 16
    for i, d in enumerate(L["days"]):
        out.append(t(gx + col * i + col / 2, gy, d, 18, MUTED, 600, anchor="middle"))
    for hh in (11, 13, 15):
        y = top + (hh - 11) * ph
        out.append(f'<line x1="{gx}" y1="{y}" x2="{gx + col * 7}" y2="{y}" stroke="{LINE}" stroke-width="2" stroke-dasharray="4 6"/>')
        out.append(t(gx - 10, y + 6, f"{hh}:00", 16, MUTED, 400, MONO, anchor="end"))

    def block(day, start, end, fill, label=None):
        y1, y2 = top + (start - 11) * ph, top + (end - 11) * ph
        x = gx + col * day + 4
        s = f'<rect x="{x}" y="{y1 + 2}" width="{col - 8}" height="{y2 - y1 - 4}" rx="8" fill="{fill}"/>'
        if label:
            s += t(x + (col - 8) / 2, (y1 + y2) / 2 + 6, label, 17, "#FFFFFF", 700, anchor="middle")
        return s

    out.append(block(1, 11, 12.5, "url(#busy)"))
    out.append(block(5, 11, 12.5, "url(#busy)"))
    out.append(block(2, 13, 14, "url(#busy)"))
    out.append(block(0, 11, 12.5, BLUE, L["blocks"][0]))
    out.append(block(3, 11, 12.5, BLUE, L["blocks"][1]))
    ly = 318
    out.append(f'<rect x="{gx}" y="{ly - 14}" width="18" height="18" rx="5" fill="{BLUE}"/>')
    out.append(t(gx + 28, ly, L["legend_new"], 17, MUTED))
    lx = gx + 60 + len(L["legend_new"]) * 9.6
    out.append(f'<rect x="{lx}" y="{ly - 14}" width="18" height="18" rx="5" fill="url(#busy)"/>')
    out.append(t(lx + 28, ly, L["legend_busy"], 17, MUTED))
    out.append("</g>")
    return svg(1200, 420, L["hero_title"], L["hero_desc"], "\n".join(out))


def workflow(L):
    out = []
    w, h, gap, x0, y0 = 258, 312, 26, 48, 40
    for i, (name, caption) in enumerate(L["steps"]):
        x = x0 + i * (w + gap)
        out.append(f'<g id="step-{i + 1}" transform="translate({x} {y0})">')
        out.append(f'<rect width="{w}" height="{h}" rx="20" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>')
        out.append(f'<circle cx="38" cy="42" r="18" fill="{BLUE}"/>')
        out.append(t(38, 49, str(i + 1), 20, "#FFFFFF", 700, anchor="middle"))
        out.append(t(66, 51, name, 26, INK, 700))
        a = []  # step artifact, area y 80..226
        if i == 0:
            for j, s in enumerate(L["bubbles"]):
                bw = int(len(s) * 10.2) + 32
                a.append(f'<rect x="{w - 20 - bw}" y="{86 + j * 48}" width="{bw}" height="38" rx="17" fill="{BLUE_SOFT}"/>')
                a.append(t(w - 20 - bw / 2, 111 + j * 48, s, 19, BLUE if j == 0 else INK, 700 if j == 0 else 500, anchor="middle"))
        elif i == 1:
            title, kind, size, dup = L["parsed"]
            a.append(f'<rect x="20" y="84" width="{w - 40}" height="138" rx="14" fill="{BG}"/>')
            a.append(t(38, 118, title, 23, INK, 700))
            a.append(t(38, 148, kind, 19, MUTED))
            a.append(t(38, 176, size, 19, MUTED))
            a.append(check(48, 203, 9))
            a.append(t(66, 209, dup, 18, INK, 600))
        elif i == 2:
            for j, s in enumerate(L["options"]):
                y = 86 + j * 48
                a.append(f'<rect x="20" y="{y}" width="{w - 40}" height="38" rx="19" fill="{BLUE if j else CARD}" stroke="{BLUE}" stroke-width="2"/>')
                a.append(check(42, y + 19, 9, "#FFFFFF" if j else BLUE, BLUE if j else "#FFFFFF"))
                a.append(t(60, y + 26, s, 18, "#FFFFFF" if j else INK, 600))
        else:
            a.append(t(20, 104, L["dest"], 18, BLUE, 600, MONO))
            for j, (d, s) in enumerate(L["plan"]):
                y = 120 + j * 36
                a.append(f'<rect x="20" y="{y}" width="{w - 40}" height="30" rx="8" fill="{BLUE_SOFT}"/>')
                a.append(f'<rect x="20" y="{y}" width="6" height="30" rx="3" fill="{BLUE}"/>')
                a.append(t(36, y + 21, f"{d} 11:00", 17, MUTED, 400, MONO))
                a.append(t(w - 30, y + 21, s, 18, INK, 600, anchor="end"))
        out.extend(a)
        out.append(t(20, 266, caption[0], 19, MUTED))
        out.append(t(20, 292, caption[1], 19, MUTED))
        out.append("</g>")
        if i < 3:
            ax = x + w + gap / 2
            out.append(f'<circle cx="{ax}" cy="{y0 + h / 2}" r="12" fill="{BG}" stroke="{LINE}" stroke-width="2"/>')
            out.append(f'<path d="M{ax - 3} {y0 + h / 2 - 6} l6 6 l-6 6" fill="none" stroke="{BLUE}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(1200, 392, L["wf_title"], L["wf_desc"], "\n".join(out))


def one_map(L):
    out = []
    agents = ["Claude Code", "Codex", "OpenCode", "claude.ai"]
    ax, aw, ah = 48, 300, 66
    centers = []
    for i, name in enumerate(agents):
        y = 44 + i * 84
        dash = ' stroke-dasharray="7 6"' if i == 3 else ""
        out.append(f'<rect x="{ax}" y="{y}" width="{aw}" height="{ah}" rx="16" fill="{CARD}" stroke="{LINE}" stroke-width="2"{dash}/>')
        out.append(t(ax + 22, y + 29, name, 22, INK, 700))
        out.append(t(ax + 22, y + 54, L["agents_note"][i], 16, MUTED, 400, MONO))
        centers.append(y + ah / 2)
    mx, my, mw, mh = 420, 92, 330, 236
    for cy in centers:
        out.append(f'<path d="M{ax + aw} {cy} C{ax + aw + 50} {cy} {mx - 50} {my + mh / 2} {mx} {my + mh / 2}" fill="none" stroke="{BUSY}" stroke-width="2"/>')
    out.append(t((ax + aw + mx) / 2, 30, L["reads"], 18, MUTED, 500, anchor="middle"))
    out.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="20" fill="{CARD}" stroke="{BLUE}" stroke-width="2.5"/>')
    out.append(t(mx + 24, my + 38, "~/.config/ticktick-routine/", 16, MUTED, 400, MONO))
    out.append(t(mx + 24, my + 70, "map.md", 28, INK, 700, MONO))
    for j, s in enumerate(L["map_lines"]):
        y = my + 108 + j * 30
        out.append(check(mx + 34, y - 6, 8))
        out.append(t(mx + 52, y, s, 19, INK))
    out.append(t(mx + mw / 2, my + mh + 34, L["map_foot"], 17, MUTED, 400, anchor="middle"))
    rx, rw = 852, 300
    out.append(f'<path d="M{mx + mw} {my + mh / 2} L{rx} {my + mh / 2}" stroke="{BLUE}" stroke-width="2.5" fill="none"/>')
    out.append(f'<path d="M{rx - 10} {my + mh / 2 - 7} l10 7 l-10 7" stroke="{BLUE}" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(t((mx + mw + rx) / 2, my + mh / 2 - 14, L["calls"], 17, MUTED, 500, anchor="middle"))
    out.append(f'<rect x="{rx}" y="{my}" width="{rw}" height="104" rx="18" fill="{BLUE}"/>')
    out.append(t(rx + 24, my + 40, "TickTick MCP", 23, "#FFFFFF", 700))
    out.append(t(rx + 24, my + 70, "mcp.ticktick.com", 17, "#FFFFFF", 400, MONO))
    out.append(t(rx + 24, my + 92, "OAuth", 16, "#DCE5FF", 400, MONO))
    out.append(f'<path d="M{rx + rw / 2} {my + 104} L{rx + rw / 2} {my + 132}" stroke="{BLUE}" stroke-width="2.5"/>')
    acc, sub = L["account"]
    out.append(f'<rect x="{rx}" y="{my + 132}" width="{rw}" height="104" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>')
    out.append(t(rx + 24, my + 174, acc, 22, INK, 700))
    out.append(t(rx + 24, my + 206, sub, 18, MUTED))
    return svg(1200, 412, L["map_title"], L["map_desc"], "\n".join(out))


def main():
    for lang, L in TEXT.items():
        d = OUT if lang == "ru" else OUT / lang
        d.mkdir(parents=True, exist_ok=True)
        for name, fn in (("hero", hero), ("workflow", workflow), ("one-map", one_map)):
            # newline="\n" keeps the output byte-identical on Windows too.
            with open(d / f"{name}.svg", "w", encoding="utf-8", newline="\n") as f:
                f.write(fn(L))
            print(f"wrote {d / name}.svg")


if __name__ == "__main__":
    main()
