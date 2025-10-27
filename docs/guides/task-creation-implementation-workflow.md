# Task Creation and Implementation Workflow Guide

## Overview
This guide explains how to create and implement tasks using the Claude Code Agentecflow system, specifically focusing on how to ask Claude Code to implement tasks and generate code.

## Prerequisites
- Claude Code Agentecflow system installed (`agentec-init` completed)
- Project initialized with a template (e.g., `agentec-init maui`)
- Understanding of EARS notation and BDD scenarios

## Workflow Phases

### 1. Requirements Gathering Phase
First, create requirements for your application. In Claude Code, run:

```markdown
/gather-requirements
```

This initiates an interactive Q&A session. For a MAUI app, you might gather requirements like:
- "Mobile app for task management"
- "Cross-platform iOS/Android support"
- "Offline-first with sync capabilities"
- "User authentication"

### 2. Formalize into EARS Requirements
Convert natural language requirements into EARS notation:

```markdown
/formalize-ears
```

This creates structured requirements in `docs/requirements/`. Example EARS requirement:

```markdown
# docs/requirements/REQ-001-user-authentication.md
---
id: REQ-001
type: event-driven
priority: high
---

## EARS Statement
**When** a user launches the app for the first time, **the system** shall present a login screen with email and password fields.

## Acceptance Criteria
- [ ] Login screen displays on first launch
- [ ] Email field has validation
- [ ] Password field is masked
- [ ] Login button is disabled until valid input
```

### 3. Generate BDD Scenarios
Generate test scenarios from requirements:

```markdown
/generate-bdd
```

This creates Gherkin scenarios in `docs/bdd/features/`:

```gherkin
# docs/bdd/features/authentication.feature
Feature: User Authentication
  As a mobile app user
  I want to securely log into the app
  So that I can access my personal data

  Scenario: Successful login with valid credentials
    Given I am on the login screen
    When I enter "user@example.com" as email
    And I enter "ValidPass123!" as password
    And I tap the login button
    Then I should see the main dashboard
    And my session should be persisted
```

### 4. Create Implementation Tasks
Create specific tasks for Claude Code to implement. Create task files in `docs/tasks/`:

```markdown
# docs/tasks/TASK-001-login-viewmodel.md
---
id: TASK-001
requirement: REQ-001
bdd: BDD-001
type: implementation
status: pending
---

# Task: Implement Login ViewModel

## Description
Create the LoginViewModel with MVVM pattern using CommunityToolkit.Mvvm

## Requirements
- Use IAuthenticationUseCase for business logic
- Implement email/password validation
- Handle loading states
- Return Either<AppError, AuthResult>

## Acceptance Criteria
- [ ] ViewModel inherits from BaseViewModel
- [ ] Email property with validation
- [ ] Password property with secure string
- [ ] LoginCommand using RelayCommand
- [ ] Error handling with Either pattern
- [ ] Loading indicator support

## Test Coverage Required
- [ ] Integration test from ViewModel to mocked API
- [ ] Validation logic tests
- [ ] Error handling scenarios
```

### 5. Ask Claude Code to Implement Tasks

Three methods to request task implementation:

#### Method 1: Direct Task Reference
```markdown
@claude Please implement TASK-001 following the MAUI template patterns. Use the UseCase pattern with Either monad for error handling.
```

#### Method 2: Context-Aware Implementation
```markdown
@claude Looking at docs/tasks/TASK-001-login-viewmodel.md, please:
1. Create LoginViewModel in ViewModels/Features/
2. Create IAuthenticationUseCase in UseCases/Interfaces/
3. Implement AuthenticationUseCase with Either<AppError, AuthResult>
4. Create integration tests in Tests/Integration/
```

#### Method 3: Test-First Approach
```markdown
@claude Following Outside-In TDD:
1. First write the integration test for login functionality
2. Then implement LoginViewModel to make the test pass
3. Use the MAUI template patterns from .claude/CLAUDE.md
```

### 6. Task Implementation Example

When Claude Code implements TASK-001, it should generate:

