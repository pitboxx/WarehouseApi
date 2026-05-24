using System.Text.Json;
using WarehouseApi.Models;

namespace WarehouseApi.Data;

public class JsonFileStorage
{
    private readonly string _dataDirectory;
    private readonly object _departmentLock = new object();
    private readonly object _productLock = new object();
    private readonly object _userLock = new object();

    public JsonFileStorage()
    {
        _dataDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Data", "JsonStorage");
        if (!Directory.Exists(_dataDirectory))
        {
            Directory.CreateDirectory(_dataDirectory);
        }
    }

    #region Department Operations
    public List<Department> GetDepartments()
    {
        lock (_departmentLock)
        {
            return ReadFromFile<List<Department>>("departments.json") ?? new List<Department>();
        }
    }

    public void SaveDepartments(List<Department> departments)
    {
        lock (_departmentLock)
        {
            WriteToFile("departments.json", departments);
        }
    }

    public Department? GetDepartment(int id)
    {
        var departments = GetDepartments();
        return departments.FirstOrDefault(d => d.Id == id);
    }

    public Department AddDepartment(Department department)
    {
        var departments = GetDepartments();
        department.Id = departments.Count > 0 ? departments.Max(d => d.Id) + 1 : 1;
        department.CreatedAt = DateTime.UtcNow;
        department.UpdatedAt = DateTime.UtcNow;
        departments.Add(department);
        SaveDepartments(departments);
        return department;
    }

    public bool UpdateDepartment(Department department)
    {
        var departments = GetDepartments();
        var existing = departments.FirstOrDefault(d => d.Id == department.Id);
        if (existing == null) return false;

        existing.Name = department.Name;
        existing.Description = department.Description;
        existing.Location = department.Location;
        existing.UpdatedAt = DateTime.UtcNow;
        
        SaveDepartments(departments);
        return true;
    }

    public bool DeleteDepartment(int id)
    {
        var departments = GetDepartments();
        var department = departments.FirstOrDefault(d => d.Id == id);
        if (department == null) return false;

        departments.Remove(department);
        SaveDepartments(departments);
        return true;
    }
    #endregion

    #region Product Operations
    public List<Product> GetProducts()
    {
        lock (_productLock)
        {
            return ReadFromFile<List<Product>>("products.json") ?? new List<Product>();
        }
    }

    public void SaveProducts(List<Product> products)
    {
        lock (_productLock)
        {
            WriteToFile("products.json", products);
        }
    }

    public Product? GetProduct(int id)
    {
        var products = GetProducts();
        return products.FirstOrDefault(p => p.Id == id);
    }

    public Product AddProduct(Product product)
    {
        var products = GetProducts();
        product.Id = products.Count > 0 ? products.Max(p => p.Id) + 1 : 1;
        product.CreatedAt = DateTime.UtcNow;
        product.UpdatedAt = DateTime.UtcNow;
        products.Add(product);
        SaveProducts(products);
        return product;
    }

    public bool UpdateProduct(Product product)
    {
        var products = GetProducts();
        var existing = products.FirstOrDefault(p => p.Id == product.Id);
        if (existing == null) return false;

        existing.Name = product.Name;
        existing.Description = product.Description;
        existing.Price = product.Price;
        existing.Quantity = product.Quantity;
        existing.Sku = product.Sku;
        existing.DepartmentId = product.DepartmentId;
        existing.UpdatedAt = DateTime.UtcNow;
        
        SaveProducts(products);
        return true;
    }

    public bool DeleteProduct(int id)
    {
        var products = GetProducts();
        var product = products.FirstOrDefault(p => p.Id == id);
        if (product == null) return false;

        products.Remove(product);
        SaveProducts(products);
        return true;
    }
    #endregion

    #region User Operations
    public List<User> GetUsers()
    {
        lock (_userLock)
        {
            return ReadFromFile<List<User>>("users.json") ?? new List<User>();
        }
    }

    public void SaveUsers(List<User> users)
    {
        lock (_userLock)
        {
            WriteToFile("users.json", users);
        }
    }

    public User? GetUser(int id)
    {
        var users = GetUsers();
        return users.FirstOrDefault(u => u.Id == id);
    }

    public User AddUser(User user)
    {
        var users = GetUsers();
        user.Id = users.Count > 0 ? users.Max(u => u.Id) + 1 : 1;
        user.CreatedAt = DateTime.UtcNow;
        user.UpdatedAt = DateTime.UtcNow;
        users.Add(user);
        SaveUsers(users);
        return user;
    }

    public bool UpdateUser(User user)
    {
        var users = GetUsers();
        var existing = users.FirstOrDefault(u => u.Id == user.Id);
        if (existing == null) return false;

        existing.FirstName = user.FirstName;
        existing.LastName = user.LastName;
        existing.Email = user.Email;
        existing.Phone = user.Phone;
        existing.Role = user.Role;
        existing.DepartmentId = user.DepartmentId;
        existing.UpdatedAt = DateTime.UtcNow;
        
        SaveUsers(users);
        return true;
    }

    public bool DeleteUser(int id)
    {
        var users = GetUsers();
        var user = users.FirstOrDefault(u => u.Id == id);
        if (user == null) return false;

        users.Remove(user);
        SaveUsers(users);
        return true;
    }
    #endregion

    #region Helper Methods
    private T? ReadFromFile<T>(string fileName)
    {
        var filePath = Path.Combine(_dataDirectory, fileName);
        if (!File.Exists(filePath))
        {
            return default;
        }

        var json = File.ReadAllText(filePath);
        return JsonSerializer.Deserialize<T>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });
    }

    private void WriteToFile<T>(string fileName, T data)
    {
        var filePath = Path.Combine(_dataDirectory, fileName);
        var json = JsonSerializer.Serialize(data, new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });
        File.WriteAllText(filePath, json);
    }
    #endregion
}