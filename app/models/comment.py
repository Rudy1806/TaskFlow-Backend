from app.extensions import db
from app.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    content = db.Column(
        db.Text,
        nullable=False
    )

    task_id = db.Column(
        db.String(36),
        db.ForeignKey("tasks.id"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    task = db.relationship(
        "Task",
        back_populates="comments"
    )

    user = db.relationship(
        "User",
        back_populates="comments"
    )