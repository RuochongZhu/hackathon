# workflow.py
# OpenAI API Workflow Demo (Python)
# Tim Fraser
#
# This script demonstrates a minimal OpenAI API request using an API key
# loaded from a local .env file.

# 0. Setup #################################

## 0.1 Load packages ############################

import os
import requests
from dotenv import load_dotenv

## 0.2 Load environment variables ############################

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")

# 1. Build request #################################

url = "https://api.openai.com/v1/responses"
headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
}
body = {
    "model": "gpt-4o-mini",
    "input": "Hello. Reply exactly with: Model is working.",
}

# 2. Send request #################################

response = requests.post(url, headers=headers, json=body, timeout=60)
response.raise_for_status()
result = response.json()

# 3. Print response #################################

output = result["output"][0]["content"][0]["text"]
print("\nModel response:\n")
print(output)
print("\nDone.\n")
