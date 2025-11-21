# Multi-Agent Attack Pipeline

An experimental multi-agent system that explores whether task decomposition by an orchestrator agent can improve code generation quality by providing more compact context to individual coding agents.

## Architecture

The system consists of two main agents:

1. **Orchestrator Agent** (Ollama - local open-weight models)
   - Analyzes complex coding tasks
   - Breaks them down into smaller, focused subtasks
   - Delegates subtasks to the coding agent via tool calls
   - Can call the coding agent multiple times iteratively
   - Assembles the final results

2. **Coding Agent** (OpenAI GPT-3.5/4)
   - Acts as a powerful "tool" for the orchestrator
   - Generates code for individual subtasks with compact context
   - Returns structured code results

## Hypothesis

By breaking down large tasks into smaller subtasks with focused context, we can achieve:
- Better code quality (less context confusion)
- More accurate implementations (clearer requirements)
- Efficient token usage (compact context per subtask)

## Project Structure

```
multi-agent-attack/
├── src/
│   ├── agents/
│   │   ├── orchestrator.py      # Ollama-based orchestrator
│   │   ├── coding_agent.py      # GPT wrapper as a tool
│   │   └── base_agent.py        # Shared interfaces
│   ├── core/
│   │   ├── models.py            # Task/subtask models (Pydantic)
│   ├── utils/
│   │   ├── ollama_client.py     # Ollama API wrapper
│   │   └── openai_client.py     # OpenAI API wrapper
│   ├── config.py                # Configuration
│   └── pipeline.py              # Main pipeline
├── examples/
│   ├── simple_example.py        # Basic demo
│   └── complex_example.py       # Complex task demo
└── requirements.txt
```

## Setup

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **OpenAI API Key** - Get from [platform.openai.com](https://platform.openai.com)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd multi-agent-attack
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install and start Ollama:
```bash
# Install Ollama (see https://ollama.ai for your OS)

# Pull a model (e.g., Llama 3.1)
ollama pull llama3.1

# Start Ollama (it runs as a service)
ollama serve
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Configuration

Edit `.env` to customize:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1  # or mistral, codellama, etc.

# Agent Configuration
ORCHESTRATOR_TEMPERATURE=0.7
CODING_AGENT_TEMPERATURE=0.2
MAX_ORCHESTRATOR_ITERATIONS=10
```

## Usage

### Basic Example

```python
from src.pipeline import MultiAgentPipeline

# Create pipeline
pipeline = MultiAgentPipeline()

# Define task
task = "Create a Python calculator with basic operations"

# Process task
result = pipeline.process(
    task_description=task,
    verbose=True
)

# Save results
pipeline.save_results(result, output_dir="./output")
```

### Run Examples

```bash
# Simple calculator example
python examples/simple_example.py

# Complex REST API example
python examples/complex_example.py
```

## How It Works

1. **User provides a task** to the pipeline
2. **Orchestrator receives the task** and analyzes it
3. **Orchestrator breaks down** the task into subtasks
4. **For each subtask**, orchestrator calls the coding agent as a tool:
   - Provides focused description
   - Includes only relevant context
   - Receives generated code
5. **Orchestrator reviews** the results and can:
   - Request refinements
   - Generate additional subtasks
   - Continue until satisfied
6. **Results are assembled** into a final output with:
   - Generated code files
   - Task summary
   - Subtask metadata

## Key Features

- **Tool-calling pattern**: Coding agent is exposed as a tool, not a peer
- **Iterative refinement**: Orchestrator can call coding agent multiple times
- **Compact context**: Each subtask has focused, minimal context
- **Flexible models**: Swap Ollama/OpenAI models easily
- **Simple generation**: Focus on code generation (no execution)

## Configuration Options

### Choosing Models

**Orchestrator (Ollama):**
- `llama3.1` - Good general reasoning (recommended)
- `mistral` - Fast and capable
- `codellama` - Specialized for code (may be too specialized for orchestration)
- `qwen2.5:32b` - Larger model for complex tasks

**Coding Agent (OpenAI):**
- `gpt-4` - Best quality (recommended for experiments)
- `gpt-4-turbo` - Faster, good quality
- `gpt-3.5-turbo` - Faster, lower cost

### Temperature Settings

- **Orchestrator**: `0.7` (higher for creative task decomposition)
- **Coding Agent**: `0.2` (lower for deterministic code generation)

## Evaluation

To evaluate whether this approach improves quality:

1. **Define benchmark tasks** (various complexity levels)
2. **Run baseline**: Single agent handles entire task
3. **Run multi-agent**: Orchestrator + coding agent
4. **Compare**:
   - Code correctness (tests passing)
   - Code quality (static analysis)
   - Token efficiency (total tokens used)
   - Task completion rate
5. **Use LLM as judge** to compare outputs

## Limitations

- Currently generates code only (no execution/modification)
- Relies on Ollama's tool calling (may vary by model)
- No validation layer (future enhancement)
- Sequential execution (no parallel subtasks yet)

## Future Enhancements

- [ ] Add validation layer (syntax check, tests)
- [ ] Support parallel subtask execution
- [ ] Add file modification/editing capabilities
- [ ] Implement evaluation framework
- [ ] Add more sophisticated context management
- [ ] Support for multi-modal tasks (images, diagrams)
- [ ] Add human-in-the-loop approval

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull a model
ollama pull llama3.1
```

### OpenAI API Errors
- Check API key in `.env`
- Verify API quota/billing
- Check network connectivity

## License

MIT

## Contributing

This is an experimental research project. Contributions, ideas, and feedback are welcome!
