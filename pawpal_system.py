"""
PawPal+ backend system — Phase 1 class skeletons.

This module defines the four core classes for PawPal+:

    Task      — a single pet care task (dataclass)
    Pet       — a pet and its associated tasks
    Owner     — a pet owner managing one or more pets
    Scheduler — coordinates daily schedule generation

Phase 1: class skeletons with type hints and docstrings only.
         Method bodies are stubs (pass) to be filled in Phase 2.
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
    priority: str           # "low" | "medium" | "high"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass


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
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks registered for this pet."""
        pass


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
        pass

    def get_all_tasks(self) -> List[Task]:
        """
        Aggregate and return all tasks across every pet owned.

        This is the single access point used by Scheduler,
        so task data is never duplicated outside of Pet.
        """
        pass


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

        Phase 2 will implement the actual logic. Expected behavior:
        - Retrieve all tasks via owner.get_all_tasks()
        - Sort or filter by priority and duration
        - Return an ordered list representing today's plan

        Returns:
            A list of Task objects representing the daily schedule.
        """
        pass
