from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Output parser using Pydantic
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Prompt template with format instructions
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools.
            Wrap the output in this format and provide no other text:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools used
tools = [search_tool]

# Agent setup 
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Invoke agent
query = input("what can I help you research? ")
raw_response = agent_executor.invoke({"query": query})

# Extract and clean JSON string from markdown block
output_text = raw_response.get("output", "")

if output_text.startswith("```json"):
    output_text = output_text.removeprefix("```json").removesuffix("```").strip()

# Parse the cleaned output

try:
    structured_response = parser.parse(output_text)
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw response - ", raw_response)


