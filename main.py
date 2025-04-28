import asyncio
import os
from dotenv import load_dotenv  # Corrected: 'load_env' → 'load_dotenv'
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient  # Assuming this is a custom module

import json
async def run_memory_chat():
    load_dotenv()  # Corrected: 'load_env()' → 'load_dotenv()'
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"

    print("initializing chat ...")
    llm = ChatGroq(model="qwen-qwq-32b")


    with open("browser_mcp.json", "r") as f:
        config_data = json.load(f)

    client = MCPClient(config_data)  # If it expects a dict or settings object
    # <-- Check if this is the right method


    # client = MCPClient(config_file=config_file)  # You were using `client` without initializing it
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ['exit', 'quit']:  # Corrected: 'quite' → 'quit'
                print("ending conversation")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("conversation history cleared")
                continue

            print("\nAssistance", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()

# Corrected this line:
if __name__ == "__main__":  # '==' not '='
    asyncio.run(run_memory_chat())  # Add '()' to call the coroutine
