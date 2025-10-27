# Fix for AI-Engineer Global Installation - Agents Not Being Copied

## Problem Identified
The `agentec-init` command was not copying agents from the templates to projects because:
1. Not all templates had agents directories
2. The init script wasn't configured to copy agents

## Solution Implemented

### 1. Added Agents to MAUI Template
Created `/installer/global/templates/maui/agents/` with all 4 core agents:
- requirements-analyst.md
- bdd-generator.md
- code-reviewer.md
- test-orchestrator.md

### 2. Updated init-claude-project.sh
Modified the `copy_template()` function to include agent copying:
```bash
# Copy agents if they exist in the template
if [ -d "$template_dir/agents" ]; then
    cp -r "$template_dir/agents/"* .claude/agents/ 2>/dev/null || true
    print_success "Copied AI agents"
fi
```

### 3. Created Fix Script
Created `/scripts/fix-template-agents.sh` to copy agents to all templates.

## To Complete the Fix

Run these commands to distribute agents to all templates:

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer

# Make the fix script executable
chmod +x scripts/fix-template-agents.sh

# Run it to copy agents to all templates
./scripts/fix-template-agents.sh

# Reinstall the global installation
cd installer
./scripts/install-global.sh
```

## Testing the Fix

After reinstalling, test with a new project:

```bash
# Create a test directory
mkdir -p ~/test-maui-project
cd ~/test-maui-project

# Initialize with MAUI template
agentec-init maui

# Verify agents were copied
ls -la .claude/agents/
```

You should see:
- bdd-generator.md
- code-reviewer.md
- requirements-analyst.md
- test-orchestrator.md

## What Each Agent Does

1. **requirements-analyst.md**: Gathers and formalizes requirements using EARS notation
2. **bdd-generator.md**: Converts EARS requirements into BDD/Gherkin scenarios
3. **code-reviewer.md**: Enforces quality standards through code review
4. **test-orchestrator.md**: Manages test execution and quality gates

## Directory Structure After Fix

```
~/.claude/templates/
├── default/
│   ├── CLAUDE.md
│   ├── agents/           # Now includes all 4 agents
│   └── templates/
├── maui/
│   ├── CLAUDE.md
│   ├── agents/           # Now includes all 4 agents
│   └── templates/
├── dotnet-microservice/
│   ├── CLAUDE.md
│   ├── agents/           # Now includes all 4 agents
│   └── templates/
├── python/
│   ├── CLAUDE.md
│   └── agents/           # Now includes all 4 agents
└── react/
    ├── CLAUDE.md
    ├── agents/           # Now includes all 4 agents
    └── templates/
```

## Verification Steps

1. Check that all templates have agents:
```bash
for template in default maui dotnet-microservice python react; do
    echo "$template:"
    ls ~/.claude/templates/$template/agents/ 2>/dev/null | wc -l
done
```

2. Test initialization with each template:
```bash
for template in default maui dotnet-microservice python react; do
    mkdir -p ~/test-$template
    cd ~/test-$template
    agentec-init $template
    echo "$template agents:"
    ls .claude/agents/ | wc -l
    cd ..
    rm -rf ~/test-$template
done
```

## Notes
- The agents are generic and work with all templates
- Each template can have additional template-specific agents if needed
- The agents use Claude Code's slash commands for interaction
