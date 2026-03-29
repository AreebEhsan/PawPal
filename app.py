import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant.")

# ---------------------------------------------------------------------------
# Session state — initialise once, persist across reruns
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Section 1 — Owner
# ---------------------------------------------------------------------------
st.subheader("Owner")

owner_name_input = st.text_input("Owner name", value=owner.name)
if owner_name_input.strip() and owner_name_input.strip() != owner.name:
    owner.name = owner_name_input.strip()

st.caption(f"Managing schedule for: **{owner.name}**")

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — Add a pet
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")

col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", key="new_pet_name")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet"):
    name = new_pet_name.strip()
    if not name:
        st.warning("Please enter a pet name.")
    elif name.lower() in [p.name.lower() for p in owner.pets]:
        st.warning(f"A pet named '{name}' already exists.")
    else:
        owner.add_pet(Pet(name, new_pet_species))
        st.success(f"Added {name} the {new_pet_species}!")

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Add a task
# ---------------------------------------------------------------------------
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names, key="task_pet_select")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20, key="task_duration")
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"], key="task_priority")

    if st.button("Add task"):
        title = task_title.strip()
        if not title:
            st.warning("Please enter a task title.")
        else:
            target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
            target_pet.add_task(Task(title, int(duration), priority))
            st.success(f"Added '{title}' to {selected_pet_name}.")

st.divider()

# ---------------------------------------------------------------------------
# Section 4 — Current pets and tasks
# ---------------------------------------------------------------------------
st.subheader("Pets & Tasks")

if not owner.pets:
    st.info("No pets added yet.")
else:
    for pet in owner.pets:
        tasks = pet.get_tasks()
        label = f"{pet.name} ({pet.species}) — {len(tasks)} task(s)"
        with st.expander(label, expanded=True):
            if not tasks:
                st.caption("No tasks yet.")
            else:
                st.table(
                    [
                        {
                            "Task": t.title,
                            "Duration (min)": t.duration_minutes,
                            "Priority": t.priority,
                            "Done": "Yes" if t.completed else "No",
                        }
                        for t in tasks
                    ]
                )

st.divider()

# ---------------------------------------------------------------------------
# Section 5 — Generate schedule
# ---------------------------------------------------------------------------
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add at least one pet and task first.")
    else:
        schedule = Scheduler(owner).generate_schedule()
        if not schedule:
            st.info("No pending tasks to schedule. All tasks may already be completed.")
        else:
            st.success(f"Daily plan for {owner.name} — {len(schedule)} task(s), sorted by priority")
            st.table(
                [
                    {
                        "Priority": t.priority.upper(),
                        "Task": t.title,
                        "Duration (min)": t.duration_minutes,
                    }
                    for t in schedule
                ]
            )
