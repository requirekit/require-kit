# Testing Agentic Flow Installation Scripts

This directory contains comprehensive testing scripts to validate the Agentic Flow installation across different platforms and shells.

## Quick Test (Recommended to Start)

**For immediate testing on your current macOS/zsh setup:**

```bash
cd /path/to/ai-engineer
./installer/scripts/quick-test.sh
```

This will:
- ✅ Create an isolated test environment
- ✅ Test the full installation process
- ✅ Verify all components are installed correctly
- ✅ Test project template initialization
- ✅ Check shell integration
- ✅ Clean up automatically

**Expected output:** "✅ Installation test PASSED"

## Comprehensive Testing Suite

### 1. Basic Installation Testing

```bash
./installer/scripts/test-installation.sh
```

**Tests:**
- Shell support (bash, zsh)
- Full installation process
- Project initialization for all templates
- Shell integration
- Error handling

### 2. Cross-Platform Testing

```bash
./installer/scripts/test-cross-platform.sh
```

**Tests:**
- Platform detection (macOS, Linux, Windows)
- Shell compatibility across platforms
- Template initialization on different OS
- Platform-specific features
- PowerShell script validation (if available)

## Windows PowerShell Testing

**For your Windows VM in Parallels:**

1. **Copy the PowerShell script to Windows:**
   ```powershell
   # In Windows PowerShell
   Copy-Item "\\Mac\Home\path\to\ai-engineer\installer\scripts\install.ps1" -Destination "C:\temp\"
   ```

2. **Test PowerShell installation:**
   ```powershell
   # Set execution policy if needed
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

   # Run in test mode
   .\install.ps1 -TestMode

   # Run full installation
   .\install.ps1
   ```

3. **Verify installation:**
   ```powershell
   agentecflow doctor
   agentecflow init react
   ```

## Testing on Virtual Machines

### macOS VM Testing
```bash
# In your macOS VM
cd /path/to/ai-engineer

# Test with different shells
export SHELL=/bin/bash
./installer/scripts/quick-test.sh

export SHELL=/bin/zsh
./installer/scripts/quick-test.sh
```

### Windows VM Testing
```powershell
# In Windows VM PowerShell
.\installer\scripts\install.ps1 -TestMode

# If successful, run full install
.\installer\scripts\install.ps1

# Test initialization
agentecflow init dotnet-microservice
agentecflow init maui
```

## Test Results Interpretation

### ✅ Success Indicators
- All directory structures created
- CLI commands are executable
- Templates initialize correctly
- Shell integration configured
- Agents and commands installed

### ❌ Failure Indicators
- Missing directories or files
- Permission errors
- Shell integration failures
- Template initialization errors

### ⚠️ Warnings (Usually OK)
- Optional dependencies missing (Node.js, Python, .NET)
- PowerShell not available on Unix
- Some shell config files not found

## Manual Verification Steps

After running tests, you can manually verify:

```bash
# Check installation
ls -la ~/.agenticflow/

# Verify agents
ls ~/.agenticflow/agents/

# Check templates
ls ~/.agenticflow/templates/

# Test CLI
agentecflow doctor
agentecflow --help

# Test template
mkdir test-project && cd test-project
agentecflow init react
ls -la
```

## Troubleshooting Common Issues

### Permission Errors
```bash
# Fix permissions
chmod +x installer/scripts/*.sh
```

### Shell Not Detected
```bash
# Explicitly set shell
export SHELL=/bin/zsh  # or /bin/bash
./installer/scripts/quick-test.sh
```

### Missing Dependencies
```bash
# macOS with Homebrew
brew install git node python

# Check prerequisites
git --version
node --version
python3 --version
```

### PowerShell Execution Policy (Windows)
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single execution
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

## Testing Different Scenarios

### 1. Clean Environment Test
```bash
# Test in completely fresh environment
docker run -it --rm ubuntu:latest bash
# Then run installation
```

### 2. Existing Installation Test
```bash
# Test upgrade/reinstall
./installer/scripts/install.sh
./installer/scripts/install.sh  # Run again
```

### 3. Different Home Directory
```bash
# Test with custom home
export HOME=/tmp/test-home
mkdir -p /tmp/test-home
./installer/scripts/quick-test.sh
```

## Expected Test Duration

| Test Suite | Duration | Coverage |
|------------|----------|----------|
| quick-test.sh | 30-60 seconds | Basic validation |
| test-installation.sh | 2-3 minutes | Comprehensive Unix/Linux/macOS |
| test-cross-platform.sh | 5-10 minutes | Full platform compatibility |
| PowerShell testing | 1-2 minutes | Windows compatibility |

## Test Environment Requirements

### Minimum Requirements
- Git installed
- Bash shell available
- Write permissions to home directory

### Recommended
- Node.js (for React/TypeScript templates)
- Python 3 (for Python templates)
- .NET SDK (for .NET templates)
- PowerShell Core (for cross-platform testing)

## Reporting Issues

If tests fail, please provide:

1. **Platform information:**
   ```bash
   uname -a
   echo $SHELL
   ```

2. **Test output:**
   ```bash
   ./installer/scripts/quick-test.sh 2>&1 | tee test-output.log
   ```

3. **Environment details:**
   ```bash
   env | grep -E "(HOME|SHELL|PATH)"
   ```

## Next Steps After Successful Testing

1. **Install for real:**
   ```bash
   ./installer/scripts/install.sh
   ```

2. **Restart shell:**
   ```bash
   exec $SHELL  # or restart terminal
   ```

3. **Verify installation:**
   ```bash
   agentecflow doctor
   ```

4. **Initialize your first project:**
   ```bash
   mkdir my-project && cd my-project
   agentecflow init [template-name]
   ```

---

**Note:** All test scripts create isolated environments and clean up after themselves, so they're safe to run multiple times without affecting your system.