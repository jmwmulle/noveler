from Modules.Database import Database

# Initialize the database connection
db = Database(uri="bolt://localhost:7687", user="neo4j", password="neo4j#9657")

# Cleanup: Delete all nodes of relevant types
with db.driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

# Ensure the schema is set up
db.setup_schema()

# Add a sample narrative with multiple entries
with db.driver.session() as session:
    session.run("""
        CREATE (e1:Entry {id: 'entry1', story_id: 'story1', text: 'The hero embarks on a journey.'})
        CREATE (e2:Entry {id: 'entry2', story_id: 'story1', text: 'The hero faces a challenge.'})
        CREATE (e3:Entry {id: 'entry3', story_id: 'story1', text: 'The hero overcomes the challenge.'})
        CREATE (s1:Summary {text: 'The journey begins.'})
        CREATE (s2:Summary {text: 'A challenge arises.'})
        CREATE (s3:Summary {text: 'The challenge is overcome.'})
        CREATE (e1)-[:NEXT]->(e2)-[:NEXT]->(e3)
        CREATE (e1)-[:NEXT]->(s1)
        CREATE (e2)-[:NEXT]->(s2)
        CREATE (e3)-[:NEXT]->(s3)
    """)

# Prune the story back to entry1
result = db.prune_story(entry_id="entry1")
print(result)

# Verify the results
with db.driver.session() as session:
    # Check that only entry1 and its summary remain
    remaining_entries = session.run("MATCH (e:Entry) RETURN e").data()
    print("Remaining Entries:", remaining_entries)

# Close the database connection
db.close()