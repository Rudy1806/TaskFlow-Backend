from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)

from marshmallow import ValidationError

from app.models.user import User

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema
)

from app.services.auth_service import (
    AuthService
)

auth_bp = Blueprint(
    "auth",
    __name__
)

register_schema = RegisterSchema()

login_schema = LoginSchema()


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    try:

        data = register_schema.load(
            request.get_json()
        )

        user = AuthService.register(
            data
        )

        return jsonify(
            {
                "success": True,
                "message": "User registered",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
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

    except ValueError as e:

        return jsonify(
            {
                "success": False,
                "message": str(e)
            }
        ), 400


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        data = login_schema.load(
            request.get_json()
        )

        result = AuthService.login(
            data["email"],
            data["password"]
        )

        return jsonify(
            {
                "success": True,
                "access_token": result["access_token"],
                "refresh_token": result["refresh_token"],
                "user": {
                    "id": result["user"].id,
                    "name": result["user"].name,
                    "email": result["user"].email
                }
            }
        )

    except ValidationError as e:

        return jsonify(
            {
                "success": False,
                "errors": e.messages
            }
        ), 400

    except ValueError as e:

        return jsonify(
            {
                "success": False,
                "message": str(e)
            }
        ), 401


@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = User.query.get(
        user_id
    )

    return jsonify(
        {
            "success": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "avatar_url": user.avatar_url
            }
        }
    )


@auth_bp.route(
    "/refresh",
    methods=["POST"]
)
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    access_token = create_access_token(
        identity=user_id
    )

    return jsonify(
        {
            "access_token": access_token
        }
    )