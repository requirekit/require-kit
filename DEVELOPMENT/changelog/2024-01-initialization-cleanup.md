# Agentecflow Initialization - Cleanup Summary

## Changes Made

### 1. Script Consolidation
- **Removed**: `init-claude-project-v2.sh` (duplicate)
- **Renamed**: `init-claude-project-v2.sh` → `init-claude-project.sh` (main script)
- **Archived**: Old versions moved to `.archive/` directory

### 2. Single Initialization Script
Now there is only ONE initialization script:
- **Location**: `installer/scripts/init-claude-project.sh`
- **Features**: Smart project detection, adaptive structure creation, no duplication

### 3. Installation Flow

```
installer/
├── scripts/
│   ├── install.sh              # Main installer
│   ├── init-claude-project.sh  # Smart init script (NEW VERSION)
│   └── .archive/               # Old versions (hidden)
└── global/
    └── bin/
        └── agentec-init        # Wrapper command
```

### 4. How It Works

1. **Installation** (`install.sh`):
   - Copies init script to `~/.agentic-flow/scripts/`
   - Creates `agentec-init` command in PATH
   - Makes everything executable

2. **Project Initialization** (`agentec-init`):
   - Detects existing project type automatically
   - Creates single .claude directory at root
   - Creates single docs directory at root
   - Adapts to existing structure (no duplication)

## Usage

### For New Projects

```bash
# 1. Create technology project first
dotnet new maui -n MyApp        # For MAUI
npx create-react-app my-app      # For React
python -m venv venv              # For Python

# 2. Initialize Agentecflow
agentec-init [template]          # Auto-detects if template not specified
```

### For Existing Projects

```bash
cd existing-project
agentec-init                     # Auto-detects and adapts
```

## Key Benefits

1. **No Confusion**: Single script, clear purpose
2. **Smart Detection**: Automatically identifies project type
3. **No Duplication**: Single .claude, single docs
4. **Clean Structure**: Adapts to existing projects
5. **Backward Compatible**: `agentec-init` command still works

## Project Structure (After Init)

### .NET MAUI Example
```
MyApp/                    # Solution root
├── .claude/             # SINGLE config location
├── docs/               # SINGLE docs location
│   └── requirements/
│       ├── draft/
│       ├── approved/
│       └── implemented/
├── MyApp.sln
├── MyApp/              # MAUI project
└── MyApp.Tests/        # Test project
```

### React Example
```
my-app/                  # Project root
├── .claude/            # SINGLE config location
├── docs/              # SINGLE docs location
├── src/               # React source
├── tests/             # Test suites
└── package.json
```

## Migration from Old Structure

If you have projects with the old structure:

1. **Backup requirements**:
   ```bash
   cp -r src/Requirements/* docs/requirements/draft/
   ```

2. **Remove duplicate .claude**:
   ```bash
   rm -rf src/.claude
   ```

3. **Re-initialize**:
   ```bash
   agentec-init [template]
   ```

## Testing the Changes

1. **Reinstall Agentecflow**:
   ```bash
   cd ~/Projects/appmilla_github/ai-engineer/installer
   ./scripts/install.sh
   ```

2. **Test initialization**:
   ```bash
   mkdir test-project
   cd test-project
   agentec-init
   ```

3. **Verify structure**:
   - Only one .claude directory (at root)
   - Only one docs directory (at root)
   - Proper template applied

## Troubleshooting

### "Command not found: agentec-init"
- Ensure you've run the installer
- Check PATH includes `~/.agentic-flow/bin`
- Restart shell or source profile

### "Template not found"
- Script will auto-detect and suggest appropriate template
- Use `agentec-init maui` for MAUI projects
- Use `agentec-init react` for React projects

### ".claude directory already exists"
- Script will offer to backup existing configuration
- Choose yes to proceed with reinitialization

## Summary

The initialization system is now:
- **Simpler**: One script, one command
- **Smarter**: Auto-detects project types
- **Cleaner**: No duplication or confusion
- **Adaptable**: Works with existing projects
