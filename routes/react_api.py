from flask import Blueprint, request, jsonify

# Create the Blueprint
react_api = Blueprint('react_api', __name__)

@react_api.route('/model', methods=['GET'])
def get_model():
    schema = {
        "objects": {
            "character": {
                "fields": [
                    {"key": "name", "type": "text", "label": "Name", "maxLength": 100},
                    {"key": "age", "type": "number", "label": "Age"},
                    {"key": "traits", "type": "multi-select", "label": "Traits", "options": ["Brave", "Cunning"]},
                    {"key": "parent", "type": "object", "label": "Inherits From", "nullable": True}
                ],
                "display": ["name", "age"],
                "actions": ["create", "update", "delete", "inherit", "clone"],
                "composition": {
                    "hierarchical": ["location"],
                    "lateral": []
                },
                "heritable": True
            }
        },
        "data": {
            "character": [
                {
                    "id": "1",
                    "name": "Batman",
                    "age": 35,
                    "traits": ["Brave", "Brooding"],
                    "parent": None
                },
                {
                    "id": "2",
                    "name": "Dark Knight",
                    "age": 36,
                    "traits": ["Brooding", "Martial Arts"],
                    "parent": "1"
                }
            ]
        }
    }
    return jsonify(schema)

@react_api.route('/list/<uuid>', methods=['GET'])
def list_objects(uuid):
    objects = [
        {
            "id": "1",
            "name": "Batman",
            "age": 35,
            "traits": ["Brave", "Brooding"],
            "parent": None
        },
        {
            "id": "2",
            "name": "Dark Knight",
            "age": 36,
            "traits": ["Brooding", "Martial Arts"],
            "parent": "1"
        }
    ]
    return jsonify(objects)

@react_api.route('/parse', methods=['POST'])
def parse_object():
    data = request.get_json()
    object_type = data.get('type')
    object_id = data.get('id')
    action = data.get('action')
    object_data = data.get('data')

    if action == "create":
        new_id = "uuid-67890"
        object_data["id"] = new_id
        return jsonify({
            "success": True,
            "id": new_id,
            "message": f"{object_type} created successfully."
        })

    if action == "update":
        return jsonify({
            "success": True,
            "message": f"{object_type} updated successfully."
        })

    if action == "delete":
        return jsonify({
            "success": True,
            "message": f"{object_type} deleted successfully."
        })

    if action == "inherit":
        inherited_id = "uuid-12345"
        return jsonify({
            "success": True,
            "id": inherited_id,
            "message": f"{object_type} inherited from {object_id}."
        })

    if action == "clone":
        return jsonify({
            "success": True,
            "message": f"{object_type} cloned successfully."
        })

    return jsonify({
        "success": False,
        "message": "Invalid action."
    })