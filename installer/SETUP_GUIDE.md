# Agentic Flow Setup Guide

Complete setup instructions for the Agentic Flow two-tier installation system.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Post-Installation Setup](#post-installation-setup)
4. [Project Initialization](#project-initialization)
5. [Stack Configuration](#stack-configuration)
6. [IDE Integration](#ide-integration)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### Required Software
- **Operating System**: macOS, Linux, or WSL on Windows
- **Shell**: Bash or Zsh
- **Git**: Version 2.0 or higher
- **curl**: For downloading installation script

### Optional but Recommended
- **Node.js**: Version 18+ for React stack
- **Python**: Version 3.10+ for Python stack
- **.NET SDK**: Version 8.0+ for .NET stacks
- **Docker**: For containerized development
- **Claude Desktop**: For AI assistance
- **Visual Studio**: 2022+ for .NET development (or JetBrains Rider)

### System Requirements
- **Disk Space**: 100MB for global installation
- **Memory**: 512MB minimum
- **Internet**: Required for installation and updates

## Installation Methods

### Method 1: Quick Install (Recommended)
```bash
# One-line installation
curl -sSL https://raw.githubusercontent.com/appmilla/agentic-flow/main/installer/scripts/install.sh | bash
```

### Method 2: Manual Installation
```bash
# Step 1: Clone the repository
git clone https://github.com/appmilla/agentic-flow.git
cd agentic-flow

# Step 2: Make installer executable
chmod +x installer/scripts/install.sh

# Step 3: Run installer
./installer/scripts/install.sh

# Step 4: Source your shell configuration
source ~/.bashrc  # or ~/.zshrc for Zsh
```

### Method 3: Custom Installation
```bash
# Install to custom location
AGENTIC_FLOW_HOME=/opt/agentic-flow ./installer/scripts/install.sh

# Install specific version
AGENTIC_FLOW_VERSION=1.0.0 ./installer/scripts/install.sh

# Install with specific stack
./installer/scripts/install.sh --stack react
```

## Post-Installation Setup

### 1. Verify Installation
```bash
# Check installation
agenticflow doctor

# Expected output:
# ✓ Agentic Flow home: ~/.agentic-flow
# ✓ Global config found
# ✓ git: /usr/bin/git
# ✓ bash: /bin/bash
```

### 2. Configure Shell
The installer automatically adds Agentic Flow to your PATH. If it doesn't work:

#### For Bash
Add to `~/.bashrc`:
```bash
export PATH="$HOME/.agentic-flow/bin:$PATH"
export AGENTIC_FLOW_HOME="$HOME/.agentic-flow"

# Enable completions
if [ -f "$HOME/.agentic-flow/completions/agenticflow.bash" ]; then
    source "$HOME/.agentic-flow/completions/agenticflow.bash"
fi
```

#### For Zsh
Add to `~/.zshrc`:
```bash
export PATH="$HOME/.agentic-flow/bin:$PATH"
export AGENTIC_FLOW_HOME="$HOME/.agentic-flow"

# Enable completions
if [ -f "$HOME/.agentic-flow/completions/agenticflow.zsh" ]; then
    source "$HOME/.agentic-flow/completions/agenticflow.zsh"
fi
```

### 3. Configure Global Settings
Edit `~/.config/agentic-flow/config.json`:
```json
{
  "version": "1.0.0",
  "claude": {
    "model": "claude-3-sonnet",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "defaults": {
    "stack": "react",  // Your preferred default stack
    "testing": {
      "coverage_threshold": 85,
      "quality_gates": true
    }
  },
  "editor": {
    "command": "code",  // or "cursor", "vim", etc.
    "args": ["-n"]
  }
}
```

## Project Initialization

### Basic Initialization
```bash
# Navigate to your project
cd ~/projects/my-app

# Initialize with interactive setup
agenticflow init

# You'll be prompted for:
# - Project name
# - Technology stack
# - Testing preferences
# - Quality gate thresholds
```

### Stack-Specific Initialization

#### React Project
```bash
agenticflow init react

# This creates:
# - React-specific CLAUDE.md with advanced patterns
# - TypeScript configuration
# - Playwright test setup
# - Component templates with hooks and error boundaries
# - Performance optimization patterns
# - Accessibility compliance setup
```

#### Python Project
```bash
agenticflow init python

# This creates:
# - Python-specific CLAUDE.md with surgical coding philosophy
# - FastAPI setup with SSE streaming
# - pytest configuration with regression markers
# - LangGraph workflow templates
# - MCP server integration patterns
# - Factory pattern implementations
```

#### .NET Microservice Project
```bash
agenticflow init dotnet-microservice

# This creates:
# - .NET 8+ solution structure
# - FastEndpoints with REPR pattern
# - Either monad error handling setup
# - OpenTelemetry observability
# - xUnit test projects
# - Domain-driven design structure
# - Health check endpoints
```

#### .NET MAUI Project
```bash
agenticflow init maui

# This creates:
# - Cross-platform mobile app structure
# - MVVM with UseCase pattern
# - CommunityToolkit.Mvvm setup
# - Functional error handling with LanguageExt
# - Integration test fixtures
# - Cache-aside pattern implementation
# - Navigation service setup
```

#### Full Stack Project
```bash
agenticflow init fullstack

# This creates:
# - Combined React + Python setup
# - API integration templates
# - E2E test configuration
# - Docker compose setup
```

### Project Structure After Initialization
```
my-app/
├── .claude/
│   ├── config.json           # Project configuration
│   ├── CLAUDE.md            # AI context
│   ├── methodology/         # Inherited from global
│   ├── agents/              # AI agents
│   ├── commands/            # Available commands
│   └── templates/           # Project templates
├── docs/
│   ├── requirements/        # EARS requirements
│   ├── bdd/                # BDD scenarios
│   │   └── features/       # Gherkin files
│   ├── adr/                # Architecture decisions
│   └── state/              # Progress tracking
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
└── src/                    # Source code
```

## Stack Configuration

### Available Stacks
```bash
# List all available stacks
agenticflow stack list

# Available stacks:
# - react           React with TypeScript, Vite, and advanced patterns
# - python          Python with FastAPI, LangGraph, and SSE streaming
# - dotnet-microservice  .NET 8+ microservices with FastEndpoints
# - maui            .NET MAUI mobile apps with MVVM
# - fullstack       Combined React + Python
# - docker          Containerization support
# - kubernetes      K8s deployment configs
# - aws             AWS infrastructure templates

# Install additional stacks
agenticflow stack install docker
agenticflow stack install kubernetes

# Remove a stack
agenticflow stack remove docker
```

### Creating Custom Stacks
Create a new stack in `~/.agentic-flow/templates/my-stack/`:

1. Create stack directory:
```bash
mkdir -p ~/.agentic-flow/templates/my-stack
```

2. Add `description.txt`:
```
Custom stack for my specific needs
```

3. Add `CLAUDE.md`:
```markdown
# My Custom Stack Context

## Technologies
- [Your technologies]

## Standards
- [Your standards]
```

4. Add `config.json`:
```json
{
  "name": "my-stack",
  "extends": ["default"],
  "dependencies": {
    "required": ["tool1", "tool2"]
  }
}
```

## IDE Integration

### VS Code / Cursor
1. Install Claude extension
2. Open project with Agentic Flow:
```bash
code .  # or cursor .
```

3. Claude will automatically detect `.claude/` directory

### Using Commands in IDE
Once in your IDE with Claude:
```
/gather-requirements   # Start requirements session
/formalize-ears       # Convert to EARS
/generate-bdd         # Create test scenarios
/execute-tests        # Run with quality gates
/update-state         # Update progress
```

### Command Shortcuts
Create aliases in `.claude/config.json`:
```json
{
  "aliases": {
    "gr": "gather-requirements",
    "fe": "formalize-ears",
    "gb": "generate-bdd",
    "test": "execute-tests"
  }
}
```

## Troubleshooting

### Common Issues

#### Issue: Command not found
```bash
# Solution: Add to PATH
export PATH="$HOME/.agentic-flow/bin:$PATH"
source ~/.bashrc
```

#### Issue: Permission denied
```bash
# Solution: Fix permissions
chmod +x ~/.agentic-flow/bin/agenticflow
```

#### Issue: Existing installation conflict
```bash
# Solution: Backup and reinstall
mv ~/.agentic-flow ~/.agentic-flow.backup
curl -sSL https://install.agenticflow.ai | bash
```

#### Issue: Stack not loading
```bash
# Solution: Check configuration
agenticflow doctor
cat .claude/config.json  # Check extends path
```

### Debug Mode
Enable debug output:
```bash
export AGENTIC_FLOW_DEBUG=1
agenticflow init
```

### Logs
Check logs at:
- Installation: `/tmp/agenticflow-install.log`
- Runtime: `~/.agentic-flow/logs/`

## Advanced Configuration

### Environment Variables
```bash
# Override configuration via environment
export AGENTIC_FLOW_HOME=/custom/path
export AGENTIC_FLOW_STACK=python
export AGENTIC_FLOW_MODEL=claude-3-opus
```

### Project Inheritance
Projects can inherit from multiple templates:
```json
{
  "extends": [
    "~/.agentic-flow/templates/react",
    "~/.agentic-flow/templates/docker",
    "./custom-template"
  ]
}
```

### Custom Commands
Add custom commands to `.claude/commands/`:

1. Create command file:
```bash
touch .claude/commands/my-command.md
```

2. Define command:
```markdown
# My Custom Command

Execute my specific workflow.

## Usage
/my-command [arguments]

## Implementation
[Command logic here]
```

### Hooks and Automation
Create automation hooks in `.claude/hooks/`:

```bash
# .claude/hooks/pre-commit.sh
#!/bin/bash
# Run before each commit

# Check EARS compliance
agenticflow check-ears

# Run tests
agenticflow execute-tests

# Update state
agenticflow update-state
```

### CI/CD Integration
Add to your CI pipeline:

```yaml
# .github/workflows/agenticflow.yml
name: Agentic Flow CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Agentic Flow
        run: |
          curl -sSL https://install.agenticflow.ai | bash
          echo "$HOME/.agentic-flow/bin" >> $GITHUB_PATH
      
      - name: Validate Requirements
        run: agenticflow validate-ears
      
      - name: Run Quality Gates
        run: agenticflow execute-tests --ci
```

## Next Steps

1. **Initialize Your First Project**
   ```bash
   cd your-project
   agenticflow init
   ```

2. **Start Requirements Gathering**
   - Open project in IDE with Claude
   - Run `/gather-requirements`

3. **Follow the Workflow**
   - Gather → Formalize → Generate → Implement → Test

4. **Explore Advanced Features**
   - Custom stacks
   - Automation hooks
   - CI/CD integration

## Getting Help

- **Run diagnostics**: `agenticflow doctor`
- **Check version**: `agenticflow version`
- **View help**: `agenticflow help`
- **Documentation**: Visit the [full documentation](https://agenticflow.ai/docs)
- **Community**: Join our [Discord](https://discord.gg/agenticflow)

---

Happy coding with Agentic Flow! 🚀
