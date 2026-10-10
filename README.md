<p align="center">
  <b>English</b> · <a href="README.ru.md">Русский</a>
</p>

<p align="center">
  <img src="./assets/readme/en/hero.svg" width="100%" alt="ticktick-routine: one line from you, a full plan in TickTick. Example on the right: a Spanish course, the chosen deadline and time, and a week where the course is split into sessions around busy time.">
</p>

**ticktick-routine is a personal planning assistant for TickTick that lives inside your AI agent.** Give it something short: a course link, a photo of a book cover or one line like "moving on November 1". It does the rest on its own: it works out what it is and how long it takes, breaks it into clear steps and puts each step into your free time in TickTick. If things don't go to plan, it moves what's left so you still make the deadline.

It works in **Claude Code**, **Codex**, **OpenCode** and the **claude.ai** chat, through the official TickTick MCP.

## One line → a full plan

You write to your agent:

> *‹link to a Spanish course›* by the end of the month

The skill then does this on its own:

1. **Reads the material.** It opens the link: a Spanish course at level A1, 20 short lessons, about 7 hours.
2. **Breaks it into steps.** It splits the course by meaning: 5 sessions of 4 lessons, each with its own topic.
3. **Finds the time.** It looks for free slots in your preferred hours, works around busy days and leaves a buffer before the deadline.

Only then does it ask what matters, in one message with ready answers:

```text
🔗 Spanish A1 — online course: 20 short lessons, ~7 h. Deadline: Sat Oct 31.

1. What to do?   Plan to the deadline (Recommended) · One task with a deadline · Skip
2. What time?    11:00–12:30 (study window) · 13:00–14:30 · Evening 20:00 · No fixed time
```

You answer "plan, at 11" and see the plan before anything appears in TickTick:

| When | What |
|---|---|
| Mon Oct 12, 11:00–12:30 | Lessons 1–4: greetings, alphabet, numbers |
| Thu Oct 15, 11:00–12:30 | Lessons 5–8: about yourself, family, the verb *ser* |
| Mon Oct 19, 11:00–12:30 | Lessons 9–12: time, days of the week, daily routine |
| Thu Oct 22, 11:00–12:30 | Lessons 13–16: food, at the café, shopping |
| Mon Oct 26, 11:00–12:30 | Lessons 17–20: the city, directions, review |

Tuesdays and Saturdays at 11:00 are already taken, so the sessions go on Mondays and Thursdays, and Oct 27–31 stays free as a buffer. After your "yes", TickTick gets a course task with the deadline and five sessions with reminders.

<sub>A simplified example. In tests on a real account (4 scenarios) the skill passed 41 of 41 checks. The same agent without it passed 35 of 41: it didn't know the convenient hours, the confirmation rule or which list things belong in.</sub>

## What it works with

Not just courses. Here is what one line turns into:

| You write | You get |
|---|---|
| a course link + "by the end of the month" | sessions by lesson up to the deadline, in your study hours |
| a photo of a book cover + "read by the 20th" | reading by chapters, spread over evenings until the 20th |
| a link to a lecture playlist | one or two lectures per free slot |
| "prepare for the job interview on Friday" | preparation steps by day: topics, practice tasks, a mock interview |
| "moving on November 1" | steps with dates: the lease, boxes, internet at the new place, change of address |
| "pay the internet bill, buy a water filter, book the dentist" | three tasks in three lists, each at its own time |
| "useful" + a link | a bookmark in the right place, no duplicates |

## What it helps with

| Without it | With it |
|---|---|
| A big task with no obvious place to start | It is broken into clear steps with dates right away |
| A course you'll take "someday" never gets started | The course becomes sessions in your free time, up to the deadline you choose |
| Planning by hand means checking the calendar, counting days and creating ten tasks | You write one line and answer 1–3 one-tap questions |
| You miss one session and the whole plan falls apart | You say "didn't make it" and the remaining steps are moved so you still make the deadline |
| Useful links pile up in the Inbox and get forgotten | Every link gets a place right away, and a time slot if you want one |

## Highlights

- **Reads it for you.** It opens a link, a file or a screenshot and works out what it is and how long it takes: lessons, chapters, lectures, pages.
- **Breaks it into meaningful steps.** A course by lessons, a book by chapters, a big task by stages. Each step becomes its own subtask with a date.
- **Finds time that suits you.** It knows your preferred hours and works around meetings, recurring tasks and your other plans. It keeps study under ~3 hours a day and leaves a buffer before the deadline.
- **Asks as little as possible.** You get 1–3 questions with ready answers, the recommended one first. It doesn't ask about anything you've already said.
- **Understands plain speech.** Write the way you talk or dictate by voice; typos and "tick-tick" are fine.
- **No duplicates.** It first checks TickTick for the same link or topic and offers to extend what's already there.
- **Your lists, your style.** It uses your own lists, columns, tags and title format, so the tasks look like you made them.
- **Learns your habits.** Say "remember that I study better in the evening" and it plans that way from then on.
- **Nothing happens silently.** It shows a plan before creating it and deletes only when you ask.
- **Keeps secrets private.** Lists that hold passwords are read by title only.

## How it works

<p align="center">
  <img src="./assets/readme/en/workflow.svg" width="100%" alt="Four steps: drop material; the skill sizes the work and splits it into steps; finds free slots, you answer in one tap; files the steps by day into your lists with reminders.">
</p>

## What else it does

