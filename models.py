from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from database import Base
from datetime import datetime, timezone
import enum


# Defines the allowed priority values for a task.
class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


# SQLAlchemy model representing the tasks table.
class Task(Base):
    __tablename__ = "tasks"

    # Unique identifier for each task.
    id = Column(Integer, primary_key=True, index=True)

    # Required task title.
    title = Column(String, nullable=False, index=True)

    # Optional additional information about the task.
    description = Column(String, nullable=True)

    # New tasks are incomplete by default.
    completed = Column(Boolean, default=False, nullable=False)

    # Tasks have low, medium, or high priority.
    priority = Column(
        Enum(Priority),
        default=Priority.medium,
        nullable=False
    )

    # Automatically stores when the task was created.
    # Store creation time in UTC.
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # Optional deadline for completing the task.
    due_date = Column(DateTime, nullable=True)