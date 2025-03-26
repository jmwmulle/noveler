from Modules.Database import Database
from Modules.GameObjects import Trait

# Initialize the database connection
db = Database(uri="bolt://localhost:7687", user="neo4j", password="neo4j#9657")

# Cleanup: Delete all nodes of relevant types
with db.driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

# Ensure the schema is set up
db.setup_schema()

# Populate the database with initial data
trait = Trait(id="trait1", title="Bravery", description="The character is exceptionally brave.")
trait.save_to_db(db)

# Add initial History node and CURRENT relationship
with db.driver.session() as session:
    session.run("""
        CREATE (h:History {id: 'history1', story_id: 'story1', state: 'Initial state'})
        WITH h
        MATCH (t:Trait {id: 'trait1'})
        CREATE (h)-[:CURRENT]->(t)
    """)

# Commit a new narrative entry and update the state
new_entry_id = db.commit_entry(
    story_id="story1",
    entry_text="The hero embarks on a journey.",
    summary_text="The journey begins.",
    state_changes=[
        {
            "type": "Trait",
            "id": "trait1",
            "new_state": "The hero gains courage."
        }
    ]
)

# Verify the results
with db.driver.session() as session:
    # Check the new Entry and Summary nodes
    entry_result = session.run("MATCH (e:Entry {id: $entry_id})-[:NEXT]->(s:Summary) RETURN e, s", entry_id=new_entry_id).data()
    print("Entry and Summary:", entry_result)

    # Check the updated History node and CURRENT relationship
    state_result = session.run("""
        MATCH (h:History)-[:CURRENT]->(t:Trait {id: 'trait1'})
        RETURN h, t
    """).data()
    print("Updated State:", state_result)

# Close the database connection
db.close()