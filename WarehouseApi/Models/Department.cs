namespace WarehouseApi.Models;

public class Department
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Location { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    
    // Navigation property for products in this department
    public List<Product> Products { get; set; } = new List<Product>();
    
    // Navigation property for users assigned to this department
    public List<User> Users { get; set; } = new List<User>();
}