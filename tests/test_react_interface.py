import pytest
from flask import Flask
from Modules.ReactInterface import react_interface

@pytest.fixture
def client(mocker):
    """Fixture to set up the Flask test client with mocked database."""
    app = Flask(__name__)
    app.register_blueprint(react_interface)

    # Mock the Database class
    mock_db = mocker.patch('Modules.ReactInterface.db')

    # Mock methods for the Database instance
    mock_db.retrieve_state.return_value = {
        "entries": [{"entry_id": "entry1", "entry_text": "Once upon a time..."}],
        "state": [{"trait_id": "trait1", "trait_title": "Bravery", "trait_description": "The hero is brave."}]
    }
    mock_db.commit_entry.return_value = "new_entry_id"
    mock_db.create_branch.return_value = "new_branch_entry_id"
    mock_db.prune_story.return_value = "Story successfully rolled back to Entry entry1."

    with app.test_client() as client:
        yield client

def test_load_story(client):
    """Test the load_story endpoint."""
    response = client.get('/api/story/load/story1')
    assert response.status_code == 200
    assert response.json == {
        "entries": [{"entry_id": "entry1", "entry_text": "Once upon a time..."}],
        "state": [{"trait_id": "trait1", "trait_title": "Bravery", "trait_description": "The hero is brave."}]
    }

def test_add_entry(client):
    """Test the add_entry endpoint."""
    response = client.post('/api/story/entry', json={
        "story_id": "story1",
        "entry_text": "The hero embarks on a journey.",
        "summary_text": "The journey begins.",
        "state_changes": [{"type": "Trait", "id": "trait1", "new_state": "The hero gains courage."}]
    })
    assert response.status_code == 201
    assert response.json == {"new_entry_id": "new_entry_id"}

def test_create_branch(client):
    """Test the create_branch endpoint."""
    response = client.post('/api/story/branch/entry1/Alternate%20Path', json={
        "branch_id": "branch1"
    })
    assert response.status_code == 201
    assert response.json == {"new_branch_entry_id": "new_branch_entry_id"}

def test_prune_story(client):
    """Test the prune_story endpoint."""
    response = client.delete('/api/story/prune/entry1')
    assert response.status_code == 200
    assert response.json == {"message": "Story successfully rolled back to Entry entry1."}