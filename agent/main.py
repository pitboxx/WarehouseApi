#!/usr/bin/env python3
"""
Warehouse API Agent CLI.
Usage:
  python main.py "JSON command"                     # direct tool call via JSON
  python main.py --llm "natural language command"   # LLM agent (requires LM Studio)

Example:
  python main.py '{"tool": "get_users", "args": {}}'
  python main.py --llm "create a user named Alex"
"""

import sys
import json
from typing import Dict, Any

from api_client import client
from tools import ALL_TOOLS


def get_tool_by_name(name: str):
    """Return tool instance by name."""
    tool_map = {tool.name: tool for tool in ALL_TOOLS}
    return tool_map.get(name)


def run_tool(tool_name: str, args: Dict[str, Any]) -> str:
    """Invoke the tool with given arguments."""
    tool = get_tool_by_name(tool_name)
    if not tool:
        return json.dumps({
            "Status": "error",
            "Action": tool_name,
            "Errors": f"Tool '{tool_name}' not found"
        }, ensure_ascii=False, indent=2)
    
    try:
        # Convert args to match tool's signature
        # The tool expects positional arguments, but we have a dict.
        # We'll need to call the underlying function directly.
        # For simplicity, we'll use the tool's func attribute.
        if hasattr(tool, 'func'):
            result = tool.func(**args)
        else:
            result = tool.run(args)
        return result
    except Exception as e:
        return json.dumps({
            "Status": "error",
            "Action": tool_name,
            "Errors": str(e)
        }, ensure_ascii=False, indent=2)


def run_llm_agent(command: str) -> str:
    """
    Run command through LLM agent.
    """
    try:
        from langchain_core.messages import HumanMessage
        from llm_agent import create_warehouse_agent
        agent = create_warehouse_agent()
        result = agent.invoke(
            {"messages": [HumanMessage(content=command)]}
        )
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            output = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        else:
            output = str(result)
        return output
    except ImportError as e:
        return json.dumps({
            "Status": "error",
            "Action": "llm_agent",
            "Errors": f"Failed to import LLM agent: {e}. Make sure langchain-openai is installed."
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "Status": "error",
            "Action": "llm_agent",
            "Errors": f"LLM agent error: {e}"
        }, ensure_ascii=False, indent=2)


def main():
    use_llm = False
    command = None
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # Check for --llm flag
    if sys.argv[1] == "--llm":
        if len(sys.argv) < 3:
            print("Error: --llm flag requires a command")
            print(__doc__)
            sys.exit(1)
        use_llm = True
        command = sys.argv[2]
    else:
        command = sys.argv[1]
    
    if use_llm:
        result = run_llm_agent(command)
        print(result)
    else:
        # Treat command as JSON
        try:
            parsed = json.loads(command)
        except json.JSONDecodeError:
            print(json.dumps({
                "Status": "error",
                "Action": "parse",
                "Errors": f"Could not parse command as JSON: {command}. Use --llm for natural language."
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        if not isinstance(parsed, dict) or "tool" not in parsed:
            print(json.dumps({
                "Status": "error",
                "Action": "parse",
                "Errors": "JSON must be an object with 'tool' field (and optional 'args')."
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        tool_name = parsed["tool"]
        args = parsed.get("args", {})
        
        result = run_tool(tool_name, args)
        print(result)


if __name__ == "__main__":
    main()