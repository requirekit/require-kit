# Installer Updates for Kanban Task Workflow

## Summary of Changes

The installer scripts have been updated to include the new Kanban task workflow system with mandatory test verification. This ensures that all projects initialized with the Agentecflow system include the complete task management infrastructure.

## Files Updated

### 1. Manifest File
**Path**: `installer/global/manifest.json`
- Added new capabilities:
  - `kanban-workflow`
  - `task-management`
  - `test-verification`

### 2. Installation Scripts

#### Main Installer (`installer/scripts/install.sh`)
- Updated `init_project` function to create task directories:
  - `tasks/backlog`
  - `tasks/in_progress`
  - `tasks/in_testing`
  - `tasks/in_review`
  - `tasks/blocked`
  - `tasks/completed`

#### Project Initializer (`installer/scripts/init-project.sh`)
- Updated `create_structure` function to include task workflow directories
- Ensures all new projects have the complete task management structure

### 3. Global Commands Added

**Path**: `installer/global/commands/`

#### Core Task Commands
- `task.md` - Main task management command with comprehensive documentation
- `task-create.md` - Create new tasks in backlog
- `task-status.md` - View kanban board and metrics dashboard

#### Supporting Commands
These commands already existed in the installer:
- `formalize-ears.md` - Convert requirements to EARS notation
- `gather-requirements.md` - Interactive requirements gathering
- `generate-bdd.md` - Generate BDD scenarios from EARS

### 4. Global Agents Added

**Path**: `installer/global/agents/`

#### New Agents
- `task-manager.md` - Manages tasks through kanban workflow with mandatory test verification
- `test-verifier.md` - Executes and verifies tests for tasks, ensuring quality gates are met

#### Existing Agents
These agents were already part of the system and support the workflow:
- Requirements analyst
- BDD generator
- Code reviewer
- Test orchestrator

## Installation Flow

When a user runs the installation:

### 1. Global Installation
```bash
./installer/scripts/install.sh
```
This installs:
- Core binaries and CLI tools
- Global commands including task management
- Global agents including task-manager and test-verifier
- Templates and configurations

### 2. Project Initialization
```bash
agentecflow init [template]
```
This creates:
- `.claude/` configuration directory
- `docs/` documentation structure
- `tests/` test directories
- **`tasks/` kanban workflow directories** (NEW)
- Template-specific files

## Directory Structure Created

After installation, projects will have:
```
project/
├── .claude/          # AI configuration
├── docs/            # Documentation
├── src/             # Source code
├── tests/           # Test suites
└── tasks/           # Kanban workflow (NEW)
    ├── backlog/     # New tasks
    ├── in_progress/ # Active development
    ├── in_testing/  # Running tests
    ├── in_review/   # Passed tests, under review
    ├── blocked/     # Failed tests or dependencies
    └── completed/   # Done with passing tests
```

## Usage After Installation

Once installed, users can:

### Create Tasks
```bash
/task create "Implement user authentication" priority:high
```

### View Task Board
```bash
/task status
```

### Move Tasks Through Workflow
```bash
/task start TASK-001
/task implement TASK-001
/task test TASK-001
/task review TASK-001
/task complete TASK-001
```

## Quality Gates Enforced

The system enforces:
- **Test Coverage**: Minimum 80% required
- **Test Passing**: 100% tests must pass
- **Review Required**: Tasks must be reviewed before completion
- **Blocked on Failure**: Failed tests automatically block tasks

## Benefits

1. **Prevents "Implemented but Not Working"**: Mandatory test verification
2. **Clear Workflow**: Visible task states and transitions
3. **Quality Enforcement**: Automatic blocking on test failures
4. **Progress Tracking**: Real-time visibility of task status
5. **Metrics Dashboard**: Team velocity and quality metrics

## Next Steps

1. **Test the installer**: Run through complete installation flow
2. **Verify directory creation**: Ensure all task directories are created
3. **Test commands**: Verify task commands work after installation
4. **Update documentation**: Add task workflow to user guides

## Migration for Existing Projects

For projects already using Agentecflow, add task workflow:

```bash
# Create task directories
mkdir -p tasks/{backlog,in_progress,in_testing,in_review,blocked,completed}

# Copy new commands from global
cp ~/.agentic-flow/commands/task*.md .claude/commands/

# Copy new agents
cp ~/.agentic-flow/agents/task-manager.md .claude/agents/
cp ~/.agentic-flow/agents/test-verifier.md .claude/agents/
```

## Verification Checklist

- [x] Manifest updated with new capabilities
- [x] Install.sh creates task directories
- [x] Init-project.sh creates task directories
- [x] Task commands copied to global
- [x] Task agents copied to global
- [x] Documentation updated
- [ ] Installation tested end-to-end
- [ ] Commands verified in new project
- [ ] Migration guide tested

The installer is now ready to deploy the complete Kanban task workflow system with mandatory test verification to all new Agentecflow projects.
