import streamlit as st
import requests

API_URL = "https://task-manager-api-2pyu.onrender.com"

st.set_page_config(page_title="Task Manager")
st.title("Task Manager")
st.write("Manage your tasks using the FastAPI backend.")

# -------------------- CREATE TASK --------------------

st.header("Create a New Task")

title = st.text_input("Task Title")
description = st.text_area("Description")
priority = st.selectbox("Priority", ["low", "medium", "high"])
due_date = st.text_input("Due Date", placeholder="2026-12-31T18:00:00")

if st.button("Create Task"):
    if not title:
        st.warning("Please enter a task title.")
    else:
        task_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date if due_date else None
        }
        try:
            response = requests.post(f"{API_URL}/tasks", json=task_data)
            if response.status_code == 201:
                st.success("Task created successfully!")
                st.rerun()
            else:
                st.error(f"Failed: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")

# -------------------- VIEW TASKS --------------------

st.header("Your Tasks")

col1, col2 = st.columns(2)
with col1:
    filter_status = st.selectbox("Status", ["All", "Incomplete", "Completed"])
with col2:
    filter_priority = st.selectbox("Priority", ["All", "low", "medium", "high"])

params = {}
if filter_status == "Completed":
    params["completed"] = True
elif filter_status == "Incomplete":
    params["completed"] = False
if filter_priority != "All":
    params["priority"] = filter_priority

try:
    response = requests.get(f"{API_URL}/tasks", params=params)
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            st.info("No tasks yet.")
        else:
            for task in tasks:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([6, 2, 2])
                    with col1:
                        st.subheader(task["title"])
                        st.write(f"**Description:** {task['description'] or 'None'}")
                        st.write(f"**Priority:** {task['priority']}")
                        st.write(f"**Status:** {'Completed' if task['completed'] else 'Incomplete'}")
                        st.write(f"**Due Date:** {task['due_date'] or 'Not set'}")
                    with col2:
                        if task["completed"]:
                            if st.button("Undo", key=f"undo_{task['id']}"):
                                requests.patch(f"{API_URL}/tasks/{task['id']}", json={"completed": False})
                                st.rerun()
                        else:
                            if st.button("Done", key=f"done_{task['id']}"):
                                requests.patch(f"{API_URL}/tasks/{task['id']}", json={"completed": True})
                                st.rerun()
                    with col3:
                        if st.button("Delete", key=f"del_{task['id']}"):
                            requests.delete(f"{API_URL}/tasks/{task['id']}")
                            st.rerun()
    else:
        st.error("Could not fetch tasks.")
except Exception as e:
    st.error(f"Could not connect to API: {e}")

# -------------------- STATS --------------------

st.divider()
st.header("Stats")

try:
    response = requests.get(f"{API_URL}/tasks/stats/summary")
    if response.status_code == 200:
        stats = response.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", stats["total"])
        col2.metric("Completed", stats["completed"])
        col3.metric("Pending", stats["pending"])
        col4.metric("Completion Rate", f"{stats['completion_rate']}%")
except Exception as e:
    st.error(f"Could not load stats: {e}")