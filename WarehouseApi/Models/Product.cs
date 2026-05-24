namespace WarehouseApi.Models;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public int Quantity { get; set; }
    public string Sku { get; set; } = string.Empty; // Stock Keeping Unit
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    
    // Foreign key to Department
    public int DepartmentId { get; set; }
    
    // Navigation property
    public Department? Department { get; set; }
}