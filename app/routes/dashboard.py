from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.models.task import Task
from app.models.activity_log import ActivityLog
from app.models.task_enums import TaskStatus

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route(
    "/stats",
    methods=["GET"]
)
@jwt_required()
def dashboard_stats():

    user_id = get_jwt_identity()

    print("=" * 50)
    print("JWT USER:", user_id)
    print("=" * 50)

    tasks = Task.query.all()

    print("ALL TASKS:")
    for task in tasks:
        print(
            task.id,
            task.created_by,
            task.title
        )

    total_tasks = Task.query.filter_by(
        created_by=user_id
    ).count()

    pending_tasks = Task.query.filter(
        Task.created_by == user_id,
        Task.status == TaskStatus.PENDING
    ).count()

    in_progress_tasks = Task.query.filter(
        Task.created_by == user_id,
        Task.status == TaskStatus.IN_PROGRESS
    ).count()

    completed_tasks = Task.query.filter(
        Task.created_by == user_id,
        Task.status == TaskStatus.COMPLETED
    ).count()

    print("TOTAL FOUND:", total_tasks)

    print("JWT USER:", repr(user_id))
    print("JWT TYPE:", type(user_id))

    for task in tasks:
        print(
            "TASK USER:",
            repr(task.created_by),
            type(task.created_by)
        )

    return jsonify(
        {
            "success": True,
            "data": {
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "in_progress_tasks": in_progress_tasks,
                "completed_tasks": completed_tasks
            }
        }
    )

@dashboard_bp.route(
    "/recent-activity",
    methods=["GET"]
)
@jwt_required()
def recent_activity():

    user_id = get_jwt_identity()

    print("JWT USER:", repr(user_id))
    print("JWT TYPE:", type(user_id))

    activities = (
        ActivityLog.query
        .filter_by(user_id=user_id)
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    data = []

    for activity in activities:

        data.append(
            {
                "id": activity.id,
                "action": activity.action,
                "task_id": activity.task_id,
                "created_at": activity.created_at
            }
        )

    return jsonify(
        {
            "success": True,
            "data": data
        }
    )


@dashboard_bp.route(
    "/upcoming-tasks",
    methods=["GET"]
)
@jwt_required()
def upcoming_tasks():

    user_id = get_jwt_identity()

    tasks = (
        Task.query
        .filter(
            Task.created_by == user_id,
            Task.status != TaskStatus.COMPLETED
        )
        .order_by(
            Task.due_date.asc()
        )
        .limit(5)
        .all()
    )

    data = []

    for task in tasks:

        data.append(
            {
                "id": task.id,
                "title": task.title,
                "status": task.status.value,
                "priority": task.priority.value,
                "due_date": task.due_date
            }
        )

    print(
        "FIRST TASK USER:",
        repr(tasks[0].created_by)
    )
    print(
        "FIRST TASK TYPE:",
        type(tasks[0].created_by)
    )

    return jsonify(
        {
            "success": True,
            "data": data
        }
    )