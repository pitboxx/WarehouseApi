using WarehouseApi.Data;
using WarehouseApi.Services;

var builder = WebApplication.CreateBuilder(args);

// Load hosting configuration
builder.Configuration.AddJsonFile("hosting.json", optional: true, reloadOnChange: true);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Register our services
builder.Services.AddSingleton<JsonFileStorage>();
builder.Services.AddScoped<IWarehouseService, WarehouseService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "Warehouse API v1");
        c.RoutePrefix = "swagger"; // Set Swagger UI at /swagger
    });
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

// Create data directory and seed initial data if needed
var dataDir = Path.Combine(Directory.GetCurrentDirectory(), "Data", "JsonStorage");
if (!Directory.Exists(dataDir))
{
    Directory.CreateDirectory(dataDir);
    
    // Seed with sample data for testing
    var storage = app.Services.GetRequiredService<JsonFileStorage>();
    
    // Create sample departments
    var departments = new List<WarehouseApi.Models.Department>
    {
        new WarehouseApi.Models.Department { Id = 1, Name = "Main Warehouse", Description = "Primary storage facility", Location = "Building A" },
        new WarehouseApi.Models.Department { Id = 2, Name = "Electronics", Description = "Electronic components and devices", Location = "Building B" },
        new WarehouseApi.Models.Department { Id = 3, Name = "Clothing", Description = "Apparel and textiles", Location = "Building C" }
    };
    storage.SaveDepartments(departments);
    
    // Create sample products
    var products = new List<WarehouseApi.Models.Product>
    {
        new WarehouseApi.Models.Product { Id = 1, Name = "Laptop", Description = "High-performance laptop", Price = 999.99m, Quantity = 10, Sku = "LP-001", DepartmentId = 2 },
        new WarehouseApi.Models.Product { Id = 2, Name = "Smartphone", Description = "Latest smartphone model", Price = 699.99m, Quantity = 25, Sku = "SP-002", DepartmentId = 2 },
        new WarehouseApi.Models.Product { Id = 3, Name = "T-Shirt", Description = "Cotton t-shirt", Price = 19.99m, Quantity = 100, Sku = "TS-003", DepartmentId = 3 }
    };
    storage.SaveProducts(products);
    
    // Create sample users
    var users = new List<WarehouseApi.Models.User>
    {
        new WarehouseApi.Models.User { Id = 1, FirstName = "John", LastName = "Doe", Email = "john.doe@example.com", Phone = "+1234567890", Role = "Manager", DepartmentId = 1 },
        new WarehouseApi.Models.User { Id = 2, FirstName = "Jane", LastName = "Smith", Email = "jane.smith@example.com", Phone = "+0987654321", Role = "Employee", DepartmentId = 2 },
        new WarehouseApi.Models.User { Id = 3, FirstName = "Bob", LastName = "Johnson", Email = "bob.johnson@example.com", Phone = "+1122334455", Role = "Admin", DepartmentId = 3 }
    };
    storage.SaveUsers(users);
}

app.Run();
