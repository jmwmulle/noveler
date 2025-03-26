# modules/llm_handler.py

import json
import traceback
from huggingface_hub import InferenceClient

class LLM:
	def __init__(self, api_key, model="meta-llama/Llama-3.3-70B-Instruct", config=None):
		"""
		Initializes the LLMHandler with the given Hugging Face API key, model, and configuration.
		
		config is an optional dictionary that can include parameters such as:
			- temperature
			- top_p
			- frequency_penalty
			- presence_penalty
			- etc.
		"""
		self.api_key = api_key
		self.model = model
		self.config = config or {}
		self.client = InferenceClient(api_key=self.api_key, model=self.model)
	
	def set_model(self, model):
		"""
		Sets the preferred model and reinitializes the InferenceClient.
		"""
		self.model = model
		self.client = InferenceClient(api_key=self.api_key, model=self.model)
	
	def set_config(self, config):
		"""
		Updates the configuration for model parameters.
		Expected keys might include:
			- temperature
			- top_p
			- frequency_penalty
			- presence_penalty
		"""
		self.config = config
	
	def update_config(self, **kwargs):
		"""
		Updates specific configuration parameters.
		For example: update_config(temperature=0.7, top_p=0.9)
		"""
		self.config.update(kwargs)
	
	def send_prompt(self, prompt):
		"""
		Sends a prompt (a JSON string) to the LLM, including any additional configuration parameters.
		Returns the parsed JSON response.
		"""
		try:
			# Combine the prompt with the configuration.
			# This assumes the API accepts a payload with "inputs" and "parameters" keys.
			payload = {
				"inputs": prompt,
				"parameters": self.config
			}
			response = self.client.infer(payload)
			return json.loads(response)
		except Exception as e:
			raise Exception(f"LLM communication error: {str(e)}\n{traceback.format_exc()}")