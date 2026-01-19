import datetime
import getpass
import os
from typing import Annotated
from typing_extensions import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import HumanMessage, ToolMessage, BaseMessage, AIMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

load_dotenv()
# --- Setup Environment ---
def _set_if_undefined(var: str) -> None:
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please enter {var}: ")

_set_if_undefined("GOOGLE_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

# --- Define LLM and Tools ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)

# --- Define Schemas ---
class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries."""
    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique."
    )

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer. Provide an answer, reflection, citations, and search queries."""
    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )

# --- Actor Logic with Retries ---
class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    def respond(self, state: dict):
        messages = state["messages"]
        for attempt in range(3):
            response = self.runnable.invoke({"messages": messages})
            try:
                # Gemini tool calling validation
                self.validator.invoke(response)
                return {"messages": [response]}
            except Exception as e:
                # Add error feedback to the message history for the next retry
                feedback = ToolMessage(
                    content=f"Validation Error: {repr(e)}. Please fix the tool call arguments.",
                    tool_call_id=response.tool_calls[0]["id"] if response.tool_calls else "none"
                )
                messages = messages + [response, feedback]
        return {"messages": [response]}

# --- Prompts and Chains ---
actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert researcher. Current time: {time}\n"
               "1. {first_instruction}\n"
               "2. Reflect and critique your answer. Be severe to maximize improvement.\n"
               "3. Recommend search queries to research information and improve your answer."),
    MessagesPlaceholder(variable_name="messages"),
    ("user", "\n\n<system>Reflect on the user's original question and the actions taken thus far. "
             "Respond using the {function_name} function.</system>"),
]).partial(time=lambda: datetime.datetime.now().isoformat())

initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
) | llm.bind_tools(tools=[AnswerQuestion])

revision_instructions = """Revise your previous answer using the new information.
- Use previous critique to add important info.
- MUST include numerical citations [1], [2], etc.
- Add a 'References' section at the bottom.
- Ensure the answer (excluding references) is under 250 words."""

revision_chain = actor_prompt_template.partial(
    first_instruction=revision_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])

# --- Nodes ---
first_responder = ResponderWithRetries(runnable=initial_answer_chain, validator=PydanticToolsParser(tools=[AnswerQuestion]))
revisor = ResponderWithRetries(runnable=revision_chain, validator=PydanticToolsParser(tools=[ReviseAnswer]))

def run_queries(search_queries: list[str], **kwargs):
    """Execute search queries using Tavily search tool."""
    return tavily_tool.batch([{"query": query} for query in search_queries])

tool_node = ToolNode([
    StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
    StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
])

# --- Graph Construction ---
class State(TypedDict):
    messages: Annotated[list, add_messages]

def event_loop(state: State):
    # Logic to stop after specific number of AI/Tool loops
    count = sum(1 for m in state["messages"] if isinstance(m, AIMessage) and m.tool_calls)
    if count > 3: # MAX_ITERATIONS
        return END
    return "execute_tools"

builder = StateGraph(State)
builder.add_node("draft", first_responder.respond)
builder.add_node("execute_tools", tool_node)
builder.add_node("revise", revisor.respond)

builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])

graph = builder.compile()

# --- Execution ---
if __name__ == "__main__":
    inputs = {"messages": [HumanMessage(content="How should we handle the climate crisis?")]}
    for event in graph.stream(inputs, stream_mode="values"):
        if "messages" in event:
            event["messages"][-1].pretty_print()