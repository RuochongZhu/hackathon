# workflow.py
# Ollama Cloud API Workflow Demo (Python)
# Tim Fraser
#
# This script demonstrates a minimal Ollama Cloud API request using an API key
# loaded from a local .env file.

# 0. Setup #################################

## 0.1 Load packages ############################

import os
import requests
from dotenv import load_dotenv

## 0.2 Load environment variables ############################

load_dotenv()
ollama_api_key = os.getenv("OLLAMA_API_KEY")

if not ollama_api_key:
    raise ValueError("OLLAMA_API_KEY not found. Add it to your .env file.")

# 1. Build request #################################

url = "https://ollama.com/api/chat"
headers = {
    "Authorization": f"Bearer {ollama_api_key}",
    "Content-Type": "application/json",
}
body = {
    "model": "gpt-oss:20b-cloud",
    "messages": [{"role": "user", "content": "Hello. Reply exactly with: Model is working."}],
    "stream": False,
}

# 2. Send request #################################

response = requests.post(url, headers=headers, json=body, timeout=60)
response.raise_for_status()
result = response.json()

# 3. Print response #################################

output = result["message"]["content"]
print("\nModel response:\n")
print(output)
print("\nDone.\n")
