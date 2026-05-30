from asyncio import tasks

from flask import Blueprint
from flask import jsonify
from flask import request

from marshmallow import ValidationError

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.models.task import Task

from app.schemas.task_schema import (
    CreateTaskSchema,
    UpdateTaskSchema
)

from app.services.task_service import (
    TaskService
)
from app.models.user import User
task_bp = Blueprint(
    "tasks",
    __name__
)

create_schema = CreateTaskSchema()
update_schema = UpdateTaskSchema()


@task_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
def create_task():

    try:

        data = create_schema.load(
            request.get_json()
        )

        task = TaskService.create_task(
            data,
            get_jwt_identity()
        )

        return jsonify(
            {
                "success": True,
                "message": "Task created",
                "data": {
                    "id": task.id,
                    "title": task.title
                }
            }
        ), 201

    except ValidationError as e:

        return jsonify(
            {
                "success": False,
                "errors": e.messages
            }
        ), 400


@task_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_tasks():
    print("GET TASKS HIT")
    query = Task.query

    status = request.args.get(
        "status"
    )

    priority = request.args.get(
        "priority"
    )

    search = request.args.get(
        "search"
    )

    sort = request.args.get(
        "sort",
        "newest"
    )

    if status:
        query = query.filter(
            Task.status == status
        )

    if priority:
        query = query.filter(
            Task.priority == priority
        )

    if search:
        query = query.filter(
            Task.title.ilike(
                f"%{search}%"
            )
        )

    page = int(
        request.args.get(
            "page",
            1
        )
    )

    limit = int(
        request.args.get(
            "limit",
            10
        )
    )

    if sort == "oldest":
        query = query.order_by(
            Task.created_at.asc()
        )
    else:
        query = query.order_by(
            Task.created_at.desc()
        )

    pagination = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    tasks = []

    tasks = pagination.items

    data = []

    for task in tasks:

        assigned_user = None

        if task.assigned_to:
            assigned_user = User.query.get(
                task.assigned_to
            )

        data.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "status": task.status.value,
                "assigned_to": task.assigned_to,
                "created_by": task.created_by,
                "due_date": task.due_date,
                "created_at": task.created_at,
                "assigned_user_name":
                    assigned_user.name
                    if assigned_user
                    else None
            }
        )

    return jsonify(
        {
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": pagination.total,
                "pages": pagination.pages
            }
        }
)
@task_bp.route(
    "/kanban",
    methods=["GET"]
)
@jwt_required()
def kanban_board():

    pending = []
    in_progress = []
    completed = []

    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(
        created_by=user_id
    ).all()

    for task in tasks:

        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value
        }

        if task.status.value == "PENDING":
            pending.append(task_data)

        elif task.status.value == "IN_PROGRESS":
            in_progress.append(task_data)

        elif task.status.value == "COMPLETED":
            completed.append(task_data)

    return jsonify(
        {
            "success": True,
            "data": {
                "PENDING": pending,
                "IN_PROGRESS": in_progress,
                "COMPLETED": completed
            }
        }
    )

@task_bp.route(
    "/<task_id>",
    methods=["GET"]
)
@jwt_required()
def get_task(task_id):

    task = TaskService.get_task(
        task_id
    )

    if not task:

        return jsonify(
            {
                "success": False,
                "message": "Task not found"
            }
        ), 404

    return jsonify(
        {
            "success": True,
            "data": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority.value
            }
        }
    )


@task_bp.route(
    "/<task_id>",
    methods=["PUT"]
)
@jwt_required()
def update_task(task_id):
    print("UPDATE ROUTE HIT")

    task = TaskService.get_task(
        task_id
    )

    if not task:

        return jsonify(
            {
                "success": False,
                "message": "Task not found"
            }
        ), 404

    try:

        data = update_schema.load(
            request.get_json()
        )

        task = TaskService.update_task(
            task,
            data,
            get_jwt_identity()
        )

        return jsonify(
            {
                "success": True,
                "message": "Task updated"
            }
        )

    except ValidationError as e:

        return jsonify(
            {
                "success": False,
                "errors": e.messages
            }
        ), 400


@task_bp.route(
    "/<task_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_task(task_id):

    task = TaskService.get_task(
        task_id
    )

    if not task:

        return jsonify(
            {
                "success": False,
                "message": "Task not found"
            }
        ), 404

    TaskService.delete_task(
        task,
        get_jwt_identity()
    )

    return jsonify(
        {
            "success": True,
            "message": "Task deleted"
        }
    )