import os
import json
from flask import Flask, send_from_directory
from Modules.ReactInterface import create_react_interface
from Modules.Database import Database
from Modules.TelegramBot import TelegramBot
from Modules.LLM import LLM

# Global variable for the current active Scenario instance.
current_scenario = None

# Initialize the Flask app
app = Flask(__name__, static_folder='noveler-frontend/build', static_url_path='/')

with open("static_files/creds.json", "r") as f:
    credentials = json.load(f)

dev_mode = True
# Load configuration from environment variables or default values.
if dev_mode:
    DB_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    DB_PASSWORD = os.environ.get("NEO4J_PASSWORD", "neo4j#9657")
else:
    DB_URI = os.environ.get("NEO4J_URI", "bolt://127.0.0.1:7687")
    DB_PASSWORD = os.environ.get("NEO4J_PASSWORD", "neo4j#9657")

DB_USER = os.environ.get("NEO4J_USER", "neo4j")

LLM_API_KEY = os.environ.get("LLM_API_KEY", credentials["hugging_face"])
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", credentials["telegram"])

LLM_MODEL = os.environ.get("LLM_MODEL", "meta-llama/Llama-3.3-70B-Instruct")

# Instantiate the Database. This will also initialize constraints.
db = Database(uri=DB_URI, user=DB_USER, password=DB_PASSWORD)

# Register the ReactInterface Blueprint, passing the Database instance
react_interface = create_react_interface(db)
app.register_blueprint(react_interface)

# Instantiate the LLM handler.
llm = LLM(api_key=LLM_API_KEY, model=LLM_MODEL)

# Instantiate the Telegram bot.
# telegram_bot = TelegramBot(TELEGRAM_TOKEN, db, llm)

    # @app.route('/')
    # def serve_react_app():
    #     return send_from_directory(app.static_folder, 'index.html')

    # @app.route('/model')
    # def serve_modeling_ui():
    #     return send_from_directory(app.static_folder, 'index.html')

    # @app.route('/story')
    # def serve_storytelling_ui():
    #     return send_from_directory(app.static_folder, 'index.html')

    # @app.route('/<path:path>')
    # def serve_static_files(path):
    #     return send_from_directory(app.static_folder, path)

# Start the Telegram bot polling (runs in a background thread).
# telegram_bot.start_polling()

# Since we don't use HTTP endpoints for now, we don't need to define any Flask routes.
# The Flask app is here mainly as a container for our application environment.
if __name__ == "__main__":
    # In your deployment, you'll likely use "flask run" instead.
    # For testing locally, you can run this file directly.
    app.run(host="0.0.0.0", port=8080, debug=True)