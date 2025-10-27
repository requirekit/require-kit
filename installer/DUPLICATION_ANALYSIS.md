# Agentecflow - Duplication Analysis & Resolution

## 📊 Duplication Analysis

After reviewing both implementations, here are the identified duplications and recommended resolutions:

## 1. DUPLICATED FILES

### Commands (Found in both locations)
**Original Location**: `.claude/commands/`
- gather-requirements.md
- formalize-ears.md
- generate-bdd.md
- execute-tests.md
- update-state.md

**New Location**: `installer/global/commands/`
- gather-requirements.md (simpler version)
- formalize-ears.md (simpler version)
- generate-bdd.md (simpler version)

**Resolution**: 
- Keep BOTH but with different purposes:
  - `installer/global/commands/` = Global reference (installed to ~/.agentic-flow/)
  - `.claude/commands/` = Project-specific enhanced versions

### Methodology Files
**Original Location**: `.claude/methodology/`
- 00-overview.md
- 01-requirements.md
- 02-bdd.md
- 03-testing.md
- 04-workflow.md

**New Location**: `installer/global/instructions/core/`
- ears-requirements.md (similar to 01-requirements.md)
- bdd-gherkin.md (similar to 02-bdd.md)
- test-orchestration.md (similar to 03-testing.md)

**Resolution**:
- Move `.claude/methodology/` content to `installer/global/instructions/core/`
- Delete `.claude/methodology/` after migration
- Projects will reference global methodology

### Template Files
**Original Location**: `.claude/templates/`
- ears-requirement.md
- bdd-scenario.md
- adr-template.md
- task-template.md

**New Location**: Not created in installer yet

**Resolution**:
- Move templates to `installer/global/templates/default/templates/`
- Remove from `.claude/templates/`

### Setup Scripts
**Original Location**: `.claude/setup.sh`
**New Location**: `installer/scripts/init-project.sh`

**Resolution**:
- Delete `.claude/setup.sh` (replaced by new installer system)

## 2. UNIQUE FILES TO PRESERVE

### In `.claude/` (Project-specific, should remain)
- CLAUDE.md (project context)
- settings.json (project settings)
- agents/*.md (AI agents)
- hooks/*.sh (automation hooks)
- stacks/ (technology stacks)

### In `installer/` (Global system, new)
- All installation scripts
- Global templates for different stacks
- Manifest and configuration

## 3. RECOMMENDED CLEAN STRUCTURE

### After Resolution:
```
ai-engineer/
├── installer/                       # GLOBAL INSTALLATION SYSTEM
│   ├── README.md                   # Installation documentation
│   ├── SETUP_GUIDE.md             # Setup guide
│   ├── scripts/
│   │   ├── install.sh             # Global installer
│   │   ├── uninstall.sh          # Uninstaller
│   │   └── init-project.sh       # Project initializer
│   └── global/                    # Files to install globally
│       ├── manifest.json
│       ├── instructions/core/     # Consolidated methodology
│       ├── templates/             # All stack templates
│       └── commands/              # Global command references
│
├── .claude/                        # PROJECT-SPECIFIC CONFIG (minimal)
│   ├── CLAUDE.md                  # Project context
│   ├── settings.json              # Project settings
│   ├── agents/                    # AI agents (unique)
│   ├── hooks/                     # Project hooks (unique)
│   └── stacks/                    # Active stacks (unique)
│
├── docs/                          # PROJECT DOCUMENTATION
├── src/                           # SOURCE CODE
└── tests/                         # TESTS
```

## 4. MIGRATION STEPS

### Step 1: Consolidate Methodology
```bash
# Move methodology to global instructions
cp .claude/methodology/00-overview.md installer/global/instructions/core/
cp .claude/methodology/01-requirements.md installer/global/instructions/core/requirements-engineering.md
cp .claude/methodology/04-workflow.md installer/global/instructions/core/development-workflow.md

# Remove duplicates
rm -rf .claude/methodology/
```

### Step 2: Consolidate Templates
```bash
# Create template directory in global
mkdir -p installer/global/templates/default/templates/

# Move templates to global
cp .claude/templates/* installer/global/templates/default/templates/

# Remove from project
rm -rf .claude/templates/
```

### Step 3: Remove Duplicate Commands
```bash
# Keep project commands as they are more detailed
# Global commands are simpler references
# No action needed - they serve different purposes
```

### Step 4: Remove Old Setup Script
```bash
# Remove old setup script
rm .claude/setup.sh
```

### Step 5: Update Project Structure
```bash
# The project .claude/ should now only contain:
# - CLAUDE.md (project context)
# - settings.json (project config)
# - agents/ (AI agents)
# - hooks/ (automation)
# - stacks/ (technology stacks)
```

## 5. BENEFITS OF SEPARATION

### Global Installation (`~/.agentic-flow/`)
- **Centralized methodology** - Update once, use everywhere
- **Reusable templates** - Consistent project initialization
- **Version management** - Control tool versions globally
- **Shared commands** - Common commands available to all projects

### Project Installation (`.claude/`)
- **Minimal footprint** - Only project-specific configuration
- **Custom agents** - Project-specific AI assistants
- **Local hooks** - Project automation
- **Override capability** - Can override global settings

## 6. NO FUNCTIONAL DUPLICATION

The two-tier system is designed to work together:
- **Global** = Methodology, templates, tools (installed once)
- **Project** = Configuration, customization (per project)

This is not duplication but separation of concerns:
- Global files are references and tools
- Project files are specific implementations

## RECOMMENDATION

1. **Keep the two-tier structure** as designed
2. **Migrate methodology** to global instructions
3. **Move templates** to global templates
4. **Remove `.claude/setup.sh`** (replaced by installer)
5. **Keep project commands** as they're more detailed
6. **Maintain separation** between global and project concerns

The system is correctly designed with intentional separation, not duplication. The apparent "duplication" is actually the proper two-tier architecture where global provides the base and projects customize as needed.
