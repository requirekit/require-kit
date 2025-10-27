using {ServiceName}.API.Domain;
using {ServiceName}.API.Infrastructure.Extensions;
using {ServiceName}.API.Models.Requests;
using {ServiceName}.API.Models.Responses;
using {ServiceName}.API.Services.Interfaces;
using {ServiceName}.API.Validators;
using FastEndpoints;
using Microsoft.AspNetCore.Http;

namespace {ServiceName}.API.Endpoints.{Feature};

/// <summary>
/// Endpoint to retrieve a {Feature} by ID
/// </summary>
public class Get{Feature}ById : Endpoint<Get{Feature}Request, {Feature}Response>
{
    private readonly I{Feature}Service _service;
    private readonly ILogger<Get{Feature}ById> _logger;
    
    public Get{Feature}ById(I{Feature}Service service, ILogger<Get{Feature}ById> logger)
    {
        _service = service;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Get("{feature}/{id}");
        AllowAnonymous(); // TODO: Update with appropriate authorization policy
        
        Validator<Get{Feature}RequestValidator>();
        
        Description(b => b
            .Accepts<Get{Feature}Request>()
            .Produces<{Feature}Response>(200, "application/json")
            .ProducesProblem(400)
            .ProducesProblem(404)
            .ProducesProblem(500)
            .WithName("Get{Feature}")
            .WithDisplayName("Get {Feature} by ID")
            .WithDescription("Retrieves a {Feature} by its unique identifier.")
            .WithSummary("Get {Feature} by ID")
            .WithTags("{Feature}"));
        
        Summary(s =>
        {
            s.Summary = "Get {Feature} by ID";
            s.Description = "Retrieves a {Feature} by its unique identifier.";
            s.Params["id"] = "The unique identifier of the {Feature}";
            s.Response(200, "The requested {Feature}", example: new {Feature}Response
            {
                Id = Guid.NewGuid(),
                Name = "Sample {Feature}",
                Description = "This is a sample {Feature}",
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            });
            s.Response(404, "The {Feature} was not found");
        });
    }

    public override async Task HandleAsync(Get{Feature}Request req, CancellationToken ct)
    {
        _logger.LogInformation("Retrieving {Feature} with ID: {Id}", req.Id);
        
        var result = await _service.Get{Feature}Async(req.Id, ct);
        
        await this.HandleEitherResultAsync(
            result,
            async response =>
            {
                _logger.LogInformation("Successfully retrieved {Feature} with ID: {Id}", req.Id);
                await SendOkAsync(response, ct);
            },
            ct
        );
    }
}

/// <summary>
/// Endpoint to create a new {Feature}
/// </summary>
public class Create{Feature} : Endpoint<Create{Feature}Request, {Feature}Response>
{
    private readonly I{Feature}Service _service;
    private readonly ILogger<Create{Feature}> _logger;
    
    public Create{Feature}(I{Feature}Service service, ILogger<Create{Feature}> logger)
    {
        _service = service;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Post("{feature}");
        AllowAnonymous(); // TODO: Update with appropriate authorization policy
        
        Validator<Create{Feature}RequestValidator>();
        
        Description(b => b
            .Accepts<Create{Feature}Request>("application/json")
            .Produces<{Feature}Response>(201, "application/json")
            .ProducesProblem(400)
            .ProducesProblem(409)
            .ProducesProblem(500)
            .WithName("Create{Feature}")
            .WithDisplayName("Create {Feature}")
            .WithDescription("Creates a new {Feature}.")
            .WithSummary("Create {Feature}")
            .WithTags("{Feature}"));
        
        Summary(s =>
        {
            s.Summary = "Create {Feature}";
            s.Description = "Creates a new {Feature} with the provided information.";
            s.ExampleRequest = new Create{Feature}Request
            {
                Name = "New {Feature}",
                Description = "Description of the new {Feature}"
            };
            s.Response(201, "The created {Feature}", example: new {Feature}Response
            {
                Id = Guid.NewGuid(),
                Name = "New {Feature}",
                Description = "Description of the new {Feature}",
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            });
            s.Response(400, "Invalid request data");
            s.Response(409, "A {Feature} with the same name already exists");
        });
    }

