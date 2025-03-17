import os
import threading
from flask import Flask
from modules.Database import Database
from modules.TelegramBot import TelegramBot
from modules.LLM import LLM
# from modules.Scenario import Scenario   # Uncomment when your Scenario class is fully implemented

# Global variable for the current active Scenario instance.
# When a story is loaded or created, this variable will be updated.
current_scenario = None

# Initialize the Flask app (even if we're not using HTTP endpoints for now)
app = Flask(__name__)

# Load configuration from environment variables or default values.
DB_URI = os.environ.get("NEO4J_URI", "bolt://127.0.0.1:7687")
DB_USER = os.environ.get("NEO4J_USER", "neo4j")
DB_PASSWORD = os.environ.get("NEO4J_PASSWORD", "neo4j#9657")

LLM_API_KEY = os.environ.get("LLM_API_KEY", "m,mm,m,m")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", ".,.,.,.,")

LLM_MODEL = os.environ.get("LLM_MODEL", "meta-llama/Llama-3.3-70B-Instruct")

# Instantiate the Database. This will also initialize constraints.
db = Database(DB_URI, DB_USER, DB_PASSWORD)

# Instantiate the LLM handler.
llm = LLM(api_key=LLM_API_KEY, model=LLM_MODEL)

# Instantiate the Telegram bot.
telegram_bot = TelegramBot(TELEGRAM_TOKEN, db, llm)


def dump(self):
    """
    Retrieves a dump of all nodes and relationships in the database with minimal properties.
    Returns a tuple: (dump_object, None) on success or (None, error_message) on failure.
    """
    # Retrieve all nodes
    query_nodes = "MATCH (n) RETURN n"
    result_nodes, err_nodes = self.execute_query(query_nodes)
    if err_nodes:
        return None, err_nodes
    nodes = []
    for record in result_nodes:
        node = record["n"]
        nodes.append({
            "id": node.get("id"),
            "name": node.get("name"),
            "labels": list(node.labels)
        })
    # Retrieve all relationships
    query_rels = "MATCH ()-[r]->() RETURN r"
    result_rels, err_rels = self.execute_query(query_rels)
    if err_rels:
        return None, err_rels
    relationships = []
    for record in result_rels:
        rel = record["r"]
        relationships.append({
            "type": rel.type,
            "start": rel.start_node.get("id"),
            "end": rel.end_node.get("id")
        })
    dump_obj = {
        "nodes": nodes,
        "relationships": relationships
    }
    return dump_obj, None

	
# --- Overriding the Telegram bot's narrative handling ---
# We modify the TelegramBotHandler's default behavior to use our global current_scenario.
# In your modules/telegram_bot.py, ensure that narrative (non-command) messages are handled as follows:


# Monkey-patch the narrative handler in TelegramBotHandler.
# This assumes that TelegramBotHandler exposes a method or attribute that allows you to override narrative handling.

# Start the Telegram bot polling (runs in a background thread).
telegram_bot.stop_polling()
telegram_bot.start_polling()

# Since we don't use HTTP endpoints for now, we don't need to define any Flask routes.
# The Flask app is here mainly as a container for our application environment.
if __name__ == "__main__":
    # In your deployment, you'll likely use "flask run" instead.
    # For testing locally, you can run this file directly.
    app.run(host="0.0.0.0", port=8080, debug=True)