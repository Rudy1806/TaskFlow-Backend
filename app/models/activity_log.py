from app.extensions import db
from app.models.base import BaseModel


class ActivityLog(BaseModel):
    __tablename__ = "activity_logs"

    action = db.Column(
        db.String(255),
        nullable=False
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    task_id = db.Column(
        db.String(36),
        db.ForeignKey("tasks.id"),
        nullable=False,
        index=True
    )

    user = db.relationship(
        "User",
        back_populates="activity_logs"
    )

    task = db.relationship(
        "Task",
        back_populates="activity_logs"
    )