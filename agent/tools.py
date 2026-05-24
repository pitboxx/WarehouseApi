import json
from typing import Optional, Dict, Any
from langchain_core.tools.structured import StructuredTool
from langchain_core.tools import ToolException

from api_client import client


def format_result(status: str, action: str, data: Any = None, errors: Optional[str] = None) -> str:
    """Format result according to contract."""
    result = {
        "Status": status,
        "Action": action,
        "Data": data,
        "Errors": errors
    }
    # Remove None values
    result = {k: v for k, v in result.items() if v is not None}
    return json.dumps(result, ensure_ascii=False, indent=2)


def handle_api_error(e: Exception, action: str) -> str:
    """Convert exception to error result."""
    error_msg = str(e)
    return format_result("error", action, errors=error_msg)


# User tools
def get_users_tool() -> str:
    """Get all users."""
    action = "get_users"
    try:
        users = client.get_users()
        return format_result("success", action, data=users)
    except Exception as e:
        return handle_api_error(e, action)


def get_user_tool(user_id: int) -> str:
    """Get user by ID."""
    action = f"get_user (id={user_id})"
    try:
        user = client.get_user(user_id)
        return format_result("success", action, data=user)
    except Exception as e:
        return handle_api_error(e, action)


def create_user_tool(first_name: str, last_name: str, email: str, phone: str, 
                     role: str = "Employee", department_id: int = 1) -> str:
    """Create a new user."""
    action = "create_user"
    user_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone,
        "role": role,
        "departmentId": department_id
    }
    try:
        created = client.create_user(user_data)
        return format_result("success", action, data=created)
    except Exception as e:
        return handle_api_error(e, action)


def update_user_tool(user_id: int, first_name: Optional[str] = None,
                     last_name: Optional[str] = None, email: Optional[str] = None,
                     phone: Optional[str] = None, role: Optional[str] = None,
                     department_id: Optional[int] = None) -> str:
    """Update an existing user."""
    action = f"update_user (id={user_id})"
    user_data = {}
    # Always include id to satisfy API validation
    user_data["id"] = user_id
    if first_name is not None:
        user_data["firstName"] = first_name
    if last_name is not None:
        user_data["lastName"] = last_name
    if email is not None:
        user_data["email"] = email
    if phone is not None:
        user_data["phone"] = phone
    if role is not None:
        user_data["role"] = role
    if department_id is not None:
        user_data["departmentId"] = department_id
    
    if not user_data:
        return format_result("error", action, errors="No fields to update provided")
    
    try:
        client.update_user(user_id, user_data)
        return format_result("success", action, data={"updated": True})
    except Exception as e:
        return handle_api_error(e, action)


def delete_user_tool(user_id: int) -> str:
    """Delete a user."""
    action = f"delete_user (id={user_id})"
    try:
        client.delete_user(user_id)
        return format_result("success", action, data={"deleted": True})
    except Exception as e:
        return handle_api_error(e, action)


# Department tools
def get_departments_tool() -> str:
    """Get all departments."""
    action = "get_departments"
    try:
        departments = client.get_departments()
        return format_result("success", action, data=departments)
    except Exception as e:
        return handle_api_error(e, action)


def get_department_tool(department_id: int) -> str:
    """Get department by ID."""
    action = f"get_department (id={department_id})"
    try:
        department = client.get_department(department_id)
        return format_result("success", action, data=department)
    except Exception as e:
        return handle_api_error(e, action)


def create_department_tool(name: str, description: str, location: str) -> str:
    """Create a new department."""
    action = "create_department"
    department_data = {
        "name": name,
        "description": description,
        "location": location
    }
    try:
        created = client.create_department(department_data)
        return format_result("success", action, data=created)
    except Exception as e:
        return handle_api_error(e, action)


def update_department_tool(department_id: int, name: Optional[str] = None,
                           description: Optional[str] = None, location: Optional[str] = None) -> str:
    """Update an existing department."""
    action = f"update_department (id={department_id})"
    department_data = {}
    # Always include id to satisfy API validation
    department_data["id"] = department_id
    if name is not None:
        department_data["name"] = name
    if description is not None:
        department_data["description"] = description
    if location is not None:
        department_data["location"] = location
    
    if not department_data:
        return format_result("error", action, errors="No fields to update provided")
    
    try:
        client.update_department(department_id, department_data)
        return format_result("success", action, data={"updated": True})
    except Exception as e:
        return handle_api_error(e, action)


def delete_department_tool(department_id: int) -> str:
    """Delete a department."""
    action = f"delete_department (id={department_id})"
    try:
        client.delete_department(department_id)
        return format_result("success", action, data={"deleted": True})
    except Exception as e:
        return handle_api_error(e, action)


