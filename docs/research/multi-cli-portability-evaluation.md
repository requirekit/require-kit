# Multi-CLI Portability Evaluation: Agentecflow Lite

**Date**: 2025-10-19
**Author**: Claude Code Analysis
**Status**: Evaluation Complete - Recommendations Pending
**Related**: Spec Kit (github/spec-kit), Agentecflow Lite

---

## Executive Summary

This document evaluates the feasibility and strategic value of making **Agentecflow Lite** compatible with multiple AI CLI systems beyond Claude Code, following the Spec Kit model which supports 12+ AI coding assistants (Claude Code, GitHub Copilot, Gemini CLI, Cursor, etc.) using a `uvx` installer approach.

**Key Findings**:
- ✅ **High Strategic Value**: Multi-CLI support significantly expands addressable market
- ✅ **Technical Feasibility**: Core architecture is CLI-agnostic markdown/filesystem-based
- ⚠️ **Moderate Effort**: Requires Python packaging, CLI adapter layer, and MCP abstraction
- ⚠️ **Maintenance Overhead**: Supporting 12+ CLI systems requires ongoing compatibility testing

**Recommendation**: **Proceed with phased approach** - Start with 3-4 major CLIs (Claude Code, Copilot, Gemini), validate market demand, then expand.

---

## Table of Contents

