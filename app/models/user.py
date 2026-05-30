from app.extensions import db
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.Text,
        nullable=False
    )

    avatar_url = db.Column(
        db.Text,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_tasks = db.relationship(
        "Task",
        foreign_keys="Task.created_by",
        back_populates="creator",
        lazy=True
    )

    assigned_tasks = db.relationship(
        "Task",
        foreign_keys="Task.assigned_to",
        back_populates="assignee",
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    provider = db.Column(
    db.String(50),
    nullable=False,
    default="local"
    )

    google_id = db.Column(
        db.String(255),
        unique=True,
        nullable=True
    )