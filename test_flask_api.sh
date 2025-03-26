#!/bin/bash

# filepath: /workspaces/noveler/test_flask_api.sh

BASE_URL="http://127.0.0.1:5000/api/story"

echo "Starting API tests..."

# Test 1: Load Story State
echo "Test 1: Load Story State"
curl -X GET "$BASE_URL/load/story1" -H "Content-Type: application/json"
echo -e "\n"

# Test 2: Commit New Entry
echo "Test 2: Commit New Entry"
curl -X POST "$BASE_URL/entry" \
    -H "Content-Type: application/json" \
    -d '{
        "story_id": "story1",
        "entry_text": "The hero embarks on a new quest.",
        "summary_text": "A new journey begins.",
        "state_changes": [
            {
                "type": "Trait",
                "id": "trait1",
                "new_state": "The hero gains wisdom."
            }
        ]
    }'
echo -e "\n"

# Test 3: Create a Branch
echo "Test 3: Create a Branch"
curl -X POST "$BASE_URL/branch/entry1/Alternate%20Path" \
    -H "Content-Type: application/json" \
    -d '{
        "branch_id": "branch1"
    }'
echo -e "\n"

# Test 4: Prune Story
echo "Test 4: Prune Story"
curl -X DELETE "$BASE_URL/prune/entry1" -H "Content-Type: application/json"
echo -e "\n"

echo "API tests completed."