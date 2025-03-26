from Modules.Database import Database

# Initialize the database connection
db = Database(uri="bolt://localhost:7687", user="neo4j", password="neo4j#9657")

# Cleanup: Delete all nodes of relevant types
with db.driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

# Ensure the schema is set up
db.setup_schema()

# Add a sample narrative entry
with db.driver.session() as session:
    session.run("""
        CREATE (e:Entry {id: 'entry1', story_id: 'story1', text: 'The hero embarks on a journey.'})
    """)

# Create a branch
new_branch_entry_id = db.create_branch(
    entry_id="entry1",
    branch_title="Alternate Path",
    branch_id="branch1"
)

# Verify the results
with db.driver.session() as session:
    # Check the new Entry node and BRANCH relationship
    branch_result = session.run("""
        MATCH (e:Entry {id: 'entry1'})-[:BRANCH {id: 'branch1'}]->(new_entry:Entry)
        RETURN e, new_entry
    """).data()
    print("Branch Result:", branch_result)

# Close the database connection
db.close()