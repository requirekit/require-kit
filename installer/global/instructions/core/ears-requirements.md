# EARS Requirements Engineering

EARS (Easy Approach to Requirements Syntax) is a structured natural language format for writing clear, unambiguous requirements.

## The Five EARS Patterns

### 1. Ubiquitous Requirements
**Pattern**: The [system] shall [function]
**When to use**: For requirements that always apply
**Example**: The system shall maintain an audit log of all transactions

### 2. Event-Driven Requirements  
**Pattern**: When [trigger], the [system] shall [response]
**When to use**: For requirements triggered by specific events
**Example**: When a user submits a form, the system shall validate all required fields

### 3. State-Driven Requirements
**Pattern**: While [in a specific state], the [system] shall [behavior]  
**When to use**: For requirements that apply during certain states
**Example**: While in maintenance mode, the system shall display a maintenance message

### 4. Unwanted Behavior Requirements
**Pattern**: If [unwanted situation], then the [system] shall [response]
**When to use**: For handling errors or exceptional conditions
**Example**: If the database connection fails, then the system shall retry 3 times

### 5. Optional Feature Requirements
**Pattern**: Where [feature is included], the [system] shall [capability]
**When to use**: For optional or configurable features
**Example**: Where two-factor authentication is enabled, the system shall require a second factor

## Writing Good EARS Requirements

### Characteristics of Good Requirements
- **Atomic**: Each requirement describes one capability
- **Testable**: Can be verified through testing
- **Traceable**: Can be linked to design and tests
- **Unambiguous**: Only one interpretation possible
- **Complete**: Contains all necessary information

### Common Pitfalls to Avoid
- Combining multiple requirements in one statement
- Using vague terms like "user-friendly" or "fast"
- Missing trigger conditions or system responses
- Unclear scope boundaries

## Converting Natural Language to EARS

### Step 1: Identify the Core Behavior
What does the system need to do?

### Step 2: Determine the Pattern
- Always happens → Ubiquitous
- Triggered by event → Event-driven
- During a state → State-driven
- Error handling → Unwanted behavior
- Optional → Optional feature

### Step 3: Apply the Template
Use the appropriate pattern template

### Step 4: Validate
- Is it testable?
- Is it unambiguous?
- Is it complete?

## Examples by Domain

### Authentication
- **Ubiquitous**: The system shall encrypt all stored passwords
- **Event-driven**: When a user logs in, the system shall verify credentials
- **State-driven**: While a session is active, the system shall maintain user context
- **Unwanted**: If login fails 3 times, then the system shall lock the account
- **Optional**: Where biometric login is configured, the system shall accept fingerprints

### API Development
- **Ubiquitous**: The API shall return JSON responses
- **Event-driven**: When an API request is received, the system shall validate the API key
- **State-driven**: While rate limited, the API shall return 429 status
- **Unwanted**: If an endpoint doesn't exist, then the API shall return 404
- **Optional**: Where caching is enabled, the API shall return cached responses
