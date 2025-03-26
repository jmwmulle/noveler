from Modules.Database import Database
from Modules.GameObjects import Trait, BaseCharacter, BaseLocation

# Initialize the database connection
db = Database(uri="bolt://localhost:7687", user="neo4j", password="neo4j#9657")

# Cleanup: Delete all nodes of relevant types
with db.driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

# Ensure the schema is set up
db.setup_schema()

# Populate the database with sample data
trait = Trait(id="trait1", title="Bravery", description="The character is exceptionally brave.")
trait.save_to_db(db)

character = BaseCharacter(id="char1", name="Hero", description="The protagonist of the story.")
character.add_trait(trait)
character.save_to_db(db)

location = BaseLocation(id="loc1", name="Castle", description="A grand medieval castle.")
location.add_trait(trait)
location.save_to_db(db)

# Add a sample narrative entry
with db.driver.session() as session:
    session.run("""
        CREATE (e:Entry {id: 'entry1', story_id: 'story1', text: 'Once upon a time...'})
        CREATE (s:Summary {text: 'A story begins.'})
        CREATE (e)-[:NEXT]->(s)
    """)

# Add History nodes and CURRENT relationships
with db.driver.session() as session:
    session.run("""
        CREATE (h:History {id: 'history1', story_id: 'story1'})
        WITH h
        MATCH (t:Trait {id: 'trait1'})
        CREATE (h)-[:CURRENT]->(t)
    """)

# Retrieve the current state
state = db.retrieve_state(story_id="story1")
print("Retrieved State:", state)

# Close the database connection
db.close()