from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

# Initialize the Language Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

# --- Prompt 1: Extract Information ---
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# --- Prompt 2: Transform to JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with "
    "'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# Converts LLM output to a plain string
extraction_chain = prompt_extract | llm | StrOutputParser()

# Full chain: extraction → transformation
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

input_text = (
    "The new laptop model features a 3.5 GHz octa-core processor, "
    "16GB of RAM, and a 1TB NVMe SSD."
)

final_result = full_chain.invoke({"text_input": input_text})

print(final_result)
