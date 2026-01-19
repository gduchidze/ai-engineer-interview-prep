import os
import getpass
import asyncio
import nest_asyncio

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_agent

# --- Environment Setup ---
load_dotenv()

# Securely prompt for API keys if not already set
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass(
        "Enter your Google API key: "
    )

# --- Initialize LLM ---
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
    )
    print(f"✅ Language model initialized: {llm.model}")
except Exception as e:
    print(f"🛑 Error initializing language model: {e}")
    llm = None

# --- Define Tool ---
@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic.
    Use this tool for factual questions like:
    - capital of France
    - weather in London
    """
    print(
        f"\n--- 🔧 Tool Called: search_information "
        f"with query: '{query}' ---"
    )

    simulated_results = {
        "weather in london": (
            "The weather in London is currently cloudy "
            "with a temperature of 15°C."
        ),
        "capital of france": "The capital of France is Paris.",
        "population of earth": (
            "The estimated population of Earth is around 8 billion people."
        ),
        "tallest mountain": (
            "Mount Everest is the tallest mountain above sea level."
        ),
    }

    result = simulated_results.get(
        query.lower(),
        f"Simulated search result for '{query}': "
        "No specific information found, but the topic seems interesting."
    )

    print(f"--- 🔍 TOOL RESULT: {result} ---")
    return result

tools = [search_information]

# --- Create Agent ---
if llm:
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a helpful assistant."
    )

# --- Async Runner ---
async def run_agent_with_tool(query: str):
    """Run the agent with a single query."""
    print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
    try:
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        print("\n--- ✅ Final Agent Response ---")
        # Extract the last message content from the response
        if "messages" in response:
            last_message = response["messages"][-1]
            print(last_message.content if hasattr(last_message, "content") else last_message)
        else:
            print(response)
    except Exception as e:
        print(f"\n🛑 Agent execution error: {e}")

async def main():
    """Run multiple agent queries concurrently."""
    tasks = [
        run_agent_with_tool("What is the capital of France?"),
        run_agent_with_tool("What's the weather like in London?"),
        run_agent_with_tool("Tell me something about dogs."),
    ]
    await asyncio.gather(*tasks)

# --- Entry Point ---
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
