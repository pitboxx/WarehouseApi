import json
import requests
from typing import Optional, Dict, Any, List


class WarehouseApiClient:
    """Client for Warehouse API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request and return JSON response."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            # Some endpoints return 204 No Content
            if response.status_code == 204:
                return {}
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg = f"{error_msg}: {error_detail}"
                except:
                    error_msg = f"{error_msg} (status {e.response.status_code})"
            raise Exception(f"API request failed: {error_msg}")
    
    # User endpoints
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        return self._request('GET', '/api/users')
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID."""
        return self._request('GET', f'/api/users/{user_id}')
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        return self._request('POST', '/api/users', json=user_data)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> None:
        """Update an existing user."""
        self._request('PUT', f'/api/users/{user_id}', json=user_data)
    
    def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        self._request('DELETE', f'/api/users/{user_id}')
    
    # Department endpoints
    def get_departments(self) -> List[Dict[str, Any]]:
        """Get all departments."""
        return self._request('GET', '/api/departments')
    
    def get_department(self, department_id: int) -> Dict[str, Any]:
        """Get department by ID."""
        return self._request('GET', f'/api/departments/{department_id}')
    
    def create_department(self, department_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new department."""
        return self._request('POST', '/api/departments', json=department_data)
    
    def update_department(self, department_id: int, department_data: Dict[str, Any]) -> None:
        """Update an existing department."""
        self._request('PUT', f'/api/departments/{department_id}', json=department_data)
    
    def delete_department(self, department_id: int) -> None:
        """Delete a department."""
        self._request('DELETE', f'/api/departments/{department_id}')
    
    # Product endpoints
    def get_products(self) -> List[Dict[str, Any]]:
        """Get all products."""
        return self._request('GET', '/api/products')
    
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """Get product by ID."""
        return self._request('GET', f'/api/products/{product_id}')
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product."""
        return self._request('POST', '/api/products', json=product_data)
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> None:
        """Update an existing product."""
        self._request('PUT', f'/api/products/{product_id}', json=product_data)
    
    def delete_product(self, product_id: int) -> None:
        """Delete a product."""
        self._request('DELETE', f'/api/products/{product_id}')


# Singleton client instance
client = WarehouseApiClient()