# Formalize EARS Command

Convert natural language requirements to EARS notation.

## Usage
Type `/formalize-ears` to convert gathered requirements into formal EARS statements.

## Input
I'll look for requirements from:
1. Recent requirements gathering session
2. Requirements in `docs/requirements/draft/`
3. Any requirements you provide directly

## EARS Patterns Applied

### Ubiquitous (Always Active)
```
The [system] shall [function]
```

### Event-Driven (Triggered)
```
When [trigger], the [system] shall [response]
```

### State-Driven (Conditional)
```
While [state], the [system] shall [behavior]
```

### Unwanted Behavior (Error Handling)
```
If [error condition], then the [system] shall [recovery]
```

### Optional Feature (Configurable)
```
Where [feature enabled], the [system] shall [capability]
```

## Example Conversion

### Input (Natural Language)
"Users should be able to reset their password by email"

### Output (EARS)
```markdown
## REQ-001: Password Reset Initiation [Event-Driven]
When a user requests a password reset, the system shall send a verification email with a secure token.

## REQ-002: Token Validation [Unwanted Behavior]
If an invalid or expired token is submitted, then the system shall display an error and require a new reset request.

## REQ-003: Password Update [Event-Driven]
When a valid token and new password are submitted, the system shall update the password and invalidate the token.
```

## Output Location
Formalized requirements will be saved to:
- `docs/requirements/[feature-name].md`

## Quality Checks
Each EARS requirement will be validated for:
- ✓ Clear trigger or condition
- ✓ Specific system response
- ✓ Testable criteria
- ✓ Unambiguous language
- ✓ Atomic behavior (one requirement per statement)

## Next Steps
After formalizing to EARS, use `/generate-bdd` to create test scenarios.
