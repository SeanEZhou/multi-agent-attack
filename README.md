# Multi-Agent Attack Pipeline

An experimental multi-agent system that explores whether task decomposition by an orchestrator agent can improve code generation quality by providing more compact context to individual coding agents.

## Architecture

The system consists of two main agents:

1. **Orchestrator Agent** (Azure AI Studio - GPT-4o or similar)
   - Analyzes complex coding tasks
   - Breaks them down into smaller, focused subtasks
   - Delegates subtasks to the coding agent via tool calls
   - Can call the coding agent multiple times iteratively
   - Assembles the final results

2. **Coding Agent** (Azure OpenAI - GPT-4)
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
│   │   ├── orchestrator.py      # Azure AI-based orchestrator
│   │   └── coding_agent.py      # Azure OpenAI wrapper as a tool
│   ├── core/
│   │   └── models.py            # Task/subtask models (Pydantic)
│   ├── utils/
│   │   ├── azure_ai_client.py   # Azure AI Studio API wrapper
│   │   └── openai_client.py     # Azure OpenAI API wrapper
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
2. **Azure OpenAI API credentials** - For the coding agent
3. **Azure AI Studio API credentials** - For the orchestrator agent

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd multi-agent-attack
```

2. Create and activate conda environment:
```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate multi-agent-attack
```

Alternatively, using pip:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your Azure credentials (see below)
```

4. Test your Azure connections:
```bash
python test_azure_connection.py
```

### Configuration

Edit `.env` with your Azure credentials:

```bash
# Azure OpenAI Configuration (for Coding Agent)
AZUREAI_OPENAI_BASE_URL=https://your-resource.openai.azure.com/
AZUREAI_OPENAI_API_KEY=your_azure_openai_api_key
AZUREAI_OPENAI_DEPLOYMENT=gpt-4  # Your deployment name
AZUREAI_OPENAI_API_VERSION=2024-02-15-preview

# Azure AI Studio Configuration (for Orchestrator Agent)
AZUREAI_API_KEY=your_azure_ai_api_key
AZUREAI_BASE_URL=https://your-endpoint.services.ai.azure.com/models
AZUREAI_MODEL=gpt-4o  # Or another available model

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
- **Azure-based**: Both agents use Azure cloud models (no local compute required)
- **Simple generation**: Focus on code generation (no execution)

## Configuration Options

### Choosing Models

**Orchestrator (Azure AI Studio):**
- `gpt-4o` - Latest GPT-4 optimized model (recommended)
- `gpt-4` - Strong reasoning for complex task decomposition
- `gpt-4-turbo` - Faster with good quality
- `gpt-35-turbo` - Cost-effective for simpler tasks

**Coding Agent (Azure OpenAI):**
- `gpt-4` - Best quality (recommended for experiments)
- `gpt-4-turbo` - Faster, good quality
- `gpt-35-turbo` - Faster, lower cost

Note: Model availability depends on your Azure deployment.

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
- Relies on Azure AI Studio's tool calling capabilities
- No validation layer (future enhancement)
- Sequential execution (no parallel subtasks yet)
- Requires Azure API access and credits

## Future Enhancements

- [ ] Add validation layer (syntax check, tests)
- [ ] Support parallel subtask execution
- [ ] Add file modification/editing capabilities
- [ ] Implement evaluation framework
- [ ] Add more sophisticated context management
- [ ] Support for multi-modal tasks (images, diagrams)
- [ ] Add human-in-the-loop approval

## Troubleshooting

### Azure OpenAI API Errors
- Check `AZUREAI_OPENAI_API_KEY` and `AZUREAI_OPENAI_BASE_URL` in `.env`
- Verify your deployment name matches `AZUREAI_OPENAI_DEPLOYMENT`
- Check Azure quota/billing
- Ensure API version is correct

### Azure AI Studio API Errors
- Check `AZUREAI_API_KEY` and `AZUREAI_BASE_URL` in `.env`
- Verify the model name in `AZUREAI_MODEL` is available in your deployment
- Check endpoint is accessible
- Review Azure network/firewall settings

### Common Issues

**"Deployment not found"**:
- Verify your deployment name in Azure Portal matches the config

**"Unauthorized"**:
- Check API keys are correct and not expired
- Ensure the keys have proper permissions

**"Rate limit exceeded"**:
- Check your Azure quota limits
- Consider adding retry logic or reducing request frequency

## License

MIT

## Contributing

This is an experimental research project. Contributions, ideas, and feedback are welcome!
