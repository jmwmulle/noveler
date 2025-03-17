# modules/telegram_bot.py

import threading
import traceback
from telebot import TeleBot
from datetime import datetime
from modules.CommandHandler import CommandHandler

# For narrative input, assume you have a Scenario class defined elsewhere
# from modules.scenario import Scenario
# For now, we simulate narrative handling.

class TelegramBot:
    def __init__(self, token, db, llm):
        self.token = token
        self.llm = llm
        self.bot = TeleBot(self.token)
        self.db = db
        self.command_handler = CommandHandler()
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.bot.message_handler(func=lambda message: True)
        def custom_handle_narrative(message):
            chat_id = message.chat.id
            user_text = message.text.strip()
            if user_text.strip().lower() == "dump":
                # call the new dump function.
                dump_obj, err = db.dump()
                if err:
                    return f"Error retrieving database dump: {err}"
                return f"Database dump: {dump_obj}"
            else:
                # For any other narrative input, send the raw text directly to the LLM.
                try:
                    llm_response = self.llm.send_prompt(user_text)
                    self.bot.send_message(chat_id, llm_response)                    
                    return f"LLM response: {llm_response}"
                except Exception as e:
                    self.bot.send_message(chat_id, str(e))    
                    return f"Error communicating with LLM: {str(e)}"
#        def handle_message(message):
#            chat_id = message.chat.id
#            user_text = message.text.strip()
#            response_text = ""
#            try:
#                if user_text.startswith("/"):
#                    # Allow for multiple commands separated by newlines.
#                    commands = [cmd for cmd in user_text.split("\n") if cmd.startswith("/")]
#                    response_text = self.command_handler.handle_commands(commands)
#                else:
#                    # For narrative input, delegate to the Scenario layer.
#                    # In your full implementation, you'd call something like:
#                    # response_text = active_scenario.process_narrative(user_text)
#                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                    response_text = f"Received narrative input at {timestamp}:\n{user_text}"
#                self.bot.send_message(chat_id, response_text)
#            except Exception as e:
#                error_message = f"Error handling message: {str(e)}\n{traceback.format_exc()}"
#                print(error_message)
#                self.bot.send_message(chat_id, error_message)
    
    def start_polling(self):
        thread = threading.Thread(target=self.bot.polling, kwargs={"none_stop": True}, daemon=True)
        thread.start()
        