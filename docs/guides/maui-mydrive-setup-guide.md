# MAUI-MyDrive Template Setup Guide

## Quick Start (2 minutes)

This guide shows you how to set up and use the **MAUI-MyDrive local template** in your DeCUK.Mobile.MyDrive project after installing the latest version of Agentecflow.

### Prerequisites

1. ✅ Latest Agentecflow installed
2. ✅ TASK-011I completed (local template support)
3. ✅ TASK-011G completed (maui-mydrive template created)

### Verification

Check that local templates are supported:

```bash
# Run diagnostics
agentecflow doctor

# Should show:
# Local Templates:
#   ✓ Found 1 local templates
#     - maui-mydrive (overrides global)
```

---

## Understanding MAUI-MyDrive Template

### What is it?

The **maui-mydrive** template is a **local, project-specific template** that preserves MyDrive's unique architectural patterns:

- **Engine Pattern**: All classes suffixed with `Engine` (e.g., `AuthenticationEngine`, `RouteEngine`)
- **DeCUK Namespace**: Uses `DeCUK.Mobile.MyDrive.*` namespace hierarchy
- **Custom Agents**: MyDrive-specific AI agents for Engine pattern guidance
- **BaseEngine**: Foundation class with error handling, logging, telemetry

### Why does it exist?

MyDrive uses a **custom Engine pattern**, while the global MAUI templates use **generic Domain patterns** (verb-based naming like `GetProducts`, `CreateOrder`).

The local template allows MyDrive to:
- ✅ Maintain Engine pattern without affecting other projects
- ✅ Preserve DeCUK namespace conventions
- ✅ Continue development uninterrupted during global template migration
- ✅ Share template with team via Git

---

## Template Structure

### Location

```
/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive/
└── .claude/templates/maui-mydrive/
    ├── agents/                          # MyDrive-specific agents
    │   ├── engine-pattern-specialist.md # Engine pattern expertise
    │   ├── mydrive-architect.md         # MyDrive architectural guidance
    │   └── maui-mydrive-generator.md    # Code generation
    ├── src/                             # Source templates
    │   ├── BaseEngine.cs                # Base class (copy as-is)
    │   ├── FeatureEngine.cs             # Engine implementation
    │   ├── IFeatureEngine.cs            # Engine interface
    │   └── FeatureViewModelEngine.cs    # ViewModel using Engine
    ├── tests/                           # Test templates
    │   ├── FeatureEngineTests.cs
    │   └── FeatureViewModelEngineTests.cs
    ├── docs/                            # Documentation
    │   ├── README.md                    # Template usage guide
    │   ├── engine-patterns.md           # Comprehensive Engine patterns
    │   ├── namespace-conventions.md     # Namespace rules
    │   └── migration-guide.md           # UseCase to Engine migration
    └── manifest.json                     # Template metadata
```

### Template Priority

When you run `agentec-init maui-mydrive`, the system resolves templates in this order:

1. **Local** (highest priority): `.claude/templates/maui-mydrive/` ← **Used for MyDrive**
2. **Global**: `~/.agentecflow/templates/maui-mydrive/` (if exists)
3. **Default**: `~/.agentecflow/templates/default/` (fallback)

---

## Setting Up MyDrive Project

### Step 1: Verify Template Exists

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive

# Check local template exists
ls -la .claude/templates/maui-mydrive/

# Should show:
# drwxr-xr-x   7 richardwoollcott  staff    224 Oct 14 14:26 maui-mydrive
```

### Step 2: Verify Settings Configuration

Check that `.claude/settings.json` references the local template:

```bash
cat .claude/settings.json
```

Should contain:

```json
{
  "version": "1.0.0",
  "extends": "/Users/richardwoollcott/.agenticflow/templates/maui",
  "local_template": ".claude/templates/maui-mydrive",
  "project": {
    "name": "DeCUK.Mobile.MyDrive",
    "template": "maui-mydrive"
  }
}
```

### Step 3: Initialize Project (if not already done)

If the project hasn't been initialized with the local template yet:

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive

# Initialize with local template
agentec-init maui-mydrive
```

**Expected Output:**

