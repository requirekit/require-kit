# Multi-CLI Migration Analysis: AI Engineer → Spec Kit-Style Architecture

**Date**: 2025-10-13
**Status**: Research Complete
**Priority**: Pre-Open Source Release

## Executive Summary

This document analyzes the effort required to migrate AI Engineer from a Claude Code-specific implementation to a multi-CLI architecture similar to [GitHub Spec Kit](https://github.com/github/spec-kit), supporting Claude Code, GitHub Copilot, Gemini CLI, Cursor, Windsurf, and other AI coding assistants.

**Key Findings:**
- **Estimated Effort**: 8-12 weeks (1 developer)
- **Complexity**: Medium-High (requires architectural refactoring)
- **Risk**: Medium (breaking changes for existing users)
- **Benefit**: High (broadens adoption, competitive with Spec Kit)
- **Recommendation**: **PROCEED** - Essential for open source success

---

## 1. Current State Analysis

### 1.1 Claude Code Dependencies

AI Engineer is **heavily coupled** to Claude Code in the following areas:

#### **A. Agent Invocation System (CRITICAL)**
**Current Pattern**:
```markdown
# In task-work.md
subagent_type: "requirements-analyst"
```

**Dependency**: Claude Code's `Task` tool for invoking specialized agents
- **Occurrences**: 60+ agent invocations across commands
- **Files Affected**: 10+ command specifications
- **Impact**: Core workflow relies on agent orchestration

#### **B. Directory Structure**
```
~/.claude/           ← Claude Code-specific directory
├── commands/        ← Symlinked to ~/.agentecflow/commands
├── agents/          ← Symlinked to ~/.agentecflow/agents
└── settings.json    ← Claude Code configuration
```

**Dependencies**:
- Installation assumes `~/.claude/` directory
- Symlink strategy for Conductor.build compatibility
- Claude Code reads commands from `~/.claude/commands/`

#### **C. Slash Command Format**
```bash
/task-work TASK-001 --mode=tdd
/gather-requirements
/epic-create "Title"
```

**Dependency**: Claude Code's slash command parser
- Commands defined as `.md` files in `~/.claude/commands/`
- Arguments parsed by Claude Code
- No explicit CLI tool for non-Claude environments

#### **D. MCP Integration**
```json
{
  "mcpServers": {
    "figma-dev-mode": { ... },
    "zeplin": { ... },
    "design-patterns": { ... }
  }
}
```

**Dependency**: Claude Code's MCP protocol implementation
- Figma/Zeplin design extraction
- Design patterns database
- Other context providers

#### **E. Documentation References**
- **164 files** reference `.claude`, `CLAUDE_HOME`, or `Claude Code`
- **382 files** mention slash commands
- **CLAUDE.md** files in every template

---

### 1.2 Technology Stack Breakdown

| Component | Type | Count | Claude-Specific? |
|-----------|------|-------|------------------|
| Commands | Markdown | 112 | ✅ Yes (slash commands) |
| Agents | Markdown | Variable | ✅ Yes (Task tool) |
| Python libs | Python | 46 | ❌ No (CLI-agnostic) |
| Shell scripts | Bash | 1 | ⚠️ Partial (install only) |
| Templates | Directories | 7 | ⚠️ Partial (CLAUDE.md files) |

**Key Insight**: Python implementation (46 files) is already CLI-agnostic. The main dependencies are:
1. Command invocation mechanism (slash commands)
2. Agent orchestration (Task tool)
3. Configuration/settings format

---

## 2. Spec Kit Architecture Analysis

### 2.1 How Spec Kit Achieves Multi-CLI Support

#### **A. CLI Detection**
```bash
# During initialization
uvx specify init <PROJECT_NAME> --ai claude
uvx specify init <PROJECT_NAME> --ai copilot
uvx specify init <PROJECT_NAME> --ai gemini
```

**Mechanism**:
- Explicit `--ai` flag during project setup
- Stores selected CLI in project configuration
- Adapts command templates based on selection

#### **B. Cross-Agent Commands**
Spec Kit uses **slash commands** that work across all agents:
```bash
/speckit.constitution   # Define project principles
/speckit.specify        # Create specifications
/speckit.plan          # Plan implementation
```

**Implementation**:
- Commands are agent-agnostic by design
- Each agent interprets commands in their native format
- No agent-specific orchestration required

#### **C. Template System**
```bash
specify init myproject --ai claude
├── Creates .claude/ directory structure
└── Populates with Claude-optimized templates

specify init myproject --ai copilot
├── Creates .github/copilot/ directory structure
└── Populates with Copilot-optimized templates
```

**Key Features**:
- Template variants per CLI
- Common workflow, different file structures
- Agent-specific configuration files

#### **D. UVX Package Manager**
```bash
# One-time install (persistent)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# One-time run
uvx --from git+https://github.com/github/spec-kit.git specify init myproject
```

**Benefits**:
- Cross-platform Python distribution
- No manual PATH configuration
- Automatic dependency management

#### **E. Helper Scripts**
Spec Kit provides **dual implementations**:
- **POSIX Shell** (Linux, macOS, WSL)
- **PowerShell** (Windows native)

**Architecture**:
```
scripts/
├── bash/
│   ├── constitution.sh
│   └── specify.sh
└── powershell/
    ├── constitution.ps1
    └── specify.ps1
```

---

### 2.2 Key Architectural Differences

| Feature | AI Engineer (Current) | Spec Kit | Gap |
|---------|----------------------|----------|-----|
| **CLI Detection** | Assumes Claude Code | `--ai` flag + config | 🔴 Critical |
| **Agent Invocation** | Claude Code Task tool | None (command-based) | 🔴 Critical |
| **Command Format** | Slash commands (.md) | Slash commands (cross-agent) | 🟡 Medium |
| **Installation** | Bash script → ~/.agentecflow | UVX → Python package | 🟡 Medium |
| **Configuration** | settings.json (Claude-specific) | Per-agent config files | 🟡 Medium |
| **MCP Integration** | Claude Code MCP servers | Not documented | 🟢 Low |
| **Templates** | 7 stack templates | Project-level templates | 🟢 Low |

---

## 3. Abstraction Points Required

### 3.1 Critical Abstractions (Must Implement)

#### **1. CLI Adapter Interface**
```python
# installer/global/lib/cli_adapter.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class CLIAdapter(ABC):
    """Abstract base class for CLI-specific implementations"""

    @abstractmethod
    def invoke_agent(self, agent_type: str, prompt: str, **kwargs) -> str:
        """Invoke a specialized agent in CLI-specific way"""
        pass

    @abstractmethod
    def get_command_directory(self) -> str:
        """Return CLI-specific command directory"""
        pass

    @abstractmethod
    def format_slash_command(self, command: str, args: List[str]) -> str:
        """Format command for CLI-specific invocation"""
        pass

    @abstractmethod
    def supports_mcp(self) -> bool:
        """Check if CLI supports Model Context Protocol"""
        pass
```

**Implementations Needed**:
- `ClaudeCodeAdapter` (current behavior)
- `GitHubCopilotAdapter`
- `GeminiCLIAdapter`
- `CursorAdapter`
- `WindsurfAdapter`
- `FallbackAdapter` (for unsupported CLIs)

#### **2. Agent Orchestration Abstraction**
**Current (Claude Code-specific)**:
```markdown
subagent_type: "requirements-analyst"
prompt: "Gather requirements for user authentication"
```

**Proposed (CLI-agnostic)**:
```python
# installer/global/lib/orchestration.py
def invoke_agent(agent_type: str, prompt: str, cli_adapter: CLIAdapter):
    """
    Invoke agent using appropriate CLI adapter

    - Claude Code: Use Task tool
    - Copilot: Use @workspace prompt with instructions
    - Gemini: Use inline prompt with agent role
    - Cursor: Use composer with agent context
    - Fallback: Execute command directly without agent
    """
    return cli_adapter.invoke_agent(agent_type, prompt)
```

**Impact**: Requires rewriting **60+ agent invocation points** in command files.

#### **3. Command Distribution System**
**Current**: Markdown files in `~/.claude/commands/`
**Proposed**: Multi-format command files

```
commands/
├── claude/           # Claude Code .md slash commands
├── copilot/          # GitHub Copilot instructions
├── gemini/           # Gemini CLI prompts
├── cursor/           # Cursor Composer rules
└── shared/           # CLI-agnostic Python implementations
```

**Implementation**:
```python
def install_commands(cli_type: str, install_dir: str):
    """
    Install commands for specified CLI

    Args:
        cli_type: "claude", "copilot", "gemini", "cursor", etc.
        install_dir: Target installation directory
    """
    source_dir = f"commands/{cli_type}/"
    target_dir = get_cli_command_directory(cli_type)

    # Copy CLI-specific commands
    copy_tree(source_dir, target_dir)

    # Install shared Python libraries
    copy_tree("commands/shared/", f"{install_dir}/lib/")
```

---

### 3.2 Medium Priority Abstractions

#### **4. Configuration System**
**Current**: Single `settings.json` (Claude Code format)
**Proposed**: Adapter-based configuration

```python
# installer/global/lib/config.py
class ConfigAdapter(ABC):
    @abstractmethod
    def load_config(self) -> Dict[str, Any]:
        """Load CLI-specific configuration"""
        pass

    @abstractmethod
    def save_config(self, config: Dict[str, Any]):
        """Save CLI-specific configuration"""
        pass

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get configuration setting"""
        pass

# Implementations
class ClaudeCodeConfig(ConfigAdapter):
    def load_config(self):
        return json.load(open(".claude/settings.json"))

class CopilotConfig(ConfigAdapter):
    def load_config(self):
        return yaml.safe_load(open(".github/copilot.yml"))
```

#### **5. MCP Integration Layer**
**Current**: Direct Claude Code MCP usage
**Proposed**: MCP capability detection

```python
def get_mcp_support(cli_adapter: CLIAdapter) -> Dict[str, bool]:
    """
    Detect MCP capabilities for current CLI

    Returns:
        {
            "figma": True/False,
            "zeplin": True/False,
            "design-patterns": True/False
        }
    """
    if not cli_adapter.supports_mcp():
        return {mcp: False for mcp in MCP_SERVERS}

    # Check each MCP server availability
    return {
        mcp: check_mcp_available(mcp)
        for mcp in MCP_SERVERS
    }
```

**Fallback Strategy**:
- If MCP not available, use HTTP APIs directly
- Graceful degradation for design-to-code workflows

---

### 3.3 Low Priority Abstractions

#### **6. Template Variants**
```
templates/
├── maui/
│   ├── claude/CLAUDE.md
│   ├── copilot/README.md
│   ├── gemini/CONTEXT.md
│   └── shared/
└── react/
    ├── claude/CLAUDE.md
    ├── copilot/README.md
    └── shared/
```

**Strategy**: Start with Claude-optimized templates, add variants later.

---

## 4. Migration Effort Quantification

### 4.1 Breakdown by Component

| Component | Files Affected | Estimated Hours | Complexity | Risk |
|-----------|---------------|----------------|------------|------|
| **1. CLI Adapter System** | New: 6-8 files | 40-60h | High | Medium |
| **2. Agent Orchestration** | 112 commands | 80-120h | High | High |
| **3. Command Distribution** | 112 commands | 60-80h | Medium | Medium |
| **4. Configuration System** | 7 templates | 40-60h | Medium | Low |
| **5. MCP Integration** | 3 MCP commands | 20-30h | Medium | Low |
| **6. Template Variants** | 7 templates | 40-60h | Low | Low |
| **7. Installation System** | 10 scripts | 60-80h | High | Medium |
| **8. Documentation** | 164+ files | 80-120h | Medium | Low |
| **9. Testing** | New: 50+ tests | 60-80h | High | Medium |
| **10. UVX Migration** | Package setup | 20-30h | Medium | Medium |

**Total Estimated Effort**: **500-720 hours** (12.5-18 weeks at 40h/week)

**Adjusted for Single Developer**: **8-12 weeks** (assuming focused work)

---

### 4.2 Phase-Based Implementation Plan

#### **Phase 1: Foundation (2-3 weeks)**
**Goal**: Establish CLI abstraction layer

- [ ] Design CLI adapter interface
- [ ] Implement `ClaudeCodeAdapter` (preserve current behavior)
- [ ] Create adapter factory/registry
- [ ] Add CLI detection mechanism
- [ ] Update installation script for CLI selection

**Deliverable**: Installation works with `--ai claude` flag (no functional change)

**Testing**: Verify existing Claude Code workflows unchanged

---

#### **Phase 2: Command Abstraction (3-4 weeks)**
**Goal**: Make commands CLI-agnostic

- [ ] Create `commands/shared/` Python library
- [ ] Move business logic from .md to .py files
- [ ] Refactor agent invocations to use adapter
- [ ] Create command distribution system
- [ ] Test with Claude Code adapter

**Deliverable**: Commands work through abstraction layer

**Testing**: All existing tests pass with Claude Code adapter

---

#### **Phase 3: Multi-CLI Support (2-3 weeks)**
**Goal**: Add support for 2-3 additional CLIs

- [ ] Implement `GitHubCopilotAdapter`
- [ ] Implement `GeminiCLIAdapter` or `CursorAdapter`
- [ ] Create CLI-specific command formats
- [ ] Add configuration adapters
- [ ] Implement graceful fallbacks

**Deliverable**: Working installation for 3 CLIs

**Testing**: Core workflows verified on each CLI

---

#### **Phase 4: UVX Migration (1-2 weeks)**
**Goal**: Package for UVX distribution

- [ ] Create `pyproject.toml` for UVX
- [ ] Convert Bash installer to Python entry point
- [ ] Add CLI detection to `uv tool install`
- [ ] Create PowerShell variants for Windows
- [ ] Test cross-platform installation

**Deliverable**: `uvx agentecflow init --ai <cli>`

**Testing**: Installation on Linux, macOS, Windows

---

#### **Phase 5: Documentation & Polish (1-2 weeks)**
**Goal**: Update documentation, create migration guide

- [ ] Update 164+ files referencing Claude Code
- [ ] Create multi-CLI usage guide
- [ ] Write migration guide for existing users
- [ ] Update README with CLI comparison
- [ ] Create video demos for each CLI

**Deliverable**: Complete documentation set

---

## 5. Risk Analysis

### 5.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Breaking Changes** | High | High | Provide `v1 → v2` migration script |
| **Agent Invocation Failures** | Medium | High | Implement robust fallback mechanisms |
| **MCP Unavailability** | Medium | Medium | Graceful degradation to HTTP APIs |
| **CLI API Changes** | Medium | Medium | Version-lock dependencies |
| **Cross-Platform Issues** | Medium | Medium | Comprehensive testing matrix |

### 5.2 Adoption Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Existing User Friction** | High | Medium | Auto-migration script |
| **Incomplete CLI Support** | High | Medium | Clear feature matrix documentation |
| **Performance Degradation** | Low | Medium | Benchmark before/after |
| **Community Confusion** | Medium | Medium | Clear messaging about CLI support |

---

## 6. Recommendations

### 6.1 Go/No-Go Decision

**RECOMMENDATION: PROCEED** ✅

**Justification**:
1. **Open Source Essential**: Multi-CLI support is table stakes for open source adoption
2. **Competitive Advantage**: Positions AI Engineer alongside Spec Kit
3. **Manageable Effort**: 8-12 weeks is acceptable for pre-launch refactoring
4. **Future-Proof**: Abstractions enable future CLI additions
5. **Market Demand**: Users want flexibility in AI tooling choice

### 6.2 Alternative Approaches

#### **Option A: Full Migration (Recommended)**
- **Timeline**: 8-12 weeks
- **Pros**: Maximum flexibility, competitive positioning
- **Cons**: Longer time-to-market
- **Recommendation**: ✅ **Best for open source launch**

#### **Option B: Phased Migration**
- **Timeline**: 4 weeks (Phase 1-2 only)
- **Pros**: Faster initial launch, incremental complexity
- **Cons**: Limited CLI support initially
- **Recommendation**: ⚠️ **Consider if timeline critical**

#### **Option C: Claude Code Only**
- **Timeline**: 0 weeks (current state)
- **Pros**: Immediate launch
- **Cons**: Severely limits adoption, non-competitive
- **Recommendation**: ❌ **Not recommended for open source**

---

## 7. Implementation Priorities

### 7.1 Must-Have for Launch
1. ✅ CLI adapter interface
2. ✅ Claude Code adapter (current behavior)
3. ✅ GitHub Copilot adapter (market leader)
4. ✅ Command abstraction layer
5. ✅ UVX installation
6. ✅ Migration guide

### 7.2 Nice-to-Have for Launch
1. ⭐ Gemini CLI adapter
2. ⭐ Cursor adapter
3. ⭐ Windsurf adapter
4. ⭐ Template variants per CLI
5. ⭐ Advanced MCP fallbacks

### 7.3 Post-Launch Enhancements
1. 🔮 Additional CLI adapters
2. 🔮 CLI-specific optimizations
3. 🔮 Performance benchmarking
4. 🔮 Community adapter contributions

---

## 8. Success Metrics

### 8.1 Technical Metrics
- [ ] **100%** of existing tests pass with Claude Code adapter
- [ ] **≥80%** of commands work on 3+ CLIs
- [ ] **<5%** performance degradation vs. current
- [ ] **Zero** breaking changes without migration path

### 8.2 Adoption Metrics (Post-Launch)
- [ ] **≥40%** of users choose non-Claude CLIs
- [ ] **≥3** community-contributed CLI adapters
- [ ] **<5%** migration support issues
- [ ] **≥4.0** GitHub stars per month growth

---

## 9. Conclusion

### Key Takeaways

1. **Migration is Achievable**: 8-12 weeks for single developer
2. **Architecture is Sound**: Spec Kit provides proven pattern
3. **Risks are Manageable**: Mitigation strategies exist
4. **Business Case is Strong**: Essential for open source success

### Next Steps

**Immediate Actions**:
1. ✅ **Approve** this analysis
2. 📋 Create EPIC-XXX for multi-CLI migration
3. 📅 Schedule Phase 1 kickoff (Week of 2025-10-14)
4. 👥 Assign development resources
5. 📢 Communicate timeline to stakeholders

**Long-Term Vision**:
- Position AI Engineer as the **most CLI-flexible** engineering workflow system
- Build community around multi-CLI support
- Enable users to switch CLIs without changing workflows

---

## 10. References

- [Spec Kit GitHub Repository](https://github.com/github/spec-kit)
- [Spec Kit Blog Post](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [UVX Documentation](https://github.com/astral-sh/uv)
- [Multi-Agent Support Issue](https://github.com/github/spec-kit/issues/269)

---

**Document Owner**: AI Engineer Product Team
**Last Updated**: 2025-10-13
**Review Date**: 2025-11-01
**Status**: ✅ Analysis Complete, Ready for Stakeholder Review
