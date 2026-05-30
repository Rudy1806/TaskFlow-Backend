from marshmallow import Schema, fields, validate


class CreateTaskSchema(Schema):
    title = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255)
    )

    description = fields.String(
        allow_none=True
    )

    priority = fields.String(
        required=True,
        validate=validate.OneOf(
            ["LOW", "MEDIUM", "HIGH"]
        )
    )

    status = fields.String(
        required=False,
        validate=validate.OneOf(
            ["PENDING", "IN_PROGRESS", "COMPLETED"]
        )
    )

    due_date = fields.DateTime(
        required=False
    )

    assigned_to = fields.String(
        required=False,
        allow_none=True
    )


class UpdateTaskSchema(Schema):
    title = fields.String()

    description = fields.String()

    priority = fields.String(
        validate=validate.OneOf(
            ["LOW", "MEDIUM", "HIGH"]
        )
    )

    status = fields.String(
        validate=validate.OneOf(
            ["PENDING", "IN_PROGRESS", "COMPLETED"]
        )
    )

    due_date = fields.DateTime()

    assigned_to = fields.String(
        allow_none=True
    )