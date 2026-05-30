from app.extensions import db
from app.models.notification import Notification


class NotificationService:

    @staticmethod
    def create_notification(
        user_id,
        title,
        message
    ):

        notification = Notification(
            user_id=user_id,
            title=title,
            message=message
        )

        db.session.add(notification)
        db.session.commit()

        return notification

    @staticmethod
    def get_user_notifications(user_id):

        return (
            Notification.query
            .filter_by(user_id=user_id)
            .order_by(
                Notification.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def mark_as_read(notification):

        notification.is_read = True

        db.session.commit()

        return notification

    @staticmethod
    def mark_all_as_read(user_id):

        notifications = (
            Notification.query
            .filter_by(
                user_id=user_id,
                is_read=False
            )
            .all()
        )

        for notification in notifications:
            notification.is_read = True

        db.session.commit()

        return len(notifications)