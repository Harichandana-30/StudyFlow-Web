
import streamlit as st
from database import (
    create_database,
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    search_tasks
)
from datetime import datetime
import os

st.set_page_config(
    page_title="StudyFlow",
    layout="wide"
)

create_database()


# ---------------- STREAK ----------------
if not os.path.exists("streak.txt"):
    with open("streak.txt", "w") as file:
        file.write("0")


def get_streak():
    with open("streak.txt", "r") as file:
        return int(file.read())


def update_streak():
    streak = get_streak() + 1

    with open("streak.txt", "w") as file:
        file.write(str(streak))


# ---------------- TASK DATA ----------------
tasks = get_tasks()

total_tasks = len(tasks)
completed_tasks = len(
    [task for task in tasks if task[4] == "Completed"]
)
pending_tasks = total_tasks - completed_tasks

progress = (
    completed_tasks / total_tasks
    if total_tasks > 0 else 0
)

# ---------------- HEADER ----------------
st.title("📚 StudyFlow")
st.subheader("Smart Study Planner")

# ---------------- DASHBOARD ----------------
col1, col2, col3 = st.columns(3)

col1.metric("📌 Total Tasks", total_tasks)
col2.metric("✅ Completed", completed_tasks)
col3.metric("⏳ Pending", pending_tasks)

st.progress(progress)

st.write(
    f"### Progress: {int(progress * 100)}% Completed"
)

st.write(
    f"🔥 Study Streak: {get_streak()} Days"
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Add Study Task")

task = st.sidebar.text_input(
    "Task"
)

subject = st.sidebar.text_input(
    "Subject"
)

deadline = st.sidebar.date_input(
    "Deadline"
)

if st.sidebar.button("Add Task"):

    if task and subject:

        add_task(
            task,
            subject,
            deadline.strftime("%d-%m-%Y")
        )

        st.success("Task Added!")

        st.rerun()

# ---------------- SEARCH ----------------
st.subheader("🔍 Search Tasks")

search_subject_input = st.text_input(
    "Search by Subject"
)

if search_subject_input:
    filtered_tasks = search_tasks(
        search_subject_input
    )
else:
    filtered_tasks = tasks

# ---------------- DEADLINE WARNING ----------------
today = datetime.today()

for task_item in tasks:

    try:
        deadline_date = datetime.strptime(
            task_item[3],
            "%d-%m-%Y"
        )

        days_left = (
            deadline_date - today
        ).days

        if (
            days_left <= 2
            and task_item[4] != "Completed"
        ):

            st.warning(
                f"⚠ Upcoming Deadline: "
                f"{task_item[1]}"
            )

            break

    except:
        pass

# ---------------- TASK LIST ----------------
st.subheader("📋 Your Study Tasks")

for task_item in filtered_tasks:

    with st.container():

        st.write(
            f"**ID:** {task_item[0]}"
        )

        st.write(
            f"**Task:** {task_item[1]}"
        )

        st.write(
            f"**Subject:** {task_item[2]}"
        )

        st.write(
            f"**Deadline:** {task_item[3]}"
        )

        status_color = (
            "🟢"
            if task_item[4] == "Completed"
            else "🔴"
        )

        st.write(
            f"**Status:** "
            f"{status_color} {task_item[4]}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                f"Complete {task_item[0]}"
            ):

                complete_task(
                    task_item[0]
                )

                update_streak()

                st.success(
                    "Task Completed!"
                )

                st.rerun()

        with col2:
            if st.button(
                f"Delete {task_item[0]}"
            ):

                delete_task(
                    task_item[0]
                )

                st.warning(
                    "Task Deleted!"
                )

                st.rerun()

        st.divider()