```csharp
// ViewModels/Features/LoginViewModel.cs
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using LanguageExt;
using static LanguageExt.Prelude;

namespace MauiAgentecFlow.ViewModels.Features;

public partial class LoginViewModel : BaseViewModel
{
    private readonly IAuthenticationUseCase _authUseCase;
    private readonly INavigationService _navigationService;

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    private string email = string.Empty;

    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Password is required")]
    [MinLength(8, ErrorMessage = "Password must be at least 8 characters")]
    private string password = string.Empty;

    public LoginViewModel(
        IAuthenticationUseCase authUseCase,
        INavigationService navigationService)
    {
        _authUseCase = authUseCase;
        _navigationService = navigationService;
    }

    [RelayCommand]
    private async Task LoginAsync()
    {
        if (HasErrors) return;

        using (var _ = new LoadingScope(this))
        {
            var result = await _authUseCase.ExecuteAsync(
                new LoginRequest(Email, Password));
            
            result.Match(
                Right: async authResult =>
                {
                    await _navigationService.NavigateToAsync("///main");
                },
                Left: error => HandleError(error)
            );
        }
    }
}
```

### 7. Update Task Status
After implementation, update the task status:

```markdown
/update-state

# This updates docs/state/current-sprint.md with:
- TASK-001: ✅ Complete
- Tests: 5/5 passing
- Coverage: 95%
```

### 8. Execute Tests
Run the test suite with quality gates:

```markdown
/execute-tests
```

This runs tests and checks quality gates defined in `.claude/hooks/quality-gates.yml`.

## Best Practices for Task Creation

### 1. Granular Tasks
Create small, focused tasks that can be completed in 1-2 hours:
- TASK-001: Create LoginViewModel
- TASK-002: Create AuthenticationUseCase
- TASK-003: Create LoginView XAML
- TASK-004: Add form validation
- TASK-005: Add error handling

### 2. Clear Context in Tasks
Include in each task:
- Links to requirements (REQ-xxx)
- Links to BDD scenarios (BDD-xxx)
- Specific file paths
- Pattern references from CLAUDE.md
- Test requirements

### 3. Progressive Implementation
Structure tasks to build incrementally:
```markdown
Sprint 1:
- TASK-001: Basic LoginViewModel (no validation)
- TASK-002: Add validation
- TASK-003: Add error handling
- TASK-004: Add loading states
- TASK-005: Add persistence
```

### 4. Test-Driven Tasks
Create test tasks before implementation:
```markdown
TASK-001-TEST: Write integration tests for login
TASK-002-IMPL: Implement LoginViewModel to pass tests
```

## Example Task Workflow Session

Complete example of interacting with Claude Code:

```markdown
# 1. Start with requirements
@claude /gather-requirements
[Interactive session about login feature]

# 2. Formalize requirements
@claude /formalize-ears
[Creates REQ-001 through REQ-005]

# 3. Generate test scenarios
@claude /generate-bdd
[Creates authentication.feature]

# 4. Create first task
@claude Please create a task file for implementing the LoginViewModel with the following requirements:
- MVVM pattern with CommunityToolkit.Mvvm
- Either monad for error handling
- Integration with AuthenticationUseCase
- Full test coverage

# 5. Implement the task
@claude Please implement the LoginViewModel task following our MAUI template patterns. Start with the integration test, then implement the ViewModel.

# 6. Review and iterate
@claude The implementation looks good. Now create a task for the LoginView XAML that binds to this ViewModel.

# 7. Update progress
@claude /update-state
[Updates sprint progress and task completion]
```

## Task Templates

Create reusable task templates in `.claude/templates/task-types/`:

```markdown
# .claude/templates/task-types/viewmodel-task.md
---
type: viewmodel
estimated_hours: 2
test_required: true
---

# Task: Implement {FeatureName}ViewModel

## Implementation Checklist
- [ ] Create ViewModel in ViewModels/Features/
- [ ] Inherit from BaseViewModel
- [ ] Add observable properties
- [ ] Implement commands with RelayCommand
- [ ] Use UseCase pattern for business logic
- [ ] Handle errors with Either pattern
- [ ] Add loading state management

## Test Requirements
- [ ] Integration test from ViewModel to mocked API
- [ ] Test all commands
- [ ] Test error scenarios
- [ ] Test loading states
```

