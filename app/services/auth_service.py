from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app.extensions import db
from app.models.user import User


class AuthService:

    @staticmethod
    def register(data):

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            raise ValueError(
                "Email already exists"
            )

        user = User(
            name=data["name"],
            email=data["email"],
            password_hash=generate_password_hash(
                data["password"]
            )
        )

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def login(email, password):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        if not check_password_hash(
            user.password_hash,
            password
        ):
            raise ValueError(
                "Invalid credentials"
            )

        access_token = create_access_token(
            identity=user.id
        )

        refresh_token = create_refresh_token(
            identity=user.id
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }