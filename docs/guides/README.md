# require-kit Documentation Guides

Welcome to the require-kit documentation! These guides will help you understand and use the requirements management toolkit that uses EARS notation for requirements, BDD/Gherkin for test specifications, and epic/feature hierarchy for organization.

## 📚 Core Guides

### 🎯 [require-kit User Guide](require_kit_user_guide.md) **START HERE!**
Comprehensive overview of the entire require-kit system including:
- System philosophy and core principles
- Complete requirements workflow (EARS → BDD → Organization)
- Epic and feature hierarchy management
- All commands with detailed examples
- PM tool integration and export
- Best practices and troubleshooting

**Perfect for**: New users, comprehensive reference

### 🚀 [Getting Started](getting_started.md)
Quick start guide to get up and running with require-kit:
- Installation and setup
- Your first requirements gathering session
- Creating epics and features
- Understanding the workflow
- Next steps and learning path

**Perfect for**: First-time users, quick onboarding

### 📖 [Command Usage Guide](command_usage_guide.md)
Detailed command reference with syntax and examples:
- Requirements commands (/gather-requirements, /formalize-ears, /generate-bdd)
- Epic management commands (/epic-create, /epic-status, /epic-sync)
- Feature management commands (/feature-create, /feature-status, /feature-sync)
- Hierarchy visualization (/hierarchy-view)
- Complete workflow examples
- Command options and parameters

**Perfect for**: Daily reference, command lookups

## 🏢 Reference Guides

### 📝 [Documentation Update Summary](documentation_update_summary.md)
Summary of documentation updates.

## 🔗 Integration and Advanced Topics

### Integration with Other Tools

**Standalone Use**
- require-kit works completely standalone for requirements management
- Generates structured markdown files with PM tool metadata
- Provides specifications for any implementation system

**Integration with Task Execution**
- Optional integration for task execution workflow
- Bidirectional detection with compatible task systems
- See [Integration Guide](../INTEGRATION-GUIDE.md) for combined workflow

**PM Tool Integration (Specification Ready)**
- Epic/feature files include structured metadata for PM tool export
- Command specifications define integration patterns with Jira, Linear, GitHub, Azure DevOps
- Actual API integration requires user implementation or MCP server
- Structured output enables custom export scripts or automation

## 📋 Quick Reference

### Essential Commands

**Requirements Gathering**
```bash
/gather-requirements   # Interactive Q&A for capturing requirements
/formalize-ears       # Convert to EARS notation
/generate-bdd         # Generate Gherkin scenarios from requirements
```

**Epic Management**
```bash
/epic-create "Title"                        # Create an epic
/epic-status EPIC-XXX                       # View epic progress
/epic-generate-features EPIC-XXX            # Generate features from epic
/epic-sync EPIC-XXX                         # Sync with PM tools
```

**Feature Management**
```bash
/feature-create "Title" epic:EPIC-XXX       # Create a feature
/feature-status FEAT-XXX                    # View feature progress
/feature-generate-tasks FEAT-XXX            # Generate task specifications
/feature-sync FEAT-XXX                      # Sync with PM tools
```

**Hierarchy and Visualization**
```bash
/hierarchy-view EPIC-XXX                    # View epic hierarchy
```

### EARS Notation Quick Reference

1. **Ubiquitous**: `The [system] shall [behavior]`
2. **Event-Driven**: `When [trigger], the [system] shall [response]`
3. **State-Driven**: `While [state], the [system] shall [behavior]`
4. **Unwanted Behavior**: `If [error], then the [system] shall [recovery]`
5. **Optional Feature**: `Where [feature], the [system] shall [behavior]`

## 🏗️ Project Structure

```
docs/
├── epics/                 # Epic specifications
├── features/              # Feature specifications
├── requirements/          # EARS requirements
├── bdd/                   # BDD/Gherkin scenarios
└── guides/                # Documentation (you are here)

installer/
└── global/
    ├── agents/            # Global agents (requirements-analyst, bdd-generator)
    └── commands/          # Global commands (epic/feature management)
```

**Note**: `.claude/` directory is gitignored as it contains user-specific local configuration (agents, commands, settings) that varies by installation.

## 🎯 Typical Workflow

1. **Gather Requirements**
   ```bash
   /gather-requirements
   ```
   Interactively capture requirements through Q&A

2. **Formalize with EARS**
   ```bash
   /formalize-ears
   ```
   Convert to structured EARS notation

3. **Generate BDD Scenarios**
   ```bash
   /generate-bdd
   ```
   Create testable Gherkin scenarios

4. **Organize into Epics**
   ```bash
   /epic-create "User Management System"
   ```
   Create strategic business initiatives

5. **Create Features**
   ```bash
   /feature-create "User Authentication" epic:EPIC-001
   ```
   Bridge strategy to implementation

6. **Export or Integrate**
   - Export to PM tools for tracking
   - Integrate with task execution systems
   - Provide specifications to development teams

## 📁 Additional Documentation

- **[Integration Guide](../INTEGRATION-GUIDE.md)** - Using require-kit with task execution systems
- **[README.md](../../README.md)** - Project overview and installation

## 🔍 Finding Help

### In Documentation
1. **New to require-kit?** → [Getting Started](getting_started.md)
2. **Need comprehensive guide?** → [require-kit User Guide](require_kit_user_guide.md)
3. **Looking up a command?** → [Command Usage Guide](command_usage_guide.md)
4. **Want to integrate?** → [Integration Guide](../INTEGRATION-GUIDE.md)

### By Task
- **Capturing requirements** → /gather-requirements, /formalize-ears
- **Creating test scenarios** → /generate-bdd
- **Organizing work** → /epic-create, /feature-create
- **Viewing structure** → /hierarchy-view
- **Exporting** → epic/feature commands with export: parameter

## 🎓 Best Practices

1. **Start with Questions**: Use `/gather-requirements` to capture complete context
2. **Formalize Early**: Convert to EARS notation while context is fresh
3. **Generate Scenarios**: Create BDD scenarios to validate understanding
4. **Organize Logically**: Structure into meaningful epics and features
5. **Maintain Traceability**: Always link requirements to features and epics
6. **Export Regularly**: Keep PM tools synchronized with latest specifications

## 📊 What require-kit Provides

### ✅ Core Features
- Requirements gathering and formalization (EARS notation)
- BDD/Gherkin scenario generation
- Epic and feature hierarchy management
- Structured markdown files with PM tool metadata
- Requirements traceability and organization

### 🔌 Integration Options
- Optional integration with task execution systems
- PM tool metadata in structured format (ready for export implementation)
- Bidirectional detection with compatible systems
- Technology-agnostic specification output

### 📋 PM Tool Export Status
**Specification Ready**: Epic and feature files include structured frontmatter with fields for PM tool integration (Jira, Linear, GitHub, Azure DevOps). The command specifications define the integration patterns. Actual API integration requires:
- User implementation of API connectors
- MCP server for PM tool integration
- Custom export scripts using the structured metadata

---

*require-kit focuses on requirements management. User-specific configuration (`.claude/` directory) is gitignored - users install and configure agents/commands locally based on their needs.*
