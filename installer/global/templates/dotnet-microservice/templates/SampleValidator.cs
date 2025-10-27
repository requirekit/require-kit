using FastEndpoints;
using FluentValidation;

namespace {ServiceName}.API.Validators;

/// <summary>
/// Validator for Get{Feature} request
/// </summary>
public class Get{Feature}RequestValidator : Validator<Get{Feature}Request>
{
    public Get{Feature}RequestValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("ID is required")
            .Must(BeAValidGuid).WithMessage("ID must be a valid GUID");
    }
    
    private bool BeAValidGuid(Guid guid)
    {
        return guid != Guid.Empty;
    }
}

/// <summary>
/// Validator for Create{Feature} request
/// </summary>
public class Create{Feature}RequestValidator : Validator<Create{Feature}Request>
{
    public Create{Feature}RequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MinimumLength(3).WithMessage("Name must be at least 3 characters long")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters")
            .Matches("^[a-zA-Z0-9 ._-]+$").WithMessage("Name contains invalid characters");
        
        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("Description must not exceed 500 characters")
            .When(x => !string.IsNullOrEmpty(x.Description));
        
        // Add custom validation rules
        RuleFor(x => x)
            .Must(NotHaveReservedName).WithMessage("The name '{PropertyValue}' is reserved and cannot be used")
            .When(x => !string.IsNullOrEmpty(x.Name));
    }
    
    private bool NotHaveReservedName(Create{Feature}Request request)
    {
        var reservedNames = new[] { "admin", "system", "root", "default" };
        return !reservedNames.Contains(request.Name?.ToLower());
    }
}

/// <summary>
/// Validator for Update{Feature} request
/// </summary>
public class Update{Feature}RequestValidator : Validator<Update{Feature}Request>
{
    public Update{Feature}RequestValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("ID is required")
            .Must(BeAValidGuid).WithMessage("ID must be a valid GUID");
        
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MinimumLength(3).WithMessage("Name must be at least 3 characters long")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters")
            .Matches("^[a-zA-Z0-9 ._-]+$").WithMessage("Name contains invalid characters");
        
        RuleFor(x => x.Description)
            .MaximumLength(500).WithMessage("Description must not exceed 500 characters")
            .When(x => !string.IsNullOrEmpty(x.Description));
    }
    
    private bool BeAValidGuid(Guid guid)
    {
        return guid != Guid.Empty;
    }
}

/// <summary>
/// Validator for Delete{Feature} request
/// </summary>
public class Delete{Feature}RequestValidator : Validator<Delete{Feature}Request>
{
    public Delete{Feature}RequestValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("ID is required")
            .Must(BeAValidGuid).WithMessage("ID must be a valid GUID");
    }
    
    private bool BeAValidGuid(Guid guid)
    {
        return guid != Guid.Empty;
    }
}

/// <summary>
/// Validator for pagination requests
/// </summary>
public class PaginationValidator<T> : Validator<T> where T : IPaginatedRequest
{
    public PaginationValidator()
    {
        RuleFor(x => x.Page)
            .GreaterThanOrEqualTo(1).WithMessage("Page must be greater than or equal to 1");
        
        RuleFor(x => x.PageSize)
            .InclusiveBetween(1, 100).WithMessage("Page size must be between 1 and 100");
    }
}

/// <summary>
/// Interface for paginated requests
/// </summary>
public interface IPaginatedRequest
{
    int Page { get; set; }
    int PageSize { get; set; }
}
