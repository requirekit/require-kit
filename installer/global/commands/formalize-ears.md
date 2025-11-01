# Formalize EARS Command

Convert natural language requirements to EARS notation.

## Usage

```bash
/formalize-ears [--concise] [--max-words N]
```

### Flags

#### --concise
Generate concise EARS requirements with ≤500 word limit.
- Uses bullet points instead of paragraphs
- Focuses on "what" not "how"
- Omits implementation details
- Target: 50-70% token reduction

#### --max-words N
Custom word limit (default: 500 in concise mode, unlimited in standard mode).

### Examples

**Standard mode (default)**:
```bash
/formalize-ears
# Generates comprehensive EARS with rationale, examples, detailed acceptance criteria
```

**Concise mode**:
```bash
/formalize-ears --concise
# Generates concise EARS with bullet points, ≤500 words per requirement
```

**Custom word limit**:
```bash
/formalize-ears --concise --max-words 300
# Generates EARS with ≤300 words per requirement
```

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
"Users should be able to authenticate with username and password"

### Output: Standard Mode (Verbose)
```markdown
## REQ-042: User Authentication

**Type**: Event-Driven

When a user submits valid login credentials through the authentication endpoint,
the system shall perform the following comprehensive sequence of operations to
ensure secure and reliable authentication:

1. The system shall validate the provided credentials against the authentication
   service using industry-standard validation protocols.
2. Upon successful validation, the system shall generate a JSON Web Token (JWT)
   with a 24-hour expiration period to maintain security while balancing user
   convenience.
3. The system shall return the generated token in the response payload to enable
   the client application to maintain an authenticated session.
4. The system shall log the successful authentication event with appropriate
   metadata for security auditing and compliance purposes.

**Rationale**:
User authentication is critical for securing the application. We use JWT tokens
for stateless authentication, allowing for scalability and easier microservices
integration...

**Acceptance Criteria**:
- Valid credentials shall be accepted and result in token generation
- Invalid credentials shall be rejected with appropriate error message
- Token expiration shall be enforced after 24 hours
- All authentication events shall be logged for audit purposes

**Word Count**: 179 words
```

### Output: Concise Mode (--concise)
```markdown
## REQ-042: User Authentication

**Type**: Event-Driven
**Constraint**: ≤500 words

When valid credentials submitted, system shall:
- Validate against auth service
- Generate JWT (24h expiry)
- Return token in response
- Log authentication event

**Acceptance Criteria**:
- ✅ Valid credentials → JWT token
- ✅ Invalid credentials → 401 error
- ✅ Token expires after 24h
- ✅ All auth events logged

**Word Count**: 47/500 ✅
```

**Token Reduction**: 74% fewer words (179 → 47 words)

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
