# backend/app/services/rag_agent.py
import json
from langchain_openai import ChatOpenAI
from langchain.agents import tool, AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers.pydantic import PydanticOutputParser

from ..db.connections import get_sql_database, get_mongo_collection
from ..models.pydantic_models import ApiResponse, TextData, TableData, ChartData
from ..core.config import settings

# --- 1. INITIALIZE THE LLM ---
# We use a powerful model like gpt-4o for better reasoning and tool use.
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.OPENAI_API_KEY)

# --- 2. DEFINE THE TOOLS ---
# The agent will have access to these tools to answer questions.

@tool
def query_client_profiles(query: str) -> str:
    """
    Use this tool to get information about clients from the MongoDB database.
    The query should be a concise question about client profiles, like 'clients with high risk appetite' or 'client ID for Aarav Sharma'.
    This tool translates your question into a MongoDB query and returns the client data as a JSON string.
    """
    # This is a simplified NL-to-MongoDB implementation. For a production system,
    # you might have another LLM chain here to generate complex aggregation pipelines.
    mongo_collection = get_mongo_collection()
    if mongo_collection is None:
        return "MongoDB connection not available."

    # Example of simple query mapping
    query_lower = query.lower()
    mongo_query = {}
    if "risk" in query_lower:
        if "high" in query_lower: mongo_query["risk_appetite"] = "High"
        elif "medium" in query_lower: mongo_query["risk_appetite"] = "Medium"
        elif "low" in query_lower: mongo_query["risk_appetite"] = "Low"

    if "crypto" in query_lower:
        mongo_query["investment_preferences"] = "Crypto"

    if not mongo_query:
        return "Could not determine a valid MongoDB query from your question."

    try:
        results = list(mongo_collection.find(mongo_query, {'_id': 0}))
        return json.dumps(results)
    except Exception as e:
        return f"Error querying MongoDB: {str(e)}"

@tool
def query_investment_transactions(sql_query: str) -> str:
    """
    Use this tool to query the MySQL database for investment and transaction data.
    The input MUST be a valid SQL query.
    Use this to find out about stock names, investment amounts, dates, and categories.
    You can also use it to aggregate data, for example, to calculate total portfolio values or investment breakups.
    """
    db = get_sql_database()
    if db is None:
        return "MySQL connection not available."
    try:
        return db.run(sql_query)
    except Exception as e:
        return f"Error executing SQL query: {str(e)}"


# --- 3. CREATE THE AGENT ---
# This agent uses the "ReAct" framework with OpenAI tools to decide which tool to use.
tools = [query_client_profiles, query_investment_transactions]

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a powerful financial data assistant for 'Valuefy'.
    Your goal is to answer user questions by querying the available databases.
    You have two tools at your disposal:
    1. `query_client_profiles`: To get data about clients (like risk appetite, preferences, IDs) from MongoDB.
    2. `query_investment_transactions`: To get data about financial transactions (investments, stocks, amounts) by executing a SQL query on MySQL.

    **Reasoning Process:**
    1.  **Analyze the question:** Understand what information is needed.
    2.  **Check for dependencies:** If a question requires client details to query transactions (e.g., 'What are the investments of high-risk clients?'), you MUST first use `query_client_profiles` to get their `client_id`s.
    3.  **Construct tool inputs:** Based on the question, formulate the correct input for the chosen tool. For the SQL tool, this means writing a valid SQL query.
    4.  **Execute and Observe:** Run the tool and analyze the result.
    5.  **Repeat if necessary:** If the first result is not the final answer (e.g., you just got client IDs), use another tool with the new information.
    6.  **Final Answer:** Once you have all the necessary data, provide it as your final answer. The data will then be formatted by another system.
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # Where the agent's thoughts and tool outputs go
])

agent = create_openai_tools_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True lets you see the agent's thoughts

# --- 4. CREATE THE SYNTHESIZER (FINAL OUTPUT FORMATTER) ---
# This chain takes the raw output from the agent and formats it into the desired Pydantic model.

# Use a PydanticOutputParser to guarantee the final JSON structure
output_parser = PydanticOutputParser(pydantic_object=ApiResponse)

base_synthesizer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a response formatting specialist.
    Your task is to take a user's question and the final data retrieved by an agent, and format it into a structured JSON response.
    The response format must adhere to the provided JSON schema.

    - For data that looks like a list of records, use the 'table' format.
    - For questions asking for a "breakup", "distribution", or "by sector/category", use the 'pie' or 'bar' chart format.
    - For simple factual answers, use the 'text' format.
    - For time-series data, use the 'line' chart format.

    {format_instructions}
    """),
    ("human", "Original Question: {question}\n\nFinal Data from Agent: {data}")
])

# Then apply partial_variables here
synthesizer_prompt = base_synthesizer_prompt.partial(
    format_instructions=output_parser.get_format_instructions()
)


synthesizer_chain = synthesizer_prompt | llm | output_parser

# --- 5. THE MAIN SERVICE FUNCTION ---

from fastapi.responses import JSONResponse

async def process_query(query: str) -> ApiResponse:
    print(">>> [DEBUG] Received query:", query)

    try:
        agent_result = await agent_executor.ainvoke({"input": query})
        print(">>> [DEBUG] Raw agent result:", agent_result)

        raw_data = agent_result["output"]

        final_response = await synthesizer_chain.ainvoke({
            "question": query,
            "data": raw_data
        })

        print(">>> [DEBUG] Final structured response:", final_response)
        return final_response

    except Exception as e:
        print(">>> [ERROR] Exception in process_query:", str(e))
        raise
