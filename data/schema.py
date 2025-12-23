user_list_schema = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string"}
                },
                "required": ["id", "email", "first_name", "last_name"]
            }
        }
    },
    "required": ["page", "per_page", "total", "total_pages", "data"]
}

error_schema = {
    "type": "object",
    "properties": {
        "error": {"type": "string"}
    },
    "required": ["error"]
}

register_user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "token": {"type": "string"}
    },
    "required": ["id", "token"]
}

update_user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "updatedAt": {"type": "string"}
    },
    "required": ["updatedAt"]
}

single_user_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string"}
            },
            "required": ["id", "email", "first_name", "last_name"]
        }
    },
    "required": ["data"]
}

post_users = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "job": {
            "type": "string"
        }
    },
    "required": [
        "name",
        "job"
    ]
}

put_users = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "job": {
            "type": "string"
        }
    },
    "required": [
        "name",
        "job"
    ]
}