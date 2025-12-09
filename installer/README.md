# AI-Engineer Installation System

A comprehensive two-tier installation architecture for the AI-Engineer software engineering lifecycle system, featuring AI agents, EARS requirements, BDD testing, and quality gates.

## 📋 Overview

AI-Engineer implements a sophisticated two-tier architecture:
- **Global Installation** (`~/.claude/`) - System-wide methodology, agents, templates, and tools
- **Project Installation** (`.claude/`) - Project-specific configuration with inherited agents

## 🚀 Quick Start

### Installation
```bash
# From the ai-engineer directory
cd installer
chmod +x scripts/install-global.sh
./scripts/install-global.sh

# Restart shell or source config
source ~/.bashrc  # or ~/.zshrc
```

### Initialize a Project
```bash
# Navigate to your project
cd my-project

# Initialize with a template
agentic-init maui                   # .NET MAUI mobile app
agentic-init react                  # React with TypeScript
agentic-init python                 # Python with FastAPI
agentic-init dotnet-microservice    # .NET microservice
agentic-init default                # Language-agnostic
```

## 🤖 AI Agents

RequireKit includes two specialized AI agents focused on requirements management:

### Core Agents
1. **requirements-analyst** - Gathers and formalizes requirements using EARS notation
2. **bdd-generator** - Converts EARS requirements to BDD/Gherkin scenarios

### Agent Files

The installer distributes both core and extended agent files:
- `bdd-generator.md` - Core BDD generation (always loaded)
- `bdd-generator-ext.md` - Extended examples (on-demand)
- `requirements-analyst.md` - Core EARS formalization (always loaded)
- `requirements-analyst-ext.md` - Extended gathering processes (on-demand)

### Using Agents in Claude
```markdown
# In your IDE with Claude:
@requirements-analyst help me gather requirements for a login feature
@bdd-generator convert REQ-001 to Gherkin scenarios
```

