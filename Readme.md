# 📋 Task Manager API

A REST API for task management, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

> Built as a portfolio project to demonstrate REST API design, Python backend development, and separation of API and database logic.

---

## Features

- ✅ **Full CRUD** — Create, Read, Update, Delete tasks
- 🏷️ **Task Priorities** — low / medium / high
- 📅 **Due Dates** — with ISO datetime support
- 🔍 **Filtering** — filter tasks by completion status or priority
- 📄 **Pagination** — skip/limit query parameters
- 📊 **Stats Endpoint** — completion rates and summary metrics
- 🧾 **Auto-generated API docs** — Swagger UI at `/docs`
- ✔️ **Input Validation** — via Pydantic v2
- 🔒 **Proper HTTP Status Codes** — 201, 404, 422

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI 0.115 |
| ORM | SQLAlchemy 2.0 |
| Database          | SQLite |
| Validation | Pydantic v2 |
| Server | Uvicorn (ASGI) |

---

## Project Structure

```
task-manager-api/
├── main.py           # FastAPI app — routes and HTTP logic
├── database.py       # Database connection setup
├── models.py         # SQLAlchemy table definitions
├── schemas.py        # Pydantic request/response schemas
├── crud.py           # Database operations (Create/Read/Update/Delete)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/Chandrima25/task-manager-api.git
cd task-manager-api

# 2. Create a virtual environment
python -m venv venv
# Mac/Linux
source venv/bin/activate        
# Windows
venv\Scripts\activate         

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | Get all tasks (with optional filters) |
| `GET` | `/tasks/{id}` | Get a task by ID |
| `PATCH` | `/tasks/{id}` | Partially update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/tasks/stats/summary` | Get task statistics |

### Query Parameters (GET /tasks)

| Parameter | Type | Description |
|---|---|---|
| `completed` | boolean | Filter by completion status |
| `priority` | string | Filter by priority (low/medium/high) |
| `skip` | integer | Pagination offset (default: 0) |
| `limit` | integer | Max results (default: 100, max: 500) |

---

## Example Requests

**Create a task:**
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
-d '{"title": "Buy groceries", "priority": "high", "due_date": "2026-12-31T00:00:00"}'
```

**Get incomplete high-priority tasks:**
```bash
curl "http://localhost:8000/tasks?completed=false&priority=high"
```

**Mark a task as done:**
```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

---

## What I Learned

- Designing a REST API with proper HTTP methods and status codes
- Using SQLAlchemy ORM to interact with databases without writing raw SQL
- Pydantic v2 data validation and the separation of input/output schemas
- FastAPI's dependency injection system (`Depends`)
- Clean separation between API routes (`main.py`) and database operations (`crud.py`)
- Partial updates with `PATCH` and `exclude_unset=True`
- Building pagination and dynamic query filtering

---

## Future Improvements

- [ ] Add JWT authentication (user accounts)
- [ ] Switch to PostgreSQL for production
- [ ] Write unit tests with `pytest`
- [ ] Deploy to Railway or Render
- [ ] Add task categories/tags

---

*Made  using FastAPI*