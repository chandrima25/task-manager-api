import streamlit as st
import requests


API_URL =  "https://task-manager-api-2pyu.onrender.com"

st.set_page_config(page_title="Task Manager")
st.title("Task Manager")
st.write("Manage your tasks using the FastAPI backend.")

# -------------------- CREATE TASK --------------------

st.header("Create a New Task")

title = st.text_input("Task Title")
description = st.text_area("Description")
priority = st.selectbox("Priority", ["low", "medium", "high"])
due_date = st.text_input("Due Date", placeholder="2026-12-31T18:00:00")

if st.button(" Create Task"):
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
                st.error(f"Failed to create task: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to the API: {e}")

# -------------------- VIEW TASKS --------------------

st.header("Your Tasks")

try:
    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            st.info("No tasks yet. Create one above!")
        else:
            for task in tasks:
                with st.container(border=True):
                    st.subheader(task["title"])
                    st.write(f"**Description:** {task['description'] or 'None'}")
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Completed:** {'✅' if task['completed'] else '❌'}")
                    st.write(f"**Due Date:** {task['due_date'] or 'Not set'}")
    else:
        st.error("Could not fetch tasks.")
except Exception as e:
    st.error(f"Could not connect to the API: {e}")