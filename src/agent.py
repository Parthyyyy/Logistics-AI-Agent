import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from duckduckgo_search import DDGS

from src.rag_tool import logistics_document_search

load_dotenv()

@tool
def live_web_search(query: str) -> str:
    """
    Use this tool to search the internet for live updates, current weather, port congestion, and global shipping news.
    Input should be a specific search query.
    """
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No internet results found."
        return "\n".join([f"- {res['body']}" for res in results])
    except Exception as e:
        return f"Web search failed: {str(e)}"

# Initializing LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Combining tools
tools = [logistics_document_search, live_web_search]

system_prompt = """You are an Advanced Enterprise Logistics AI Agent.
Your goal is to answer user queries regarding logistics, supply chains, and company policies.

You have access to two tools:
1. logistics_document_search: ALWAYS use this first to check for internal company policies, manuals, and proprietary data.
2. live_web_search: Use this to fetch real-time, external world information (e.g., current port delays, live weather, global news).

If you need both internal and external data, use both tools! 
Always synthesize the tool outputs into a clear, professional, and factual final answer. Do not guess information.
"""

logistics_agent = create_react_agent(llm, tools)

def run_agent(user_query: str):
    """Helper function to run the agent and extract the final response."""
    print(f"\n🤖 Agent is evaluating query: '{user_query}'...")
    
    inputs = {"messages":[
        ("system", system_prompt),
        ("user", user_query)
    ]}
    
    final_response = ""
    for chunk in logistics_agent.stream(inputs, stream_mode="values"):
        message = chunk["messages"][-1]
        
        # Print agent's internal thoughts/tool calls for debugging
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"   [Tool Decision] Agent decided to use: {message.tool_calls[0]['name']}...")
            
        final_response = message.content
        
    return final_response

# Testing the agent
if __name__ == "__main__":
    print("\n--- TEST 1: Internal Knowledge ---")
    print(run_agent("What are the standard guidelines mentioned in our logistics documents?"))
    
    print("\n--- TEST 2: Live Web Search ---")
    print(run_agent("What is the current news regarding water levels in the Panama Canal?"))