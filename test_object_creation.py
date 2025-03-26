from Modules.Database import Database
from Modules.GameObjects import Trait, BaseCharacter, BaseLocation

# Initialize the database connection
db = Database(uri="bolt://localhost:7687", user="neo4j", password="neo4j#9657")

# Cleanup: Delete all nodes of relevant types
with db.driver.session() as session:
    session.run("MATCH (t:Trait) DETACH DELETE t")
    session.run("MATCH (c:Character) DETACH DELETE c")
    session.run("MATCH (l:Location) DETACH DELETE l")

# Ensure the schema is set up
db.setup_schema()

# Create and save a Trait
trait = Trait(id="trait1", title="Bravery", description="The character is exceptionally brave.")
trait.save_to_db(db)

# Create and save a Character with a Trait
character = BaseCharacter(id="char1", name="Hero", description="The protagonist of the story.")
character.add_trait(trait)
character.save_to_db(db)

# Create and save a Location with a Trait
location = BaseLocation(id="loc1", name="Castle", description="A grand medieval castle.")
location.add_trait(trait)
location.save_to_db(db)

# Close the database connection
db.close()

print("Test completed: Objects created and saved to the database.")