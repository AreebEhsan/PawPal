"""
PawPal+ tests — Phase 2 + Phase 4.

Run with:  python -m pytest
"""

from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

def test_task_mark_complete():
    """mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", 30, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


# ---------------------------------------------------------------------------
# Pet tests
# ---------------------------------------------------------------------------

def test_pet_add_task_increases_count():
    """Adding a task to a pet should increase its task list by one."""
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Feeding", 10, "high"))
    assert len(pet.get_tasks()) == 1


# ---------------------------------------------------------------------------
# Owner tests
# ---------------------------------------------------------------------------

def test_owner_aggregates_tasks_across_pets():
    """get_all_tasks() should return tasks from every pet combined."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    mochi.add_task(Task("Walk", 30, "high"))
    luna.add_task(Task("Feeding", 10, "medium"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    assert len(owner.get_all_tasks()) == 2


# ---------------------------------------------------------------------------
# Scheduler tests
# ---------------------------------------------------------------------------

def test_scheduler_excludes_completed_tasks():
    """generate_schedule() should not include tasks already marked complete."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    walk = Task("Walk", 30, "high")
    feeding = Task("Feeding", 10, "medium")
    feeding.mark_complete()
    pet.add_task(walk)
    pet.add_task(feeding)
    owner.add_pet(pet)

    schedule = Scheduler(owner).generate_schedule()
    assert len(schedule) == 1
    assert schedule[0].title == "Walk"


def test_scheduler_orders_by_priority():
    """generate_schedule() should return high-priority tasks before low ones."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Grooming", 15, "low"))
    pet.add_task(Task("Medication", 5, "high"))
    pet.add_task(Task("Playtime", 20, "medium"))
    owner.add_pet(pet)

    schedule = Scheduler(owner).generate_schedule()
    priorities = [t.priority for t in schedule]
    assert priorities == ["high", "medium", "low"]


# ---------------------------------------------------------------------------
# Phase 4 — filtering
# ---------------------------------------------------------------------------

def test_filter_schedule_returns_only_named_pet_tasks():
    """filter_schedule() should return only tasks belonging to the named pet."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna  = Pet("Luna",  "cat")
    mochi.add_task(Task("Walk", 30, "high"))
    luna.add_task(Task("Feeding", 10, "medium"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    result = Scheduler(owner).filter_schedule("Mochi")
    assert len(result) == 1
    assert result[0].title == "Walk"


def test_filter_schedule_unknown_pet_returns_empty():
    """filter_schedule() should return an empty list for an unknown pet name."""
    owner = Owner("Jordan")
    owner.add_pet(Pet("Mochi", "dog"))
    result = Scheduler(owner).filter_schedule("Ghost")
    assert result == []


def test_filter_schedule_excludes_completed():
    """filter_schedule() should not include completed tasks."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    done = Task("Walk", 30, "high")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task("Feeding", 10, "medium"))
    owner.add_pet(pet)

    result = Scheduler(owner).filter_schedule("Mochi")
    assert len(result) == 1
    assert result[0].title == "Feeding"


# ---------------------------------------------------------------------------
# Phase 4 — recurrence
# ---------------------------------------------------------------------------

def test_reset_daily_tasks_resets_completed_daily_tasks():
    """reset_daily_tasks() should un-complete tasks with recurrence='daily'."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    daily = Task("Walk", 30, "high", recurrence="daily")
    daily.mark_complete()
    pet.add_task(daily)
    owner.add_pet(pet)

    Scheduler(owner).reset_daily_tasks()
    assert daily.completed is False


def test_reset_daily_tasks_leaves_once_tasks_alone():
    """reset_daily_tasks() should not touch tasks with recurrence='once'."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    one_off = Task("Vet visit", 60, "high")  # recurrence defaults to "once"
    one_off.mark_complete()
    pet.add_task(one_off)
    owner.add_pet(pet)

    Scheduler(owner).reset_daily_tasks()
    assert one_off.completed is True


# ---------------------------------------------------------------------------
# Phase 4 — conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_finds_same_time_slot():
    """detect_conflicts() should report tasks sharing the same time_slot."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Walk",    30, "high",   time_slot="08:00"))
    pet.add_task(Task("Feeding", 10, "high",   time_slot="08:00"))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_no_conflicts_when_slots_differ():
    """detect_conflicts() should return empty list when no slots overlap."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Walk",    30, "high", time_slot="08:00"))
    pet.add_task(Task("Feeding", 10, "high", time_slot="09:00"))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts()
    assert warnings == []


def test_detect_conflicts_ignores_completed_tasks():
    """Completed tasks should not be included in conflict checks."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    done = Task("Walk", 30, "high", time_slot="08:00")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task("Feeding", 10, "high", time_slot="08:00"))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts()
    assert warnings == []
