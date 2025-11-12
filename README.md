# OpenAI Agent SDK Orchestrator

A multi-agent system that intelligently processes user prompts by decomposing them, understanding true intent, refining them, and executing them with specialized AI agents.

## Overview

This project uses the OpenAI Agents SDK to create an orchestrated system of AI agents that work together to:

1. **Analyze** your prompt to understand what you really want
2. **Refine** your prompt to make it clearer and more actionable
3. **Execute** the refined prompt using specialized agents
4. **Report** comprehensive results back to you

## Architecture

The system consists of 7 specialized agents:

- **Prompt Analyzer**: Understands user intent and identifies implicit requirements
- **Prompt Refiner**: Creates an improved, clearer version of the original prompt
- **Research Specialist**: Handles information gathering and research tasks
- **Task Executor**: Manages action-oriented tasks and planning
- **Creative Specialist**: Generates creative ideas and solutions
- **Task Router**: Decides which specialist agent should handle the task
- **Results Reporter**: Synthesizes all findings into a comprehensive report

## Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- `uv` package manager ([Install here](https://docs.astral.sh/uv/))

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd auto-project-001
```

### 2. Set up virtual environment with uv

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Configure API key

Create a `.env` file from the example template:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## Usage

### Interactive Mode

Run the script without arguments for interactive mode:

```bash
python agent_orchestrator.py
```

Then enter your prompt when requested.

### Command-Line Mode

Pass your prompt directly as an argument:

```bash
python agent_orchestrator.py "Help me plan a machine learning project"
```

### Example Prompts

Try these example prompts to see the system in action:

```bash
# Research-oriented
python agent_orchestrator.py "What are the best practices for API design?"

# Task-oriented
python agent_orchestrator.py "I need to organize a team hackathon"

# Creative
python agent_orchestrator.py "Give me ideas for a mobile app that helps people learn languages"

# Complex/Vague
python agent_orchestrator.py "Make my code better"
```

## How It Works

When you submit a prompt, here's what happens:

1. **Analysis Phase**: The Prompt Analyzer examines your input to identify:
   - Core objectives
   - Implicit requirements
   - Ambiguities
   - Context clues
   - Success criteria

2. **Refinement Phase**: The Prompt Refiner creates an improved version that's:
   - Clear and unambiguous
   - Complete with necessary context
   - Structured for optimal AI understanding

3. **Routing Phase**: The Task Router determines which specialist agent is best suited for your refined prompt

4. **Execution Phase**: The chosen specialist agent processes your refined prompt and generates results

5. **Reporting Phase**: The Results Reporter synthesizes everything into a comprehensive, actionable report

## Output

The system provides:

- Real-time progress updates for each phase
- Detailed analysis of your original prompt
- The refined version of your prompt
- Execution results from specialist agents
- A comprehensive final report
- Option to save all results to a file

## Tracing and Debugging

The system has tracing enabled, which means you can view detailed execution logs in the [OpenAI Platform Dashboard](https://platform.openai.com/). This helps you:

- Understand how agents made decisions
- Debug any issues
- Optimize prompts and agent instructions

## Project Structure

```
auto-project-001/
├── agent_orchestrator.py   # Main orchestration script
├── requirements.txt         # Python dependencies
├── .env.example            # Template for environment variables
├── .env                    # Your actual API key (git-ignored)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Customization

You can customize the system by editing `agent_orchestrator.py`:

- **Modify agent instructions**: Change how each agent behaves
- **Add new specialist agents**: Create agents for specific domains
- **Adjust the pipeline**: Change the order or add new processing steps
- **Configure model settings**: Use different models or adjust parameters

Example of adding a custom agent:

```python
self.code_agent = Agent(
    name="Code Specialist",
    instructions="""You are a coding expert who excels at:
    1. Writing clean, efficient code
    2. Debugging and optimization
    3. Explaining complex programming concepts
    ..."""
)
```

## Cost Considerations

This system makes multiple API calls per prompt:
- Analysis: 1 call
- Refinement: 1 call
- Routing + Execution: 1-2 calls (depending on handoffs)
- Reporting: 1 call

Total: ~4-5 API calls per user prompt

Consider this when processing many prompts. Monitor your usage in the [OpenAI Dashboard](https://platform.openai.com/usage).

## Troubleshooting

### "OPENAI_API_KEY not found"

Make sure you've:
1. Created a `.env` file (not `.env.example`)
2. Added your actual API key
3. Activated your virtual environment

### Import errors

Ensure all dependencies are installed:

```bash
uv pip install -r requirements.txt
```

### API errors

Check that:
- Your API key is valid
- You have sufficient credits in your OpenAI account
- You're not hitting rate limits

## License

MIT

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

## Links

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Platform](https://platform.openai.com/)
- [uv Documentation](https://docs.astral.sh/uv/)