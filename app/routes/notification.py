from flask import Blueprint
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.models.notification import Notification

from app.services.notification_service import (
    NotificationService
)

notification_bp = Blueprint(
    "notifications",
    __name__
)


@notification_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_notifications():

    user_id = get_jwt_identity()

    notifications = (
        NotificationService
        .get_user_notifications(user_id)
    )

    data = []

    for notification in notifications:

        data.append(
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at
            }
        )

    return jsonify(
        {
            "success": True,
            "data": data
        }
    )


@notification_bp.route(
    "/<notification_id>/read",
    methods=["PUT"]
)
@jwt_required()
def mark_read(notification_id):

    notification = (
        Notification.query.get(
            notification_id
        )
    )

    if not notification:

        return jsonify(
            {
                "success": False,
                "message": "Notification not found"
            }
        ), 404

    NotificationService.mark_as_read(
        notification
    )

    return jsonify(
        {
            "success": True,
            "message": "Notification marked as read"
        }
    )


@notification_bp.route(
    "/read-all",
    methods=["PUT"]
)
@jwt_required()
def mark_all_read():

    user_id = get_jwt_identity()

    count = (
        NotificationService
        .mark_all_as_read(user_id)
    )

    return jsonify(
        {
            "success": True,
            "message": f"{count} notifications updated"
        }
    )