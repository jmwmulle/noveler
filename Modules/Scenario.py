import json
import uuid
import re
from datetime import datetime
from app import execute_cypher  # Assumes execute_cypher is globally available
import copy

class Scenario:
	"""
	The core Scenario class encapsulates the narrative (authorial) logic.
	
	Key responsibilities:
		- Instantiate or load a Story node in the database.
		- Compose a structured JSON prompt for the LLM using a fixed template.
		- Parse the LLM's JSON response, validating against a fixed response template.
		
	Notes:
		- The prompt template is stored as a property (self.prompt_template) and includes keys:
			directives, errors, OOC, context, content, history, database_map.
		These keys will be filled on each prompt composition.
		- Only history is persistent (updated cumulatively). Dynamic values such as context and 
			database_map are computed on demand.
		- The directives property is a dict that the user populates with instructions.
		- Errors are stored as a list.
	"""
	
	def __init__(self, story_id=None):
		# Directives stored as a dict. The user is responsible for populating this.
		self.directives = {
			"main": "You are an LLM maintaining characters and world state in a prose exchange game."
		}
		# Errors is an array.
		self.errors = []
		# History (a list of summaries) is persistent.
		self.history = []
		
		# The following two are not stored persistently:
		# Context and database_map will be computed when needed.
		
		# Prompt template: the keys are fixed and in the desired order.
		# (Note: as a property, we hold a "template" which is a dict we will update on every prompt.)
		self.prompt_template = {
			"directives": None,    # Will be populated from self.directives.
			"errors": None,        # Will be populated from self.errors.
			"OOC": None,           # Out-of-character content from the user.
			"context": None,       # Computed dynamically.
			"content": None,       # Cleaned user input.
			"history": None,       # From self.history.
			"database_map": None   # Computed dynamically.
		}
		
		# Response template stored as a property for validation purposes.
		self.response_template = {
			"OOC": "",
			"response": {
				"content": "",
				"updates": [],   # Must be an array.
				"summary": "",
				"core": ""
			}
		}
		
		self.story_id = story_id
		self.init_story()

	def init_story(self):
		"""
		Instantiate a new Story node if no story_id is provided, or verify the story exists.
		"""
		if self.story_id is None:
			new_story_id = str(uuid.uuid4())
			query = """
			CREATE (s:Story {id: $story_id, created_at: timestamp()})
			RETURN s
			"""
			result, err = execute_cypher(query, {"story_id": new_story_id})
			if err:
				raise Exception(f"Error creating new story: {err}")
			self.story_id = new_story_id
		else:
			query = """
			MATCH (s:Story {id: $story_id})
			RETURN s
			"""
			result, err = execute_cypher(query, {"story_id": self.story_id})
			if err or not result:
				raise Exception(f"Error loading story {self.story_id}: {err or 'Story not found'}")
		return self.story_id

	def extract_ooc(self, text):
		"""
		Extract out-of-character (OOC) content from the given text.
		Assumes OOC content is enclosed in [OOC: ...].
		
		Returns:
			(clean_text, ooc_text)
		"""
		ooc_matches = re.findall(r'\[OOC:(.*?)\]', text, flags=re.IGNORECASE)
		ooc_text = " ".join(ooc_matches).strip()
		clean_text = re.sub(r'\[OOC:.*?\]', '', text, flags=re.IGNORECASE).strip()
		return clean_text, ooc_text

	def get_context(self):
		"""
		Compute and return dynamic context.
		This could include current characters, room state, upcoming events, etc.
		For now, we return an empty dict as a placeholder.
		"""
		# TODO: Replace with actual dynamic context computation.
		return {}

	def get_database_map(self):
		"""
		Compute and return a structured snapshot of the database state.
		For now, return an empty dict as a placeholder.
		"""
		# TODO: Replace with actual database map logic.
		return {}

	def compose_prompt(self, user_text):
		"""
		Composes a JSON prompt for the LLM.
		
		The final JSON object includes keys in this order:
			directives, errors, OOC, context, content, history, database_map.
		The values for 'directives', 'errors', and 'history' come from the object's properties.
		'context' and 'database_map' are computed on demand.
		'OOC' and 'content' come from processing the user_text.
		"""
		clean_text, ooc_text = self.extract_ooc(user_text)
		
		# Create a fresh copy of the prompt template.
		prompt_obj = copy.deepcopy(self.prompt_template)
		
		prompt_obj["directives"] = self.directives
		prompt_obj["errors"] = self.errors  # This is now an array.
		prompt_obj["OOC"] = ooc_text
		prompt_obj["context"] = self.get_context()
		prompt_obj["content"] = clean_text
		prompt_obj["history"] = self.history
		prompt_obj["database_map"] = self.get_database_map()
		
		return json.dumps(prompt_obj)

	def parse_response(self, response_json):
		"""
		Parses the LLM's JSON response.
		
		Expected schema:
			{
				"OOC": "<string>",
				"response": {
					"content": "<string>",
					"updates": [ ... ],    // Array of update commands.
					"summary": "<string>", // Summary for history.
					"core": "<string>"     // Core narrative detail.
				}
			}
		
		Validates required keys against the stored response template.
		Raises an exception if validation fails.
		"""
		try:
			# Validate top-level keys.
			if "OOC" not in response_json:
				raise ValueError("Response JSON missing 'OOC' key.")
			if "response" not in response_json:
				raise ValueError("Response JSON missing 'response' key.")
			
			resp_obj = response_json["response"]
			for key in ["content", "updates", "summary", "core"]:
				if key not in resp_obj:
					raise ValueError(f"Response 'response' object missing key: {key}")
			
			# Optionally, additional validation against self.response_template can occur here.
			return {
				"OOC": response_json["OOC"],
				"response": {
					"content": resp_obj["content"],
					"updates": resp_obj["updates"],
					"summary": resp_obj["summary"],
					"core": resp_obj["core"]
				}
			}
		except Exception as e:
			raise Exception(f"Error parsing response: {str(e)}")