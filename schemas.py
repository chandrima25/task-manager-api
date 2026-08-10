from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from models import Priority


# Schema used when creating a new task.
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title"
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task details"
    )

    priority: Priority = Field(
        Priority.medium,
        description="Task priority: low, medium, high"
    )

    due_date: Optional[datetime] = Field(
        None,
        description="Optional task deadline"
    )



class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200
    )

    description: Optional[str] = Field(
        None,
        max_length=1000
    )

    completed: Optional[bool] = None

    priority: Optional[Priority] = None

    due_date: Optional[datetime] = None


# Schema used when returning task data through the API.
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    created_at: datetime
    due_date: Optional[datetime]

    # Allows Pydantic to create the response from a SQLAlchemy model object.
    model_config = {"from_attributes": True}


# Schema used for responses that contain a message and optional task data.
class MessageResponse(BaseModel):
    message: str
    task: Optional[TaskResponse] = None