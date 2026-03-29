"""
PawPal+ CLI demo — Phase 2.

Run with:  python main.py

This script creates a sample owner, two pets, and several tasks, then
uses the Scheduler to produce and print a daily care plan.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    # --- Set up owner ---
    owner = Owner("Jordan")

    # --- Create pets ---
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    # --- Add tasks to Mochi ---
    mochi.add_task(Task("Morning walk",  30, "high"))
    mochi.add_task(Task("Feeding",       10, "high"))
    mochi.add_task(Task("Playtime",      20, "medium"))

    # --- Add tasks to Luna ---
    luna.add_task(Task("Feeding",        10, "high"))
    luna.add_task(Task("Grooming",       15, "low"))

    # --- Register pets with owner ---
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # --- Generate schedule ---
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()

    # --- Print schedule ---
    print(f"\nPawPal+ — Daily Schedule for {owner.name}")
    print("=" * 42)

    if not schedule:
        print("  No tasks scheduled for today.")
    else:
        for i, task in enumerate(schedule, start=1):
            print(f"  {i}. [{task.priority.upper():6}] {task.title:<20} {task.duration_minutes} min")

    print("=" * 42)
    print(f"  Total: {len(schedule)} task(s)\n")


if __name__ == "__main__":
    main()
