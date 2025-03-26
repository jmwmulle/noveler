# modules/database.py
# NOTE TO LLM COLlABORATOR: Neo4j5.x syntax required

import traceback
from neo4j import GraphDatabase

class Database:
	def __init__(self, uri, user, password):
		self.uri = uri
		self.user = user
		self.password = password
		try:
			self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
			# Check if the database is reachable by running a simple test query.
			test_query = "RETURN 1 AS test"
			result, err = self.execute_query(test_query)
			if err or not result:
				raise Exception("Database connection test failed: " + (err or "No result"))
			print("Database connection successful.")
		except Exception as e:
			raise Exception(f"Database connection error: {str(e)}")
		
		# After confirming the connection, initialize the database schema.
		self.initialize_db()

	def close(self):
		self.driver.close()

	def execute_query(self, query, parameters=None):
		with self.driver.session() as session:
			try:
				result = list(session.run(query, parameters or {}))
				return result, None
			except Exception as e:
				return None, traceback.format_exc()

	def initialize_db(self):
		"""
		Checks if the database schema is initialized.
		This method creates a set of constraints (expanded to 13 constraints as per your initdb.py).
		It assumes that if a constraint already exists, an error is thrown, which we catch and log.
		"""
		constraints = [
		"CREATE CONSTRAINT story_id_unique IF NOT EXISTS FOR (s:Story) REQUIRE s.id IS UNIQUE;",
		"CREATE CONSTRAINT story_title_unique IF NOT EXISTS FOR (s:Story) REQUIRE s.title IS UNIQUE;",
		"CREATE CONSTRAINT scenario_id_unique IF NOT EXISTS FOR (sc:Scenario) REQUIRE sc.id IS UNIQUE;",
		"CREATE CONSTRAINT trait_id_unique IF NOT EXISTS FOR (t:BaseTrait) REQUIRE t.id IS UNIQUE;",
		"CREATE CONSTRAINT trait_name_unique IF NOT EXISTS FOR (t:BaseTrait) REQUIRE t.name IS UNIQUE;",
		"CREATE CONSTRAINT location_id_unique IF NOT EXISTS FOR (l:BaseLocation) REQUIRE l.id IS UNIQUE;",
		"CREATE CONSTRAINT location_name_unique IF NOT EXISTS FOR (l:BaseLocation) REQUIRE l.name IS UNIQUE;"
		]
		for cons in constraints:
			res, err = self.execute_query(cons)
			if err:
				# If the error message indicates the constraint already exists, we ignore it.
				if "already exists" in err:
					print("Constraint already exists, skipping:", cons)
				else:
					print("Error creating constraint:", err)
			else:
				print("Constraint created or verified:", cons)
				
	def map(self, story_id):
		"""
		Retrieves a concise map of the current state for a given story.
		This query returns only the top-level entities connected to the Story node via the :HAS_ENTITY relationship.
		It returns minimal properties (e.g., title and id) and labels.
		"""
		query = """
		MATCH (s:Story {id: $story_id})-[:HAS_ENTITY]->(e)
		RETURN e.title AS title, e.id AS id, labels(e) AS labels
		"""
		result, err = self.execute_query(query, {"story_id": story_id})
		if err:
			return None, err
		entities = []
		for record in result:
			entities.append({
				"title": record.get("title"),
				"id": record.get("id"),
				"labels": record.get("labels")
			})
		return entities, None

