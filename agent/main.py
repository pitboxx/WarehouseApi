#!/usr/bin/env python3
"""
Warehouse API Agent CLI.
Usage:
  python main.py "natural language command"           # rule-based parser
  python main.py --llm "natural language command"     # LLM agent (requires LM Studio)

Example:
  python main.py "создай пользователя с именем Alex"
  python main.py --llm "create a user named Alex"
"""

import sys
import re
import json
from typing import Dict, Any, Optional

from api_client import client
from tools import ALL_TOOLS, create_user, get_users, update_user, delete_user, \
                  create_department, get_departments, update_department, delete_department, \
                  create_product, get_products, update_product, delete_product


def parse_command(command: str) -> Optional[Dict[str, Any]]:
    """
    Simple rule-based parser for natural language commands.
    Returns dict with tool name and arguments.
    """
    command_lower = command.lower()
    
    # User commands
    if re.search(r'создай пользователя|create user', command_lower):
        # Extract name
        name_match = re.search(r'с именем (\w+)', command_lower)
        first_name = name_match.group(1) if name_match else "Alex"
        last_name = "Doe"  # default
        email = f"{first_name.lower()}@example.com"
        phone = "+1234567890"
        return {
            "tool": "create_user",
            "args": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "role": "Employee",
                "department_id": 1
            }
        }
    
    elif re.search(r'покажи пользователей|show users|get users', command_lower):
        return {"tool": "get_users", "args": {}}
    
    elif re.search(r'удали пользователя|delete user', command_lower):
        id_match = re.search(r'id (\d+)', command_lower)
        if id_match:
            user_id = int(id_match.group(1))
            return {"tool": "delete_user", "args": {"user_id": user_id}}
        else:
            print("Error: Please specify user ID")
            return None
    
    elif re.search(r'свяжи пользователя|link user', command_lower):
        # Extract user name and department name
        user_match = re.search(r'пользователя (\w+)', command_lower)
        dept_match = re.search(r'подразделением (\w+)', command_lower)
        if not user_match or not dept_match:
            print("Error: Please specify user name and department name")
            return None
        user_name = user_match.group(1)
        dept_name = dept_match.group(1)
        
        # Find user ID by first name (case-insensitive)
        users = client.get_users()
        user = next((u for u in users if u['firstName'].lower() == user_name.lower()), None)
        if not user:
            print(f"Error: User '{user_name}' not found")
            return None
        
        # Find department ID by name
        departments = client.get_departments()
        dept = next((d for d in departments if d['name'].lower() == dept_name.lower()), None)
        if not dept:
            print(f"Error: Department '{dept_name}' not found")
            return None
        
        return {
            "tool": "update_user",
            "args": {
                "user_id": user['id'],
                "department_id": dept['id']
            }
        }
    
    # Department commands
    elif re.search(r'создай отдел|create department', command_lower):
        name_match = re.search(r'название (\w+)', command_lower)
        name = name_match.group(1) if name_match else "New Department"
        desc = "Description"
        location = "Location"
        return {
            "tool": "create_department",
            "args": {
                "name": name,
                "description": desc,
                "location": location
            }
        }
    
    elif re.search(r'покажи отделы|show departments|get departments', command_lower):
        return {"tool": "get_departments", "args": {}}
    
    elif re.search(r'добавь товар|add product', command_lower):
        # Extract product name and department name
        product_match = re.search(r'товар (\w+)', command_lower)
        dept_match = re.search(r'подразделение (\w+)', command_lower)
        if not product_match or not dept_match:
            print("Error: Please specify product name and department name")
            return None
        product_name = product_match.group(1)
        dept_name = dept_match.group(1)
        
        # Find department ID by name
        departments = client.get_departments()
        dept = next((d for d in departments if d['name'].lower() == dept_name.lower()), None)
        if not dept:
            print(f"Error: Department '{dept_name}' not found")
            return None
        
        # Default values for other fields
        description = f"Product {product_name}"
        price = 10.0
        quantity = 1
        sku = f"SKU-{product_name.upper()}"
        
        return {
            "tool": "create_product",
            "args": {
                "name": product_name,
                "description": description,
                "price": price,
                "quantity": quantity,
                "sku": sku,
                "department_id": dept['id']
            }
        }
    
    # Product commands
    elif re.search(r'создай продукт|create product', command_lower):
        name_match = re.search(r'название (\w+)', command_lower)
        name = name_match.group(1) if name_match else "New Product"
        price = 10.0
        quantity = 100
        sku = "SKU123"
        dept_id = 1
        return {
            "tool": "create_product",
            "args": {
                "name": name,
                "description": "Description",
                "price": price,
                "quantity": quantity,
                "sku": sku,
                "department_id": dept_id
            }
        }
    
    elif re.search(r'покажи продукты|show products|get products', command_lower):
        return {"tool": "get_products", "args": {}}
    
    elif re.search(r'удали товар|delete product', command_lower):
        # Extract product name
        product_match = re.search(r'товар (\w+)', command_lower)
        if not product_match:
            print("Error: Please specify product name")
            return None
        product_name = product_match.group(1)
        
        # Find product by name
        products = client.get_products()
        product = next((p for p in products if p['name'].lower() == product_name.lower()), None)
        if not product:
            print(f"Error: Product '{product_name}' not found")
            return None
        
        return {
            "tool": "delete_product",
            "args": {
                "product_id": product['id']
            }
        }
    
    # If no match, return None
    return None


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
        from llm_agent import create_warehouse_agent
        agent = create_warehouse_agent()
        result = agent.invoke({"input": command})
        output = result.get("output", str(result))
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
        parsed = parse_command(command)
        
        if parsed is None:
            # Fallback: treat command as JSON
            try:
                parsed = json.loads(command)
            except json.JSONDecodeError:
                print(json.dumps({
                    "Status": "error",
                    "Action": "parse",
                    "Errors": f"Could not parse command: {command}"
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
        
        tool_name = parsed["tool"]
        args = parsed.get("args", {})
        
        result = run_tool(tool_name, args)
        print(result)


if __name__ == "__main__":
    main()