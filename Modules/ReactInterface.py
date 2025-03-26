from flask import Flask
from Modules.Database import Database
from flask import Blueprint, request, jsonify

def create_react_interface(db):
    """
    Factory function to create the ReactInterface Blueprint with a shared Database instance.
    
    Args:
        db (Database): The shared Database instance.
    
    Returns:
        Blueprint: The ReactInterface Blueprint.
    """
    react_interface = Blueprint('react_interface', __name__)

    @react_interface.route('/api/story/load/<storyID>', methods=['GET'])
    def load_story(storyID):
        """Retrieve the current state of the story."""
        try:
            state = db.retrieve_state(story_id=storyID)
            return jsonify(state), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @react_interface.route('/api/story/entry', methods=['POST'])
    def add_entry():
        """Commit a new narrative entry and update the state."""
        try:
            data = request.json
            story_id = data['story_id']
            entry_text = data['entry_text']
            summary_text = data['summary_text']
            state_changes = data.get('state_changes', [])
            new_entry_id = db.commit_entry(story_id, entry_text, summary_text, state_changes)
            return jsonify({"new_entry_id": new_entry_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @react_interface.route('/api/story/branch/<entryID>/<title>', methods=['POST'])
    def create_branch(entryID, title):
        """Create a new branch starting from the specified entry."""
        try:
            branch_id = request.json.get('branch_id', None)
            new_branch_entry_id = db.create_branch(entry_id=entryID, branch_title=title, branch_id=branch_id)
            return jsonify({"new_branch_entry_id": new_branch_entry_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @react_interface.route('/api/story/prune/<entryID>', methods=['DELETE'])
    def prune_story(entryID):
        """Roll back the story to the specified entry."""
        try:
            result = db.prune_story(entry_id=entryID)
            return jsonify({"message": result}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return react_interface