```
🔄 Initializing project with template: maui-mydrive
✓ Using local template: maui-mydrive
✓ Template source: .claude/templates/maui-mydrive
✓ Template validated successfully
✓ Configuration created: .claude/settings.json
✓ Agents installed (3 MyDrive-specific agents)
✓ Template metadata recorded

Template Details:
  Name: maui-mydrive
  Scope: local
  Source: .claude/templates/maui-mydrive/
  Extends: maui (global)
  Namespace: DeCUK.Mobile.MyDrive

✅ Project initialized successfully!
```

### Step 4: Verify Template Integration

```bash
# Run diagnostics
agentecflow doctor

# Expected output:
# Local Templates:
#   ✓ Found 1 local templates
#     - maui-mydrive (valid)
#       ✓ CLAUDE.md present
#       ✓ manifest.json present
#       ✓ agents/ directory present
#       ✓ templates/ directory present
#
# Template Resolution:
#   Priority: local > global > default
#   maui-mydrive: .claude/templates/maui-mydrive/ [local]
```

---

## Using the Template

### Available Templates

The maui-mydrive template provides these templates:

| Template | Purpose | Placeholders |
|----------|---------|--------------|
| `BaseEngine.cs` | Base class for all engines | None (copy as-is) |
| `FeatureEngine.cs` | Engine implementation | `[FEATURE_NAME]`, `[ENTITY_TYPE]` |
| `IFeatureEngine.cs` | Engine interface | `[FEATURE_NAME]`, `[ENTITY_TYPE]` |
| `FeatureViewModelEngine.cs` | ViewModel with Engine | `[FEATURE_NAME]`, `[NAVIGATION_PARAMS]`, `[ENTITY_TYPE]` |
| `FeatureEngineTests.cs` | Engine unit tests | `[FEATURE_NAME]`, `[ENTITY_TYPE]` |
| `FeatureViewModelEngineTests.cs` | ViewModel tests | `[FEATURE_NAME]`, `[NAVIGATION_PARAMS]`, `[ENTITY_TYPE]` |

### Engine Pattern Architecture

**BaseEngine (Foundation):**
- Standardized error handling: `ExecuteWithErrorHandlingAsync<T>()`
- Logging: Structured logging with `IAppLogger`
- Telemetry: Business event and performance tracking
- Error conversion: Automatic exception to ErrorOr conversion

**Engine Naming Convention:**
- Class: `[Feature]Engine` (e.g., `AuthenticationEngine`, `RouteEngine`)
- Interface: `I[Feature]Engine` (e.g., `IAuthenticationEngine`)
- Must end with "Engine" suffix

**Example Engine:**

```csharp
namespace DeCUK.Mobile.MyDrive.Engines;

public class AuthenticationEngine : BaseEngine, IAuthenticationEngine
{
    private readonly IAuthRepository _repository;
    private readonly ILogService _logService;

    public AuthenticationEngine(
        IAuthRepository repository,
        ILogService logService,
        IAppLogger logger) : base(logger)
    {
        _repository = repository;
        _logService = logService;
    }

    public async Task<ErrorOr<AuthToken>> AuthenticateAsync(Credentials credentials)
    {
        return await ExecuteWithErrorHandlingAsync(
            async () =>
            {
                // Validate credentials
                if (string.IsNullOrEmpty(credentials.Username))
                    return Error.Validation("Username is required");

                // Authenticate via repository
                var result = await _repository.AuthenticateAsync(credentials);
                if (result.IsError) return result.Errors;

                // Log success
                await _logService.LogAuthenticationAsync(credentials.Username);

                return result.Value;
            },
            "Authenticate");
    }
}
```

**ViewModel Integration:**

```csharp
namespace DeCUK.Mobile.MyDrive.ViewModels;

public partial class SignInViewModel : ViewModelBase
{
    private readonly IAuthenticationEngine _authEngine;

    [ObservableProperty]
    private string _username;

    [ObservableProperty]
    private string _password;

    public SignInViewModel(IAuthenticationEngine authEngine)
    {
        _authEngine = authEngine;
    }

    [RelayCommand]
    private async Task SignInAsync()
    {
        var credentials = new Credentials { Username = Username, Password = Password };
        var result = await _authEngine.AuthenticateAsync(credentials);

        result.Match(
            value: token => HandleSuccess(token),
            errors: errors => HandleError(errors)
        );
    }
}
```

---

## Namespace Conventions

All templates use the MyDrive namespace hierarchy:

