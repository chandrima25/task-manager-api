from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List

from database import engine, SessionLocal, Base
import models
import schemas
import crud
from models import Priority


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Manager API",
    description="""
RESTful API for managing tasks with CRUD operations, filtering,
pagination, priorities, due dates and task statistics.
""",
    version="1.0.0"
)


# Provides a database session to each API request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- CREATE --------------------

@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    tags=["Tasks"]
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    return crud.create_task(db=db, task_data=task)


# -------------------- READ --------------------

@app.get(
    "/tasks",
    response_model=List[schemas.TaskResponse],
    summary="Get all tasks",
    tags=["Tasks"]
)
def get_tasks(
    completed: Optional[bool] = Query(
        None,
        description="Filter tasks by completion status"
    ),
    priority: Optional[Priority] = Query(
        None,
        description="Filter tasks by priority"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of tasks to skip"
    ),
    limit: int = Query(
        100,
        ge=1,
        le=500,
        description="Maximum number of tasks to return"
    ),
    db: Session = Depends(get_db)
):
    return crud.get_tasks(
        db,
        completed=completed,
        priority=priority,
        skip=skip,
        limit=limit
    )


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Get a task by ID",
    tags=["Tasks"]
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = crud.get_task(db, task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


# -------------------- UPDATE --------------------

@app.patch(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Update a task",
    tags=["Tasks"]
)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = crud.update_task(
        db,
        task_id=task_id,
        task_data=task_data
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


# -------------------- DELETE --------------------

@app.delete(
    "/tasks/{task_id}",
    response_model=schemas.MessageResponse,
    summary="Delete a task",
    tags=["Tasks"]
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = crud.delete_task(db, task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return {
        "message": f"Task '{task.title}' deleted successfully",
        "task": task
    }


# -------------------- STATISTICS --------------------

@app.get(
    "/tasks/stats/summary",
    summary="Get task statistics",
    tags=["Stats"]
)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_task_stats(db)


# -------------------- HEALTH CHECK --------------------

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Task Manager API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }