"""
PawPal+ backend system — Phase 4 implementation.

This module defines the four core classes for PawPal+:

    Task      — a single pet care task (dataclass)
    Pet       — a pet and its associated tasks
    Owner     — a pet owner managing one or more pets
    Scheduler — coordinates daily schedule generation, filtering,
                recurrence reset, and conflict detection
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """
    Represents a single pet care task (e.g., morning walk, feeding, medication).

    A dataclass is used here because tasks are simple data records.
    Required fields (no defaults) must come before optional ones.
    """

    title: str
    duration_minutes: int
    priority: str               # "low" | "medium" | "high"
    completed: bool = False
    recurrence: str = "once"    # "once" | "daily" | "weekly"
    time_slot: str = ""         # optional, e.g. "08:00" — used for conflict detection

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

class Pet:
    """
    Represents a pet and the care tasks associated with it.

    Each Pet stores its own task list so that task ownership is always
    clear, even when an owner has multiple pets.
    """

    def __init__(self, name: str, species: str) -> None:
        """
        Initialize a Pet.

        Args:
            name:    The pet's name (e.g., "Mochi").
            species: The type of animal (e.g., "dog", "cat").
        """
        self.name: str = name
        self.species: str = species
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """
        Add a care task to this pet.

        Args:
            task: A Task instance to associate with this pet.
        """
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks registered for this pet."""
        return self.tasks


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    """
    Represents the pet owner and manages their pets.

    Owner is the top-level object in the system. The Scheduler accesses
    all task data through Owner so there is a single source of truth.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize an Owner.

        Args:
            name: The owner's name (e.g., "Jordan").
        """
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """
        Register a pet under this owner.

        Args:
            pet: A Pet instance to add.
        """
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """
        Aggregate and return all tasks across every pet owned.

        This is the single access point used by Scheduler,
        so task data is never duplicated outside of Pet.
        """
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """
    Coordinates daily schedule generation for an owner's pets.

    Scheduler depends on Owner to access task data. It does not store
    tasks itself — all task data lives in the Owner/Pet hierarchy.
    """

    def __init__(self, owner: Owner) -> None:
        """
        Initialize the Scheduler with an Owner.

        Args:
            owner: The Owner whose pets and tasks will be scheduled.
        """
        self.owner: Owner = owner

    def generate_schedule(self) -> List[Task]:
        """
        Select and order tasks to build a daily care plan.

        Steps:
        1. Retrieve all tasks from every pet via owner.get_all_tasks().
        2. Drop any tasks already marked complete.
        3. Sort by priority (high first), then by duration (shorter first)
           so that urgent tasks always appear at the top.

        Returns:
            A list of pending Task objects in priority order.
        """
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        return sorted(pending, key=lambda t: (priority_order.get(t.priority, 3), t.duration_minutes))

    def filter_schedule(self, pet_name: str) -> List[Task]:
        """
        Return the pending tasks for a single named pet, sorted by priority.

        Args:
            pet_name: The name of the pet whose tasks should be returned.

        Returns:
            A sorted list of pending Task objects for that pet,
            or an empty list if the pet is not found.
        """
        priority_order = {"high": 0, "medium": 1, "low": 2}
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                pending = [t for t in pet.get_tasks() if not t.completed]
                return sorted(pending, key=lambda t: (priority_order.get(t.priority, 3), t.duration_minutes))
        return []

    def detect_conflicts(self) -> List[str]:
        """
        Find tasks that share the same non-empty time_slot.

        Two pending tasks scheduled at the same time slot are a conflict.
        Returns human-readable warning strings rather than raising errors.

        Returns:
            A list of warning strings, one per conflict pair found.
            An empty list means no conflicts were detected.
        """
        warnings: List[str] = []
        seen: dict = {}  # time_slot -> title of first task seen there
        for task in self.owner.get_all_tasks():
            if task.time_slot and not task.completed:
                if task.time_slot in seen:
                    warnings.append(
                        f"Conflict at {task.time_slot}: '{seen[task.time_slot]}' and '{task.title}'"
                    )
                else:
                    seen[task.time_slot] = task.title
        return warnings

    def reset_daily_tasks(self) -> None:
        """
        Reset the completed flag on all daily recurring tasks.

        Call this at the start of a new day. Tasks with recurrence="once"
        or recurrence="weekly" are not affected.
        """
        for task in self.owner.get_all_tasks():
            if task.completed and task.recurrence == "daily":
                task.completed = False
