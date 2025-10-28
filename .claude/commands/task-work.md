# Task Work - Unified Implementation Command

Execute complete implementation workflow including code generation, testing, and verification with support for multiple development modes.

## Feature Detection and Package Integration

The `/task-work` command automatically detects which Agentecflow packages are installed and adapts its behavior accordingly, enabling **bidirectional optional integration** between taskwright and require-kit.

### Package-Specific Features

| Installed Packages | Available Features | Unavailable Features |
|-------------------|-------------------|----------------------|
| **taskwright only** | ✅ Task execution workflow<br>✅ Quality gate validation<br>✅ TDD/Standard modes<br>✅ Test orchestration | ❌ BDD mode (requires scenarios)<br>❌ Requirements loading<br>❌ Epic/Feature context |
| **Both installed** | ✅ All features above<br>✅ BDD mode with Gherkin scenarios<br>✅ Requirements context loading<br>✅ Epic/Feature hierarchy | None - full integration |

### Automatic Detection

The command uses package detection to determine available features:
- **taskwright.marker**: Enables task execution and quality gates
- **require-kit.marker**: Enables requirements, BDD scenarios, and hierarchy

### Graceful Degradation

**When require-kit is not installed:**
- ✅ Standard and TDD modes work normally
- ❌ BDD mode unavailable (requires BDD scenarios from require-kit)
- ℹ️ Requirements loading skipped
- ℹ️ Epic/Feature context not loaded

**Example output (taskwright only):**
```
🚀 Starting Task Work: TASK-045

ℹ️  Package Detection:
- taskwright: ✅ installed
- require-kit: ❌ not installed

📋 Task Loading
✅ Loaded from tasks/in_progress/TASK-045.md
✅ Acceptance criteria loaded
ℹ️ Requirements loading skipped (install require-kit for EARS requirements)
ℹ️ BDD scenarios skipped (install require-kit for BDD mode)

🛠️  Mode: Standard (BDD mode unavailable)
```

## Usage
```bash
/task-work TASK-XXX [--mode=standard|tdd|bdd] [--language=auto|python|typescript|csharp] [--coverage-threshold=80]
```

## Examples
```bash
# Standard development (implementation + tests together)
/task-work TASK-042

# Test-Driven Development (tests first, then implementation)
/task-work TASK-042 --mode=tdd

# Behavior-Driven Development (from scenarios to implementation)
/task-work TASK-042 --mode=bdd

# With custom coverage threshold
/task-work TASK-042 --coverage-threshold=90

# Fix only mode for blocked tasks
/task-work TASK-042 --fix-only
```

## Development Modes

### Standard Mode (Default)
Traditional development approach:
1. Generate implementation based on requirements
2. Create comprehensive test suite
3. Run tests and verify quality
4. Update task state based on results

### TDD Mode (Test-Driven Development)
Follow Red-Green-Refactor cycle:
1. **RED**: Generate failing tests based on requirements
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while keeping tests green
4. Verify coverage and quality gates

### BDD Mode (Behavior-Driven Development)
Start from user scenarios:
1. Load linked BDD scenarios (Gherkin)
2. Generate step definitions
3. Implement features to satisfy scenarios
4. Add unit tests for completeness
5. Verify all scenarios pass

**Note**: BDD mode requires **require-kit** to be installed. If require-kit is not detected, the command will display an error with installation instructions.

## Process Flow

### Step 1: Task Loading and Analysis
```yaml
Load task from: tasks/in_progress/TASK-XXX.md
Extract:
  - Acceptance criteria (always)
  - Technology stack (always)
  - Requirements (EARS) - if require-kit installed
  - BDD scenarios - if require-kit installed
  - Epic/Feature context - if require-kit installed
```

**Conditional Loading**: The system automatically detects installed packages and loads available features. If require-kit is not installed, the workflow continues with acceptance criteria only.

### Step 2: Mode-Specific Implementation

#### Standard Mode Flow
```mermaid
graph LR
    A[Load Task] --> B[Generate Code]
    B --> C[Generate Tests]
    C --> D[Run Tests]
    D --> E{Pass?}
    E -->|Yes| F[Check Coverage]
    E -->|No| G[Block Task]
    F --> H{≥80%?}
    H -->|Yes| I[Move to Review]
    H -->|No| J[Add Tests]
```