1. [Spec Kit Architecture Analysis](#1-spec-kit-architecture-analysis)
2. [Agentecflow Lite Current State](#2-agentecflow-lite-current-state)
3. [Portability Assessment](#3-portability-assessment)
4. [Technical Feasibility Analysis](#4-technical-feasibility-analysis)
5. [Implementation Strategy](#5-implementation-strategy)
6. [Effort Estimation](#6-effort-estimation)
7. [Risk Analysis](#7-risk-analysis)
8. [Strategic Recommendations](#8-strategic-recommendations)

---

## 1. Spec Kit Architecture Analysis

### 1.1 Multi-CLI Integration Model

**How Spec Kit Works**:

```
┌─────────────────────────────────────────────────────────┐
│ Spec Kit CLI (Python)                                   │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ specify init <project> --ai claude|copilot|gemini   │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Core Components:                                        │
│ - Markdown templates (CLI-agnostic)                     │
│ - Slash commands (/speckit.specify, /speckit.plan)      │
│ - File-based state (specs/, tasks/, plans/)             │
│ - Text I/O contract (stdin → stdout/JSON)              │
└─────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        │ AI CLI Detection & Configuration     │
        │ - Detects available CLI tools         │
        │ - Configures slash commands for CLI   │
        │ - Sets up CLI-specific workflows      │
        └──────────────────┬──────────────────┘
                           ↓
    ┌──────────────────────┴────────────────────────┐
    │ Supported AI CLIs (12+)                       │
    ├───────────────────────────────────────────────┤
    │ ✅ Claude Code (Anthropic)                    │
    │ ✅ GitHub Copilot CLI                         │
    │ ✅ Gemini CLI (Google)                        │
    │ ✅ Cursor                                     │
    │ ✅ Qwen Code, opencode, Windsurf, Kilo Code   │
    │ ✅ Auggie CLI, CodeBuddy CLI, Roo Code        │
    │ ✅ Codex CLI                                  │
    │ ⚠️  Amazon Q Developer (limited)              │
    └───────────────────────────────────────────────┘
```

### 1.2 Key Architectural Patterns

**Pattern 1: CLI-Agnostic Core**
- All core logic in Python (platform-independent)
- State stored in markdown files (universal format)
- Commands exposed via slash commands (standard across CLIs)
- Text-based I/O contract (all CLIs support)

**Pattern 2: Installation via uvx**
```bash
# One-time usage (ephemeral)
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>

# Persistent installation
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**Benefits**:
- ✅ No system-wide dependencies (isolated Python environment)
- ✅ Works on Windows, macOS, Linux
- ✅ Single installation command
- ✅ Version pinning and updates via uv

**Pattern 3: AI CLI Initialization Flags**
```bash
specify init my-project --ai claude
specify init my-project --ai copilot
specify init my-project --ai gemini
```

**Effect**: Customizes slash commands and workflows per CLI:
- Claude Code: `/speckit.specify`, `/speckit.plan`
- Copilot: Same commands, different execution context
- Gemini CLI: Same commands, adapted for Gemini's capabilities

**Pattern 4: Markdown-Driven Workflows**
- Specifications: `specs/[feature]/spec.md`
- Plans: `specs/[feature]/plan.md`
- Tasks: `specs/[feature]/tasks.md`
- Templates: `templates/` (CLI-agnostic)

### 1.3 What Makes Spec Kit Portable

| Feature | Implementation | Portability Impact |
|---------|---------------|-------------------|
| **State Management** | Markdown files + filesystem | ✅ Universal (all CLIs read files) |
| **Commands** | Slash commands | ✅ Standard across CLIs |
| **Templates** | Markdown templates with structured prompts | ✅ CLI-agnostic (text-based) |
| **I/O Contract** | Text in (stdin/args) → Text out (stdout/JSON) | ✅ Universal |
| **Installation** | Python package via uv/uvx | ✅ Cross-platform |
| **Configuration** | JSON/YAML config files | ✅ Universal |
| **CLI Detection** | Auto-detect via environment/flags | ✅ Adaptive |

---

## 2. Agentecflow Lite Current State

### 2.1 Architecture Overview

**Current Design** (Claude Code-specific):

```
┌─────────────────────────────────────────────────────────┐
│ Agentecflow Lite (Embedded in Claude Code)              │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ /task-work TASK-XXX [--design-only|--implement-only]│ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Command Implementation:                                 │
│ - installer/global/commands/task-work.md (spec)         │
│ - Claude Code interprets and executes phases            │
│ - No separate CLI binary or Python package              │
│ - State: tasks/{backlog,in_progress,in_review,blocked}/ │
└─────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        │ Installation (Claude Code-specific)  │
        │ - Bash script: installer/scripts/    │
        │ - Symlinks: ~/.claude → ~/.agentecflow │
        │ - Templates: installer/global/templates/ │
        └──────────────────┬──────────────────┘
                           ↓
    ┌──────────────────────┴────────────────────────┐
    │ Supported CLIs (1)                            │
    ├───────────────────────────────────────────────┤
    │ ✅ Claude Code ONLY                           │
    │ ❌ GitHub Copilot (not supported)             │
    │ ❌ Gemini CLI (not supported)                 │
    │ ❌ Cursor, Codex, etc. (not supported)        │
    └───────────────────────────────────────────────┘
```

### 2.2 Core Components

**Component 1: Command Specifications** (Markdown)
- Location: `installer/global/commands/*.md`
- Format: Markdown with structured instructions
- Examples: `task-work.md`, `task-create.md`, `task-status.md`
- **Portability**: ✅ CLI-agnostic (text-based)

**Component 2: Agent Definitions** (Markdown)
- Location: `installer/global/agents/*.md`
- Format: Markdown prompts for specialized agents
- Examples: `architectural-reviewer.md`, `test-verifier.md`
- **Portability**: ✅ CLI-agnostic (all CLIs support prompts)

**Component 3: State Management** (Filesystem)
- Location: `tasks/{backlog,in_progress,in_review,blocked,completed}/`
- Format: Markdown files with YAML frontmatter
- **Portability**: ✅ Universal (file-based)

**Component 4: Templates** (Markdown + Code)
- Location: `installer/global/templates/{react,python,maui,etc.}/`
- Format: Markdown docs + code templates
- **Portability**: ✅ CLI-agnostic

**Component 5: Installation** (Bash Script)
- Location: `installer/scripts/install.sh`
- Format: Bash script (creates symlinks, copies files)
- **Portability**: ⚠️ Unix-only (no Windows support)

### 2.3 Claude Code Dependencies

**Hard Dependencies** (CLI-specific):
1. ❌ **Slash Command Execution**: Relies on Claude Code's `/command` syntax
2. ❌ **MCP Integration**: Uses Claude Code's MCP server protocol
3. ❌ **File Operations**: Assumes Claude Code's file reading/writing tools
4. ❌ **Symlink Strategy**: `~/.claude/` symlinks to `~/.agentecflow/`

**Soft Dependencies** (could be abstracted):
1. ⚠️ **Multi-Agent Orchestration**: Uses Task tool for agent delegation
2. ⚠️ **State Transitions**: Moves files between folders using Claude Code tools
3. ⚠️ **Testing Execution**: Runs tests via Bash tool in Claude Code

### 2.4 Portability-Friendly Aspects

**Already Portable**:
- ✅ Markdown-based command specifications
- ✅ File-based state management
- ✅ Text-based I/O (task descriptions, plans, results)
- ✅ Template-driven workflows
- ✅ Stack-agnostic design (works with any language)

**Would Need Adaptation**:
- ⚠️ Slash command registration (different per CLI)
- ⚠️ MCP server integration (different protocols per CLI)
- ⚠️ Tool invocation (file operations, bash commands)
- ⚠️ Agent orchestration (if CLI doesn't support multi-agent)

---

## 3. Portability Assessment

### 3.1 Portability Matrix

| Component | Current State | Claude Code-Specific? | Portability Effort |
|-----------|--------------|----------------------|-------------------|
| **Command Specs** | Markdown | ❌ No | ✅ Low (already portable) |
| **Agent Definitions** | Markdown | ❌ No | ✅ Low (prompts are universal) |
| **State Management** | Filesystem | ❌ No | ✅ Low (file-based) |
| **Templates** | Markdown + Code | ❌ No | ✅ Low (text-based) |
| **Slash Commands** | `/task-work`, etc. | ✅ Yes | ⚠️ Medium (need CLI adapters) |
| **MCP Integration** | Claude Code MCP | ✅ Yes | 🔴 High (protocol differences) |
| **File Operations** | Claude Code tools | ✅ Yes | ⚠️ Medium (need abstraction layer) |
| **Installation** | Bash script | Partial | ⚠️ Medium (need Python package) |
| **Agent Orchestration** | Task tool | ✅ Yes | 🔴 High (CLI-specific) |

### 3.2 CLI Capability Comparison

| Capability | Claude Code | Copilot | Gemini CLI | Cursor | Priority |
|-----------|------------|---------|-----------|--------|----------|
| **Slash Commands** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | P0 |
| **File Read/Write** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | P0 |
| **Bash Execution** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | P0 |
| **Multi-Agent** | ✅ Task tool | ❌ No | ❌ No | ⚠️ Limited | P1 |
| **MCP Protocol** | ✅ Native | ❌ No | ⚠️ Custom | ⚠️ Custom | P1 |
| **State Tracking** | ✅ Files | ✅ Files | ✅ Files | ✅ Files | P0 |
| **Custom Args** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Limited | P0 |

**Key Insights**:
- ✅ **Core workflow operations** (file I/O, bash, slash commands) are universal
- ⚠️ **Multi-agent orchestration** is Claude Code-specific (would need fallback)
- ⚠️ **MCP integration** varies significantly across CLIs
- ✅ **State management** (file-based) works everywhere

### 3.3 Feature Portability by CLI

**Tier 1 Features** (Portable across all CLIs):
- ✅ Complexity Evaluation (Phase 2.7)
- ✅ Design-First Workflow (--design-only, --implement-only)
- ✅ Test Enforcement Loop (Phase 4.5)
- ✅ Plan Audit (Phase 5.5)
- ✅ State Management (BACKLOG → IN_PROGRESS → IN_REVIEW)

**Tier 2 Features** (Requires adaptation per CLI):
- ⚠️ Architectural Review (Phase 2.5B) - needs LLM prompt execution
- ⚠️ Human Checkpoints (Phase 2.8) - needs interactive input
- ⚠️ Iterative Refinement (/task-refine) - needs command registration

**Tier 3 Features** (Claude Code-specific, hard to port):
- 🔴 MCP Tool Discovery (Phase 2.8) - MCP protocol varies
- 🔴 Design System Detection (Figma, Zeplin) - MCP-dependent
- 🔴 Multi-Agent Orchestration - Task tool is Claude Code-specific

---

## 4. Technical Feasibility Analysis

### 4.1 Required Architectural Changes

**Change 1: Python CLI Package** (like Spec Kit)

**Current**: Bash script installer + markdown command specs
**Target**: Python package installable via `uvx`

```python
# pyproject.toml
[project]
name = "agentecflow-lite"
version = "1.0.0"
description = "Lightweight task workflow for AI coding assistants"
dependencies = [
    "typer",      # CLI framework
    "rich",       # Terminal formatting
    "pyyaml",     # YAML parsing
    "platformdirs" # Cross-platform paths
]

[project.scripts]
agentecflow = "agentecflow_lite:main"
```

**CLI Entry Point**:
```python
# src/agentecflow_lite/cli.py
import typer
app = typer.Typer()

@app.command()
def init(
    project_name: str,
    ai: str = typer.Option("claude", help="AI CLI to use"),
    template: str = typer.Option("default", help="Project template")
):
    """Initialize Agentecflow Lite project for specified AI CLI."""
    # Detect AI CLI capabilities
    # Configure slash commands for that CLI
    # Create project structure
    pass

@app.command()
def task_work(task_id: str, design_only: bool = False, implement_only: bool = False):
    """Execute task workflow (delegates to AI CLI)."""
    # Load task file
    # Generate prompt for AI CLI
    # Execute workflow phases
    pass
```

**Change 2: CLI Adapter Layer**

**Purpose**: Abstract CLI-specific operations behind common interface

```python
# src/agentecflow_lite/adapters/base.py
from abc import ABC, abstractmethod

class CLIAdapter(ABC):
    """Base adapter for AI CLI integration."""

    @abstractmethod
    def register_command(self, name: str, spec_path: str):
        """Register slash command with CLI."""
        pass

    @abstractmethod
    def execute_prompt(self, prompt: str) -> str:
        """Execute prompt and return response."""
        pass

    @abstractmethod
    def read_file(self, path: str) -> str:
        """Read file contents."""
        pass

    @abstractmethod
    def write_file(self, path: str, content: str):
        """Write file contents."""
        pass

# src/agentecflow_lite/adapters/claude_code.py
class ClaudeCodeAdapter(CLIAdapter):
    """Adapter for Claude Code."""

    def register_command(self, name: str, spec_path: str):
        # Create symlink in ~/.claude/commands/
        # Or copy markdown file
        pass

    def execute_prompt(self, prompt: str) -> str:
        # Use Task tool for agent invocation
        pass

# src/agentecflow_lite/adapters/copilot.py
class CopilotAdapter(CLIAdapter):
    """Adapter for GitHub Copilot CLI."""

    def register_command(self, name: str, spec_path: str):
        # Register in Copilot's command registry
        pass

    def execute_prompt(self, prompt: str) -> str:
        # Use Copilot's chat API
        pass
```

**Change 3: MCP Abstraction Layer**

**Current**: Direct MCP tool invocation via Claude Code
**Target**: Optional MCP integration with fallback

```python
# src/agentecflow_lite/mcp/manager.py
class MCPManager:
    """Manage MCP tool discovery and invocation with graceful fallback."""

    def __init__(self, cli_adapter: CLIAdapter):
        self.adapter = cli_adapter
        self.available_tools = self._discover_tools()

    def _discover_tools(self) -> dict:
        """Discover available MCP tools for current CLI."""
        try:
            # Try to detect MCP servers
            # Claude Code: Check ~/.claude/mcp_servers.json
            # Others: Check CLI-specific configs
            return discovered_tools
        except Exception:
            # No MCP support in this CLI
            return {}

    def invoke_tool(self, tool_name: str, params: dict) -> dict:
        """Invoke MCP tool with fallback to manual workflow."""
        if tool_name in self.available_tools:
            # Use MCP protocol
            return self._invoke_mcp(tool_name, params)
        else:
            # Fallback: Prompt user for manual steps
            return self._manual_fallback(tool_name, params)
```

### 4.2 Installation Workflow

**Spec Kit Pattern** (uvx):
```bash
# One-time usage
uvx --from git+https://github.com/appmilla/agentecflow-lite.git agentecflow init my-project --ai claude

# Persistent installation
uv tool install agentecflow-lite --from git+https://github.com/appmilla/agentecflow-lite.git

# Usage after installation
agentecflow init my-project --ai copilot
agentecflow task-work TASK-001
```

**Proposed Agentecflow Lite Workflow**:
```bash
# Step 1: Install CLI tool
uvx --from git+https://github.com/appmilla/agentecflow-lite.git agentecflow init my-project --ai claude

# Step 2: AI CLI detects commands automatically
# Claude Code: ~/.claude/commands/task-work.md
# Copilot: ~/.config/copilot/commands/task-work.json
# Gemini: ~/.config/gemini/slash-commands/task-work.md

# Step 3: Use commands in AI CLI
/task-work TASK-001
/task-create "Fix authentication bug"
/task-status
```

### 4.3 Command Registration by CLI

| CLI | Command Storage | Format | Registration Method |
|-----|----------------|--------|-------------------|
| **Claude Code** | `~/.claude/commands/` | Markdown | Symlink/Copy .md files |
| **GitHub Copilot** | `.github/.copilot/commands/` | JSON | JSON schema definition |
| **Gemini CLI** | `~/.config/gemini/commands/` | Markdown | Markdown with metadata |
| **Cursor** | `.cursor/commands/` | Markdown | Similar to Claude Code |

**Universal Approach**: Generate CLI-specific command files from markdown templates

```python
def register_commands(cli: str, commands_dir: Path):
    """Register all commands for specified CLI."""
    for cmd_file in (TEMPLATE_DIR / "commands").glob("*.md"):
        if cli == "claude":
            # Symlink to ~/.claude/commands/
            register_claude_command(cmd_file)
        elif cli == "copilot":
            # Convert to JSON and register
            register_copilot_command(cmd_file)
        elif cli == "gemini":
            # Copy to ~/.config/gemini/commands/
            register_gemini_command(cmd_file)
```

---

## 5. Implementation Strategy

### 5.1 Phased Rollout Plan

**Phase 1: Core Portability Infrastructure** (4-6 weeks)
- Create Python package structure (`pyproject.toml`)
- Implement CLI adapter abstraction layer
- Build adapters for Claude Code, Copilot, Gemini (top 3)
- Port installation to `uvx` installer
- Create cross-platform tests (Windows, macOS, Linux)

**Phase 2: Command Adaptation** (3-4 weeks)
- Refactor command specifications to be CLI-agnostic
- Implement command registration for each CLI
- Create CLI-specific command translators
- Test slash commands across 3 CLIs

**Phase 3: MCP Abstraction** (2-3 weeks)
- Build MCP abstraction layer with fallback
- Implement graceful degradation for CLIs without MCP
- Test design system integration (Figma, Zeplin) on Claude Code
- Implement manual fallback workflows for other CLIs

**Phase 4: Testing & Documentation** (2-3 weeks)
- Comprehensive testing across 3 CLIs
- Update documentation for multi-CLI usage
- Create CLI-specific quick start guides
- Build compatibility matrix documentation

**Phase 5: Expansion to Additional CLIs** (4-6 weeks)
- Add Cursor adapter
- Add Codex CLI adapter
- Add Windsurf, Qwen, others (based on demand)
- Continuous integration tests for all supported CLIs

**Total Estimated Duration**: 15-22 weeks (4-5.5 months)

### 5.2 Technical Milestones

**Milestone 1: Python Package Release** (Week 6)
- Deliverable: `agentecflow-lite` installable via `uvx`
- Success Criteria: Installation works on Windows, macOS, Linux
- Test: `uvx --from git+... agentecflow init test-project --ai claude`

**Milestone 2: Multi-CLI Command Support** (Week 10)
- Deliverable: `/task-work` command works in Claude Code, Copilot, Gemini
- Success Criteria: All 3 CLIs can execute full workflow
- Test: Run same task in all 3 CLIs, verify state transitions

**Milestone 3: Feature Parity** (Week 13)
- Deliverable: 9 core features work across 3 CLIs
- Success Criteria: Complexity, Design-First, Test Enforcement all functional
- Test: Comprehensive feature matrix testing

**Milestone 4: Public Beta** (Week 16)
- Deliverable: Public release for 3 CLIs
- Success Criteria: 50+ users testing across different CLIs
- Test: User feedback, bug reports, compatibility issues

**Milestone 5: Full CLI Support** (Week 22)
- Deliverable: 10+ CLIs supported
- Success Criteria: Feature parity across all CLIs (with documented exceptions)
- Test: Automated compatibility testing in CI/CD

### 5.3 Backward Compatibility Strategy

**Guarantee**: Existing Claude Code users should have zero breaking changes

**Approach 1: Dual Installation Support**
```bash
# Option A: Legacy bash installer (Claude Code only)
./installer/scripts/install.sh

# Option B: New uvx installer (multi-CLI)
uvx --from git+... agentecflow init --ai claude
```

**Approach 2: Auto-Detection**
```python
def detect_installation_method():
    """Detect if user is using legacy or new installation."""
    if Path.home() / ".agentecflow" / "legacy_marker" exists:
        return "legacy"  # Use bash installer flow
    else:
        return "modern"  # Use Python CLI flow
```

**Migration Path**:
1. Keep bash installer for 6 months (v1.x)
2. Add deprecation warnings in v2.0
3. Remove bash installer in v3.0 (12+ months out)
4. Provide automated migration tool: `agentecflow migrate-from-legacy`

---

## 6. Effort Estimation

### 6.1 Development Effort Breakdown

| Task | Complexity | Estimated Effort | Dependencies |
|------|-----------|-----------------|--------------|
| **Python Package Structure** | Medium | 1-2 weeks | None |
| **CLI Adapter Abstraction** | High | 2-3 weeks | Package structure |
| **Claude Code Adapter** | Medium | 1 week | CLI abstraction |
| **Copilot Adapter** | High | 2 weeks | CLI abstraction |
| **Gemini Adapter** | High | 2 weeks | CLI abstraction |
| **MCP Abstraction Layer** | High | 2-3 weeks | CLI adapters |
| **Command Registration** | Medium | 1-2 weeks | CLI adapters |
| **State Management Refactor** | Low | 1 week | None |
| **Installation (uvx)** | Medium | 1 week | Package structure |
| **Testing (3 CLIs)** | High | 2-3 weeks | All adapters |
| **Documentation** | Medium | 1-2 weeks | Testing complete |
| **CI/CD Multi-CLI Tests** | Medium | 1 week | Testing complete |

**Total Effort**: 18-27 weeks (4.5-6.5 months) for core team of 2-3 developers

### 6.2 Resource Requirements

**Team Composition**:
- **Lead Architect**: 1 FTE (full-time) - CLI abstraction, architecture decisions
- **Python Developer**: 1-2 FTE - Adapters, MCP layer, testing
- **DevOps Engineer**: 0.5 FTE - CI/CD, cross-platform testing
- **Technical Writer**: 0.5 FTE - Documentation, migration guides

**Infrastructure**:
- GitHub Actions CI/CD (multi-platform testing)
- Test accounts for all supported CLIs
- Test environments (Windows, macOS, Linux)

### 6.3 Maintenance Effort (Ongoing)

**Per CLI Supported**:
- Initial adapter development: 1-2 weeks
- Ongoing maintenance: 1-2 hours/week
- Breaking changes (CLI updates): 4-8 hours/quarter

**Total Maintenance** (10 CLIs):
- Initial: 10-20 weeks (spread over months)
- Ongoing: 10-20 hours/week (bug fixes, updates)
- Major updates: 40-80 hours/quarter

---

## 7. Risk Analysis

### 7.1 Technical Risks

**Risk 1: CLI Capability Gaps**
- **Severity**: High
- **Likelihood**: Medium
- **Description**: Some CLIs may lack features needed for full workflow (e.g., multi-agent orchestration)
- **Mitigation**:
  - Document feature matrix per CLI
  - Implement graceful degradation (e.g., manual steps instead of MCP)
  - Clearly communicate limitations in documentation

**Risk 2: Breaking Changes in CLIs**
- **Severity**: High
- **Likelihood**: High (CLIs evolve rapidly)
- **Description**: Updates to supported CLIs could break adapters
- **Mitigation**:
  - Automated compatibility testing in CI/CD
  - Version pinning for known-good CLI versions
  - Community monitoring for CLI updates

**Risk 3: MCP Protocol Fragmentation**
- **Severity**: Medium
- **Likelihood**: High
- **Description**: MCP implementation varies significantly across CLIs (or doesn't exist)
- **Mitigation**:
  - MCP abstraction layer with fallback
  - Manual workflow alternatives for non-MCP CLIs
  - Focus on core features that don't require MCP

**Risk 4: Performance Degradation**
- **Severity**: Medium
- **Likelihood**: Low
- **Description**: Abstraction layers could slow down workflow execution
- **Mitigation**:
  - Benchmark against current Claude Code implementation
  - Optimize hot paths (file I/O, state transitions)
  - Profile and optimize adapter layer

### 7.2 Strategic Risks

**Risk 5: Market Fragmentation**
- **Severity**: Medium
- **Likelihood**: Medium
- **Description**: Supporting too many CLIs spreads development thin, dilutes quality
- **Mitigation**:
  - Start with top 3 CLIs (80% of market)
  - Add CLIs incrementally based on demand
  - Maintain tiered support (Tier 1: Full, Tier 2: Partial, Tier 3: Community)

**Risk 6: User Confusion**
- **Severity**: Medium
- **Likelihood**: Medium
- **Description**: Multi-CLI support adds complexity, confuses users about which CLI to use
- **Mitigation**:
  - Clear decision matrix in documentation
  - CLI-specific quick start guides
  - Default to Claude Code for new users (preserve current UX)

**Risk 7: Maintenance Burden**
- **Severity**: High
- **Likelihood**: High
- **Description**: Supporting 10+ CLIs requires ongoing effort, could become unsustainable
- **Mitigation**:
  - Community contributions for adapters (open source model)
  - Deprecation policy for low-usage CLIs
  - Automated testing to catch regressions early

### 7.3 Competitive Risks

**Risk 8: Spec Kit Competition**
- **Severity**: Medium
- **Likelihood**: Medium
- **Description**: Spec Kit already has multi-CLI support, first-mover advantage
- **Mitigation**:
  - Differentiate on lightweight philosophy (Agentecflow Lite vs Full Spec Kit)
  - Target different user segments (solo devs vs enterprise teams)
  - Highlight unique features (architectural review, test enforcement)

**Risk 9: CLI Consolidation**
- **Severity**: Low
- **Likelihood**: Medium
- **Description**: Market consolidation could reduce need for multi-CLI support
- **Mitigation**:
  - Focus on 3-4 dominant CLIs (Claude Code, Copilot, Gemini)
  - Prepare for future with modular adapter system (easy to add/remove CLIs)

---

## 8. Strategic Recommendations

### 8.1 Go/No-Go Decision Framework

**GO Criteria** (Must meet ALL):
- ✅ **Market Demand**: Clear evidence that users want multi-CLI support (surveys, GitHub issues, feature requests)
- ✅ **Resource Availability**: Team capacity to support 4-6 month development effort
- ✅ **Technical Feasibility**: Validation that core features work across 3+ CLIs (PoC successful)
- ✅ **Strategic Alignment**: Multi-CLI support aligns with product vision and roadmap

**NO-GO Criteria** (Any one triggers reconsideration):
- ❌ **Low Demand**: <10% of users express interest in non-Claude Code CLIs
- ❌ **Resource Constraints**: Team lacks capacity for 4-6 month effort
- ❌ **Technical Blockers**: PoC reveals fundamental incompatibilities
- ❌ **Strategic Misalignment**: Multi-CLI support diverts from core product priorities

### 8.2 Recommended Approach

**Recommendation: Phased "Validate-Then-Scale" Strategy**

**Phase 0: Validation** (2-4 weeks)
1. **User Research**: Survey Claude Code users about CLI preferences
   - "Which AI coding assistant do you use?" (Claude Code, Copilot, Gemini, Cursor, Other)
   - "Would you use Agentecflow Lite with [other CLI]?" (Yes/No/Maybe)
   - Target: 100+ responses, >30% interest in multi-CLI

2. **Technical PoC**: Build minimal adapter for 1 non-Claude CLI (e.g., Copilot)
   - Implement `/task-work` command in Copilot
   - Test core workflow (BACKLOG → IN_PROGRESS → IN_REVIEW)
   - Validate: Can achieve feature parity with <2 weeks effort?

3. **Market Analysis**: Research Spec Kit adoption and feedback
   - GitHub stars, issues, community discussions
   - Identify pain points and opportunities to differentiate

**Decision Point 1** (End of Phase 0):
- **If validation succeeds** (demand + technical feasibility): Proceed to Phase 1 (Core Infrastructure)
- **If validation fails**: Stop here, focus on improving Claude Code experience

**Phase 1: Core Infrastructure** (4-6 weeks)
- Python package structure
- CLI adapter abstraction
- Adapters for top 3 CLIs (Claude Code, Copilot, Gemini)
- uvx installer

**Decision Point 2** (End of Phase 1):
- **If infrastructure stable**: Proceed to Phase 2 (Command Adaptation)
- **If major technical issues**: Re-evaluate approach, consider alternative architectures

**Phase 2: Command Adaptation** (3-4 weeks)
- Refactor commands to be CLI-agnostic
- Implement command registration for 3 CLIs
- Test core workflows across all 3

**Decision Point 3** (End of Phase 2):
- **If feature parity achieved**: Proceed to Phase 3 (Beta Release)
- **If gaps remain**: Decide whether to continue or pivot

**Phase 3: Beta Release** (2-3 weeks)
- Public beta for 3 CLIs
- Gather user feedback
- Monitor adoption metrics

**Decision Point 4** (End of Phase 3):
- **If beta successful** (>50 users, >80% positive feedback): Proceed to Phase 4 (Expansion)
- **If beta struggles**: Re-evaluate market fit, consider alternative positioning

**Phase 4: Expansion** (4-6 weeks)
- Add 3-5 more CLIs (Cursor, Codex, Windsurf, etc.)
- Comprehensive testing and documentation
- Public v1.0 release

### 8.3 Alternative Approaches

**Alternative 1: "Claude Code First, Others Later"**
- Continue focusing exclusively on Claude Code for 6-12 months
- Monitor market for clear signals that multi-CLI is essential
- Re-evaluate based on competitive pressure and user demand
- **Pros**: Lower risk, preserves focus, faster iteration on core features
- **Cons**: Misses first-mover advantage, cedes market to Spec Kit

**Alternative 2: "Partnership with Spec Kit"**
- Instead of building multi-CLI support, integrate Agentecflow Lite into Spec Kit
- Contribute Agentecflow Lite features as Spec Kit plugins/extensions
- Position as "Spec Kit Lite" or complementary offering
- **Pros**: Leverage existing multi-CLI infrastructure, faster time-to-market, community support
- **Cons**: Loss of product independence, dependent on Spec Kit roadmap

**Alternative 3: "Copilot-Only Expansion"**
- Target GitHub Copilot specifically (largest market share after Claude Code)
- Build deep integration with Copilot ecosystem
- Prove multi-CLI viability with single alternative CLI
- **Pros**: Focused effort, clear market opportunity, validates approach
- **Cons**: Limited to 2 CLIs, may still require abstraction layer

### 8.4 Final Recommendation

**Recommendation**: **Proceed with "Validate-Then-Scale" Strategy, Starting with Phase 0 (Validation)**

**Justification**:
1. **Strategic Alignment**: Multi-CLI support expands addressable market significantly (Copilot has 1M+ users, Gemini growing rapidly)
2. **Competitive Positioning**: Spec Kit validates market demand; Agentecflow Lite can differentiate on lightweight philosophy
3. **Technical Feasibility**: Core architecture is already CLI-agnostic (markdown, filesystem, text I/O)
4. **Risk Management**: Phased approach with decision points minimizes wasted effort

**Success Metrics** (Phase 0 Validation):
- **User Research**: >30% of respondents interested in multi-CLI support
- **Technical PoC**: /task-work command working in Copilot within 2 weeks
- **Market Analysis**: Spec Kit showing strong adoption (>500 GitHub stars, active community)

**Timeline**:
- **Phase 0 (Validation)**: Weeks 1-4
- **Decision Point 1**: End of Week 4
- **Phase 1 (Infrastructure)**: Weeks 5-10 (if validation succeeds)
- **Phase 2 (Commands)**: Weeks 11-14
- **Phase 3 (Beta)**: Weeks 15-17
- **Phase 4 (Expansion)**: Weeks 18-23
- **Public Release**: Week 24

**Resource Commitment** (Phase 0):
- 1 FTE developer (PoC)
- 0.5 FTE researcher (user survey, market analysis)
- Budget: Minimal (developer time only)

**Go/No-Go Decision**: End of Week 4
- **If validation succeeds**: Commit to full 6-month effort, allocate 2-3 FTE
- **If validation fails**: Stop multi-CLI effort, focus resources on Claude Code enhancements

---

## 9. Appendix

### 9.1 Comparison: Agentecflow Lite vs Spec Kit

| Aspect | Agentecflow Lite (Current) | Spec Kit | Multi-CLI Agentecflow Lite (Proposed) |
|--------|---------------------------|----------|-------------------------------------|
| **CLIs Supported** | 1 (Claude Code) | 12+ | 3-10 (phased rollout) |
| **Installation** | Bash script | uvx (Python) | uvx (Python) |
| **State Management** | Filesystem | Filesystem | Filesystem |
| **Workflow Phases** | 9 features, 6 phases | 4 phases | 9 features, 6 phases |
| **Requirements** | Task descriptions | EARS notation | Task descriptions (lighter) |
| **Test Specs** | Test code | BDD/Gherkin | Test code |
| **Complexity** | Lightweight | Comprehensive | Lightweight |
| **Setup Time** | 5 min | 2-4 hours | 5-10 min |
| **Per-Task Overhead** | 10-15 min | 30-60 min | 10-20 min |
| **Quality Gates** | Strong | Comprehensive | Strong |
| **MCP Integration** | Claude Code MCP | CLI-specific | Abstracted with fallback |
| **Multi-Agent** | Claude Code Task tool | No | Optional (CLI-dependent) |

### 9.2 CLI Market Share (Estimated)

Based on industry research and community discussions (2025):

| AI CLI | Estimated Users | Market Share | Priority |
|--------|----------------|--------------|----------|
| **GitHub Copilot** | 1M+ | 40-50% | P0 |
| **Claude Code** | 100K+ | 10-15% | P0 |
| **Cursor** | 200K+ | 15-20% | P0 |
| **Gemini CLI** | 50K+ | 5-10% | P1 |
| **Codex** | 30K+ | 3-5% | P2 |
| **Others** | 50K+ | 5-10% | P3 |

**Note**: Market share estimates based on GitHub activity, community discussions, and public announcements.

### 9.3 References

- **Spec Kit GitHub**: https://github.com/github/spec-kit
- **Spec Kit Docs**: https://github.com/github/spec-kit/blob/main/spec-driven.md
- **Agentecflow Lite Guide**: [docs/guides/agentecflow-lite-workflow.md](../guides/agentecflow-lite-workflow.md)
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **uv Installer**: https://docs.astral.sh/uv/

---

**Document Status**: ✅ Complete - Ready for review and decision
**Next Steps**: Present to stakeholders → Conduct Phase 0 validation → Decision Point 1
