#!/usr/bin/env python3
"""
OpenAI Agent SDK Orchestrator
This script uses multiple agents to:
1. Analyze a user prompt to understand intent
2. Refine the prompt to be clearer and more actionable
3. Execute the refined prompt with specialized agents
4. Report back the results
"""

import asyncio
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv()


class PromptOrchestrator:
    """Orchestrates multiple agents to process and improve user prompts."""

    def __init__(self):
        """Initialize the orchestrator and all agents."""
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )

        # Note: Tracing is enabled by default in the SDK
        # View traces in OpenAI Platform Dashboard

        # Initialize all agents
        self._setup_agents()

    def _setup_agents(self):
        """Create and configure all agents in the system."""

        # Agent 1: Prompt Analyzer - understands what the user really wants
        self.analyzer_agent = Agent(
            name="Prompt Analyzer",
            instructions="""You are an expert at understanding user intent.
            Your job is to analyze user prompts and identify:
            1. The core objective - what does the user truly want to achieve?
            2. Implicit requirements - what might be unstated but necessary?
            3. Ambiguities - what needs clarification?
            4. Context clues - what domain or field is this related to?
            5. Success criteria - how would we know if we've met their needs?

            Provide a detailed analysis in a structured format.
            Be thorough and insightful."""
        )

        # Agent 2: Prompt Refiner - creates a better prompt
        self.refiner_agent = Agent(
            name="Prompt Refiner",
            instructions="""You are an expert at crafting clear, actionable prompts.
            Based on the analysis provided, create an improved version of the original prompt that:
            1. Is clear and unambiguous
            2. Includes all necessary context
            3. Specifies expected outputs or deliverables
            4. Addresses any identified gaps or ambiguities
            5. Is structured for optimal AI understanding

            Output the refined prompt in a clear, ready-to-use format.
            Make it significantly better than the original."""
        )

        # Agent 3: Research Specialist - for information gathering tasks
        self.research_agent = Agent(
            name="Research Specialist",
            instructions="""You are a research specialist who excels at:
            1. Gathering and synthesizing information
            2. Identifying key facts and insights
            3. Providing comprehensive, well-structured answers
            4. Citing reasoning and thought processes

            When given a prompt, provide thorough, accurate information."""
        )

        # Agent 4: Task Executor - for action-oriented tasks
        self.task_agent = Agent(
            name="Task Executor",
            instructions="""You are a task execution specialist who excels at:
            1. Breaking down complex tasks into steps
            2. Providing clear action plans
            3. Identifying resources and requirements needed
            4. Anticipating potential challenges

            When given a prompt, provide a detailed execution plan or solution."""
        )

        # Agent 5: Creative Specialist - for creative tasks
        self.creative_agent = Agent(
            name="Creative Specialist",
            instructions="""You are a creative specialist who excels at:
            1. Generating original ideas and content
            2. Thinking outside the box
            3. Providing multiple creative options
            4. Balancing creativity with practicality

            When given a prompt, provide creative, innovative solutions."""
        )

        # Agent 6: Router - decides which executor agent to use
        self.router_agent = Agent(
            name="Task Router",
            instructions="""You are a routing specialist who decides which agent should handle a task.
            Based on the refined prompt, determine if it's primarily:
            - Research/Information gathering → use Research Specialist
            - Task execution/Planning → use Task Executor
            - Creative/Ideation → use Creative Specialist

            Choose the most appropriate agent and explain your reasoning briefly.""",
            handoffs=[self.research_agent, self.task_agent, self.creative_agent]
        )

        # Agent 7: Reporter - synthesizes and reports results
        self.reporter_agent = Agent(
            name="Results Reporter",
            instructions="""You are a results synthesizer and reporter.
            Your job is to take all the information from the process and create a clear,
            comprehensive report for the user that includes:
            1. What we understood from their original request
            2. How we refined their prompt
            3. What approach we took to fulfill it
            4. The actual results/answer/solution
            5. Any recommendations or next steps

            Make the report clear, organized, and actionable.
            Use headers and structure for readability."""
        )

    async def process_prompt(self, user_prompt: str) -> dict:
        """
        Process a user prompt through the entire agent pipeline.

        Args:
            user_prompt: The original user prompt to process

        Returns:
            Dictionary containing all stages of processing and final results
        """
        print("\n" + "="*80)
        print("🤖 AGENT ORCHESTRATION SYSTEM")
        print("="*80)

        results = {
            "original_prompt": user_prompt,
            "analysis": None,
            "refined_prompt": None,
            "execution_results": None,
            "final_report": None
        }

        # Step 1: Analyze the prompt
        print("\n📊 STEP 1: Analyzing your prompt...")
        print("-" * 80)
        analysis_result = await Runner.run(
            self.analyzer_agent,
            user_prompt
        )
        results["analysis"] = analysis_result.final_output
        print(f"\nAnalysis:\n{results['analysis']}")

        # Step 2: Refine the prompt
        print("\n✨ STEP 2: Refining your prompt...")
        print("-" * 80)
        refiner_input = f"""Original prompt: {user_prompt}

Analysis: {results['analysis']}

Based on this analysis, create a refined, improved version of the prompt."""

        refiner_result = await Runner.run(
            self.refiner_agent,
            refiner_input
        )
        results["refined_prompt"] = refiner_result.final_output
        print(f"\nRefined Prompt:\n{results['refined_prompt']}")

        # Step 3: Execute with appropriate specialist agent
        print("\n⚡ STEP 3: Executing the refined prompt...")
        print("-" * 80)
        execution_result = await Runner.run(
            self.router_agent,
            results["refined_prompt"]
        )
        results["execution_results"] = execution_result.final_output
        print(f"\nExecution Results:\n{results['execution_results']}")

        # Step 4: Generate final report
        print("\n📝 STEP 4: Generating final report...")
        print("-" * 80)
        report_input = f"""Please create a comprehensive report based on this process:

ORIGINAL USER PROMPT:
{user_prompt}

OUR ANALYSIS:
{results['analysis']}

REFINED PROMPT:
{results['refined_prompt']}

EXECUTION RESULTS:
{results['execution_results']}

Create a clear, well-structured report for the user."""

        report_result = await Runner.run(
            self.reporter_agent,
            report_input
        )
        results["final_report"] = report_result.final_output

        return results

    def display_final_report(self, results: dict):
        """Display the final report to the user."""
        print("\n" + "="*80)
        print("📋 FINAL REPORT")
        print("="*80)
        print(results["final_report"])
        print("\n" + "="*80)


async def main():
    """Main entry point for the orchestrator."""
    print("OpenAI Agent SDK Orchestrator")
    print("=" * 80)

    # Check for command-line argument
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        print("\nEnter your prompt (or 'quit' to exit):")
        user_prompt = input("> ").strip()

        if not user_prompt or user_prompt.lower() == 'quit':
            print("Goodbye!")
            return

    try:
        # Initialize orchestrator
        orchestrator = PromptOrchestrator()

        # Process the prompt
        results = await orchestrator.process_prompt(user_prompt)

        # Display final report
        orchestrator.display_final_report(results)

        # Optionally save results to file
        save = input("\n💾 Would you like to save the full results to a file? (y/n): ").strip().lower()
        if save == 'y':
            filename = "orchestration_results.txt"
            with open(filename, 'w') as f:
                f.write("AGENT ORCHESTRATION RESULTS\n")
                f.write("=" * 80 + "\n\n")
                for key, value in results.items():
                    f.write(f"{key.upper().replace('_', ' ')}:\n")
                    f.write("-" * 80 + "\n")
                    f.write(f"{value}\n\n")
            print(f"✅ Results saved to {filename}")

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
