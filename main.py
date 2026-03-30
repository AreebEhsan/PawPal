"""
PawPal+ CLI demo — Phase 4.

Run with:  python main.py

Demonstrates:
  - Sorting by priority and duration
  - Filtering the schedule by pet name
  - Recurrence: resetting daily tasks at the start of a new day
  - Conflict detection: warning when two tasks share a time slot
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(label: str, schedule: list) -> None:
    print(f"\n{label}")
    print("-" * 44)
    if not schedule:
        print("  (no pending tasks)")
    else:
        for i, task in enumerate(schedule, start=1):
            slot = f" @ {task.time_slot}" if task.time_slot else ""
            recur = f" [{task.recurrence}]" if task.recurrence != "once" else ""
            print(f"  {i}. [{task.priority.upper():6}] {task.title:<22} {task.duration_minutes} min{slot}{recur}")
    print("-" * 44)


def main() -> None:
    # --- Setup ---
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog")
    luna  = Pet("Luna",  "cat")

    # Mochi's tasks — note two tasks share time slot "08:00" (conflict)
    mochi.add_task(Task("Morning walk",  30, "high",   time_slot="08:00", recurrence="daily"))
    mochi.add_task(Task("Feeding",       10, "high",   time_slot="08:00", recurrence="daily"))
    mochi.add_task(Task("Playtime",      20, "medium", time_slot="17:00"))

    # Luna's tasks
    luna.add_task(Task("Feeding",        10, "high",   time_slot="09:00", recurrence="daily"))
    luna.add_task(Task("Grooming",       15, "low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    # --- 1. Full sorted schedule ---
    print_schedule(f"Full schedule for {owner.name}", scheduler.generate_schedule())

    # --- 2. Filtered: Mochi only ---
    print_schedule("Filtered: Mochi's tasks only", scheduler.filter_schedule("Mochi"))

    # --- 3. Filtered: Luna only ---
    print_schedule("Filtered: Luna's tasks only", scheduler.filter_schedule("Luna"))

    # --- 4. Conflict detection ---
    print("\nConflict check")
    print("-" * 44)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  WARNING: {warning}")
    else:
        print("  No conflicts detected.")
    print("-" * 44)

    # --- 5. Recurrence: mark daily tasks complete, then reset ---
    print("\nRecurrence demo")
    print("-" * 44)
    # Mark Mochi's daily tasks complete (simulating end-of-day)
    for task in mochi.get_tasks():
        if task.recurrence == "daily":
            task.mark_complete()
    print("  Marked Mochi's daily tasks as complete.")
    print(f"  Pending tasks before reset: {len(scheduler.generate_schedule())}")

    # Reset daily tasks (simulating next morning)
    scheduler.reset_daily_tasks()
    print("  Called reset_daily_tasks() — new day begins.")
    print(f"  Pending tasks after reset:  {len(scheduler.generate_schedule())}")
    print("-" * 44)


if __name__ == "__main__":
    main()
