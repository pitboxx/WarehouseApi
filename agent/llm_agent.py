#!/usr/bin/env python3
"""
LLM Agent for Warehouse API using Qwen via LM Studio.
Uses LangChain tools and OpenAI-compatible API.
"""

import sys
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from tools import ALL_TOOLS


def create_warehouse_agent(llm_base_url: str = "http://localhost:1234/v1",
                          model: str = "qwen/qwen3.6-35b-a3b",
                          temperature: float = 0.0):
    """
    Create LangChain agent with tools using create_agent (langchain >= 1.3).
    Returns a CompiledStateGraph.
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
    system_prompt = """You are a Warehouse API operator. You can only manage users, departments, and products via the provided tools. You cannot perform any other actions. Always respond with the tool output exactly as returned — do not rephrase or summarize.

CRITICAL RULES:
1. You MUST call a tool for every user request. Never answer without calling a tool.
2. When you receive the tool output, you MUST return it EXACTLY as-is, without any changes, formatting, translation, or summarization.
3. Do NOT add any introductory text, explanations, bullet points, or markdown formatting.
4. Do NOT translate field names or values.
5. The tool output is already properly formatted JSON. Just output it directly.
6. If the user asks something outside users/departments/products, say: "I can only manage users, departments, and products." and do not attempt anything else."""
    
    # Create agent using the new create_agent API (langchain >= 1.3)
    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=system_prompt,
    )
    
    return agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python llm_agent.py \"your natural language command\"")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        agent = create_warehouse_agent()
        # Invoke the agent with a human message
        result = agent.invoke(
            {"messages": [HumanMessage(content=command)]}
        )
        # Extract the last AI message content
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            output = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        else:
            output = str(result)
        print(output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()