**Note**: For code review and test orchestration, use [GuardKit](https://github.com/guardkit/guardkit) which provides implementation agents.

## 📁 Installation Structure

### Global Installation (~/.claude/)
```
~/.claude/
├── templates/                      # Project templates
│   ├── default/
│   │   ├── CLAUDE.md              # Context file
│   │   ├── agents/                # AI agents (2 core)
│   │   │   ├── requirements-analyst.md
│   │   │   └── bdd-generator.md
│   │   └── templates/             # Document templates
│   ├── maui/                      # .NET MAUI template
│   │   ├── CLAUDE.md              # MVVM + UseCases context
│   │   ├── agents/                # Same 2 core agents
│   │   └── templates/             # MAUI-specific templates
│   ├── react/                     # React template
│   │   ├── CLAUDE.md              # React patterns
│   │   ├── agents/                # Same 2 core agents
│   │   └── PATTERNS.md            # Advanced patterns
│   ├── python/                    # Python template
│   │   ├── CLAUDE.md              # FastAPI + LangGraph
│   │   └── agents/                # Same 2 core agents
│   └── dotnet-microservice/       # .NET microservice
│       ├── CLAUDE.md              # FastEndpoints patterns
│       ├── agents/                # Same 2 core agents
│       └── templates/             # C# templates
├── instructions/                   # Core methodology
│   └── core/
│       ├── ears-requirements.md
│       ├── bdd-gherkin.md
│       └── test-orchestration.md
└── commands/                       # Claude commands
    ├── gather-requirements.md
    ├── formalize-ears.md
    └── generate-bdd.md
```

### Project Structure (.claude/)
```
project/.claude/
├── CLAUDE.md                      # Project context
├── settings.json                  # Configuration
├── agents/                        # AI agents (copied from template)
│   ├── requirements-analyst.md
│   └── bdd-generator.md
├── commands/                      # Command links
├── templates/                     # Project templates
└── hooks/                         # Automation scripts
```

## 🛠 Features

### EARS Requirements Engineering
Transform natural language into structured requirements:
- **Ubiquitous**: "The system shall..."
- **Event-driven**: "When [event], the system shall..."
- **State-driven**: "While [state], the system shall..."
- **Unwanted**: "If [error], then the system shall..."
- **Optional**: "Where [feature], the system shall..."

### BDD/Gherkin Generation
Automatic conversion from EARS to test scenarios:
```gherkin
Feature: User Authentication
  Scenario: Successful login
    Given a registered user
    When they submit valid credentials
    Then they should be authenticated
```

### Quality Gates
Automated enforcement of standards:
- Code coverage ≥ 80%
- Cyclomatic complexity < 10
- EARS compliance 100%
- BDD coverage ≥ 95%

## 📚 Stack Templates

### .NET MAUI (`maui`)
- MVVM architecture with ViewModels and UseCases
- Functional error handling with Either monad
- Outside-In TDD with integration tests
- LanguageExt for functional programming

### React (`react`)
- TypeScript with advanced patterns
- Error boundaries and SSE hooks
- Performance optimization patterns
- Playwright for E2E testing

### Python (`python`)
- FastAPI with async support
- LangGraph for workflow orchestration
- SSE streaming patterns
- Surgical coding philosophy

### .NET Microservice (`dotnet-microservice`)
- FastEndpoints with REPR pattern
- Either monad for error handling
- OpenTelemetry observability
- Domain-driven design

## 🔧 Extending the System

### Adding a New Agent
See [EXTENDING_THE_SYSTEM.md](EXTENDING_THE_SYSTEM.md) for detailed instructions:
1. Create agent in `.claude/agents/`
2. Copy to all templates
3. Reinstall global system

### Adding a New Template
1. Create template directory structure
2. Add CLAUDE.md context file
3. Copy base agents
4. Update init script
5. Reinstall

## 📋 Commands

### Claude Commands (In IDE)
```
/gather-requirements   # Start requirements gathering session
/formalize-ears       # Convert requirements to EARS notation
/generate-bdd         # Create BDD scenarios from EARS
/execute-tests        # Run tests with quality gates
/update-state         # Update sprint progress
```

### Using Agents
```markdown
# Direct agent interaction
@requirements-analyst what questions should I ask stakeholders?
@bdd-generator create scenarios for REQ-001
```

## 🔄 Updating

### After Adding Agents or Templates
```bash
cd installer
./scripts/install-global.sh
```

### Fixing Missing Agents
```bash
# Run the provided fix script
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer
chmod +x copy-agents.sh
./copy-agents.sh

# Reinstall
cd installer
./scripts/install-global.sh
```

## 🧪 Testing

### Verify Installation
```bash
# Check global installation
ls ~/.claude/templates/*/agents/

# Test project initialization
mkdir test-project
cd test-project
agentic-init maui
ls .claude/agents/  # Should show 2 agents
```

## 📖 Documentation

- [Installation Guide](INSTALLATION_GUIDE.md) - Detailed setup instructions
- [Extending the System](EXTENDING_THE_SYSTEM.md) - Add agents and templates
- [Migration Guide](MIGRATION_COMPLETE.md) - Upgrading from older versions

### Agent Documentation
- [Requirements Analyst](.claude/agents/requirements-analyst.md)
- [BDD Generator](.claude/agents/bdd-generator.md)

## 🗑 Uninstallation

```bash
# Remove global installation
rm -rf ~/.claude
rm -rf ~/.config/claude
rm ~/.local/bin/agentic-init

# Remove from PATH (edit shell config)
# Remove: export PATH="$HOME/.local/bin:$PATH"
```

## 🤝 Contributing

To contribute new agents or templates:
1. Follow guidelines in [EXTENDING_THE_SYSTEM.md](EXTENDING_THE_SYSTEM.md)
2. Test thoroughly
3. Document your additions
4. Submit PR with clear description

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

## 🆘 Troubleshooting

### Agents Not Appearing
```bash
# Check template has agents
ls ~/.claude/templates/[template]/agents/

# Verify init script
grep -n "agents" installer/scripts/init-claude-project.sh

# Reinstall
cd installer && ./scripts/install-global.sh
```

### Command Not Found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall
./scripts/install-global.sh
```

## 🎯 Next Steps

1. **Install AI-Engineer**: Run `./scripts/install-global.sh`
2. **Initialize Project**: Use `agentic-init [template]`
3. **Open in IDE**: Use VS Code with Claude or Cursor
4. **Start Development**: Begin with `/gather-requirements`
5. **Use Agents**: Interact with `@agent-name` in Claude

---

Built with ❤️ for AI-powered software engineering
