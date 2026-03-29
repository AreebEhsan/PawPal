"""
PawPal+ tests — Phase 2.

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