#### TDD Mode Flow
```mermaid
graph LR
    A[Load Task] --> B[Write Tests]
    B --> C[Run Tests RED]
    C --> D[Write Code]
    D --> E[Run Tests]
    E --> F{GREEN?}
    F -->|No| G[Fix Code]
    F -->|Yes| H[Refactor]
    H --> I[Final Tests]
    I --> J[Review]
```

#### BDD Mode Flow
```mermaid
graph LR
    A[Load Scenarios] --> B[Step Defs]
    B --> C[Implementation]
    C --> D[Run Scenarios]
    D --> E{Pass?}
    E -->|Yes| F[Unit Tests]
    E -->|No| G[Fix]
    F --> H[Review]
```

### Step 3: Test Execution

Automatic detection and execution based on project type:

#### Python Projects
```bash
pytest tests/ -v --cov=src --cov-report=term --cov-report=json
```

#### TypeScript/JavaScript Projects
```bash
npm test -- --coverage --json --outputFile=test-results.json
```

#### .NET Projects
```bash
dotnet test --collect:"XPlat Code Coverage" --logger:"json"
```

### Step 4: Quality Gates Evaluation

```yaml
quality_gates:
  tests:
    all_passing: required
    no_skipped: warning
  coverage:
    lines: ≥ 80%      # Required
    branches: ≥ 75%   # Required
    functions: ≥ 80%  # Warning
  performance:
    total_time: < 30s
    single_test: < 5s
```

### Step 5: State Management

Automatic state transitions based on results:
- ✅ All gates pass → `IN_REVIEW`
- ❌ Tests fail → `BLOCKED`
- ⚠️ Coverage low → Request more tests
- 🔄 Minor issues → `IN_REVIEW` with notes

## Output Format

### Success Output
```
✅ Task Work Complete - TASK-XXX

📊 Implementation Summary
Mode: TDD
Duration: 45 seconds
Files Created: 7
Tests Written: 15

🧪 Test Results
Total: 15 tests
Passed: 15 ✅
Failed: 0
Coverage: 92%

📈 Quality Gates
✅ All tests passing
✅ Coverage exceeds 80%
✅ No security issues
✅ Performance acceptable

🔄 Status Update
From: IN_PROGRESS
To: IN_REVIEW
Reason: All quality gates passed

Next: /task-review TASK-XXX
```

### Failure Output
```
❌ Task Work Failed - TASK-XXX

📊 Test Results
Total: 15 tests
Passed: 12 ⚠️
Failed: 3 ❌

Failed Tests:
1. test_auth_service.py::test_login
   AssertionError: Expected 200, got 401
   
2. test_auth_service.py::test_session
   TimeoutError: Exceeded 5s limit

📈 Quality Issues
❌ 3 tests failing
⚠️ Coverage at 75% (min: 80%)

🔄 Status Update
From: IN_PROGRESS
To: BLOCKED
Reason: Test failures

Fix issues and run:
/task-work TASK-XXX --fix-only
```

## Mode-Specific Templates

### TDD Mode Template
```python
# Step 1: Generate failing tests (RED)
def test_feature_requirement_1():
    """Test: {requirement_description}"""
    # This should fail initially
    service = FeatureService()
    result = service.process(test_data)
    assert result.success == True
    assert result.value == expected_value

# Step 2: Minimal implementation (GREEN)
class FeatureService:
    def process(self, data):
        # Minimal code to pass test
        return Result(success=True, value=expected_value)

# Step 3: Refactor (REFACTOR)
class FeatureService:
    def __init__(self, validator, repository):
        self.validator = validator
        self.repository = repository
    
    def process(self, data):
        # Improved implementation
        if not self.validator.is_valid(data):
            return Result(success=False, error="Invalid data")
        
        processed = self._transform(data)
        self.repository.save(processed)
        return Result(success=True, value=processed)
```

