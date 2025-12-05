# Agentic Flow Installation System - Updated

## 🚀 Quick Start

### Fresh Installation

```bash
# Navigate to installer directory
cd ~/Projects/appmilla_github/ai-engineer/installer

# Run the installer
chmod +x scripts/install.sh
./scripts/install.sh

# Restart your shell or source config
source ~/.zshrc  # or ~/.bashrc

# Initialize a project
cd ~/your-project
agentic-init dotnet-microservice
```

## 📁 What Gets Installed

The installer creates a complete `~/.agenticflow` structure (matching Product Owner's setup):

```
~/.agenticflow/
├── agents/                 # Global AI agents (2 core agents)
│   ├── requirements-analyst.md
│   └── bdd-generator.md
├── bin/                    # Executable commands
│   ├── agentic-init       # Primary initialization command
│   ├── agenticflow        # Main CLI
│   ├── af                 # Short alias for agenticflow
│   └── ai                 # Short alias for agentic-init
├── cache/                  # Cache directories
│   ├── responses/
│   ├── artifacts/
│   └── sessions/
├── commands/               # Claude command definitions
│   ├── gather-requirements.md
│   ├── formalize-ears.md
│   ├── generate-bdd.md
│   └── task-*.md
├── completions/            # Shell completions
│   └── agenticflow.bash
├── docs/                   # Documentation
│   └── PROJECT_STRUCTURE.md
├── instructions/           # Core methodology
│   └── core/
│       ├── 00-overview.md
│       ├── ears-requirements.md
│       ├── bdd-gherkin.md
│       ├── test-orchestration.md
│       └── 04-workflow.md
├── plugins/                # Plugin directory (for extensions)
├── scripts/                # Utility scripts
│   └── init-project.sh
├── templates/              # Project templates
│   ├── default/
│   ├── react/
│   ├── python/
│   ├── maui/
│   ├── dotnet-microservice/
│   └── fullstack/
└── versions/               # Version management
    ├── current            # Current version file
    ├── latest -> 1.0.0    # Symlink to latest
    └── 1.0.0/
        └── info.json      # Version info
```

## 🛠 Available Commands

After installation, you'll have these commands available:

| Command | Description | Example |
|---------|-------------|---------|
| `agentic-init` | Initialize a project with a template | `agentic-init dotnet-microservice` |
| `agenticflow init` | Alternative initialization syntax | `agenticflow init react` |
| `agenticflow doctor` | Check installation health | `agenticflow doctor` |
| `af` | Short alias for agenticflow | `af doctor` |
| `ai` | Short alias for agentic-init | `ai python` |

## 📋 Available Templates

- **default** - Language-agnostic template
- **react** - React with TypeScript, advanced patterns
- **python** - Python with FastAPI, LangGraph
- **maui** - .NET MAUI mobile app with MVVM
- **dotnet-microservice** - .NET microservice with FastEndpoints
- **fullstack** - Combined React + Python

## 🔄 Migration from Old Installation

The installer automatically backs up existing installations:
- `~/.claude` → `~/.claude.backup.[timestamp]`
- `~/.agentic-flow` → `~/.agentic-flow.backup.[timestamp]`
- `~/.agenticflow` → `~/.agenticflow.backup.[timestamp]`

## ✅ Verification

After installation, verify everything is working:

```bash
# Check installation health
agenticflow doctor

# This will show:
# - Installation directory status
# - All required directories
# - Number of agents installed
# - PATH configuration status

# List available templates
agentic-init --help
```

## 🎯 Project Initialization

When you run `agentic-init [template]` in a project:

1. **Auto-detects** existing project type (.NET, React, Python)
2. **Suggests** matching template or lets you override
3. **Creates** `.claude/` directory with:
   - Project context (CLAUDE.md)
   - AI agents (2 core agents: requirements-analyst, bdd-generator)
   - Commands (linked to global)
   - Templates (project-specific)
   - Configuration (settings.json)
4. **Creates** `docs/` structure for documentation
5. **Sets up** test directories (if appropriate)

## 🐛 Troubleshooting

### Command Not Found

If `agentic-init` is not found after installation:

```bash
# Add to PATH manually
export PATH="$HOME/.agenticflow/bin:$PATH"

# Make permanent by adding to ~/.zshrc or ~/.bashrc
echo 'export PATH="$HOME/.agenticflow/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Wrong Directory Structure

If you have old installations causing conflicts:

```bash
# Remove all old installations (after backing up)
rm -rf ~/.claude ~/.agentic-flow ~/.agenticflow

# Run fresh installation
cd ~/Projects/appmilla_github/ai-engineer/installer
./scripts/install.sh
```

### Missing Agents

The installer now properly installs 2 core agents. If missing:

```bash
# Check agent count
ls -la ~/.agenticflow/agents/

# Should show:
# - requirements-analyst.md
# - bdd-generator.md
```

**Note**: For code review and test orchestration agents, use [GuardKit](https://github.com/guardkit/guardkit).

## 📊 What's Fixed

This updated installer fixes:

1. ✅ **Consistent naming** - Uses `~/.agenticflow` throughout
2. ✅ **Complete directory structure** - All directories Product Owner has
3. ✅ **Proper commands** - `agentic-init` works correctly
4. ✅ **Global agents** - 2 core agents installed globally
5. ✅ **Version management** - Proper versions directory
6. ✅ **Cache setup** - Cache directories created
7. ✅ **Shell completions** - Bash completions installed
8. ✅ **PATH integration** - Automatic PATH configuration
9. ✅ **Template detection** - Smart project type detection
10. ✅ **Backup handling** - Automatic backup of existing installations

## 🚦 Quick Test

After installation, test with your .NET microservice:

```bash
# Create a test project
mkdir test-microservice
cd test-microservice

# Initialize with .NET microservice template
agentic-init dotnet-microservice

# Check what was created
ls -la .claude/
ls -la docs/

# Verify agents
ls .claude/agents/
```

You should see 2 agents (requirements-analyst.md, bdd-generator.md) and complete project structure ready for Claude Code!
