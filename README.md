# Multi-Agent Attack Pipeline

An experimental multi-agent system that explores whether task decomposition by an orchestrator agent can improve code generation quality by providing more compact context to individual coding agents.

## Architecture

The system consists of two main agents:

1. **Orchestrator Agent** (Azure AI or Local Ollama)
   - Analyzes complex coding tasks
   - Breaks them down into smaller, focused subtasks
   - Delegates subtasks to the coding agent via tool calls
   - Can call the coding agent multiple times iteratively
   - Assembles the final results
   - Supports two backends:
     - **Azure**: Cloud-based models (DeepSeek, GPT-4, etc.)
     - **Ollama**: Local models (Llama3.2 1B, etc.)

2. **Coding Agent** (Azure OpenAI)
   - Acts as a powerful "tool" for the orchestrator
   - Generates code for individual subtasks with compact context
   - Returns structured code results
   - Always uses Azure-hosted models for maximum capability

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
2. **Azure OpenAI API credentials** - For the coding agent (required)
3. **Either**:
   - **Azure AI credentials** - For cloud-based orchestrator (DeepSeek, GPT-4, etc.)
   - **Ollama** - For local orchestrator (Llama3.2 1B, etc.)

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

Edit `.env` with your credentials:

```bash
# Azure Configuration (OpenAI v1 compatible endpoint)
AZUREAI_BASE_URL=https://your-resource.openai.azure.com/
AZUREAI_API_KEY=your_azure_api_key

# Ollama Configuration (for local orchestrator)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# Orchestrator Backend Selection
# Options: "azure" or "ollama"
ORCHESTRATOR_BACKEND=azure

# Model Selection
CODING_AGENT_MODEL=gpt-4.1-mini
ORCHESTRATOR_MODEL=DeepSeek-V3.1  # Only used if ORCHESTRATOR_BACKEND=azure

# Agent Configuration
ORCHESTRATOR_TEMPERATURE=0.7
CODING_AGENT_TEMPERATURE=0.2
MAX_ORCHESTRATOR_ITERATIONS=10
```

#### Using Azure Backend (Default)

The Azure backend uses OpenAI v1 compatible endpoints and supports models like:
- DeepSeek-V3.1
- gpt-4.1, gpt-4.1-mini, gpt-5, gpt-5-mini, gpt-5-nano
- grok-3, grok-3-mini, grok-4-fast-reasoning

Set `ORCHESTRATOR_BACKEND=azure` in `.env`.

#### Using Ollama Backend (Local)

To use a local Llama model as the orchestrator:

1. Install Ollama: https://ollama.ai/
2. Pull the model:
   ```bash
   ollama pull llama3.2:1b
   ```
3. Start Ollama server (usually runs automatically)
4. Set `ORCHESTRATOR_BACKEND=ollama` in `.env`

This is useful for:
- Testing with weaker orchestrators to understand task decomposition quality
- Reducing costs (local orchestrator, cloud coding agent)
- Offline development

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
# Simple calculator example (uses Azure backend by default)
python -m examples.simple_example

# Complex REST API example
python -m examples.complex_example

# Using Ollama backend with Llama3.2 1B orchestrator
python -m examples.ollama_example

# Benchmark: Ollama single-model agent baseline
python -m examples.benchmark_ollama_example

# Benchmark: Azure single-model agent baseline
python -m examples.benchmark_azure_example
```

### Programmatic Usage with Different Backends

**Using Azure backend:**
```python
from src.pipeline import create_pipeline

pipeline = create_pipeline(
    orchestrator_backend="azure",
    orchestrator_model="DeepSeek-V3.1"
)

result = pipeline.process("Create a web scraper...")
```

**Using Ollama backend:**
```python
from src.pipeline import create_pipeline

pipeline = create_pipeline(
    orchestrator_backend="ollama",
    orchestrator_model="llama3.2:1b",
    orchestrator_base_url="http://localhost:11434"
)

result = pipeline.process("Create a web scraper...")
```

## Benchmarking

To validate the hypothesis that multi-agent decomposition improves code quality, the system includes baseline benchmark agents for comparison.

### Benchmark Agents

Benchmark agents complete tasks using a single model without decomposition. Two agents are provided:

1. **BenchmarkOllamaAgent**: Uses local Ollama models (e.g., qwen2.5:7b)
2. **BenchmarkAzureAgent**: Uses cloud Azure models (e.g., gpt-4.1-mini)

**Key features:**
- Same prompt for all models (fair comparison)
- Single API call - no task decomposition
- Uses appropriate backend automatically (no configuration mixing)

### Running Benchmarks

```bash
# Test individual benchmark agents
python -m examples.benchmark_ollama_example  # Local Ollama model
python -m examples.benchmark_azure_example   # Cloud Azure model

# Full benchmark comparing all three approaches
python benchmark.py
```

The benchmark script compares:
- **Multi-agent pipeline**: Orchestrator + coding agent with task decomposition
- **Benchmark Ollama agent**: Single call to local Ollama model
- **Benchmark Azure agent**: Single call to cloud Azure model

### Benchmark Metrics

For each approach, the benchmark tracks:
- Execution time
- Number of subtasks created
- Generated code quality (manual evaluation)
- Token usage efficiency

Results are saved in organized directories for easy comparison:
```
benchmark_output/
├── 1_multi_agent_pipeline/
│   ├── summary.txt
│   └── metadata.json
├── 2_benchmark_ollama/
│   ├── code.txt
│   └── metadata.json
├── 3_benchmark_azure/
│   ├── code.txt
│   └── metadata.json
└── comparison.json
```

### Expected Results

The hypothesis is that the multi-agent pipeline should achieve:
- **Better code quality** through focused subtasks
- **More modular outputs** that are easier to maintain
- **Potentially longer execution time** due to multiple LLM calls
- **Better handling of complex tasks** that benefit from decomposition

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