## Task Types and Examples

### ViewModel Tasks
```markdown
# docs/tasks/TASK-002-product-list-viewmodel.md
---
id: TASK-002
type: viewmodel
requirement: REQ-005
---

# Task: ProductList ViewModel

Create ViewModel for displaying products with:
- Pagination support
- Pull-to-refresh
- Search functionality
- Offline caching
```

### UseCase Tasks
```markdown
# docs/tasks/TASK-003-sync-usecase.md
---
id: TASK-003
type: usecase
requirement: REQ-010
---

# Task: Data Synchronization UseCase

Implement offline-first sync:
- Queue local changes
- Sync when online
- Conflict resolution
- Either<SyncError, SyncResult>
```

### View Tasks
```markdown
# docs/tasks/TASK-004-login-view.md
---
id: TASK-004
type: view
requirement: REQ-001
---

# Task: Login View XAML

Create login screen with:
- Material Design styling
- Input validation display
- Loading overlay
- Error message display
```

### Integration Tasks
```markdown
# docs/tasks/TASK-005-api-integration.md
---
id: TASK-005
type: integration
requirement: REQ-015
---

# Task: API Service Integration

Integrate with backend API:
- JWT authentication
- Refresh token handling
- Request/response logging
- Retry logic with Polly
```

## Quality Gates and Validation

### Pre-Implementation Checklist
Before implementing a task, ensure:
- [ ] Requirement (REQ-xxx) exists and is approved
- [ ] BDD scenario (BDD-xxx) is defined
- [ ] Dependencies are identified
- [ ] Test approach is clear

### Post-Implementation Checklist
After implementation, verify:
- [ ] Code follows template patterns
- [ ] Tests pass (unit/integration)
- [ ] Coverage meets threshold (>80%)
- [ ] Documentation is updated
- [ ] Task status is updated

### Quality Gate Configuration
```yaml
# .claude/hooks/quality-gates.yml
quality_gates:
  task_completion:
    - name: "Code Coverage"
      threshold: 80
      required: true
    - name: "Test Pass Rate"
      threshold: 100
      required: true
    - name: "Pattern Compliance"
      check: "UseCase + Either pattern"
      required: true
```

## Common Patterns and Anti-Patterns

### ✅ Good Patterns
- Small, focused tasks (1-2 hours)
- Clear acceptance criteria
- Test-first approach
- Pattern consistency
- Incremental progress

### ❌ Anti-Patterns to Avoid
- Large, monolithic tasks
- Vague requirements
- Implementation without tests
- Skipping error handling
- Breaking established patterns

## Troubleshooting

### Issue: Task Too Large
**Solution**: Break into subtasks:
```markdown
TASK-010: Parent Task
├── TASK-010.1: Data layer
├── TASK-010.2: Business logic
├── TASK-010.3: UI layer
└── TASK-010.4: Tests
```

### Issue: Unclear Requirements
**Solution**: Return to requirements phase:
```markdown
@claude The requirements for TASK-015 are unclear. Let's run /gather-requirements for the specific feature area.
```

### Issue: Test Failures
**Solution**: Use TDD cycle:
```markdown
@claude Following RED-GREEN-REFACTOR:
1. Show me the failing test
2. Implement minimal code to pass
3. Refactor while keeping tests green
```

## Conclusion

This workflow ensures:
1. **Traceability** - Every task links to requirements and tests
2. **Quality** - Tests are written first or alongside implementation
3. **Consistency** - Templates ensure uniform implementation
4. **Progress Tracking** - State is continuously updated
5. **Maintainability** - Clear patterns and documentation

By following this structured approach, you can efficiently create and implement tasks with Claude Code while maintaining high code quality and project organization.