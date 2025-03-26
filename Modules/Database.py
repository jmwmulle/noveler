from neo4j import GraphDatabase

class Database:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def setup_schema(self):
        """Ensures the database schema supports the required node and relationship types."""
        with self.driver.session() as session:
            # Execute each CREATE CONSTRAINT statement separately
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entry) REQUIRE e.id IS UNIQUE;")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Trait) REQUIRE t.id IS UNIQUE;")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Character) REQUIRE c.id IS UNIQUE;")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE;")

    def create_trait(self, id, title, description):
        """Creates a Trait node in the database if it doesn't already exist."""
        with self.driver.session() as session:
            session.run("""
                MERGE (t:Trait {id: $id})
                ON CREATE SET t.title = $title, t.description = $description
            """, id=id, title=title, description=description)

    def create_character(self, id, name, description):
        """Creates a Character node in the database if it doesn't already exist."""
        with self.driver.session() as session:
            session.run("""
                MERGE (c:Character {id: $id})
                ON CREATE SET c.name = $name, c.description = $description
            """, id=id, name=name, description=description)

    def create_location(self, id, name, description):
        """Creates a Location node in the database if it doesn't already exist."""
        with self.driver.session() as session:
            session.run("""
                MERGE (l:Location {id: $id})
                ON CREATE SET l.name = $name, l.description = $description
            """, id=id, name=name, description=description)

    def retrieve_state(self, story_id):
        """Retrieves the current state of the narrative and game objects for a given story."""
        with self.driver.session() as session:
            # Retrieve narrative entries
            entries = session.run("""
                MATCH (e:Entry)-[:NEXT*]->(s:Summary)
                WHERE e.story_id = $story_id
                RETURN e.id AS entry_id, e.text AS entry_text, s.text AS summary_text
            """, story_id=story_id).data()

            # Retrieve mutable state (Traits, Characters, Locations)
            state = session.run("""
                MATCH (h:History)-[:CURRENT]->(t:Trait)
                WHERE h.story_id = $story_id
                RETURN t.id AS trait_id, t.title AS trait_title, t.description AS trait_description
            """, story_id=story_id).data()

            # Combine narrative and state into a structured response
            return {
                "entries": entries,
                "state": state
            }

    def commit_entry(self, story_id, entry_text, summary_text, state_changes):
        """
        Commits a new narrative entry and updates the mutable state.
        
        Args:
            story_id (str): The ID of the story.
            entry_text (str): The text of the new narrative entry.
            summary_text (str): A summary of the entry.
            state_changes (list): A list of state changes, where each change is a dict with:
                - "type": The type of object ("Trait", "Character", "Location").
                - "id": The ID of the object.
                - "new_state": The new state description.
        
        Returns:
            str: The ID of the newly created Entry node.
        """
        with self.driver.session() as session:
            # Create the Entry and Summary nodes
            result = session.run("""
                CREATE (e:Entry {id: randomUUID(), story_id: $story_id, text: $entry_text})
                CREATE (s:Summary {text: $summary_text})
                CREATE (e)-[:NEXT]->(s)
                RETURN e.id AS entry_id
            """, story_id=story_id, entry_text=entry_text, summary_text=summary_text)
            
            entry_id = result.single()["entry_id"]

            # Update mutable state
            for change in state_changes:
                obj_type = change["type"]
                obj_id = change["id"]
                new_state = change["new_state"]

                session.run(f"""
                    MATCH (o:{obj_type} {{id: $obj_id}})
                    MATCH (h:History)-[r:CURRENT]->(o)
                    DELETE r
                    CREATE (new_h:History {{id: randomUUID(), story_id: $story_id, state: $new_state}})
                    CREATE (new_h)-[:CURRENT]->(o)
                """, obj_id=obj_id, story_id=story_id, new_state=new_state)

            return entry_id

    def create_branch(self, entry_id, branch_title=None, branch_id=None):
        """
        Creates a new branch starting from the specified Entry node.
        
        Args:
            entry_id (str): The ID of the Entry node where the branch starts.
            branch_title (str, optional): A title for the branch.
            branch_id (str, optional): A unique identifier for the branch.
        
        Returns:
            str: The ID of the newly created Entry node for the branch.
        """
        with self.driver.session() as session:
            # Create the new Entry node and link it with a BRANCH relationship
            result = session.run("""
                MATCH (e:Entry {id: $entry_id})
                CREATE (new_entry:Entry {id: randomUUID(), text: 'Branch starting point'})
                CREATE (e)-[:BRANCH {title: $branch_title, id: $branch_id}]->(new_entry)
                RETURN new_entry.id AS new_entry_id
            """, entry_id=entry_id, branch_title=branch_title, branch_id=branch_id)
            
            return result.single()["new_entry_id"]

    def prune_story(self, entry_id):
        """
        Rolls back the story to the specified Entry node by deleting all subsequent entries and state changes.
        
        Args:
            entry_id (str): The ID of the Entry node to roll back to.
        
        Returns:
            str: A confirmation message indicating the rollback was successful.
        """
        with self.driver.session() as session:
            # Collect the IDs of all subsequent entries
            session.run("""
                MATCH (e:Entry {id: $entry_id})-[:NEXT*]->(to_delete:Entry)
                OPTIONAL MATCH (to_delete)-[:NEXT]->(s:Summary)
                DETACH DELETE to_delete, s
            """, entry_id=entry_id)

            # Remove all History nodes and CURRENT relationships associated with pruned entries
            session.run("""
                MATCH (e:Entry {id: $entry_id})-[:NEXT*]->(to_delete:Entry)
                WITH collect(to_delete.story_id) AS pruned_story_ids
                MATCH (h:History)-[:CURRENT]->(o)
                WHERE h.story_id IN pruned_story_ids
                DETACH DELETE h
            """, entry_id=entry_id)

            return f"Story successfully rolled back to Entry {entry_id}."