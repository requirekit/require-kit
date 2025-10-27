# Agentecflow - AI-Powered Software Engineering Lifecycle

A two-tier installation system that provides global methodology and project-specific implementation for AI-assisted development using Claude.

## 🚀 Quick Start

### Global Installation (One-time)

```bash
# Download and run installer
curl -sSL https://raw.githubusercontent.com/yourusername/agentic-flow/main/install.sh | bash

# Or clone and install locally
git clone https://github.com/yourusername/agentic-flow.git
cd agentic-flow
./install.sh
```

### Project Initialization (Per project)

```bash
# Navigate to your project
cd your-project

# Initialize Agentecflow
agentic-flow init

# Or with a specific stack
agentic-flow init react
agentic-flow init python
```

## 📁 Two-Tier Architecture

### Global Installation (`~/.agentecflow/`)
Contains methodology, instructions, and templates shared across all projects:

```
~/.agentecflow/
├── bin/                    # agentic-flow executable
├── instructions/           # Core methodology
│   ├── core/              # EARS, BDD, requirements guides
│   └── stacks/            # Technology-specific instructions
├── templates/             # Project templates
│   ├── default/
│   ├── react/
│   └── python/
├── commands/              # Global Claude commands
└── config.json           # Global configuration
```

### Project Installation (`.claude/`)
Lightweight project-specific configuration:

```
project/.claude/
├── config.json           # Project configuration
├── context/             # Project-specific context
├── overrides/           # Override global instructions
└── CLAUDE.md           # Project context for Claude
```

## 🎯 Core Features

### EARS Requirements Notation
- Five patterns for clear, testable requirements
- Automatic validation and formatting
- Traceable from requirements to tests

### BDD/Gherkin Generation
- Convert EARS requirements to test scenarios
- Executable specifications
- Complete test coverage

### Quality Gates
- Automated test execution
- Coverage thresholds
- Complexity metrics
- Compliance checking

### Stack Support
- React/TypeScript
- Python/FastAPI
- Go
- Rust
- Extensible to any technology

## 🔧 Commands

### CLI Commands
```bash
agentic-flow init [template]    # Initialize project
agentic-flow stack list         # List available stacks
agentic-flow stack install      # Install a stack
agentic-flow update            # Update Agentecflow
agentic-flow doctor            # Check system health
```

### Claude Commands (in project)
```
/gather-requirements    # Start requirements session
/formalize-ears        # Convert to EARS notation
/generate-bdd          # Create BDD scenarios
/execute-tests         # Run tests with gates
/update-state          # Update progress tracking
```

## 🏗️ Workflow

1. **Gather Requirements**
   - Interactive Q&A sessions
   - Document natural language requirements
   - Define acceptance criteria

2. **Formalize with EARS**
   - Convert to structured notation
   - Ensure testability
   - Add measurements and thresholds

3. **Generate BDD Scenarios**
   - Create Gherkin specifications
   - Cover all test cases
   - Link to requirements

4. **Implementation**
   - Test-driven development
   - Quality gates enforcement
   - Progress tracking

5. **Verification**
   - Automated test execution
   - Coverage reporting
   - State updates

## 🔌 Stack Installation

### Install Additional Stacks
```bash
# List available stacks
agentic-flow stack list

# Install a stack
agentic-flow stack install react
agentic-flow stack install python
agentic-flow stack install docker
```

### Create Custom Stack
1. Create stack directory in `~/.agentecflow/instructions/stacks/`
2. Add stack-specific instructions and templates
3. Register in configuration

## ⚙️ Configuration

### Global Configuration (`~/.agentecflow/config.json`)
```json
{
  "version": "1.0.0",
  "claude": {
    "model": "claude-3-sonnet",
    "temperature": 0.7
  },
  "defaults": {
    "testCoverage": 80,
    "earsCompliance": 100
  }
}
```

### Project Configuration (`.claude/config.json`)
```json
{
  "extends": ["~/.agentecflow/config.json"],
  "project": {
    "name": "my-project",
    "type": "react",
    "stack": "react"
  }
}
```

### Configuration Cascade
1. Command-line flags (highest priority)
2. Environment variables
3. Project configuration
4. User configuration
5. System defaults (lowest priority)

## 🔄 Updates

### Update Global Installation
```bash
# Check for updates
agentic-flow update

# Manual update
cd ~/.agentecflow
git pull origin main
```

### Preserve Project Customizations
- Updates only affect global installation
- Project overrides are preserved
- Backward compatibility maintained

## 🩺 Troubleshooting

### Check System Health
```bash
agentic-flow doctor
```

### Common Issues

**Command not found**
```bash
# Add to PATH
export PATH="$HOME/.agentecflow/bin:$PATH"
```

**Permission denied**
```bash
# Make executable
chmod +x ~/.agentecflow/bin/agentic-flow
```

**Project not initialized**
```bash
# Initialize in project root
cd your-project
agentic-flow init
```

## 📚 Methodology Guides

### Requirements Engineering
- Interactive gathering sessions
- EARS notation patterns
- Traceability management

### Test Specification
- BDD/Gherkin scenarios
- Coverage strategies
- Quality gates

### Progress Tracking
- Sprint management
- State synchronization
- Automated reporting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure quality gates pass
5. Submit pull request

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- EARS notation by Alistair Mavin
- BDD methodology by Dan North
- Inspired by Agent OS architecture

## 📞 Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/agentic-flow/issues)
- Documentation: [Full docs](https://docs.agentecflow.ai)
- Community: [Discord server](https://discord.gg/agentic-flow)

---

Built with ❤️ for AI-powered software engineering
