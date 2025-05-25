import asyncio
import base64
import json
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

load_dotenv()

# Initialize the OpenAI chat model
model = ChatOpenAI(model="gpt-4.1")
opensearch_server = "http://127.0.0.1:9200"

async def main():
    # Create MCP client with OpenSearch connection details
    client = MultiServerMCPClient({
        "opensearch": { 
            "url": f"{opensearch_server}/_plugins/_ml/mcp/sse?append_to_base_url=true",
            "transport": "sse",
            "headers": {
                "Content-Type": "application/json",
                "Accept-Encoding": "identity",
            }
        }
    })

    tools = await client.get_tools()

    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs={
            "system_message": "You are a helpful assistant that can interact with OpenSearch to retrieve and process data.",
            "max_iterations": 5,
            "max_execution_time": 60,
        },
        handle_parsing_errors=True,
        verbose=True,
    )

    while True:
        user_input = input("Input (type 'exit' to quit): ")
        if user_input.strip().lower() == "exit":
            break
        result = await agent.ainvoke({"input": user_input})
        print("Result:", result['output'])

if __name__ == "__main__":
    asyncio.run(main())