| You write | What happens |
|---|---|
| "what's on tomorrow / this week?" | an overview of your tasks and free slots |
| "didn't make it", "move it" | the remaining steps are moved so you still make the deadline |
| "weekly review" | results, leftovers and a plan for next week |
| "remember that I study better in the evening" | a new rule, and the skill plans that way from then on |

## Get started

1. **Install the skill.** One command covers every agent (needs Node.js):

   ```bash
   npx skills add phloya/ticktick-routine -g -a claude-code -a codex -a opencode
   ```

2. **Connect TickTick.** Add the official server `https://mcp.ticktick.com/` to your agent and sign in with your TickTick account in the browser. There are no keys to copy. The commands for each agent are below.
3. **Send your agent any link.** On the first run the skill looks through your lists (read-only), asks 3–4 questions about your routine and saves its settings. From then on it just works. To redo the setup, say "reconfigure the skill" or "I have new lists".

<details>
<summary><b>Connect TickTick in Claude Code</b></summary>

If TickTick is already connected as a claude.ai connector (Settings → Connectors), Claude Code picks it up by itself. Otherwise:

```bash
claude mcp add --transport http --scope user ticktick https://mcp.ticktick.com/
```

Then inside Claude Code: `/mcp` → `ticktick` → sign in.

</details>

<details>
<summary><b>Connect TickTick in Codex</b></summary>

```bash
codex mcp add ticktick --url https://mcp.ticktick.com/
```

```bash
codex mcp login ticktick
```

The skill triggers on its own; to call it explicitly, use `$ticktick-routine`.

</details>

<details>
<summary><b>Connect TickTick in OpenCode</b></summary>

```bash
opencode mcp add ticktick --url https://mcp.ticktick.com/
```

```bash
opencode mcp auth ticktick
```

OpenCode also reads skills from `~/.claude/skills`, so if the skill is installed for Claude Code you don't need a second copy.

</details>

<details>
<summary><b>claude.ai on the web and on your phone</b></summary>

Connect the TickTick connector in claude.ai (Settings → Connectors). Then build the skill archive together with your settings:

```bash
./install.sh --claude-ai
```

Upload `dist/ticktick-routine.skill` in claude.ai: Settings → Capabilities → Skills. The archive contains your personal settings, so don't publish it. Without them the skill still works and runs the setup right in the chat.

</details>

<details>
<summary><b>Other ways to install</b></summary>

**With the script from the repository** (macOS, Linux; on Windows use Git Bash or WSL):

```bash
git clone https://github.com/phloya/ticktick-routine.git
```

```bash
cd ticktick-routine && ./install.sh
```

`install.sh` finds Claude Code, Codex and OpenCode on its own. Flags: `--claude`, `--codex`, `--opencode`, `--claude-ai`, `--uninstall`.

**As a Claude Code plugin:**

```text
/plugin marketplace add phloya/ticktick-routine
/plugin install ticktick-routine@ticktick-routine
```

</details>

## Privacy and limits

- It writes to TickTick only after you answer, and creates a plan of several tasks only after your "yes". It deletes only when you ask.
- Lists with secrets, such as bookmarks with passwords, are read by title only and left out of schedule checks.
- The skill stores no passwords or tokens: you sign in through the official TickTick server.
- Busy time comes from TickTick only. Google Calendar and other calendars are not checked.
- The skill's instructions are written in Russian, but it replies in your language.

## Technical details

<details>
<summary><b>How it is built</b></summary>

The skill is a set of agent instructions (`SKILL.md`) plus a personal settings file, the map of your account. All TickTick access goes through the official MCP server `https://mcp.ticktick.com/` with OAuth sign-in.

<p align="center">
  <img src="./assets/readme/en/one-map.svg" width="100%" alt="Claude Code, Codex, OpenCode and claude.ai read one map, ~/.config/ticktick-routine/map.md, and work with TickTick through the official MCP server.">
</p>

The map is plain Markdown in `~/.config/ticktick-routine/map.md`. It holds your lists and their IDs, columns, convenient hours, filing rules and private lists. It lives outside the skill folder, so updates never touch it, and Claude Code, Codex and OpenCode on one machine all see the same file (for claude.ai it is packed into the skill archive). You can edit it by hand or just tell the agent. The format is in [ticktick-map.example.md](skills/ticktick-routine/references/ticktick-map.example.md).

TickTick returns only the next occurrence of a recurring task, so the skill works out the following ones itself.

</details>

<details>
<summary><b>Repository layout</b></summary>

```text
skills/ticktick-routine/
├── SKILL.md                      main workflow
├── agents/openai.yaml            Codex card and MCP dependency
├── references/
│   ├── setup.md                  first run: account map
│   ├── ticktick-map.example.md   map template
│   ├── ticktick-api.md           TickTick MCP cheat sheet
│   └── routines.md               overview, rescheduling, weekly review
└── scripts/days.py               calendar with weekday names
install.sh                        installer for Claude Code, Codex, OpenCode, claude.ai
.claude-plugin/                   Claude Code plugin and marketplace
assets/readme/                    illustrations (source: source/build_svgs.py)
```

</details>

<details>
<summary><b>Update or remove</b></summary>

```bash
npx skills update ticktick-routine
```

Or `git pull && ./install.sh`. To remove it, run `./install.sh --uninstall` or `npx skills remove ticktick-routine`. Your settings in `~/.config/ticktick-routine/` stay; delete them by hand if you no longer need them.

</details>

## License

[MIT](LICENSE)