    public override async Task HandleAsync(Create{Feature}Request req, CancellationToken ct)
    {
        _logger.LogInformation("Creating new {Feature} with name: {Name}", req.Name);
        
        var dto = new Create{Feature}Dto
        {
            Name = req.Name,
            Description = req.Description
        };
        
        var result = await _service.Create{Feature}Async(dto, ct);
        
        await this.HandleEitherResultAsync(
            result,
            async response =>
            {
                _logger.LogInformation("Successfully created {Feature} with ID: {Id}", response.Id);
                await SendCreatedAtAsync<Get{Feature}ById>(
                    new { id = response.Id }, 
                    response, 
                    generateAbsoluteUrl: true,
                    cancellation: ct);
            },
            ct
        );
    }
}

/// <summary>
/// Endpoint to update an existing {Feature}
/// </summary>
public class Update{Feature} : Endpoint<Update{Feature}Request, {Feature}Response>
{
    private readonly I{Feature}Service _service;
    private readonly ILogger<Update{Feature}> _logger;
    
    public Update{Feature}(I{Feature}Service service, ILogger<Update{Feature}> logger)
    {
        _service = service;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Put("{feature}/{id}");
        AllowAnonymous(); // TODO: Update with appropriate authorization policy
        
        Validator<Update{Feature}RequestValidator>();
        
        Description(b => b
            .Accepts<Update{Feature}Request>("application/json")
            .Produces<{Feature}Response>(200, "application/json")
            .ProducesProblem(400)
            .ProducesProblem(404)
            .ProducesProblem(409)
            .ProducesProblem(500)
            .WithName("Update{Feature}")
            .WithDisplayName("Update {Feature}")
            .WithDescription("Updates an existing {Feature}.")
            .WithSummary("Update {Feature}")
            .WithTags("{Feature}"));
    }

    public override async Task HandleAsync(Update{Feature}Request req, CancellationToken ct)
    {
        _logger.LogInformation("Updating {Feature} with ID: {Id}", req.Id);
        
        var dto = new Update{Feature}Dto
        {
            Name = req.Name,
            Description = req.Description
        };
        
        var result = await _service.Update{Feature}Async(req.Id, dto, ct);
        
        await this.HandleEitherResultAsync(
            result,
            async response =>
            {
                _logger.LogInformation("Successfully updated {Feature} with ID: {Id}", req.Id);
                await SendOkAsync(response, ct);
            },
            ct
        );
    }
}

/// <summary>
/// Endpoint to delete a {Feature}
/// </summary>
public class Delete{Feature} : Endpoint<Delete{Feature}Request, EmptyResponse>
{
    private readonly I{Feature}Service _service;
    private readonly ILogger<Delete{Feature}> _logger;
    
    public Delete{Feature}(I{Feature}Service service, ILogger<Delete{Feature}> logger)
    {
        _service = service;
        _logger = logger;
    }
    
    public override void Configure()
    {
        Delete("{feature}/{id}");
        AllowAnonymous(); // TODO: Update with appropriate authorization policy
        
        Validator<Delete{Feature}RequestValidator>();
        
        Description(b => b
            .Accepts<Delete{Feature}Request>()
            .Produces(204)
            .ProducesProblem(404)
            .ProducesProblem(500)
            .WithName("Delete{Feature}")
            .WithDisplayName("Delete {Feature}")
            .WithDescription("Deletes an existing {Feature}.")
            .WithSummary("Delete {Feature}")
            .WithTags("{Feature}"));
    }

    public override async Task HandleAsync(Delete{Feature}Request req, CancellationToken ct)
    {
        _logger.LogInformation("Deleting {Feature} with ID: {Id}", req.Id);
        
        var result = await _service.Delete{Feature}Async(req.Id, ct);
        
        await this.HandleEitherResultAsync(
            result,
            async _ =>
            {
                _logger.LogInformation("Successfully deleted {Feature} with ID: {Id}", req.Id);
                await SendNoContentAsync(ct);
            },
            ct
        );
    }
}
