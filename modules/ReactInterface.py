from flask import Blueprint, request, jsonify
from modules.Database import Database
from Modules.LLM import LLM

react_api = Blueprint('react_api', __name__)

# In-memory storage for demonstration purposes
object_types = [
    {"id": "1", "name": "Character"},
    {"id": "2", "name": "Location"},
    {"id": "3", "name": "Item"}
]

objects = {
    "Character": [],
    "Location": [],
    "Item": []
}

stories = {}

@react_api.route('/user/routes/builder/object-types', methods=['GET'])
def get_object_types():
    return jsonify(object_types)

@react_api.route('/list/<object_type>', methods=['GET'])
def list_objects(object_type):
    return jsonify(objects.get(object_type, []))

@react_api.route('/create/<object_type>', methods=['POST'])
def create_object(object_type):
    data = request.json
    new_object = {
        "id": str(len(objects[object_type]) + 1),
        "name": data.get("name"),
        "description": data.get("description"),
        "inheritance": data.get("inheritance"),
        "composition": data.get("composition", {"hierarchical": [], "lateral": []}),
        "links": data.get("links", []),
        "properties": data.get("properties", []),
        "sections": data.get("sections", [])
    }
    objects[object_type].append(new_object)
    return jsonify({"status": "success", "data": objects[object_type]})

@react_api.route('/update/<object_type>/<object_id>', methods=['PUT'])
def update_object(object_type, object_id):
    data = request.json
    for obj in objects[object_type]:
        if obj["id"] == object_id:
            obj.update(data)
            return jsonify({"status": "success", "data": objects[object_type]})
    return jsonify({"status": "error", "message": "Object not found"}), 404

@react_api.route('/delete/<object_id>', methods=['DELETE'])
def delete_object(object_id):
    for object_type in objects:
        objects[object_type] = [obj for obj in objects[object_type] if obj["id"] != object_id]
    return jsonify({"status": "success"})

@react_api.route('/story/<story_id>/add-entry', methods=['POST'])
def add_story_entry(story_id):
    data = request.json
    if story_id not in stories:
        stories[story_id] = {"id": story_id, "entries": []}
    stories[story_id]["entries"].append(data)
    return jsonify({"status": "success", "data": stories[story_id]})

@react_api.route('/story/<story_id>/annotate', methods=['POST'])
def annotate_story(story_id):
    data = request.json
    if story_id not in stories:
        return jsonify({"status": "error", "message": "Story not found"}), 404
    stories[story_id]["entries"].append(data)
    return jsonify({"status": "success", "data": stories[story_id]})