### BDD Mode Template
```gherkin
# Start with scenario
Feature: User Authentication
  Scenario: Successful login
    Given a registered user with email "user@example.com"
    When they submit valid credentials
    Then they should be logged in successfully
    And a session token should be created

# Generate step definitions
@given('a registered user with email "{email}"')
def step_registered_user(context, email):
    context.user = User(email=email, password="hashed")
    context.db.save(context.user)

@when('they submit valid credentials')
def step_submit_credentials(context):
    context.response = auth_service.login(
        email=context.user.email,
        password="correct_password"
    )

@then('they should be logged in successfully')
def step_verify_login(context):
    assert context.response.success == True
    assert context.response.token is not None
```

### Standard Mode Template
```typescript
// Implementation and tests created together

// Implementation
export class AuthenticationService {
  async login(credentials: LoginCredentials): Promise<AuthResult> {
    const user = await this.userRepo.findByEmail(credentials.email);
    if (!user || !await this.verifyPassword(credentials.password, user.password)) {
      return { success: false, error: 'Invalid credentials' };
    }
    
    const token = this.generateToken(user);
    return { success: true, token, user };
  }
}

// Tests
describe('AuthenticationService', () => {
  it('should authenticate valid user', async () => {
    const service = new AuthenticationService(mockRepo);
    const result = await service.login(validCredentials);
    expect(result.success).toBe(true);
    expect(result.token).toBeDefined();
  });
  
  it('should reject invalid credentials', async () => {
    const service = new AuthenticationService(mockRepo);
    const result = await service.login(invalidCredentials);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Invalid credentials');
  });
});
```

## Error Handling

### Common Issues and Solutions

#### Issue: BDD Mode Without require-kit
```
❌ BDD mode unavailable

BDD mode requires BDD scenarios from require-kit.

Current configuration:
- taskwright: ✅ installed
- require-kit: ❌ not installed

To use BDD mode:
1. Install require-kit package
2. Link BDD scenarios to your task
3. Run /task-work TASK-XXX --mode=bdd

Alternative: Use --mode=standard or --mode=tdd instead
```

#### Issue: Import Errors (TDD Mode)
```
❌ ImportError: cannot import name 'ServiceClass'

This is expected in TDD RED phase.
Creating minimal implementation...
✅ Import errors resolved
```

#### Issue: Low Coverage
```
⚠️ Coverage at 72% (minimum: 80%)

Analyzing uncovered code...
Generating additional tests for:
- Error handling (lines 45-52)
- Edge cases (lines 78-85)

✅ Added 4 tests
✅ Coverage now: 86%
```

#### Issue: Slow Tests
```
⚠️ Test performance warning
- test_large_dataset: 7.2s (max: 5s)
- test_integration_flow: 6.1s (max: 5s)

Consider:
- Mocking external dependencies
- Using test fixtures
- Reducing test data size
```

## Advanced Options

### Fix-Only Mode
```bash
# Only fix failing tests, don't regenerate
/task-work TASK-XXX --fix-only
```

### Watch Mode
```bash
# Continuously run tests as changes are made
/task-work TASK-XXX --watch
```

### Dry Run
```bash
# Show what would be done without executing
/task-work TASK-XXX --dry-run
```

### Custom Language
```bash
# Override auto-detection
/task-work TASK-XXX --language=python
```

## Integration Points

### Git Integration
- Automatic commits after each phase (RED, GREEN, REFACTOR)
- Branch creation for task work
- PR/MR creation when ready for review

### CI/CD Integration
- Webhook triggers on task completion
- Test results posted to CI system
- Coverage reports uploaded

### External PM Tool Integration (require-kit)
When require-kit is installed:
- Sync task status to Jira/Azure DevOps/Linear
- Post test results to external systems
- Update external tickets on completion
- Track progress rollup to epics and features

## Best Practices

1. **Always start with requirements**: Ensure task has clear acceptance criteria
2. **Choose the right mode**: 
   - TDD for complex logic
   - BDD for user-facing features
   - Standard for straightforward implementations
3. **Don't skip refactoring**: In TDD mode, always improve after GREEN
4. **Review test quality**: High coverage doesn't mean good tests
5. **Document failures**: When blocked, provide clear unblocking steps

## Migration from Old Commands

The following commands are deprecated but still functional:
- `/task-implement` → Use `/task-work`
- `/task-test` → Integrated into `/task-work`
- Individual test commands → Automatic in `/task-work`

These will show deprecation warnings and suggest using `/task-work` instead.
