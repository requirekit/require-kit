# Claude/Agentic Flow Installation System

## 📋 Two-Step Installation Process

This system uses a **two-step installation** approach:

1. **Global Installation** (once per machine) → `~/.claude/`
2. **Project Initialization** (per project) → `.claude/` in project

---

## 🌍 Step 1: Global Installation

Install the Claude/Agentic Flow methodology and tools globally to `~/.claude/`:

```bash
# From the installer directory
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer/installer

# Make scripts executable
chmod +x scripts/*.sh

# Run global installation
./scripts/install-global.sh
```

### What Gets Installed Where:

```
~/.claude/                          # Global installation directory
├── instructions/                   # Methodology documentation
│   └── core/
│       ├── 00-overview.md         # System overview
│       ├── ears-requirements.md   # EARS notation guide
│       ├── bdd-gherkin.md        # BDD/Gherkin patterns
│       ├── test-orchestration.md  # Testing strategies
│       └── 04-workflow.md         # Development workflow
├── templates/                      # Project templates
│   ├── default/                   # Default template
│   │   ├── CLAUDE.md             # Context file
│   │   ├── agents/               # AI agents (2 core agents)
│   │   └── templates/            # Document templates
│   ├── react/                    # React template with advanced patterns
│   │   ├── CLAUDE.md
│   │   ├── PATTERNS.md           # Production patterns
│   │   └── agents/               # AI agents
│   ├── python/                   # Python template with LangGraph
│   │   ├── CLAUDE.md             # Surgical coding philosophy
│   │   └── agents/               # AI agents
│   ├── dotnet-microservice/      # .NET microservice template
│   │   ├── CLAUDE.md             # FastEndpoints + Either monad
│   │   ├── agents/               # AI agents
│   │   └── templates/            # C# templates
│   └── maui/                     # .NET MAUI template
│       ├── CLAUDE.md             # MVVM + UseCases
│       ├── agents/               # AI agents
│       └── templates/            # MAUI templates
├── commands/                       # Claude command references
│   ├── gather-requirements.md
│   ├── formalize-ears.md
│   └── generate-bdd.md
├── scripts/                        # Utility scripts
│   └── claude-init                # Project init script
└── version                        # Version file

~/.config/claude/                   # Configuration directory
└── config.json                    # Global configuration

~/.local/bin/                       # User binaries
└── claude-init                    # Command to initialize projects
```

### After Installation:
- Restart your shell or run: `source ~/.bashrc` (or `~/.zshrc`)
- The `claude-init` command will be available globally

---

## 🚀 Step 2: Project Initialization

Initialize Claude/Agentic Flow in any project directory:

```bash
# Navigate to your project
cd ~/my-project

# Initialize with default template
claude-init

# Or choose a specific template
claude-init react               # React with TypeScript + advanced patterns
claude-init python              # Python with FastAPI + LangGraph
claude-init dotnet-microservice # .NET 8+ microservice with FastEndpoints
claude-init maui                # .NET MAUI mobile app with MVVM
claude-init fullstack           # React + Python
```

### What Gets Created in Your Project:

```
my-project/
├── .claude/                        # Project configuration
│   ├── CLAUDE.md                  # Project context for AI
│   ├── settings.json              # Project settings
│   ├── agents/                    # AI agent specifications
│   │   ├── requirements-analyst.md  # EARS requirements specialist
│   │   └── bdd-generator.md        # BDD/Gherkin converter
│   ├── commands/                  # Links to global commands
│   ├── hooks/                     # Automation hooks
│   ├── stacks/                    # Technology stack config
│   └── templates/                 # Project-specific templates
├── docs/
│   ├── requirements/              # EARS requirements
│   │   ├── draft/                # Work in progress
│   │   ├── approved/             # Approved requirements
│   │   └── implemented/          # Completed requirements
│   ├── bdd/
│   │   └── features/             # Gherkin feature files
│   ├── adr/                      # Architecture decisions
│   │   └── 0001-adopt-agentic-flow.md
│   └── state/
│       └── current-sprint.md     # Sprint tracking
├── tests/
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
└── src/                           # Source code (created if missing)
```

---

## 📊 Installation Flow Diagram

```
1. GLOBAL INSTALLATION (Once)
   installer/scripts/install-global.sh
   ↓
   Creates ~/.claude/ (methodology, templates, commands)
   ↓
   Adds 'claude-init' command to PATH

2. PROJECT INITIALIZATION (Per Project)
   claude-init [template]
   ↓
   Creates .claude/ in project
   ↓
   Links to global ~/.claude/ resources
   ↓
   Sets up project structure
```

---

## 🎯 Usage Examples

### Complete Setup Flow:

```bash
# Step 1: Install globally (one time)
cd /path/to/ai-engineer/installer
./scripts/install-global.sh

# Restart shell or source config
source ~/.bashrc

# Step 2: Initialize a project with your chosen stack

# For React project with advanced patterns:
mkdir my-react-app
cd my-react-app
claude-init react
npm install

# For Python API with LangGraph:
mkdir my-api
cd my-api
claude-init python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# For .NET Microservice:
mkdir my-service
cd my-service
claude-init dotnet-microservice
dotnet restore

# For .NET MAUI App:
mkdir my-app
cd my-app
claude-init maui
dotnet restore

# Step 3: Open in IDE with Claude
cursor .  # or code . or Visual Studio

# Step 4: Use Claude commands
# In Claude chat: /gather-requirements
```

### Initialize Existing Project:

```bash
# Navigate to existing project
cd ~/existing-project

# Initialize with appropriate template
claude-init python  # for Python project

# Project now has Claude/Agentic Flow structure
```

---

## 🔧 Alternative: Direct Script Usage

If you prefer not to install globally, you can run scripts directly:

```bash
# Run project initialization directly
cd ~/my-project
bash /path/to/installer/scripts/init-claude-project.sh [template]
```

---

## ❓ FAQ

### Q: Why two separate steps?
**A:** This separates concerns:
- **Global** = Shared methodology, templates, and tools (installed once)
- **Project** = Specific configuration and customization (per project)

### Q: What if I already have a .claude directory?
**A:** The initialization script will ask to backup existing configuration before reinitializing.

### Q: Can I use different templates for different projects?
**A:** Yes! Each project can use a different template:
- **react** - React with TypeScript, advanced patterns, SSE hooks
- **python** - Python with FastAPI, LangGraph, SSE streaming
- **dotnet-microservice** - .NET 8+ with FastEndpoints, Either monad
- **maui** - .NET MAUI with MVVM, UseCases, functional error handling
- **fullstack** - Combined React + Python
- **default** - Language-agnostic base configuration

### Q: Where are the Claude commands used?
**A:** In your IDE with Claude integration (VS Code with Claude extension, Cursor, etc.)

### Q: Can I customize the templates?
**A:** Yes, modify files in `~/.claude/templates/` to customize for all future projects.

---

## 🚨 Troubleshooting

### "claude-init: command not found"
```bash
# Add to PATH manually
export PATH="$HOME/.local/bin:$PATH"

# Or run installer again
./scripts/install-global.sh
```

### "Claude global installation not found"
```bash
# Check if installed
ls ~/.claude

# If not, run global installation
./scripts/install-global.sh
```

### Permission Denied
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

---

## 📝 Summary

1. **Run once**: `./scripts/install-global.sh` → Installs to `~/.claude/`
2. **Run per project**: `claude-init [template]` → Creates `.claude/` in project
3. **Use in IDE**: Open project and use `/gather-requirements` etc. in Claude

The system maintains clean separation between global methodology and project-specific configuration!
