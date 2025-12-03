# Extending the AI-Engineer System

This guide explains how to add new agents and templates to the AI-Engineer global installation system.

## Table of Contents
- [System Architecture Overview](#system-architecture-overview)
- [Adding a New Agent](#adding-a-new-agent)
- [Adding a New Template](#adding-a-new-template)
- [Testing Your Extensions](#testing-your-extensions)
- [Best Practices](#best-practices)

## System Architecture Overview

The AI-Engineer system uses a two-tier architecture:

```
~/.claude/                          # Global installation
├── templates/                      # Project templates
│   ├── default/                   # Base template
│   │   ├── CLAUDE.md             # Project context
│   │   ├── agents/               # AI agents (copied to projects)
│   │   └── templates/            # File templates
│   ├── maui/                     # .NET MAUI template
│   ├── react/                    # React template
│   ├── python/                   # Python template
│   └── dotnet-microservice/      # .NET microservice template
├── instructions/                   # Global methodology docs
└── commands/                       # Global commands

project/.claude/                    # Project installation
├── agents/                        # Copied from template
├── commands/                      # Linked to global
├── templates/                     # Copied from template
└── settings.json                  # Project configuration
```

## Adding a New Agent

Agents are specialized AI assistants that help with specific aspects of the development lifecycle.

### Step 1: Create the Agent File

Create a new markdown file in the base agents directory:

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/.claude/agents/
```

Create your agent file (e.g., `performance-optimizer.md`):

```markdown
---
name: performance-optimizer
description: Specialist in identifying and fixing performance bottlenecks
model: sonnet
tools: Read, Write, Search, Grep, Bash
---

You are a performance optimization specialist focused on improving application speed and resource usage.

## Your Primary Responsibilities

1. **Performance Analysis**: Identify bottlenecks and inefficiencies
2. **Optimization Strategies**: Recommend and implement improvements
3. **Metrics Collection**: Measure and track performance gains
4. **Best Practices**: Ensure code follows performance best practices

## Analysis Areas

### Frontend Performance
- Bundle size optimization
- Lazy loading strategies
- Render performance
- Network request optimization
- Caching strategies

### Backend Performance
- Database query optimization
- API response times
- Memory usage patterns
- Concurrency handling
- Resource pooling

### Infrastructure
- Container optimization
- Scaling strategies
- CDN configuration
- Load balancing
- Resource allocation

## Performance Metrics

Track these key metrics:
- **Time to First Byte (TTFB)**: < 200ms
- **First Contentful Paint (FCP)**: < 1.8s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Cumulative Layout Shift (CLS)**: < 0.1
- **First Input Delay (FID)**: < 100ms

## Optimization Techniques

### Code Level
```javascript
// ❌ Inefficient
for (let i = 0; i < items.length; i++) {
  document.getElementById('list').innerHTML += '<li>' + items[i] + '</li>';
}

// ✅ Optimized
const fragment = document.createDocumentFragment();
items.forEach(item => {
  const li = document.createElement('li');
  li.textContent = item;
  fragment.appendChild(li);
});
document.getElementById('list').appendChild(fragment);
```

### Database Level
```sql
-- ❌ N+1 Query Problem
SELECT * FROM users;
-- Then for each user:
SELECT * FROM posts WHERE user_id = ?;

-- ✅ Optimized with JOIN
SELECT u.*, p.*
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;
```

## Your Working Process

1. **Measure First**: Establish baseline metrics
2. **Identify Bottlenecks**: Use profiling tools
3. **Prioritize Issues**: Focus on high-impact areas
4. **Implement Solutions**: Apply optimizations
5. **Verify Improvements**: Measure again
6. **Document Changes**: Record what was done and why

Remember: Premature optimization is the root of all evil. Measure first, optimize what matters.
```

### Step 2: Determine Agent Scope and Add to Templates

**IMPORTANT**: Before copying your agent, determine if it's **global** or **stack-specific**:

#### Global Agents (Language-Agnostic)
Agents that work with ANY technology stack should be added to **ALL templates**.

**Examples of Global Agents**:
- `requirements-analyst` - EARS requirements work with any language
- `bdd-generator` - BDD/Gherkin works with any language
- `performance-optimizer` - Performance analysis works across stacks

**Note**: For implementation-focused agents like `architectural-reviewer`, `code-reviewer`, and `test-orchestrator`, see [GuardKit](https://github.com/guardkit-dev/guardkit).

**When to make an agent global**:
- ✅ Functionality is language/framework-agnostic
- ✅ Applies to all project types
- ✅ No stack-specific knowledge required

**How to add global agent**:
```bash
# Copy to ALL templates
for template in default maui react python dotnet-microservice typescript-api fullstack; do
  cp performance-optimizer.md \
    /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/$template/agents/
done
```

#### Stack-Specific Agents (Technology-Specific)
Agents that only work with ONE technology stack should be added to **THAT TEMPLATE ONLY**.

**Examples of Stack-Specific Agents**:
- `python-api-specialist` → Python template only (FastAPI expertise)
- `python-langchain-specialist` → Python template only (LangChain/LangGraph)
- `python-mcp-specialist` → Python template only (Python MCP servers)
- `react-state-specialist` → React template only (React state management)
- `maui-viewmodel-specialist` → MAUI template only (C# MVVM patterns)

**When to make an agent stack-specific**:
- ✅ Uses language-specific libraries (e.g., Python `mcp` package)
- ✅ Framework-specific patterns (e.g., React hooks, MAUI MVVM)
- ✅ Only relevant to one technology stack
- ✅ Requires stack-specific expertise

**How to add stack-specific agent**:
```bash
# Copy to SPECIFIC template only
# Example: Adding a Python-specific agent
cp my-python-agent.md \
  /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/python/agents/

# Example: Adding a React-specific agent
cp my-react-agent.md \
  /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/react/agents/

# Example: Adding a MAUI-specific agent
cp my-maui-agent.md \
  /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/maui/agents/
```

#### Decision Tree

Ask yourself: **"Does this agent's expertise apply to ALL stacks, or just ONE stack?"**

```
Does the agent work with any language/framework?
│
├─ YES → Global Agent
│         └─ Copy to ALL templates
│
└─ NO → Stack-Specific Agent
         └─ Copy to SPECIFIC template only
```

**Common Mistake to Avoid**:
❌ Don't copy stack-specific agents (like `python-mcp-specialist`) to all templates
✅ Only copy them to the relevant template (like `python` template)

This keeps agent lists clean and relevant for each project type.

### Step 3: Update Documentation

Add your agent to the main documentation in `.claude/CLAUDE.md`:

```markdown
## Available Agents

- **requirements-analyst**: Gathers and formalizes requirements using EARS
- **bdd-generator**: Converts EARS to BDD/Gherkin scenarios
- **performance-optimizer**: [NEW] Identifies and fixes performance bottlenecks

**Note**: For implementation agents (`code-reviewer`, `test-orchestrator`), use [GuardKit](https://github.com/guardkit-dev/guardkit).
```

### Step 4: Create a Command (Optional)

If your agent needs a specific command, create one in `installer/global/commands/`:

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/commands/
```

Create `optimize-performance.md`:

```markdown
Analyze and optimize performance issues in the current project.

## Usage
Use this command when you need to improve application performance.

## Process
1. Run performance profiling
2. Identify bottlenecks
3. Suggest optimizations
4. Implement approved changes
5. Verify improvements

## Example
```
/optimize-performance --area=frontend --metric=bundle-size
```
```

## Adding a New Template

Templates provide stack-specific configurations and resources for different project types.

### Step 1: Create Template Directory Structure

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/
mkdir -p my-template/{agents,templates}
```

### Step 2: Create CLAUDE.md Context File

Create `my-template/CLAUDE.md` with stack-specific context:

```markdown
# My Template Project Context

You are working on a [template type] project using the AI-Engineer methodology.

## Technology Stack
- **Language**: [Primary language]
- **Framework**: [Main framework]
- **Testing**: [Test framework]
- **Build**: [Build tool]

## Project Structure
```
project/
├── src/               # Source code
├── tests/            # Test files
├── docs/             # Documentation
└── .claude/          # AI-Engineer configuration
```

## Development Workflow
1. Gather requirements using `/gather-requirements`
2. Formalize with EARS using `/formalize-ears`
3. Generate BDD scenarios using `/generate-bdd`
4. Implement with TDD
5. Run tests using `/execute-tests`

## Best Practices
- [Stack-specific best practices]
- [Coding standards]
- [Testing requirements]

## Common Patterns
[Include common code patterns for this stack]
```

### Step 3: Copy Base Agents

Copy the standard agents to your template:

```bash
cp /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/default/agents/*.md \
   /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer/global/templates/my-template/agents/
```

### Step 4: Add Template-Specific Files

Add any template-specific files to `my-template/templates/`:

```bash
cd my-template/templates/
```

For example, create configuration templates, boilerplate code, etc.

### Step 5: Update Installation Script

Edit `/installer/scripts/init-claude-project.sh` to add your template to the stack-specific configuration section:

```bash
# Find the create_stack_files() function and add:
my-template)
    print_info "Adding My Template-specific configuration..."
    cat > .claude/stacks/my-template.json << 'EOF'
{
  "name": "my-template",
  "testing": "my-test-framework",
  "framework": "my-framework",
  "language": "my-language"
}
EOF
    ;;
```

### Step 6: Update Template Detection

Edit `/installer/scripts/install-global.sh` to include your template in the detection:

```bash
# Find the section that lists templates and add your template
echo "  • my-template - Description of your template"
```

### Step 7: Create Template-Specific Documentation

Create a README in your template directory:

```markdown
# My Template

## Overview
Description of what this template provides.

## Technology Stack
- Language: [Language]
- Framework: [Framework]
- Testing: [Test Framework]

## Getting Started
1. Initialize project: `agentic-init my-template`
2. Install dependencies: `[package manager] install`
3. Run tests: `[test command]`

## Project Structure
```
.
├── src/              # Application source
├── tests/           # Test files
└── .claude/         # AI-Engineer config
```

## Available Commands
- `/gather-requirements` - Start requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Create test scenarios
- `/execute-tests` - Run test suite

## Best Practices
[Template-specific best practices]
```

## Testing Your Extensions

### Testing a New Agent

1. **Unit Test**: Create a test project and verify the agent is copied:
```bash
mkdir ~/test-agent-project
cd ~/test-agent-project
agentic-init default
ls .claude/agents/  # Should show your new agent
```

2. **Integration Test**: Test the agent's functionality in Claude:
```markdown
# In Claude, reference your agent
@performance-optimizer analyze the current codebase for bottlenecks
```

### Testing a New Template

1. **Installation Test**:
```bash
# Reinstall global system
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer
./scripts/install-global.sh

# Verify template appears in list
agentic-init --list  # Should show your template
```

2. **Initialization Test**:
```bash
mkdir ~/test-my-template
cd ~/test-my-template
agentic-init my-template

# Verify structure
ls -la .claude/
ls -la .claude/agents/
cat .claude/CLAUDE.md
```

3. **Command Test**: Test that all commands work in the new template

## Best Practices

### For Agents

1. **Single Responsibility**: Each agent should focus on one area
2. **Clear Documentation**: Include examples and anti-patterns
3. **Tool Requirements**: Specify which tools the agent needs
4. **Output Formats**: Define clear output structures
5. **Quality Criteria**: Include measurable success metrics

### For Templates

1. **Minimal Boilerplate**: Only include essential files
2. **Clear Documentation**: Explain the stack and patterns
3. **Working Examples**: Include sample code that works
4. **Test Coverage**: Provide test examples
5. **Integration Ready**: Ensure all base commands work

### Naming Conventions

- **Global Agents**: Use kebab-case (e.g., `performance-optimizer.md`, `requirements-analyst.md`, `bdd-generator.md`)
- **Stack-Specific Agents**: Use `{stack}-{specialization}.md` pattern
  - Python: `python-api-specialist.md`, `python-mcp-specialist.md`
  - React: `react-state-specialist.md`, `react-testing-specialist.md`
  - MAUI: `maui-viewmodel-specialist.md`, `maui-ui-specialist.md`
  - .NET: `dotnet-api-specialist.md`, `dotnet-domain-specialist.md`
- **Templates**: Use kebab-case (e.g., `my-template`, `python`, `react`)
- **Commands**: Use kebab-case (e.g., `optimize-performance.md`, `gather-requirements.md`)

**Naming Pattern Rationale**:
The `{stack}-` prefix makes it immediately clear which agents are stack-specific and prevents accidentally copying them to wrong templates.

**Recent Example - bdd-generator**:
- ✅ Global agent (BDD/Gherkin applies to all stacks)
- ✅ Added to ALL templates
- ✅ Integrated into generate-bdd command for all stacks
- ✅ Language-agnostic BDD scenario generation capability

**Note**: Implementation agents like `architectural-reviewer` are provided by [GuardKit](https://github.com/guardkit-dev/guardkit).

### Version Control

When adding new agents or templates:

1. Test locally first
2. Document the addition
3. Update this guide if needed
4. Commit with clear message:
   ```bash
   git add .
   git commit -m "feat: add performance-optimizer agent for performance analysis"
   ```

## Troubleshooting

### Agent Not Appearing in Projects

1. Check agent exists in template:
```bash
ls ~/.claude/templates/[template]/agents/
```

2. Verify init script has agent copying:
```bash
grep -n "agents" installer/scripts/init-claude-project.sh
```

3. Reinstall global system:
```bash
cd installer && ./scripts/install-global.sh
```

### Template Not Listed

1. Verify template directory exists:
```bash
ls ~/.claude/templates/
```

2. Check template has required files:
```bash
ls ~/.claude/templates/my-template/
# Should have: CLAUDE.md, agents/, templates/
```

3. Update installation script detection

## Quick Reference

### Add New Global Agent (Language-Agnostic)
```bash
# 1. Create agent
vim installer/global/agents/new-global-agent.md

# 2. Copy to ALL templates (because it's global)
for t in default maui react python dotnet-microservice typescript-api fullstack; do
  cp installer/global/agents/new-global-agent.md installer/global/templates/$t/agents/
done

# 3. Reinstall
cd installer && ./scripts/install-global.sh
```

### Add New Stack-Specific Agent
```bash
# 1. Create agent
vim installer/global/agents/python-specific-agent.md

# 2. Copy to SPECIFIC template ONLY (not all templates)
cp installer/global/agents/python-specific-agent.md \
   installer/global/templates/python/agents/

# 3. Reinstall
cd installer && ./scripts/install-global.sh
```

### Decision: Global vs Stack-Specific?
```bash
# Ask: Does this agent work with ANY language/framework?
#
# YES → Global agent
#       Copy to ALL templates (default, maui, react, python, etc.)
#
# NO  → Stack-specific agent
#       Copy to SPECIFIC template only (e.g., python/ only)
```

### Add New Template Commands
```bash
# 1. Create template structure
mkdir -p installer/global/templates/new-template/{agents,templates}

# 2. Add CLAUDE.md
vim installer/global/templates/new-template/CLAUDE.md

# 3. Copy base agents
cp installer/global/templates/default/agents/*.md \
   installer/global/templates/new-template/agents/

# 4. Update init script
vim installer/scripts/init-claude-project.sh

# 5. Reinstall
cd installer && ./scripts/install-global.sh
```

## Support

For issues or questions about extending the system:
1. Check this documentation
2. Review existing agents/templates for examples
3. Test in isolation first
4. Document your additions