# Product tools
def get_products_tool() -> str:
    """Get all products."""
    action = "get_products"
    try:
        products = client.get_products()
        return format_result("success", action, data=products)
    except Exception as e:
        return handle_api_error(e, action)


def get_product_tool(product_id: int) -> str:
    """Get product by ID."""
    action = f"get_product (id={product_id})"
    try:
        product = client.get_product(product_id)
        return format_result("success", action, data=product)
    except Exception as e:
        return handle_api_error(e, action)


def create_product_tool(name: str, description: str, price: float, quantity: int,
                        sku: str, department_id: int) -> str:
    """Create a new product."""
    action = "create_product"
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "sku": sku,
        "departmentId": department_id
    }
    try:
        created = client.create_product(product_data)
        return format_result("success", action, data=created)
    except Exception as e:
        return handle_api_error(e, action)


def update_product_tool(product_id: int, name: Optional[str] = None,
                        description: Optional[str] = None, price: Optional[float] = None,
                        quantity: Optional[int] = None, sku: Optional[str] = None,
                        department_id: Optional[int] = None) -> str:
    """Update an existing product."""
    action = f"update_product (id={product_id})"
    product_data = {}
    # Always include id to satisfy API validation
    product_data["id"] = product_id
    if name is not None:
        product_data["name"] = name
    if description is not None:
        product_data["description"] = description
    if price is not None:
        product_data["price"] = price
    if quantity is not None:
        product_data["quantity"] = quantity
    if sku is not None:
        product_data["sku"] = sku
    if department_id is not None:
        product_data["departmentId"] = department_id
    
    if not product_data:
        return format_result("error", action, errors="No fields to update provided")
    
    try:
        client.update_product(product_id, product_data)
        return format_result("success", action, data={"updated": True})
    except Exception as e:
        return handle_api_error(e, action)


def delete_product_tool(product_id: int) -> str:
    """Delete a product."""
    action = f"delete_product (id={product_id})"
    try:
        client.delete_product(product_id)
        return format_result("success", action, data={"deleted": True})
    except Exception as e:
        return handle_api_error(e, action)


# Create LangChain tools
get_users = StructuredTool.from_function(
    func=get_users_tool,
    name="get_users",
    description="Get all users. No arguments required."
)

get_user = StructuredTool.from_function(
    func=get_user_tool,
    name="get_user",
    description="Get user by ID. Provide user_id (integer)."
)

create_user = StructuredTool.from_function(
    func=create_user_tool,
    name="create_user",
    description="Create a new user. Provide first_name, last_name, email, phone, role (optional, default Employee), department_id (optional, default 1)."
)

update_user = StructuredTool.from_function(
    func=update_user_tool,
    name="update_user",
    description="Update an existing user. Provide user_id and optional fields: first_name, last_name, email, phone, role, department_id."
)

delete_user = StructuredTool.from_function(
    func=delete_user_tool,
    name="delete_user",
    description="Delete a user. Provide user_id (integer)."
)

get_departments = StructuredTool.from_function(
    func=get_departments_tool,
    name="get_departments",
    description="Get all departments. No arguments required."
)

get_department = StructuredTool.from_function(
    func=get_department_tool,
    name="get_department",
    description="Get department by ID. Provide department_id (integer)."
)

create_department = StructuredTool.from_function(
    func=create_department_tool,
    name="create_department",
    description="Create a new department. Provide name, description, location."
)

update_department = StructuredTool.from_function(
    func=update_department_tool,
    name="update_department",
    description="Update an existing department. Provide department_id and optional fields: name, description, location."
)

delete_department = StructuredTool.from_function(
    func=delete_department_tool,
    name="delete_department",
    description="Delete a department. Provide department_id (integer)."
)

get_products = StructuredTool.from_function(
    func=get_products_tool,
    name="get_products",
    description="Get all products. No arguments required."
)

get_product = StructuredTool.from_function(
    func=get_product_tool,
    name="get_product",
    description="Get product by ID. Provide product_id (integer)."
)

create_product = StructuredTool.from_function(
    func=create_product_tool,
    name="create_product",
    description="Create a new product. Provide name, description, price (float), quantity (int), sku (string), department_id (int)."
)

update_product = StructuredTool.from_function(
    func=update_product_tool,
    name="update_product",
    description="Update an existing product. Provide product_id and optional fields: name, description, price, quantity, sku, department_id."
)

delete_product = StructuredTool.from_function(
    func=delete_product_tool,
    name="delete_product",
    description="Delete a product. Provide product_id (integer)."
)


# List of all tools
ALL_TOOLS = [
    get_users, get_user, create_user, update_user, delete_user,
    get_departments, get_department, create_department, update_department, delete_department,
    get_products, get_product, create_product, update_product, delete_product
]