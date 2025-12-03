"""
Benchmark script to compare multi-agent pipeline vs benchmark agents.

Compares three approaches:
1. Multi-agent pipeline (orchestrator + coding agent)
2. Benchmark Ollama agent (local model)
3. Benchmark Azure agent (cloud model)
"""

import time
import json
from src.pipeline import MultiAgentPipeline
from src.agents.benchmark_ollama_agent import BenchmarkOllamaAgent
from src.agents.benchmark_azure_agent import BenchmarkAzureAgent
from src.core.models import Task


def run_benchmark(task_description: str, requirements: str = None, output_dir: str = "./benchmark_output"):
    """
    Run benchmark comparing all three approaches.

    Args:
        task_description: The task to complete
        requirements: Optional requirements
        output_dir: Directory to save results
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    task = Task(
        description=task_description,
        requirements=requirements
    )

    results = {}

    print("\n" + "="*80)
    print("BENCHMARK: Multi-Agent Pipeline vs Singleton Agents")
    print("="*80)
    print(f"Task: {task_description}\n")

    # 1. Multi-agent pipeline
    print("\n" + "="*80)
    print("APPROACH 1: Multi-Agent Pipeline")
    print("="*80)
    start_time = time.time()
    pipeline = MultiAgentPipeline()
    result_pipeline = pipeline.process(task_description=task_description, requirements=requirements, verbose=True)
    pipeline_time = time.time() - start_time

    results["multi_agent_pipeline"] = {
        "time_seconds": pipeline_time,
        "num_subtasks": len(result_pipeline.subtasks),
        "num_code_results": len(result_pipeline.code_results),
        "code_results": [cr.model_dump() for cr in result_pipeline.code_results],
        "summary": result_pipeline.summary
    }

    # Save pipeline results
    pipeline_dir = os.path.join(output_dir, "1_multi_agent_pipeline")
    pipeline.save_results(result_pipeline, output_dir=pipeline_dir)

    # 2. Benchmark Ollama agent
    print("\n" + "="*80)
    print("APPROACH 2: Benchmark Ollama Agent (Local Model)")
    print("="*80)

    start_time = time.time()
    ollama_agent = BenchmarkOllamaAgent()
    result_ollama = ollama_agent.process_task(task, verbose=True)
    ollama_time = time.time() - start_time

    results["benchmark_ollama"] = {
        "model": ollama_agent.model,
        "backend": "ollama",
        "time_seconds": ollama_time,
        "num_subtasks": len(result_ollama.subtasks),
        "num_code_results": len(result_ollama.code_results),
        "code_results": [cr.model_dump() for cr in result_ollama.code_results],
        "summary": result_ollama.summary
    }

    # Save Ollama results
    ollama_dir = os.path.join(output_dir, "2_benchmark_ollama")
    os.makedirs(ollama_dir, exist_ok=True)
    with open(os.path.join(ollama_dir, "code.txt"), 'w') as f:
        f.write(result_ollama.code_results[0].code)
    with open(os.path.join(ollama_dir, "metadata.json"), 'w') as f:
        json.dump(results["benchmark_ollama"], f, indent=2)

    # 3. Benchmark Azure agent
    print("\n" + "="*80)
    print("APPROACH 3: Benchmark Azure Agent (Cloud Model)")
    print("="*80)

    start_time = time.time()
    azure_agent = BenchmarkAzureAgent()
    result_azure = azure_agent.process_task(task, verbose=True)
    azure_time = time.time() - start_time

    results["benchmark_azure"] = {
        "model": azure_agent.model,
        "backend": "azure",
        "time_seconds": azure_time,
        "num_subtasks": len(result_azure.subtasks),
        "num_code_results": len(result_azure.code_results),
        "code_results": [cr.model_dump() for cr in result_azure.code_results],
        "summary": result_azure.summary
    }

    # Save Azure results
    azure_dir = os.path.join(output_dir, "3_benchmark_azure")
    os.makedirs(azure_dir, exist_ok=True)
    with open(os.path.join(azure_dir, "code.txt"), 'w') as f:
        f.write(result_azure.code_results[0].code)
    with open(os.path.join(azure_dir, "metadata.json"), 'w') as f:
        json.dump(results["benchmark_azure"], f, indent=2)

    # Print summary
    print("\n" + "="*80)
    print("BENCHMARK RESULTS SUMMARY")
    print("="*80)
    print(f"\n1. Multi-Agent Pipeline:")
    print(f"   - Time: {pipeline_time:.2f}s")
    print(f"   - Subtasks: {len(result_pipeline.subtasks)}")
    print(f"   - Code results: {len(result_pipeline.code_results)}")

    print(f"\n2. Benchmark Ollama Agent ({ollama_agent.model}):")
    print(f"   - Time: {ollama_time:.2f}s")
    print(f"   - Code results: {len(result_ollama.code_results)}")

    print(f"\n3. Benchmark Azure Agent ({azure_agent.model}):")
    print(f"   - Time: {azure_time:.2f}s")
    print(f"   - Code results: {len(result_azure.code_results)}")

    print(f"\nResults saved to: {output_dir}/")
    print("="*80 + "\n")

    # Save comparison
    comparison = {
        "task": task.model_dump(),
        "results": results,
        "comparison": {
            "multi_agent_vs_ollama_speedup": ollama_time / pipeline_time if pipeline_time > 0 else 0,
            "multi_agent_vs_azure_speedup": azure_time / pipeline_time if pipeline_time > 0 else 0
        }
    }

    with open(os.path.join(output_dir, "comparison.json"), 'w') as f:
        json.dump(comparison, f, indent=2)

    return results


if __name__ == "__main__":
    # Example benchmark task
    task = """
    Create a simple web scraper that extracts article titles and URLs from a news website.
    The scraper should handle pagination and save results to a CSV file.
    """

    requirements = """
    - Use requests and BeautifulSoup libraries
    - Handle HTTP errors gracefully
    - Include rate limiting to be respectful
    - Save to 'articles.csv' with columns: title, url, date_scraped
    """

    run_benchmark(task, requirements, output_dir="./benchmark_output/web_scraper")
