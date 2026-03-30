# PawPal+ (Module 2 Project)

A smart pet care planning assistant built with Python and Streamlit.

---

## Project Overview

**PawPal+** helps a busy pet owner stay consistent with pet care. The owner registers their pets, adds care tasks for each one, and gets a prioritized daily schedule. The system filters completed tasks, detects scheduling conflicts, and resets recurring tasks at the start of each new day.

---

## Features

| Feature | Description |
|---|---|
| **Owner & Pet management** | Register an owner and add multiple pets |
| **Task management** | Add tasks to individual pets with title, duration, and priority |
| **Priority scheduling** | Schedule sorts tasks high → medium → low, then shorter-first within each tier |
| **Completion filtering** | Completed tasks are excluded from the generated schedule |
| **Pet filtering** | View the pending task list for a single named pet |
| **Recurrence** | Mark tasks as `once`, `daily`, or `weekly`; daily tasks reset each new day |
| **Conflict detection** | Tasks sharing the same time slot trigger a clear warning |
| **Streamlit UI** | Browser-based interface for all features |
| **CLI demo** | `main.py` runs a full demo in the terminal |
| **Test suite** | 13 pytest tests covering all major behaviors |

---

## How to Run

### Setup (one time)

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\activate
pip install -r requirements.txt
```

### CLI demo

```bash
python main.py
```

### Tests

```bash
python -m pytest
```

### Streamlit app

```bash
streamlit run app.py
```

---

## Smarter Scheduling

### Sorting

`Scheduler.generate_schedule()` sorts all pending tasks by:
1. **Priority** — `high` before `medium` before `low`
2. **Duration** — shorter tasks first within the same priority tier

This keeps the plan actionable: urgent, quick tasks appear at the top.

### Filtering

`Scheduler.filter_schedule(pet_name)` returns only the pending tasks for a single pet, using the same sort order. Useful when an owner wants to focus on one animal at a time.

### Recurrence

Each task has a `recurrence` field: `"once"` (default), `"daily"`, or `"weekly"`.

`Scheduler.reset_daily_tasks()` resets the `completed` flag on all daily tasks so they reappear in the next day's schedule. One-time tasks stay completed.

### Conflict detection

Each task has an optional `time_slot` field (e.g. `"08:00"`).

`Scheduler.detect_conflicts()` scans all pending tasks. If two tasks share the same non-empty time slot, it returns a human-readable warning string. No crash — just clear feedback.

---

## Testing PawPal+

### What is tested

| Area | Tests |
|---|---|
| Task | `mark_complete()` flips `completed` to `True` |
| Pet | `add_task()` increases the task list count |
| Owner | `get_all_tasks()` aggregates across all pets |
| Scheduler — schedule | Completed tasks excluded; priority order correct |
| Scheduler — filter | Returns only the named pet's tasks; handles unknown pet; excludes completed |
| Scheduler — recurrence | Daily tasks reset; once-tasks untouched by reset |
| Scheduler — conflicts | Same slot detected; different slots pass; completed tasks ignored |

### How to run

```bash
python -m pytest          # run all tests
python -m pytest -v       # verbose output
```

### Confidence level

**4 / 5** — All core behaviors are covered. Edge cases not yet tested include an owner with no pets, tasks with `"weekly"` recurrence, and duplicate task titles.

---

## Demo

Add a screenshot here after running `streamlit run app.py`.

![PawPal screenshot](scrsht.png)

---

## Project Structure

```
PawPal/
├── app.py               # Streamlit UI
├── pawpal_system.py     # Core backend: Task, Pet, Owner, Scheduler
├── main.py              # CLI demo
├── requirements.txt
├── reflection.md
├── tests/
│   └── test_pawpal.py   # pytest test suite (13 tests)
└── README.md
```
