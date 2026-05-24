using Microsoft.AspNetCore.Mvc;
using WarehouseApi.Models;
using WarehouseApi.Services;

namespace WarehouseApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IWarehouseService _service;

    public UsersController(IWarehouseService service)
    {
        _service = service;
    }

    /// <summary>
    /// Get all users
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(List<User>), 200)]
    public async Task<IActionResult> GetAll()
    {
        var users = await _service.GetUsersAsync();
        return Ok(users);
    }

    /// <summary>
    /// Get user by ID
    /// </summary>
    /// <param name="id">User ID</param>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(User), 200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> GetById(int id)
    {
        var user = await _service.GetUserAsync(id);
        if (user == null)
        {
            return NotFound($"User with ID {id} not found");
        }
        return Ok(user);
    }

    /// <summary>
    /// Create a new user
    /// </summary>
    /// <param name="user">User data</param>
    [HttpPost]
    [ProducesResponseType(typeof(User), 201)]
    [ProducesResponseType(400)]
    public async Task<IActionResult> Create([FromBody] User user)
    {
        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        try
        {
            var created = await _service.CreateUserAsync(user);
            return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    /// <summary>
    /// Update an existing user
    /// </summary>
    /// <param name="id">User ID</param>
    /// <param name="user">Updated user data</param>
    [HttpPut("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(400)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Update(int id, [FromBody] User user)
    {
        if (id != user.Id)
        {
            return BadRequest("ID in URL does not match ID in body");
        }

        if (!ModelState.IsValid)
        {
            return BadRequest(ModelState);
        }

        try
        {
            var success = await _service.UpdateUserAsync(user);
            if (!success)
            {
                return NotFound($"User with ID {id} not found");
            }

            return NoContent();
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    /// <summary>
    /// Delete a user
    /// </summary>
    /// <param name="id">User ID</param>
    [HttpDelete("{id}")]
    [ProducesResponseType(204)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> Delete(int id)
    {
        var success = await _service.DeleteUserAsync(id);
        if (!success)
        {
            return NotFound($"User with ID {id} not found");
        }

        return NoContent();
    }
}