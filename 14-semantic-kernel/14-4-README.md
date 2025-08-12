# Sequential Orchestration

## Overview

The sequential orchestration pattern organizes agents in a pipeline. Each agent processes the task in turn, passing its output to the next agent. This is ideal for workflows where each step builds upon the previous one, such as document review or multi-stage reasoning.

<p align="left">
  <img src="image.png" alt="Semantic Kernel Multi Agent Sequential Orchestration" width="500" height="550"/>
</p>


## Files

- `sequential-orchestration.py`: Fitness post optimization pipeline.
- `sequential-orchestration-V2.py`: Business post optimization pipeline.

## How It Works

This example optimizes a social media post using a pipeline of three agents:

1. **AnalyzerAgent**: Analyzes the original post for tone, engagement, and areas to improve.
2. **OptimizerAgent**: Uses the analysis to rewrite the post for better engagement and clarity.
3. **ReviewerAgent**: Polishes the optimized post, ensuring perfect grammar, effective hashtags, and a compelling call-to-action.

The output from each agent is passed to the next, resulting in a final, highly optimized post ready for publishing.


## Setup

1. Install dependencies (from project root):
   ```sh
   pip install -r ../requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials.
3. Change to this directory:
   ```sh
   cd sequential
   ```

## Running the Examples

- **Fitness Post Optimization:**
  ```sh
  python sequential-orchestration.py
  ```
- **Business Post Optimization:**
  ```sh
  python sequential-orchestration-V2.py
  ```

## Customization

You can modify the agent instructions or add new pipeline steps in the scripts to fit your workflow.

## Notes

- Ensure your `.env` file contains valid Azure OpenAI credentials.