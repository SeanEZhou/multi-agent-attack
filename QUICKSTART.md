# Quick Start Guide

Get up and running with the multi-agent pipeline in 5 minutes.

## Step 1: Create Conda Environment

```bash
conda env create -f environment.yml
conda activate multi-agent-attack
```

## Step 2: Verify Configuration

Your `.env` file is already configured with your team's Azure credentials:

```bash
# Azure OpenAI (Coding Agent)
AZUREAI_OPENAI_BASE_URL=https://rfogliato-0714-resource.openai.azure.com/
AZUREAI_OPENAI_DEPLOYMENT=gpt-4

# Azure AI Studio (Orchestrator)
AZUREAI_BASE_URL=https://ahibr-m6p0rpp2-australiaeast.services.ai.azure.com/models
AZUREAI_MODEL=gpt-4o
```

**Important**: Verify that:
1. The deployment name `gpt-4` exists in your Azure OpenAI resource
2. The model `gpt-4o` is available in your Azure AI Studio endpoint

## Step 3: Test Azure Connections

```bash
python test_azure_connection.py
```

Expected output:
```
============================================================
Azure API Connection Test
============================================================
Testing Azure OpenAI connection...
✓ Azure OpenAI connection successful!
Response preview: ...

Testing Azure AI Studio connection...
✓ Azure AI Studio connection successful!
Response: Hello, Azure AI!

============================================================
Summary:
============================================================
Azure OpenAI (Coding Agent): ✓ OK
Azure AI Studio (Orchestrator): ✓ OK

✓ All connections successful! You're ready to run the pipeline.
```

## Step 4: Run a Simple Example

```bash
python examples/simple_example.py
```

This will:
1. Task the orchestrator to create a simple Python calculator
2. Orchestrator breaks down the task into subtasks
3. Orchestrator calls the coding agent for each subtask
4. Results are assembled and saved to `./output/simple_calculator/`

## Step 5: Try a Complex Task

```bash
python examples/complex_example.py
```

This creates a full REST API with user management and todo items.

## Common Issues

### "Deployment not found"

Check your Azure OpenAI deployment name:
```bash
# In .env, make sure AZUREAI_OPENAI_DEPLOYMENT matches your actual deployment
AZUREAI_OPENAI_DEPLOYMENT=your-actual-deployment-name
```

### "Model not available"

Check your Azure AI Studio model:
```bash
# In .env, verify the model is available in your endpoint
AZUREAI_MODEL=gpt-4o  # or gpt-4, gpt-35-turbo
```

### Import Errors

Make sure the conda environment is activated:
```bash
conda activate multi-agent-attack
```

## Next Steps

1. **Customize tasks**: Edit the examples to try different coding tasks
2. **Adjust parameters**: Modify `.env` to change temperatures, models, etc.
3. **Build evaluation**: Create your own benchmark tasks to test the hypothesis
4. **Add validation**: Extend the pipeline with code validation and testing

## Usage Example

```python
from src.pipeline import MultiAgentPipeline

# Create pipeline
pipeline = MultiAgentPipeline()

# Process a task
result = pipeline.process(
    task_description="Create a Python class for a binary search tree",
    verbose=True
)

# Save results
pipeline.save_results(result, output_dir="./output/bst")
```

## Monitoring Costs

Both agents use Azure cloud services. To monitor costs:
1. Check Azure Portal > Cost Management
2. Track token usage in the verbose output
3. Consider using `gpt-35-turbo` for experimentation to reduce costs

## Getting Help

- Check [README.md](README.md) for full documentation
- Review [AZURE_MIGRATION.md](AZURE_MIGRATION.md) for technical details
- Check Azure Portal for deployment and quota information
