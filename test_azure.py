"""
Simple test script to verify Azure OpenAI endpoint is working.
Uses environment variables from .env file.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get configuration from .env
api_key = os.getenv("AZUREAI_API_KEY")
base_url = os.getenv("AZUREAI_BASE_URL")
model = os.getenv("ORCHESTRATOR_MODEL", "gpt-4.1-mini")

# Create client
client = OpenAI(
    base_url=f"{base_url}openai/v1",
    api_key=api_key,
)

print(f"Testing Azure OpenAI endpoint...")
print(f"Base URL: {base_url}openai/v1")
print(f"Model: {model}\n")

# Test the endpoint
resp = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain yourself to me in 2 sentences."},
    ],
)

print("Response:")
print(resp.choices[0].message.content)
print("\n✓ Azure OpenAI endpoint is working!")