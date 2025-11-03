# Getting Started with require-kit

**Quick Start Guide** | **Version 1.0.0**

## Welcome to require-kit!

require-kit is a requirements management toolkit that helps you capture, formalize, and organize software requirements using proven methodologies. This guide will get you started in just a few minutes.

---

## Table of Contents

1. [Installation](#installation)
2. [Your First Requirements Session](#your-first-requirements-session)
3. [Understanding the Workflow](#understanding-the-workflow)
4. [Quick Examples](#quick-examples)
5. [Next Steps](#next-steps)

---

## Installation

### Prerequisites

- Claude Code or compatible Claude environment
- Git (for version control of requirements)

### Install require-kit

```bash
# Clone the repository
git clone https://github.com/requirekit/require-kit.git
cd require-kit

# Run the installer
chmod +x ./installer/scripts/install.sh
./installer/scripts/install.sh
```

### Verify Installation

```bash
# Check that commands are available
/gather-requirements --version
/formalize-ears --version
/generate-bdd --version

# All should respond with require-kit version info
```

### Project Initialization

```bash
# Initialize require-kit in your project
cd /path/to/your/project
/require-kit init

# Creates directory structure:
# docs/
# ├── epics/
# ├── features/
# ├── requirements/
# └── bdd/
```

---

## Your First Requirements Session

Let's capture requirements for a simple user login feature.

### Step 1: Gather Requirements (2 minutes)

```bash
/gather-requirements user-login
```

**The system will guide you through questions:**

```
Claude: Let's gather requirements for user-login. What problem are we solving?

You: Users need to securely log into our application with email and password.

Claude: Who will be using this feature?

You: Regular users and administrators.

Claude: What should happen on successful login?

You: Redirect to dashboard and create a session.

Claude: What should happen on failed login?

You: Show an error message.

Claude: Any performance requirements?

You: Login should complete in under 1 second.

Claude: Security requirements?

You: Passwords must be hashed. Use HTTPS only.

Claude: ✅ Requirements captured!

Output: docs/requirements/draft/user-login.md
```

### Step 2: Formalize with EARS (1 minute)

```bash
/formalize-ears
```

**Output:**
```
✅ Created 5 EARS requirements:

REQ-001: When a user submits valid credentials, the system shall
         authenticate and redirect to dashboard within 1 second.

REQ-002: If authentication fails, then the system shall display
         "Invalid email or password" message.

REQ-003: The system shall hash all passwords using bcrypt.

REQ-004: The system shall accept authentication requests only over HTTPS.

REQ-005: While a user session is active, the system shall validate
         the session token on each request.

Files: docs/requirements/REQ-001.md through REQ-005.md
```

### Step 3: Generate BDD Scenarios (1 minute)

```bash
/generate-bdd
```

**Output:**
```
✅ Generated BDD scenarios:

Feature: User Authentication
  Scenario: Successful login
  Scenario: Failed login
  Scenario: HTTPS enforcement
  Scenario: Session validation

File: docs/bdd/BDD-001-user-authentication.feature
```

### 🎉 Congratulations!

You've just created complete, testable requirements in under 5 minutes:
- ✅ 5 EARS-formatted requirements
- ✅ 4 BDD scenarios for testing
- ✅ Full traceability

---

## Understanding the Workflow

### The require-kit Process

```
┌─────────────────┐
│ 1. GATHER       │  Interactive Q&A
│  Requirements   │  /gather-requirements
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. FORMALIZE    │  Convert to EARS
│  with EARS      │  /formalize-ears
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. GENERATE     │  Create BDD scenarios
│  BDD Scenarios  │  /generate-bdd
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. ORGANIZE     │  Epic/Feature hierarchy
│  Hierarchy      │  /epic-create, /feature-create
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. EXPORT       │  PM tools or implementation
│  Integration    │  /feature-sync --jira
└─────────────────┘
```

### EARS Notation Patterns

require-kit uses five patterns for clear requirements:

1. **Ubiquitous**: `The system shall [behavior]`
   - Always applies, no conditions

2. **Event-Driven**: `When [trigger], the system shall [response]`
   - Triggered by specific events

3. **State-Driven**: `While [state], the system shall [behavior]`
   - Applies in certain states

4. **Unwanted Behavior**: `If [error], then the system shall [recovery]`
   - Error handling

5. **Optional Feature**: `Where [feature], the system shall [behavior]`
   - Optional/conditional features

---

## Quick Examples

### Example 1: Complete Feature Specification

```bash
# Gather requirements
/gather-requirements shopping-cart

# Answer questions about adding items, removing items, calculating totals

# Formalize to EARS
/formalize-ears
# Output: REQ-010 through REQ-015

# Generate BDD
/generate-bdd
# Output: BDD-002-shopping-cart.feature with scenarios

# Create epic and feature
/epic-create "E-Commerce Platform"
/feature-create "Shopping Cart" epic:EPIC-001 requirements:[REQ-010,REQ-011,REQ-012]

# View complete hierarchy
/hierarchy-view EPIC-001
```

### Example 2: Export to Jira

```bash
# After creating requirements and features
/feature-sync FEAT-001 --jira

# Creates Jira ticket with:
# - Feature description
# - Requirements as acceptance criteria
# - BDD scenarios for testing
# - Links to epic
```

### Example 3: Multiple Features in Epic

```bash
# Create epic
/epic-create "User Management"

# Create multiple features
/feature-create "Login" epic:EPIC-002
/feature-create "Registration" epic:EPIC-002
/feature-create "Password Reset" epic:EPIC-002

# For each feature:
/gather-requirements login
/formalize-ears
/generate-bdd
# Repeat for registration, password reset

# View complete epic
/hierarchy-view EPIC-002
```

---

## Next Steps

### Learn More

- **[require-kit User Guide](REQUIRE-KIT-USER-GUIDE.md)** - Comprehensive guide to all features
- **[Command Reference](COMMAND_USAGE_GUIDE.md)** - Complete command documentation
- **[Integration Guide](../INTEGRATION-GUIDE.md)** - Using with taskwright or PM tools

### Common Workflows

#### Workflow 1: Start New Project

```bash
# Initialize
/require-kit init

# Create project epic
/epic-create "My Application"

# For each major feature:
/gather-requirements feature-name
/formalize-ears
/generate-bdd
/feature-create "Feature Name" epic:EPIC-001
```

#### Workflow 2: Add Requirements to Existing Project

```bash
# Document existing functionality
/gather-requirements existing-feature

# Formalize what exists
/formalize-ears

# Create BDD for regression testing
/generate-bdd

# Organize into hierarchy
/epic-create "Existing System"
/feature-create "Existing Feature" epic:EPIC-001
```

#### Workflow 3: Requirements Review Cycle

```bash
# Draft requirements
/gather-requirements proposed-feature

# Formalize for review
/formalize-ears

# Share docs/requirements/ files with stakeholders

# Iterate based on feedback (edit files)

# Generate BDD scenarios for discussion
/generate-bdd

# Finalize and organize
/epic-create "Feature Area"
/feature-create "Proposed Feature" epic:EPIC-001
```

### Integration Options

#### Standalone Use
Use require-kit for requirements management, export to your preferred PM tool:

```bash
/feature-sync FEAT-001 --jira      # Export to Jira
/feature-sync FEAT-001 --linear    # Export to Linear
/feature-sync FEAT-001 --github    # Export to GitHub Projects
```

#### Full Integration with taskwright
For complete requirements-to-implementation workflow with quality gates:

```bash
# Install taskwright
cd /path/to/taskwright
./installer/scripts/install.sh

# Now use combined workflow:
/gather-requirements          # require-kit
/formalize-ears              # require-kit
/generate-bdd                # require-kit
/feature-generate-tasks FEAT-001  # require-kit generates task specs
/task-work TASK-001          # taskwright executes with context

# See Integration Guide for full details
```

### Best Practices

1. **Start with Questions**: Use `/gather-requirements` - don't skip the Q&A process
2. **Be Specific**: Include concrete numbers for performance, scalability
3. **Cover Error Cases**: What happens when things go wrong?
4. **Link Everything**: Maintain traceability Epic → Feature → Requirement → BDD
5. **Version Control**: Commit requirements files with your code

### Essential Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/gather-requirements` | Interactive Q&A | Start of every feature |
| `/formalize-ears` | Convert to EARS | After gathering |
| `/generate-bdd` | Create test scenarios | After formalizing |
| `/epic-create` | Create epic | Organizing features |
| `/feature-create` | Create feature | For each capability |
| `/hierarchy-view` | View structure | Check organization |

---

## Getting Help

### Documentation
- **[User Guide](REQUIRE-KIT-USER-GUIDE.md)** - Complete feature documentation
- **[Integration Guide](../INTEGRATION-GUIDE.md)** - Integration with taskwright
- **[README](../../README.md)** - Overview and quick reference

### Support
- **GitHub Issues**: [require-kit issues](https://github.com/requirekit/require-kit/issues)
- **Examples**: See `docs/requirements/`, `docs/bdd/` for example output

### Quick Tips

**Tip 1**: Requirements gathering takes 2-5 minutes per feature. Don't skip it - it saves hours later.

**Tip 2**: EARS patterns make requirements unambiguous. Choose the right pattern for each requirement.

**Tip 3**: BDD scenarios become your acceptance criteria and can drive automated testing.

**Tip 4**: Organize early. Create your epic structure before diving into features.

**Tip 5**: Use `--help` with any command for detailed usage: `/gather-requirements --help`

---

## What's Next?

Now that you've completed your first requirements session, you can:

1. **Explore Features**: Read the [User Guide](REQUIRE-KIT-USER-GUIDE.md) for advanced capabilities
2. **Practice**: Create requirements for a real feature in your project
3. **Export**: Try exporting to your PM tool with `/feature-sync`
4. **Integrate**: If you need task execution, explore [taskwright integration](../INTEGRATION-GUIDE.md)

---

## Quick Reference

### Installation
```bash
git clone https://github.com/requirekit/require-kit.git
cd require-kit && ./installer/scripts/install.sh
```

### Basic Workflow
```bash
/gather-requirements     # Interactive Q&A
/formalize-ears         # Convert to EARS
/generate-bdd           # Create scenarios
```

### Organization
```bash
/epic-create "Name"                    # Create epic
/feature-create "Name" epic:EPIC-XXX   # Create feature
/hierarchy-view EPIC-XXX               # View structure
```

### Export
```bash
/feature-sync FEAT-XXX --jira    # Export to Jira
/feature-sync FEAT-XXX --linear  # Export to Linear
```

---

**Ready to start?** Run `/gather-requirements` and begin capturing your first feature requirements!

For detailed documentation, see [REQUIRE-KIT-USER-GUIDE.md](REQUIRE-KIT-USER-GUIDE.md).
