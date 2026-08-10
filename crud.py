from sqlalchemy.orm import Session
from typing import Optional, List

from models import Task, Priority
from schemas import TaskCreate, TaskUpdate


# CREATE
def create_task(db: Session, task_data: TaskCreate) -> Task:
    # Convert the validated Pydantic schema into a SQLAlchemy model.
    db_task = Task(**task_data.model_dump())

    db.add(db_task)
    db.commit()

    # Refresh the object to get database-generated values such as the ID.
    db.refresh(db_task)

    return db_task


# READ - single task
def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


# READ - multiple tasks
def get_tasks(
    db: Session,
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Task]:

    query = db.query(Task)

    # Apply filters only when the corresponding parameter is provided.
    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    # Return newest tasks first and support pagination.
    return (
        query
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate
) -> Optional[Task]:

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    # Only update fields that were included in the PATCH request.
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task



def delete_task(db: Session, task_id: int) -> Optional[Task]:
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    db.delete(task)
    db.commit()

    return task


# TASK STATISTICS
def get_task_stats(db: Session) -> dict:
    total = db.query(Task).count()

    completed = (
        db.query(Task)
        .filter(Task.completed == True)
        .count()
    )

    pending = total - completed

    high_priority = (
        db.query(Task)
        .filter(
            Task.priority == Priority.high,
            Task.completed == False
        )
        .count()
    )

    completion_rate = (
        round((completed / total) * 100, 1)
        if total > 0
        else 0.0
    )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority_pending": high_priority,
        "completion_rate": completion_rate
    }