using WarehouseApi.Data;
using WarehouseApi.Models;

namespace WarehouseApi.Services;

public class WarehouseService : IWarehouseService
{
    private readonly JsonFileStorage _storage;

    public WarehouseService(JsonFileStorage storage)
    {
        _storage = storage;
    }

    #region Department Operations
    public Task<List<Department>> GetDepartmentsAsync()
    {
        var departments = _storage.GetDepartments();
        return Task.FromResult(departments);
    }

    public Task<Department?> GetDepartmentAsync(int id)
    {
        var department = _storage.GetDepartment(id);
        return Task.FromResult(department);
    }

    public Task<Department> CreateDepartmentAsync(Department department)
    {
        var created = _storage.AddDepartment(department);
        return Task.FromResult(created);
    }

    public Task<bool> UpdateDepartmentAsync(Department department)
    {
        var result = _storage.UpdateDepartment(department);
        return Task.FromResult(result);
    }

    public Task<bool> DeleteDepartmentAsync(int id)
    {
        var result = _storage.DeleteDepartment(id);
        return Task.FromResult(result);
    }
    #endregion

    #region Product Operations
    public Task<List<Product>> GetProductsAsync()
    {
        var products = _storage.GetProducts();
        return Task.FromResult(products);
    }

    public Task<Product?> GetProductAsync(int id)
    {
        var product = _storage.GetProduct(id);
        return Task.FromResult(product);
    }

    public Task<Product> CreateProductAsync(Product product)
    {
        // Validate department exists
        var department = _storage.GetDepartment(product.DepartmentId);
        if (department == null)
        {
            throw new ArgumentException($"Department with ID {product.DepartmentId} does not exist");
        }

        var created = _storage.AddProduct(product);
        return Task.FromResult(created);
    }

    public Task<bool> UpdateProductAsync(Product product)
    {
        // Validate department exists if changing department
        if (product.DepartmentId > 0)
        {
            var department = _storage.GetDepartment(product.DepartmentId);
            if (department == null)
            {
                throw new ArgumentException($"Department with ID {product.DepartmentId} does not exist");
            }
        }

        var result = _storage.UpdateProduct(product);
        return Task.FromResult(result);
    }

    public Task<bool> DeleteProductAsync(int id)
    {
        var result = _storage.DeleteProduct(id);
        return Task.FromResult(result);
    }
    #endregion

    #region User Operations
    public Task<List<User>> GetUsersAsync()
    {
        var users = _storage.GetUsers();
        return Task.FromResult(users);
    }

    public Task<User?> GetUserAsync(int id)
    {
        var user = _storage.GetUser(id);
        return Task.FromResult(user);
    }

    public Task<User> CreateUserAsync(User user)
    {
        // Validate department exists
        var department = _storage.GetDepartment(user.DepartmentId);
        if (department == null)
        {
            throw new ArgumentException($"Department with ID {user.DepartmentId} does not exist");
        }

        var created = _storage.AddUser(user);
        return Task.FromResult(created);
    }

    public Task<bool> UpdateUserAsync(User user)
    {
        // Validate department exists if changing department
        if (user.DepartmentId > 0)
        {
            var department = _storage.GetDepartment(user.DepartmentId);
            if (department == null)
            {
                throw new ArgumentException($"Department with ID {user.DepartmentId} does not exist");
            }
        }

        var result = _storage.UpdateUser(user);
        return Task.FromResult(result);
    }

    public Task<bool> DeleteUserAsync(int id)
    {
        var result = _storage.DeleteUser(id);
        return Task.FromResult(result);
    }
    #endregion
}