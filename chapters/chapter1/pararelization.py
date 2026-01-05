import asyncio
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableParallel,
    RunnablePassthrough,
)
from dotenv import load_dotenv

load_dotenv()
# --- Configuration ---
# Ensure your GOOGLE_API_KEY environment variable is set

try:
    llm: Optional[ChatGoogleGenerativeAI] = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None

# --- Define Independent Chains (Parallel Tasks) ---

summarize_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Summarize the following topic concisely:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

questions_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate three interesting questions about the following topic:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

terms_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        (
            "system",
            "Identify 5–10 key terms from the following topic, separated by commas:"
        ),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

# --- Parallel Map Step ---
map_chain = RunnableParallel(
    {
        "summary": summarize_chain,
        "questions": questions_chain,
        "key_terms": terms_chain,
        "topic": RunnablePassthrough(),
    }
)

# --- Synthesis Step ---
synthesis_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Based on the following information:
Summary: {summary}
Related Questions: {questions}
Key Terms: {key_terms}

Synthesize a comprehensive answer."""
    ),
    ("user", "Original topic: {topic}")
])

# --- Full Chain ---
full_parallel_chain = (
    map_chain
    | synthesis_prompt
    | llm
    | StrOutputParser()
)

# --- Run the Chain ---
async def run_parallel_example(topic: str) -> None:
    if not llm:
        print("LLM not initialized. Cannot run example.")
        return

    print(f"\n--- Running Parallel Gemini LangChain Example for Topic: '{topic}' ---")

    try:
        response = await full_parallel_chain.ainvoke(topic)
        print("\n--- Final Response ---")
        print(response)
    except Exception as e:
        print(f"\nAn error occurred during chain execution: {e}")

if __name__ == "__main__":
    test_topic = "The history of space exploration"
    asyncio.run(run_parallel_example(test_topic))
