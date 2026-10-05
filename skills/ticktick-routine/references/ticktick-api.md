# TickTick MCP: шпаргалка

Официальный сервер — `https://mcp.ticktick.com/` (streamable HTTP, вход через OAuth). Имена инструментов ниже — без префикса, который добавляет агент; у части серверов те же инструменты доступны и через дефис (`list-projects`).

## Даты и время

- Всегда ISO 8601 со смещением часового пояса из карты: `2026-10-12T11:00:00+0300`. Без смещения время может уехать (сервер поймёт его как UTC).
- В задаче — `timeZone: "<часовой пояс из карты>"`, в вызове — `client_timezone` с тем же значением.
- **Блок времени** (занятие 11:00–12:30): `startDate: "…T11:00:00+0300"`, `dueDate: "…T12:30:00+0300"`, `isAllDay: false`, `reminders: ["TRIGGER:PT0S"]` — напоминание в момент начала. Для занятий всегда давай и начало, и конец, иначе задача станет моментом, а не блоком.
- **На весь день:** `startDate = dueDate = "YYYY-MM-DDT00:00:00+0300"`, `isAllDay: true`. Напоминание для таких задач — смещение от полуночи этого дня: `TRIGGER:P0DT9H0M0S` = 9:00 в тот же день, `TRIGGER:P0DT11H0M0S` = 11:00, `TRIGGER:-P0DT15H0M0S` = 9:00 накануне.
- **Без даты:** просто не передавай `startDate` и `dueDate`.
- Убрать дату у существующей задачи: `update_task` с `"1970-01-01T00:00:00.000+0000"`.
- Для повторяющейся задачи `startDate`/`dueDate` — первое вхождение.

## Поля задачи

| Поле | Что ставить |
|---|---|
| `projectId` | ID списка из карты. Обязателен в batch-вызовах; указывай всегда |
| `columnId` | ID колонки канбана из карты |
| `kind` | `"TEXT"` — обычная задача · `"NOTE"` — заметка (закладки, контент) · `"CHECKLIST"` — чек-лист: пункты в `items`, текст в `desc` |
| `title` | коротко; длинное — в `content` |
| `content` | текст и ссылки (для TEXT и NOTE); ссылку ставь первой строкой |
| `priority` | `0` нет · `1` низкий · `3` средний · `5` высокий |
| `tags` | `["книга"]` — имена тегов в нижнем регистре, как в карте |
| `parentId` | ID родителя — задача становится подзадачей |
| `repeatFlag` | `RRULE:FREQ=MONTHLY;BYMONTHDAY=8` · `RRULE:FREQ=WEEKLY;BYDAY=SA` · `RRULE:FREQ=DAILY` |
| `repeatFrom` | `"2"` (по умолчанию) |
| `reminders` | см. «Даты и время» |

## Типовые операции

- **Одна задача:** `create_task(task={…}, client_timezone=…)` → в ответе `id`.
- **Несколько задач:** `batch_add_tasks(tasks=[…], client_timezone=…)`.
- **План с подзадачами:** `create_task` (родитель) → `id` → `batch_add_tasks` (занятия с `parentId`, тем же `projectId` и `columnId`). После создания перечитай родителя (`get_task_by_id`) и сверь `childIds`; не прицепившимся проставь `parentId` через `batch_update_tasks`.
- **Изменить:** `update_task(task_id, task={id, projectId, …только меняемые поля})`; пачкой — `batch_update_tasks(tasks=[{id, projectId, …}])`. Переданное поле заменяется целиком: чтобы дополнить `content`, сначала перечитай задачу и передай старый текст плюс новый.
- **Переложить в другой список:** `move_task(moves=[{taskId, fromProjectId, toProjectId}])`. Колонку внутри списка меняют через `update_task` (`columnId`).
- **Завершить:** `complete_task(project_id, task_id)`.
- **Найти:** `search_task(query)` — по ключевому слову; `filter_tasks(filter={projectIds, startDate, endDate, tag, status, priority, kind})`.
- **Расписание:**
  - `list_undone_tasks_by_date(search={startDate, endDate, projectIds})` — основной способ. Диапазон не больше 14 дней, длиннее дели на части. В `projectIds` — все списки из `list_projects`, кроме секретных;
  - `list_completed_tasks_by_date(search={startDate, endDate, projectIds})` — с теми же `projectIds`;
  - `list_undone_tasks_by_time_query(query_command=today|tomorrow|next7day|…)` по спискам не фильтрует и возвращает заметки вместе с содержимым — если есть секретные списки, не используй.
  - Повторяющаяся задача приходит только ближайшим вхождением (еженедельная воскресная видна на ближайшее вс, но не на следующие) — дальше вычисляй по `repeatFlag`.
- **Список целиком с колонками:** `get_project_with_undone_tasks(project_id)`.
- **Привычки:** `list_habits` — там напоминания, то есть ритм дня.

## Грабли

- Ответы по секретным спискам могут содержать пароли в `content` — не цитируй его.
- `delete_task` — только по явной просьбе пользователя.
- ID списков и колонок бери из карты, подтверждённой `list_projects`, — не придумывай.
