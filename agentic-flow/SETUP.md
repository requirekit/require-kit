# Agentecflow Setup Guide

This guide walks you through installing and configuring the Agentecflow system for AI-powered software engineering.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Post-Installation Setup](#post-installation-setup)
4. [Project Initialization](#project-initialization)
5. [Stack Configuration](#stack-configuration)
6. [Claude Integration](#claude-integration)
7. [Verification](#verification)

## System Requirements

### Minimum Requirements
- **OS**: macOS, Linux, or WSL on Windows
- **Shell**: Bash or Zsh
- **Git**: Version 2.0 or higher
- **Disk Space**: 50MB for global installation

### Recommended
- **Claude**: Claude Desktop or API access
- **Node.js**: For JavaScript/React projects
- **Python**: For Python projects
- **Docker**: For containerized workflows

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Download and run the installer
curl -sSL https://raw.githubusercontent.com/yourusername/agentic-flow/main/install.sh | bash

# Follow the prompts
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-flow.git
cd agentic-flow

# Run the installer
chmod +x install.sh
./install.sh

# Or manually copy files
cp -r global/* ~/.agentecflow/
chmod +x ~/.agentecflow/bin/agentic-flow
```

### Method 3: Development Installation

```bash
# Clone for development
git clone https://github.com/yourusername/agentic-flow.git
cd agentic-flow

# Create symlink for development
ln -s "$(pwd)/global" "$HOME/.agentecflow"
ln -s "$(pwd)/global/bin/agentic-flow" "/usr/local/bin/agentic-flow"
```

## Post-Installation Setup

### 1. Configure Shell

#### Bash
```bash
# Add to ~/.bashrc or ~/.bash_profile
echo 'export PATH="$HOME/.agentecflow/bin:$PATH"' >> ~/.bashrc
echo 'export AGENTECFLOW_HOME="$HOME/.agentecflow"' >> ~/.bashrc

# Reload shell
source ~/.bashrc
```

#### Zsh
```bash
# Add to ~/.zshrc
echo 'export PATH="$HOME/.agentecflow/bin:$PATH"' >> ~/.zshrc
echo 'export AGENTECFLOW_HOME="$HOME/.agentecflow"' >> ~/.zshrc

# Reload shell
source ~/.zshrc
```

### 2. Verify Installation

```bash
# Check installation
agentic-flow --version

# Run system check
agentic-flow doctor

# Expected output:
# ✓ Installation directory exists
# ✓ agentic-flow is in PATH
# ✓ Global configuration found
# ✓ All checks passed! System is healthy.
```

### 3. Configure Global Settings

Edit `~/.agentecflow/config.json`:

```json
{
  "version": "1.0.0",
  "claude": {
    "model": "claude-3-sonnet",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "defaults": {
    "testCoverage": 80,
    "earsCompliance": 100,
    "bddCoverage": 95
  },
  "user": {
    "name": "Your Name",
    "email": "your.email@example.com"
  }
}
```

## Project Initialization

### Basic Initialization

```bash
# Navigate to your project
cd /path/to/your-project

# Initialize with auto-detection
agentic-flow init

# Project type will be detected automatically:
# - package.json → JavaScript/React
# - requirements.txt → Python
# - go.mod → Go
# - Cargo.toml → Rust
```

### Stack-Specific Initialization

```bash
# Initialize with specific stack
agentic-flow init react    # React/TypeScript project
agentic-flow init python   # Python project
agentic-flow init go       # Go project
```

### What Gets Created

```
your-project/
├── .claude/                    # Claude configuration
│   ├── config.json            # Project config
│   ├── CLAUDE.md              # Project context
│   └── context/               # Additional context
├── docs/
│   ├── requirements/          # EARS requirements
│   ├── bdd/                   # BDD scenarios
│   │   └── features/
│   ├── adr/                   # Architecture decisions
│   └── state/                 # Progress tracking
└── tests/                     # Test structure
    ├── unit/
    ├── integration/
    └── e2e/
```

## Stack Configuration

### Install Additional Stacks

```bash
# List available stacks
agentic-flow stack list

# Output:
# Available stacks:
# - default
# - react
# - python
# - typescript
# - go
# - docker

# Install a stack
agentic-flow stack install python
agentic-flow stack install docker
```

### Configure Stack for Project

Edit `.claude/config.json`:

```json
{
  "extends": ["~/.agentecflow/config.json"],
  "project": {
    "stack": "react",
    "stacks": ["react", "docker"]  // Multiple stacks
  },
  "testing": {
    "framework": "vitest",
    "e2e": "playwright"
  }
}
```

### Create Custom Stack

1. Create stack directory:
```bash
mkdir -p ~/.agentecflow/instructions/stacks/my-stack
```

2. Add stack instructions:
```bash
# Create methodology files
vim ~/.agentecflow/instructions/stacks/my-stack/testing.md
vim ~/.agentecflow/instructions/stacks/my-stack/deployment.md
```

3. Create stack template:
```bash
mkdir -p ~/.agentecflow/templates/my-stack
vim ~/.agentecflow/templates/my-stack/template.json
```

## Claude Integration

### Using Claude Desktop

1. Open Claude Desktop
2. Navigate to your project directory
3. Claude will automatically detect `.claude/` configuration
4. Use slash commands:
   - `/gather-requirements`
   - `/formalize-ears`
   - `/generate-bdd`

### Claude Configuration

The `.claude/CLAUDE.md` file provides context:

```markdown
# Project Context for Claude

## Available Commands
- `/gather-requirements` - Start requirements session
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Create BDD scenarios
- `/execute-tests` - Run tests
- `/update-state` - Update progress

## Project Structure
[Project-specific information]

## Current Sprint
[Sprint goals and progress]
```

### Custom Commands

Add project-specific commands in `.claude/commands/`:

```bash
# Create custom command
cat > .claude/commands/deploy.md << 'EOF'
# Deploy Command

Deploy the application to production.

## Steps
1. Run tests
2. Build application
3. Deploy to cloud
4. Verify deployment
EOF
```

## Verification

### Complete Setup Checklist

```bash
# Run comprehensive check
agentic-flow doctor

# Manual verification
echo "Checking installation..."

# 1. Binary accessible
which agentic-flow

# 2. Environment variables set
echo $AGENTECFLOW_HOME

# 3. Configuration exists
ls -la ~/.agentecflow/config.json

# 4. Instructions installed
ls ~/.agentecflow/instructions/core/

# 5. Templates available
ls ~/.agentecflow/templates/

# 6. In project, check initialization
ls -la .claude/
```

### Test Project Setup

```bash
# Create test project
mkdir test-project
cd test-project

# Initialize
agentic-flow init

# Check created structure
tree -L 2

# Verify in Claude
echo "Open Claude and test /gather-requirements command"
```

### Troubleshooting Common Issues

#### Issue: Command not found
```bash
# Fix: Add to PATH
export PATH="$HOME/.agentecflow/bin:$PATH"
# Add to shell config file permanently
```

#### Issue: Permission denied
```bash
# Fix: Make executable
chmod +x ~/.agentecflow/bin/agentic-flow
```

#### Issue: Stack not found
```bash
# Fix: Install the stack
agentic-flow stack install [stack-name]
```

#### Issue: Claude commands not working
```bash
# Fix: Ensure in project directory
pwd  # Should show project with .claude/
ls .claude/  # Should exist
```

## Next Steps

1. **Create your first requirement**:
   ```bash
   # In Claude
   /gather-requirements
   ```

2. **Formalize to EARS**:
   ```bash
   # In Claude
   /formalize-ears
   ```

3. **Generate BDD scenarios**:
   ```bash
   # In Claude
   /generate-bdd
   ```

4. **Start implementation** with TDD approach

5. **Track progress**:
   ```bash
   # View current state
   cat docs/state/current-sprint.md
   ```

## Getting Help

- **Documentation**: Check `~/.agentecflow/instructions/core/`
- **System Check**: Run `agentic-flow doctor`
- **Version Info**: Run `agentic-flow --version`
- **GitHub Issues**: Report bugs and request features
- **Community**: Join our Discord server

## Updating Agentecflow

```bash
# Check for updates
agentic-flow update

# Manual update
cd ~/.agentecflow
git pull origin main

# Verify update
agentic-flow --version
```

---

Congratulations! You've successfully set up Agentecflow. Start building with AI-powered engineering!
