import os
import requests

class OllamaClient:
    def __init__(self, model="gemma3:4b", url=None):
        base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self.url = url or f"{base_url}/api/chat"

    def generate(self, prompt, system=None):
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        if system:
            data["system"] = system
        response = requests.post(self.url, json=data)
        response.raise_for_status()
        msg = response.json().get("message", {})
        if msg.get("role") == "assistant":
            return msg.get("content", "")
        return ""
