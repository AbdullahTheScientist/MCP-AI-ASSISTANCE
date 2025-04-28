import asyncio
import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient  # Assuming your custom modules

# Initialize Flask app
app = Flask(__name__)

# Global variables
agent = None
client = None

# Setup on app start
def initialize_agent():
    global agent, client
    load_dotenv()
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

    config_file = "browser_mcp.json"
    with open(config_file, "r") as f:
        config_data = json.load(f)

    llm = ChatGroq(model="qwen-qwq-32b")
    client = MCPClient(config_data)
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

# Async route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    if user_input.lower() in ['exit', 'quit']:
        return jsonify({'message': 'Conversation ended.'})

    if user_input.lower() == 'clear':
        agent.clear_conversation_history()
        return jsonify({'message': 'Conversation history cleared.'})

    try:
        # Run the async agent.run inside the event loop
        response = asyncio.run(agent.run(user_input))
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Cleanup when shutting down
@app.teardown_appcontext
def shutdown_session(exception=None):
    if client and client.sessions:
        asyncio.run(client.close_all_sessions())

# Main entry
if __name__ == '__main__':
    initialize_agent()
    app.run(host='0.0.0.0', port=5000, debug=True)