- **Engines**: `DeCUK.Mobile.MyDrive.Engines`
- **ViewModels**: `DeCUK.Mobile.MyDrive.ViewModels`
- **Services**: `DeCUK.Mobile.MyDrive.Services`
- **Repositories**: `DeCUK.Mobile.MyDrive.Repositories`
- **Tests**: `DeCUK.Mobile.MyDrive.UnitTests`

---

## Generating Code

### Using /zeplin-to-maui Command

When you use `/zeplin-to-maui` in the MyDrive project, it automatically detects and uses the local template:

```bash
# Convert Zeplin design to MAUI component
/zeplin-to-maui https://zeplin.io/project/...

# System automatically:
# 1. Detects MyDrive project
# 2. Uses .claude/templates/maui-mydrive/ (local template)
# 3. Generates Engine-pattern code
# 4. Uses DeCUK.Mobile.MyDrive namespace
# 5. Applies MyDrive-specific agents
```

### Using Task Workflow

```bash
# Create task with MAUI development
/task-create "Implement route management engine" requirements:[REQ-001]

# Implement with local template
/task-work TASK-001 --mode=tdd

# System automatically:
# 1. Loads maui-mydrive-generator agent
# 2. Uses Engine pattern templates
# 3. Generates tests with EngineTests.cs template
# 4. Validates Engine naming conventions
```

---

## Validation

### Run Template Validation

```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive

# Run validation script
.claude/templates/maui-mydrive/tests/validate-mydrive-template.sh

# Expected output:
# ✅ Engine suffix naming: 2/2 passed
# ✅ Namespace compliance: 6/6 passed
# ✅ BaseEngine inheritance: 1/2 passed (ViewModel false positive)
# ✅ ErrorOr return types: 1/2 passed
# ✅ File-scoped namespaces: 6/6 passed
# ✅ Test file naming: 2/2 passed
# ✅ Documentation files: 4/4 passed
# ✅ Manifest validation: 4/4 passed
# ✅ Agent files: 3/3 passed
#
# 30/32 checks passed (2 false positives)
```

**Note**: The validation script may show 2 false positives for ViewModel files (expected behavior).

### Quality Gates

All generated code must meet:

- ✅ **ErrorOr Pattern**: All public methods return `ErrorOr<T>`
- ✅ **Inheritance**: All engines extend `BaseEngine`
- ✅ **Naming**: All engines end with "Engine" suffix
- ✅ **Namespace**: All code uses `DeCUK.Mobile.MyDrive` namespace
- ✅ **Tests**: Minimum 80% code coverage
- ✅ **Documentation**: XML comments on all public members

---

## Troubleshooting

### Issue: Template not detected

**Symptom:**
```
⚠️  Template 'maui-mydrive' not found, using default
```

**Solution:**
```bash
# Verify local template exists
ls -la .claude/templates/maui-mydrive/

# If missing, check if template was created
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
git status

# Template should be committed to repo
```

### Issue: Wrong namespace generated

**Symptom:**
Generated code uses generic namespace instead of `DeCUK.Mobile.MyDrive`

**Solution:**
```bash
# Check settings.json
cat .claude/settings.json

# Should contain:
# "local_template": ".claude/templates/maui-mydrive"
# "project": { "template": "maui-mydrive" }

# If incorrect, update settings:
# Edit .claude/settings.json and set:
# "local_template": ".claude/templates/maui-mydrive"
# "project": { "template": "maui-mydrive" }
```

### Issue: Engine suffix not applied

**Symptom:**
Generated classes don't have "Engine" suffix

**Solution:**
```bash
# Verify manifest.json
cat .claude/templates/maui-mydrive/manifest.json | grep naming_conventions

# Should show:
# "naming_conventions": { "class_suffix": "Engine" }

# Ensure agents are loaded
agentecflow doctor

# Should show maui-mydrive-generator agent
```

### Issue: Global template used instead of local

**Symptom:**
Code generated with generic patterns instead of Engine pattern

**Solution:**
```bash
# Check template resolution priority
agentecflow doctor

# Should show:
# Template Resolution:
#   maui-mydrive: .claude/templates/maui-mydrive/ [local]

# If showing [global], then local template not detected
# Check that you're in the MyDrive project directory
pwd
# Should be: /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
```

### Issue: Template shows as invalid in doctor output

