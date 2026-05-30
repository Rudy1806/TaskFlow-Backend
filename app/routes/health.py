from flask import Blueprint, jsonify

health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route(
    "/health",
    methods=["GET"]
)
def health():
    return jsonify(
        {
            "success": True,
            "message": "TaskFlow API Running"
        }
    ), 200