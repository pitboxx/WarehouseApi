using Microsoft.AspNetCore.Mvc;
using WarehouseApi.Models;
using WarehouseApi.Services;

namespace WarehouseApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IWarehouseService _service;

    public ProductsController(IWarehouseService service)
    {
        _service = service;
    }

    /// <summary>
    /// Get all products
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(List<Product>), 200)]
    public async Task<IActionResult> GetAll()
    {
        var products = await _service.GetProductsAsync();
        return Ok(products);
    }

    /// <summary>
    /// Get product by ID
    /// </summary>
    /// <param name="id">Product ID</param>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(Product), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetById(int id)
    {
        var product = await _service.GetProductAsync(id);
        if (product == null)
        {
            return NotFound($"Product with ID {id} not found");
        }
        return Ok(product);
    }

    /// <summary>
    /// Create a new product
    /// </summary>
    /// <param name="product">Product data</param>
    [HttpPost]
    [ProducesResponseType(typeof(Product), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> Create([FromBody] Product product)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        try
        {
            var created = await _service.CreateProductAsync(product);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    /// <summary>
    /// Update an existing product
    /// </summary>
    /// <param name="id">Product ID</param>
    /// <param name="product">Updated product data</param>
    [HttpPut("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Update(int id, [FromBody] Product product)
    {
        if (id != product.Id)
        {
            return BadRequest("ID in URL does not match ID in body");
        }

        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        try
        {
            var success = await _service.UpdateProductAsync(product);
            if (!success)
            {
                return NotFound($"Product with ID {id} not found");
            }

            return NoContent();
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    /// <summary>
    /// Delete a product
    /// </summary>
    /// <param name="id">Product ID</param>
    [HttpDelete("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Delete(int id)
    {
        var success = await _service.DeleteProductAsync(id);
        if (!success)
        {
            return NotFound($"Product with ID {id} not found");
        }

        return NoContent();
    }
}