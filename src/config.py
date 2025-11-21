import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Agent Configuration
ORCHESTRATOR_TEMPERATURE = float(os.getenv("ORCHESTRATOR_TEMPERATURE", "0.7"))
CODING_AGENT_TEMPERATURE = float(os.getenv("CODING_AGENT_TEMPERATURE", "0.2"))
MAX_ORCHESTRATOR_ITERATIONS = int(os.getenv("MAX_ORCHESTRATOR_ITERATIONS", "10"))
