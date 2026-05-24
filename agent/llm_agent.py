#!/usr/bin/env python3
"""
LLM Agent for Warehouse API using Qwen via LM Studio.
Uses LangChain tools and OpenAI-compatible API.
"""

import sys
from langchain_openai import ChatOpenAI
from langchain.agents.factory import create_agent
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from tools import ALL_TOOLS


def create_warehouse_agent(llm_base_url: str = "http://localhost:1234/v1", 
                          model: str = "local", 
                          temperature: float = 0.0):
    """
    Create LangChain agent with tools using factory.create_agent.
    """
    # Initialize LLM with LM Studio endpoint
    llm = ChatOpenAI(
        base_url=llm_base_url,
        model=model,
        temperature=temperature,
        api_key="lm-studio",  # dummy key, LM Studio doesn't require auth
        max_tokens=None,
        timeout=30,
    )
    
    # System prompt
    system_prompt = """You are a helpful assistant that can interact with a Warehouse API.
    You have access to tools for managing users, departments, and products.
    Always use the tools to perform actions. When the user asks you to do something, 
    call the appropriate tool and return the result in the same format as the tool outputs.
    The tool outputs are already formatted as JSON with Status, Action, Data, Errors.
    You should just present the tool's output to the user.
    If you need to ask for clarification, do so.
    """
    
    # Create agent using factory.create_agent
    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=system_prompt,
        debug=True,
    )
    
    return agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python llm_agent.py \"your natural language command\"")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        agent = create_warehouse_agent()
        # Invoke the agent
        result = agent.invoke({"input": command}, RunnableConfig())
        # The result is a dict with 'output' key
        output = result.get("output", str(result))
        print(output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()