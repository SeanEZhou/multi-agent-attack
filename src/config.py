import os
from dotenv import load_dotenv

load_dotenv()

# Azure Configuration (shared by both agents)
AZUREAI_BASE_URL = os.getenv("AZUREAI_BASE_URL")
AZUREAI_API_KEY = os.getenv("AZUREAI_API_KEY")

# Model Selection
CODING_AGENT_MODEL = os.getenv("CODING_AGENT_MODEL", "gpt-5")
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "grok-4-fast-reasoning")

# Agent Configuration
ORCHESTRATOR_TEMPERATURE = float(os.getenv("ORCHESTRATOR_TEMPERATURE", "0.7"))
CODING_AGENT_TEMPERATURE = float(os.getenv("CODING_AGENT_TEMPERATURE", "0.2"))
MAX_ORCHESTRATOR_ITERATIONS = int(os.getenv("MAX_ORCHESTRATOR_ITERATIONS", "10"))
