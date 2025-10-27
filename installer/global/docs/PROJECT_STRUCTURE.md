# Agentic Flow Project Structure Guide

## Overview

Agentic Flow uses a **smart initialization** approach that adapts to your existing project structure rather than imposing its own. This prevents duplication and confusion while maintaining a clean separation of concerns.

## Core Principle: Single Source of Truth

- **ONE .claude directory** at project root
- **ONE docs directory** for all documentation
- **NO duplication** of configuration or requirements

## Recommended Workflow

### For New Projects

1. **Create your technology project first**:
   ```bash
   # .NET MAUI
   dotnet new maui -n MyApp
   
   # React
   npx create-react-app my-app
   
   # Python
   python -m venv venv
   ```

2. **Then initialize Agentic Flow**:
   ```bash
   agentic-init [template]
   ```

### For Existing Projects

Simply run `agentic-init` in your project root. It will:
- Detect your project type automatically
- Select the appropriate template
- Adapt to your existing structure
- Avoid creating duplicate directories

## Directory Structure

### Universal Structure (All Projects)

```
project-root/
├── .claude/              # SINGLE configuration location
│   ├── CLAUDE.md        # Project context for Claude Code
│   ├── settings.json    # Configuration
│   ├── agents/          # AI agents
│   ├── commands/        # Available commands
│   └── templates/       # Code generation templates
├── docs/                # SINGLE documentation location
│   ├── requirements/    # Requirements in EARS notation
│   │   ├── draft/      # Work in progress
│   │   ├── approved/   # Ready for implementation
│   │   └── implemented/# Completed features
│   ├── bdd/            # BDD test scenarios
│   │   └── features/   # Gherkin feature files
│   ├── adr/            # Architecture decision records
│   └── state/          # Sprint progress tracking
└── [project files]      # Your actual project code
```

### Technology-Specific Adaptations

#### .NET Projects (MAUI, Microservices)

```
solution-root/
├── .claude/             # At solution root
├── docs/                # At solution root
├── MySolution.sln
├── MyApp/               # Main project
│   └── MyApp.csproj
└── MyApp.Tests/         # Test project
    └── MyApp.Tests.csproj
```

**Key Points**:
- Tests are in .NET test projects (not separate tests/ directory)
- No src/ directory needed - .NET has its own structure
- Agentic Flow configuration at solution level

#### React/Node Projects

```
project-root/
├── .claude/
├── docs/
├── src/                 # React source code
├── tests/               # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── package.json
└── node_modules/
```

#### Python Projects

```
project-root/
├── .claude/
├── docs/
├── src/                 # Python modules
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
└── venv/
```

## Smart Detection

The initialization script automatically detects:

- **MAUI**: Finds Microsoft.Maui in .csproj files
- **Microservices**: Finds Microsoft.AspNetCore in .csproj files
- **React**: Finds react in package.json
- **Python**: Finds requirements.txt or pyproject.toml
- **Vue**: Finds vue in package.json

And adapts accordingly:
- Selects appropriate template
- Skips creating duplicate directories
- Configures for technology-specific patterns

## Requirements Flow

Requirements follow a clear progression through directories:

```
docs/requirements/draft/     # Initial gathering
         ↓
docs/requirements/approved/  # Formalized in EARS
         ↓
docs/requirements/implemented/ # Completed features
```

## Common Issues and Solutions

### Issue: Duplicate .claude directories
**Solution**: Only one .claude at project root. Delete any in subdirectories.

### Issue: Requirements in multiple places
**Solution**: All requirements go in docs/requirements/. Remove any in src/.

### Issue: Confusion about where to create project
**Solution**: Create technology project first, then init Agentic Flow.

### Issue: Tests directory for .NET
**Solution**: .NET uses test projects, not tests/ directory. Script detects this.

## Commands Available

After initialization, these commands are available in Claude Code:

- `/gather-requirements` - Interactive requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Create BDD test scenarios
- `/execute-tests` - Run test suite with quality gates
- `/update-state` - Update sprint progress

## Best Practices

1. **Create technology project first** - Let IDE/CLI create proper structure
2. **Run agentic-init at root** - Always at project/solution root
3. **Let auto-detection work** - Don't force template if not needed
4. **Keep single source of truth** - One .claude, one docs
5. **Follow requirements flow** - draft → approved → implemented

## Configuration

The `.claude/settings.json` tracks:

```json
{
  "version": "1.0.0",
  "project": {
    "name": "MyApp",
    "template": "maui",
    "detected_type": "maui"
  },
  "structure": {
    "use_src_folder": false,
    "test_location": "solution"
  }
}
```

This helps Agentic Flow understand your project structure and adapt its behavior accordingly.

## Migration from Old Structure

If you have an old structure with duplication:

1. Backup your requirements:
   ```bash
   cp -r src/Requirements/* docs/requirements/draft/
   ```

2. Remove duplicate .claude:
   ```bash
   rm -rf src/.claude
   ```

3. Update paths in your workflow

4. Re-initialize if needed:
   ```bash
   agentic-init [template]
   ```

## Technology-Specific Guidance

### .NET MAUI Projects

1. Create solution and projects:
   ```bash
   dotnet new sln -n MyApp
   dotnet new maui -n MyApp
   dotnet new xunit -n MyApp.Tests
   dotnet sln add MyApp/MyApp.csproj
   dotnet sln add MyApp.Tests/MyApp.Tests.csproj
   ```

2. Initialize Agentic Flow at solution root:
   ```bash
   agentic-init maui
   ```

3. Add required packages:
   ```bash
   cd MyApp
   dotnet add package LanguageExt.Core
   dotnet add package CommunityToolkit.Mvvm
   ```

### React Projects

1. Create React app:
   ```bash
   npx create-react-app my-app --template typescript
   cd my-app
   ```

2. Initialize Agentic Flow:
   ```bash
   agentic-init react
   ```

3. Install test dependencies:
   ```bash
   npm install -D vitest @testing-library/react @playwright/test
   ```

### Python FastAPI Projects

1. Set up Python project:
   ```bash
   mkdir my-api && cd my-api
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. Initialize Agentic Flow:
   ```bash
   agentic-init python
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn pytest pytest-asyncio
   ```

## Troubleshooting

### Script Can't Find Templates
Ensure `CLAUDE_HOME` is set correctly:
```bash
export CLAUDE_HOME=$HOME/.claude
```

### Permission Denied
Make script executable:
```bash
chmod +x agentic-init
```

### Wrong Template Selected
Override auto-detection:
```bash
agentic-init maui  # Force specific template
```

### Git Hooks Not Working
Ensure you're in a git repository:
```bash
git init
agentic-init [template]
```

## Support

For issues or questions:
1. Check this documentation
2. Review the template-specific CLAUDE.md file
3. Look at example projects in the templates directory
4. Consult the ADR documents for architectural decisions
