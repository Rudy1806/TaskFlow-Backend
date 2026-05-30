from app.extensions import db

from app.models.task import Task
from app.models.user import User
from app.models.activity_log import ActivityLog

from app.models.task_enums import (
    TaskPriority,
    TaskStatus
)
from app.services.notification_service import NotificationService

class TaskService:

    @staticmethod
    def create_activity(user_id, task_id, action):
        activity = ActivityLog(
            user_id=user_id,
            task_id=task_id,
            action=action
        )

        db.session.add(activity)
        db.session.commit()

    @staticmethod
    def create_task(data, user_id):

        task = Task(
            title=data["title"],
            description=data.get("description"),
            priority=TaskPriority(
                data["priority"]
            ),
            status=TaskStatus(
                data.get(
                    "status",
                    "PENDING"
                )
            ),
            due_date=data.get("due_date"),
            assigned_to=data.get("assigned_to"),
            created_by=user_id
        )

        db.session.add(task)
        db.session.commit()

        TaskService.create_activity(
            user_id=user_id,
            task_id=task.id,
            action="TASK_CREATED"
        )

        NotificationService.create_notification(
            user_id=user_id,
            title="Task Created",
            message=f"{task.title} was created"
        )

        return task

    @staticmethod
    def get_task(task_id):
        return db.session.get(
            Task,
            task_id
        )

    @staticmethod
    def update_task(task, data, user_id):

        old_assignee = task.assigned_to

        for key, value in data.items():

            if key == "priority":
                value = TaskPriority(value)

            if key == "status":
                value = TaskStatus(value)

            setattr(task, key, value)

        db.session.commit()

        TaskService.create_activity(
            user_id=user_id,
            task_id=task.id,
            action="TASK_UPDATED"
        )

        if (
            "assigned_to" in data
            and data["assigned_to"] != old_assignee
        ):
            TaskService.create_activity(
                user_id=user_id,
                task_id=task.id,
                action="TASK_ASSIGNED"
            )

        if (
            "status" in data
            and data["status"] == "COMPLETED"
        ):
            TaskService.create_activity(
                user_id=user_id,
                task_id=task.id,
                action="TASK_COMPLETED"
            )
            NotificationService.create_notification(
                user_id=user_id,
                title="Task Updated",
                message=f"{task.title} was updated"
            )

        return task

    @staticmethod
    def delete_task(task, user_id):

        task_id = task.id

        TaskService.create_activity(
            user_id=user_id,
            task_id=task_id,
            action="TASK_DELETED"
        )

        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def get_user(user_id):
        return db.session.get(
            User,
            user_id
        )