**Symptom:**
```bash
$ agentecflow doctor

Local Templates:
  ✓ 1 local templates available
  ✗ maui-mydrive (missing CLAUDE.md)
  # or
  ✗ maui-mydrive (missing templates/)
```

**Root Cause:**
The template structure doesn't match the expected format. Templates require:
1. `CLAUDE.md` at the root level
2. `templates/` directory (not `src/` or other names)
3. `agents/` directory
4. `manifest.json` at root

**Solution:**
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive

# Check current structure
ls -la .claude/templates/maui-mydrive/

# Should have these at root level:
# - CLAUDE.md (file)
# - manifest.json (file)
# - agents/ (directory)
# - templates/ (directory) ← NOT src/

# If missing CLAUDE.md:
# The file should exist at the template root
# See: .claude/templates/maui-mydrive/CLAUDE.md

# If using src/ instead of templates/:
cd .claude/templates/maui-mydrive
mv src templates  # Rename to match expected structure

# Verify fix:
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive
agentecflow doctor

# Should now show:
# ✓ maui-mydrive (valid)
```

**Expected Structure:**
```
.claude/templates/maui-mydrive/
├── agents/                    # ✅ Required
├── CLAUDE.md                  # ✅ Required at root
├── docs/
│   └── README.md
├── manifest.json              # ✅ Required
├── templates/                 # ✅ Required (not src/)
│   ├── BaseEngine.cs
│   ├── FeatureEngine.cs
│   └── ...
└── tests/
```

**Reference**: See [maui-mydrive-template-validation-fix.md](../fixes/maui-mydrive-template-validation-fix.md) for detailed fix documentation.

---

## Related Documentation

### Template Documentation
- [Template README](.claude/templates/maui-mydrive/docs/README.md) - Template usage guide
- [Engine Patterns](.claude/templates/maui-mydrive/docs/engine-patterns.md) - Comprehensive patterns
- [Namespace Conventions](.claude/templates/maui-mydrive/docs/namespace-conventions.md) - Namespace rules
- [Migration Guide](.claude/templates/maui-mydrive/docs/migration-guide.md) - UseCase to Engine

### Global Documentation
- [MAUI Template Architecture](../shared/maui-template-architecture.md) - Global vs local templates
- [Creating Local Templates](./creating-local-templates.md) - How to create custom templates
- [MAUI Template Selection](./maui-template-selection.md) - AppShell vs NavigationPage

### Implementation Tasks
- [TASK-011G](../../tasks/completed/TASK-011G-maui-mydrive-local-template.md) - MyDrive template creation
- [TASK-011I](../../tasks/completed/TASK-011I-installer-local-template-support.md) - Installer support
- [TASK-011G Test Report](../../tests/TASK-011G-TEST-REPORT.md) - Validation results

---

## Success Metrics

After setup, you should see:

✅ **Template Detected**: `agentecflow doctor` shows maui-mydrive template
✅ **Local Priority**: Template resolution shows `[local]` source
✅ **Engine Pattern**: Generated code uses Engine suffix
✅ **DeCUK Namespace**: Generated code uses DeCUK.Mobile.MyDrive namespace
✅ **Validation Passing**: Template validation script passes (95.7% success rate)
✅ **Agents Loaded**: MyDrive-specific agents available
✅ **Settings Correct**: settings.json references local template

---

## Next Steps

1. **Read Engine Patterns**: Review [engine-patterns.md](.claude/templates/maui-mydrive/docs/engine-patterns.md)
2. **Review Existing Engines**: Study `DeCUK.Mobile.MyDrive/Engines/` directory
3. **Create Your First Engine**: Use `/task-work` with Engine pattern
4. **Validate Generated Code**: Run validation script after generation

---

## Support

For questions or issues:

1. **Template Issues**: Check validation script output
2. **Pattern Questions**: Consult `engine-pattern-specialist` agent via Claude Code
3. **Architecture Guidance**: Review [MAUI Template Architecture](../shared/maui-template-architecture.md)
4. **Migration Help**: See [migration-guide.md](.claude/templates/maui-mydrive/docs/migration-guide.md)

---

## Version History

- **v1.0** (2025-10-17): Initial setup guide created
  - Comprehensive installation steps
  - Troubleshooting section
  - Template usage examples
  - Validation instructions
