# Installation

Install RequireKit and set up your environment for requirements management.

## Prerequisites

- Claude Code or compatible Claude environment
- Git (for version control of requirements)
- Text editor or IDE (optional, for viewing/editing markdown files)

## Installation Steps

### Method 1: Quick Install (Recommended)

**For macOS/Linux:**

```bash
curl -sSL https://raw.githubusercontent.com/requirekit/require-kit/main/installer/scripts/install.sh | bash
```

This single command downloads and runs the installer, setting up require-kit globally on your system.

**For Windows (via WSL2):**

1. Ensure WSL2 is installed on your Windows machine
2. Open your WSL2 terminal
3. Run the same curl command above

### Method 2: Clone Repository

If you prefer to clone the source code first:

```bash
git clone https://github.com/requirekit/require-kit.git
cd require-kit
chmod +x installer/scripts/install.sh
./installer/scripts/install.sh
```

### What the Installer Does

The installer will:
- Install global agents (requirements-analyst, bdd-generator) to `~/.agentecflow/agents/`
- Install global commands (epic/feature management) to `~/.agentecflow/commands/`
- Create marker file for package detection at `~/.agentecflow/require-kit.marker`
- Add `~/.agentecflow/bin` to your PATH
- Set up Claude Code integration

### Verify Installation

After installation, verify that require-kit is available:

```bash
# Check installation directory
ls ~/.agentecflow/

# Verify marker file exists
cat ~/.agentecflow/require-kit.marker
```

## Project Initialization

Navigate to your project and create the require-kit documentation structure:

```bash
cd /path/to/your/project
mkdir -p docs/requirements/{draft,approved,implemented}
mkdir -p docs/epics/{active,completed,cancelled}
mkdir -p docs/features/{active,in_progress,completed}
mkdir -p docs/bdd
```

After creating the directory structure, require-kit commands are automatically available in Claude Code:
- `/gather-requirements` - Interactive requirements gathering
- `/formalize-ears` - Convert to EARS notation
- `/generate-bdd` - Generate BDD scenarios
- `/epic-create` - Create epic
- `/feature-create` - Create feature
- `/hierarchy-view` - View epic/feature hierarchy

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

To uninstall require-kit:

```bash
# Remove require-kit files
rm -rf ~/.agentecflow/agents/require-kit
rm -rf ~/.agentecflow/commands/require-kit
rm -rf ~/.agentecflow/lib  # Shared library files
rm ~/.agentecflow/require-kit.marker

# Remove installation tracking
rm -f ~/.agentecflow/.installed/require-kit.*
```

**If you don't have taskwright or other packages installed**, you can remove the entire directory:

```bash
rm -rf ~/.agentecflow
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
