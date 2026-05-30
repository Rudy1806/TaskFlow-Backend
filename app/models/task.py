from app.extensions import db

from app.models.base import BaseModel
from app.models.task_enums import (
    TaskPriority,
    TaskStatus
)


class Task(BaseModel):
    __tablename__ = "tasks"

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.Enum(TaskPriority),
        nullable=False,
        default=TaskPriority.MEDIUM
    )

    status = db.Column(
        db.Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )

    due_date = db.Column(
        db.DateTime,
        nullable=True
    )

    assigned_to = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    created_by = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    creator = db.relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks"
    )

    assignee = db.relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_tasks"
    )

    comments = db.relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="task",
        cascade="all, delete-orphan"
    )