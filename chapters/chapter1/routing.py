from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch, RunnableLambda
from dotenv import load_dotenv

load_dotenv()
# --- Configuration ---
# Ensure your GOOGLE_API_KEY environment variable is set

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )
    print(f"Language model initialized: {llm.model}")
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None

# --- Simulated Sub-Agent Handlers ---
def booking_handler(request: str) -> str:
    """Simulates the Booking Agent handling a request."""
    print("\n--- DELEGATING TO BOOKING HANDLER ---")
    return (
        f"Booking Handler processed request: '{request}'. "
        "Result: Simulated booking action."
    )

def info_handler(request: str) -> str:
    """Simulates the Info Agent handling a request."""
    print("\n--- DELEGATING TO INFO HANDLER ---")
    return (
        f"Info Handler processed request: '{request}'. "
        "Result: Simulated information retrieval."
    )

def unclear_handler(request: str) -> str:
    """Handles requests that couldn't be delegated."""
    print("\n--- HANDLING UNCLEAR REQUEST ---")
    return (
        f"Coordinator could not delegate request: '{request}'. "
        "Please clarify."
    )

# --- Coordinator Router Prompt ---
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Analyze the user's request and determine which specialist handler should process it.
- If the request is related to booking flights or hotels, output 'booker'.
- For general information questions, output 'info'.
- If the request is unclear, output 'unclear'.
ONLY output one word: 'booker', 'info', or 'unclear'."""
    ),
    ("user", "{request}")
])

# Initialize coordinator_router_chain (will be None if llm fails to initialize)
coordinator_router_chain = None
if llm:
    coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

# --- Delegation Logic ---
branches = {
    "booker": RunnablePassthrough.assign(
        output=lambda x: booking_handler(x["request"]["request"])  # type: ignore[arg-type]
    ),
    "info": RunnablePassthrough.assign(
        output=lambda x: info_handler(x["request"]["request"])  # type: ignore[arg-type]
    ),
    "unclear": RunnablePassthrough.assign(
        output=lambda x: unclear_handler(x["request"]["request"])  # type: ignore[arg-type]
    ),
}

delegation_branch = RunnableBranch(
    (lambda x: x["decision"].strip() == "booker", branches["booker"]),  # type: ignore[arg-type]
    (lambda x: x["decision"].strip() == "info", branches["info"]),  # type: ignore[arg-type]
    branches["unclear"], # type: ignore[arg-type]
)

# --- Coordinator Agent ---
coordinator_agent = (
    {
        "decision": coordinator_router_chain,
        "request": RunnablePassthrough(),
    }
    | delegation_branch  # type: ignore[arg-type]
    | RunnableLambda(lambda x: x["output"])
)

# --- Example Usage ---
def main():
    if not llm:
        print("\nSkipping execution due to LLM initialization failure.")
        return

    print("\n--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"Final Result A: {result_a}")

    print("\n--- Running with an info request ---")
    request_b = "What is the capital of Italy?"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"Final Result B: {result_b}")

    print("\n--- Running with an unclear request ---")
    request_c = "Tell me about quantum physics."
    result_c = coordinator_agent.invoke({"request": request_c})
    print(f"Final Result C: {result_c}")

if __name__ == "__main__":
    main()
