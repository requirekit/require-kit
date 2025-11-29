# Installation

Install RequireKit and set up your environment for requirements management.

## Prerequisites

- Claude Code or compatible Claude environment
- Git (for version control of requirements)
- Text editor or IDE (optional, for viewing/editing markdown files)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/requirekit/require-kit.git
cd require-kit
```

### 2. Run the Installer

```bash
chmod +x ./installer/scripts/install.sh
./installer/scripts/install.sh
```

The installer will:
- Install global agents (requirements-analyst, bdd-generator)
- Install global commands (epic/feature management)
- Create marker file for package detection
- Set up PATH for commands

### 3. Verify Installation

```bash
# Check that commands are available
/gather-requirements --version
/formalize-ears --version
/generate-bdd --version

# All should respond with require-kit version info
```

## Project Initialization

Initialize RequireKit in your project:

```bash
cd /path/to/your/project
/require-kit init

# Creates directory structure:
# docs/
# ├── epics/
# ├── features/
# ├── requirements/
# └── bdd/
```

## Configuration

RequireKit stores configuration in `.claude/` directory (user-specific, gitignored):

- **Agents**: `.claude/agents/` - requirements-analyst, bdd-generator
- **Commands**: `.claude/commands/` - epic/feature management commands
- **Settings**: `.claude/settings.json` - user preferences

## Package Status

RequireKit is **standalone** with no dependencies:

- ✅ Works independently for requirements management
- ✅ No external packages required
- ✅ Optional integration with taskwright
- ✅ Bidirectional detection when both installed

## Optional: Install taskwright

For complete requirements-to-implementation workflow:

```bash
# Clone taskwright
git clone https://github.com/taskwright-dev/taskwright.git
cd taskwright

# Run installer
./installer/scripts/install.sh

# Verify integration
ls ~/.agentecflow/*.marker
# Should show both: require-kit.marker + taskwright.marker
```

[Learn more about integration →](integration.md)

## Troubleshooting

### Commands Not Found

If commands are not recognized:

1. **Verify PATH**:
```bash
echo $PATH | grep agentecflow
# Should show: ...:/Users/yourusername/.agentecflow/bin:...
```

2. **Add to PATH** (add to `~/.bashrc` or `~/.zshrc`):
```bash
export PATH="$HOME/.agentecflow/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

3. **Restart terminal**:
```bash
exec $SHELL
```

### Installation Failed

If installation fails:

1. Check prerequisites are installed
2. Ensure you have write permissions to `~/.agentecflow/`
3. Review installer output for error messages
4. Try running installer with `--repair` flag:
```bash
./installer/scripts/install.sh --repair
```

### Marker File Missing

If integration not detected:

```bash
# Check marker files
ls -la ~/.agentecflow/*.marker

# Re-run installer if missing
cd /path/to/require-kit
./installer/scripts/install.sh --repair
```

## Uninstallation

To uninstall RequireKit:

```bash
# Remove agentecflow directory
rm -rf ~/.agentecflow

# Remove from PATH (edit ~/.bashrc or ~/.zshrc)
# Remove line: export PATH="$HOME/.agentecflow/bin:$PATH"

# Reload shell
exec $SHELL
```

## What's Next?

- 🚀 [Try the Quickstart Guide](quickstart.md)
- 📝 [Gather Your First Requirements](first-requirements.md)
- 📖 [Read the Complete User Guide](../guides/require_kit_user_guide.md)

## Need Help?

- Check the [Troubleshooting Guide](../troubleshooting/index.md)
- Review the [FAQ](../faq.md)
- Report issues on [GitHub](https://github.com/requirekit/require-kit/issues)

---

**Installation complete?** Continue to the [Quickstart Guide](quickstart.md)
