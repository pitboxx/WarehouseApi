using Microsoft.AspNetCore.Mvc;
using WarehouseApi.Models;
using WarehouseApi.Services;

namespace WarehouseApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DepartmentsController : ControllerBase
{
    private readonly IWarehouseService _service;

    public DepartmentsController(IWarehouseService service)
    {
        _service = service;
    }

    /// <summary>
    /// Get all departments
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(List<Department>), 200)]
    public async Task<IActionResult> GetAll()
    {
        var departments = await _service.GetDepartmentsAsync();
        return Ok(departments);
    }

    /// <summary>
    /// Get department by ID
    /// </summary>
    /// <param name="id">Department ID</param>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(Department), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetById(int id)
    {
        var department = await _service.GetDepartmentAsync(id);
        if (department == null)
        {
            return NotFound($"Department with ID {id} not found");
        }
        return Ok(department);
    }

    /// <summary>
    /// Create a new department
    /// </summary>
    /// <param name="department">Department data</param>
    [HttpPost]
    [ProducesResponseType(typeof(Department), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> Create([FromBody] Department department)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var created = await _service.CreateDepartmentAsync(department);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    /// <summary>
    /// Update an existing department
    /// </summary>
    /// <param name="id">Department ID</param>
    /// <param name="department">Updated department data</param>
    [HttpPut("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Update(int id, [FromBody] Department department)
    {
        if (id != department.Id)
        {
            return BadRequest("ID in URL does not match ID in body");
        }

        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        var success = await _service.UpdateDepartmentAsync(department);
        if (!success)
        {
            return NotFound($"Department with ID {id} not found");
        }

        return NoContent();
    }

    /// <summary>
    /// Delete a department
    /// </summary>
    /// <param name="id">Department ID</param>
    [HttpDelete("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Delete(int id)
    {
        var success = await _service.DeleteDepartmentAsync(id);
        if (!success)
        {
            return NotFound($"Department with ID {id} not found");
        }

        return NoContent();
    }
}