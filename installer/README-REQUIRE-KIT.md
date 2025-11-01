# require-kit Installer

This directory contains the require-kit-specific installer that installs to namespaced directories for bidirectional optional integration with taskwright.

## Installation Model

**Bidirectional Optional Integration:**
- require-kit works standalone (requirements management only)
- taskwright works standalone (task execution only)
- Both packages detect each other via marker files
- Enhanced features available when both installed
- No hard dependencies either way

## Installation Scripts

### install-require-kit.sh
Installs require-kit to `~/.agentecflow` using namespaced directories:
- Commands: `~/.agentecflow/commands/require-kit/`
- Agents: `~/.agentecflow/agents/require-kit/`
- Marker: `~/.agentecflow/require-kit.marker`
- Lib: `~/.agentecflow/lib/` (shared with taskwright)

Creates backwards-compatible symlinks for commands and agents.

**Usage:**
```bash
cd require-kit/installer
bash scripts/install-require-kit.sh
```

### uninstall-require-kit.sh
Removes require-kit from `~/.agentecflow`:
- Removes namespaced directories
- Removes symlinks pointing to require-kit
- Removes marker file
- Preserves feature_detection.py if taskwright is installed
- Cleans up empty directories

**Usage:**
```bash
cd require-kit/installer
bash scripts/uninstall-require-kit.sh
```

### init-require-kit-project.sh
Initializes a project for require-kit:
- Creates `docs/requirements/` (draft, approved, implemented)
- Creates `docs/epics/` (active, completed, cancelled)
- Creates `docs/features/` (active, in_progress, completed)
- Creates `docs/bdd/`
- Creates `.claude/CLAUDE.md` with configuration
- Detects taskwright integration if available

**Usage:**
```bash
cd your-project
~/.agentecflow/bin/require-kit init
# OR
bash /path/to/require-kit/installer/scripts/init-require-kit-project.sh
```

### test-require-kit-install.sh
Automated test suite that verifies:
- Directory structure creation
- Commands and agents installation
- Symlink creation
- Marker file creation
- feature_detection.py installation
- Version tracking
- Clean uninstallation

**Usage:**
```bash
cd require-kit/installer
bash scripts/test-require-kit-install.sh
```

## Directory Structure After Installation

```
~/.agentecflow/
├── commands/
│   ├── require-kit/           # Namespaced commands
│   │   ├── gather-requirements.md
│   │   ├── formalize-ears.md
│   │   ├── generate-bdd.md
│   │   └── ...
│   ├── gather-requirements.md -> require-kit/gather-requirements.md  # Symlinks
│   └── ...
├── agents/
│   ├── require-kit/           # Namespaced agents
│   │   ├── requirements-analyst.md
│   │   ├── bdd-generator.md
│   │   └── ...
│   ├── requirements-analyst.md -> require-kit/requirements-analyst.md  # Symlinks
│   └── ...
├── lib/
│   └── feature_detection.py   # Shared with taskwright
├── .installed/
│   ├── require-kit.version
│   └── require-kit.timestamp
└── require-kit.marker         # Package detection marker
```

## Marker File Format

The installer creates `~/.agentecflow/require-kit.marker`:

```json
{
  "name": "require-kit",
  "version": "1.0.0",
  "installed_at": "2025-10-28T12:00:00Z",
  "install_dir": "~/.agentecflow",
  "capabilities": [
    "requirements-engineering",
    "ears-notation",
    "bdd-generation",
    "epic-feature-hierarchy",
    "requirements-traceability"
  ]
}
```

This allows taskwright to detect require-kit and enable extended features.

## Feature Detection

The installer copies `feature_detection.py` to `~/.agentecflow/lib/` for use by both require-kit and taskwright.

**Example usage:**
```python
from lib.feature_detection import is_require_kit_installed, supports_bdd

if supports_bdd():
    # BDD mode available
    load_bdd_scenarios()
else:
    # Gracefully skip BDD features
    print("Install require-kit for BDD mode")
```

## Integration with taskwright

**When only require-kit is installed:**
- Requirements engineering (EARS notation)
- Epic/Feature hierarchy management
- BDD/Gherkin scenario generation
- Requirements traceability
- Output for any PM tool (Jira, Linear, GitHub, etc.)

**When both installed:**
- All of the above PLUS:
- Requirements can be linked to tasks
- Tasks can reference epics/features
- Full traceability: requirements → epics → features → tasks → implementation
- Integrated status reporting
- BDD mode in /task-work

## Testing

The test script verifies all acceptance criteria from REQ-003A:

- [x] install-require-kit.sh installs to namespaced directories
- [x] Symlinks created for backwards compatibility
- [x] manifest.json updated with namespace info
- [x] uninstall-require-kit.sh removes only require-kit files
- [x] Version tracking works (.installed/)
- [x] Marker file created (require-kit.marker with JSON metadata)
- [x] feature_detection.py copied to ~/.agentecflow/lib/
- [x] Dependency check for taskwright marker file
- [x] Standalone installation works
- [x] Project initialization works
- [x] Verification tests pass

Run tests:
```bash
cd require-kit/installer
bash scripts/test-require-kit-install.sh
```

## Files

- `scripts/install-require-kit.sh` - Main installation script
- `scripts/uninstall-require-kit.sh` - Uninstallation script
- `scripts/init-require-kit-project.sh` - Project initialization
- `scripts/test-require-kit-install.sh` - Automated test suite
- `manifest.json` - Package metadata
- `global/lib/feature_detection.py` - Feature detection library (shared)

## Comparison with Full Installer

**install.sh** (full Agentecflow):
- Installs everything (commands, agents, templates, docs)
- Creates full ~/.agentecflow structure
- Includes both require-kit AND taskwright
- Used for complete Agentecflow installation

**install-require-kit.sh** (require-kit only):
- Installs only require-kit components
- Uses namespaced directories
- Allows coexistence with taskwright
- Used for require-kit as a standalone package

Both can coexist - install.sh installs the full system, while install-require-kit.sh can be used to update just the require-kit portion or install require-kit standalone.
