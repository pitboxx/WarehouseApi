using WarehouseApi.Models;

namespace WarehouseApi.Services;

public interface IWarehouseService
{
    // Department operations
    Task<List<Department>> GetDepartmentsAsync();
    Task<Department?> GetDepartmentAsync(int id);
    Task<Department> CreateDepartmentAsync(Department department);
    Task<bool> UpdateDepartmentAsync(Department department);
    Task<bool> DeleteDepartmentAsync(int id);
    
    // Product operations
    Task<List<Product>> GetProductsAsync();
    Task<Product?> GetProductAsync(int id);
    Task<Product> CreateProductAsync(Product product);
    Task<bool> UpdateProductAsync(Product product);
    Task<bool> DeleteProductAsync(int id);
    
    // User operations
    Task<List<User>> GetUsersAsync();
    Task<User?> GetUserAsync(int id);
    Task<User> CreateUserAsync(User user);
    Task<bool> UpdateUserAsync(User user);
    Task<bool> DeleteUserAsync(int id);
}