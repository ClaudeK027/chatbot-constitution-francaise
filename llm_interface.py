import requests
import json

m1 = 'mistral'
m2 = 'phi3'

class LLMInterface:
    def __init__(self, model_name=m2):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def generate_response(self, prompt, max_tokens=500):
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return json.loads(response.text)['response']
        except requests.exceptions.RequestException as e:
            return f"Error: Unable to generate response. {str(e)}"

    def simple_query(self, question):
        prompt = f"Human: {question}\n\nAssistant:"
        return self.generate_response(prompt)

