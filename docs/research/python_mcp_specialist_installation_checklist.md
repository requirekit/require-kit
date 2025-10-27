# Python MCP Specialist Installation Checklist

**Date**: 2025-09-30
**Purpose**: Verify all required updates for adding `python-mcp-specialist` agent
**Reference**: `installer/EXTENDING_THE_SYSTEM.md`

---

## ✅ Checklist: Adding New Agent

Based on the official guide (`installer/EXTENDING_THE_SYSTEM.md`), here's what needs to be done:

### Step 1: Create the Agent File ✅
- [x] **Created**: `installer/global/agents/python-mcp-specialist.md`
- [x] **Size**: 22.3 KB with comprehensive examples
- [x] **Format**: Proper YAML frontmatter with name, description, tools, model
- [x] **Content**: Complete expertise areas, patterns, best practices

**Location**: `installer/global/agents/python-mcp-specialist.md`

### Step 2: Add Agent to All Templates ❌ (NOT DONE)
According to the guide, agents should be copied to ALL template directories:

**Required Locations**:
- [ ] `installer/global/templates/default/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/maui/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/react/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/python/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/dotnet-microservice/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/typescript-api/agents/python-mcp-specialist.md`
- [ ] `installer/global/templates/fullstack/agents/python-mcp-specialist.md`

**Current Status**: ❌ Only created in `installer/global/agents/`, NOT copied to templates

**Why This Matters**:
- Templates are what get copied to projects during `agentec-init`
- Without copying to templates, the agent won't appear in new projects
- Each template needs its own copy (not symlinked)

### Step 3: Update Documentation ⚠️ (PARTIAL)

#### 3.1. Python Template CLAUDE.md ✅
- [x] **Updated**: `installer/global/templates/python/CLAUDE.md`
- [x] **Added**: MCP Server Development section
- [x] **References**: `python-mcp-specialist` agent
- [x] **Examples**: MCP server structure and integration patterns

#### 3.2. Main README.md ❌ (NOT DONE)
- [ ] **Should update**: `installer/README.md`
- [ ] **Add agent to list**: Include `python-mcp-specialist` in agent documentation
- [ ] **Update agent count**: Currently says "4 agents" - should remain 4 (this is Python-specific)

**Current text in README.md**:
```markdown
### Core Agents
1. **requirements-analyst** - Gathers and formalizes requirements using EARS notation
2. **bdd-generator** - Converts EARS requirements to BDD/Gherkin scenarios
3. **code-reviewer** - Enforces quality standards and best practices
4. **test-orchestrator** - Manages test execution and quality gates
```

**Recommendation**: Add note about stack-specific agents:
```markdown
### Stack-Specific Agents

Some templates include additional specialized agents:

**Python Template**:
- **python-langchain-specialist** - LangChain/LangGraph workflows
- **python-api-specialist** - FastAPI development
- **python-testing-specialist** - pytest and testing
- **python-mcp-specialist** - MCP server development (NEW)
```

#### 3.3. EXTENDING_THE_SYSTEM.md ⚠️ (COULD BE UPDATED)
- [ ] **Optional**: Add `python-mcp-specialist` as an example
- [ ] **Benefit**: Shows real-world example of adding specialized agent
- [ ] **Location**: `installer/EXTENDING_THE_SYSTEM.md`

### Step 4: Create a Command (Optional) ❌ (NOT APPLICABLE)
- [ ] N/A - MCP specialist doesn't need a dedicated command
- [ ] Agent is engaged directly, not through commands
- [ ] No action needed

### Step 5: Reinstall Global System ❌ (PENDING)
- [ ] **Must run**: `cd installer && ./scripts/install-global.sh`
- [ ] **After**: Copying agent to all templates
- [ ] **Verifies**: Installation to `~/.claude/templates/*/agents/`

---

## Additional Checks

### Manifest.json ✅ (NO UPDATE NEEDED)
- [x] **Reviewed**: `installer/global/manifest.json`
- [x] **Status**: No update needed - manifest doesn't list individual agents
- [x] **Capabilities**: General capabilities already covered

**Why no update needed**: The manifest tracks system-wide capabilities, not individual agents. MCP development falls under existing "test-orchestration" and Python stack capabilities.

### Global Agents List ✅ (ALREADY EXISTS)
- [x] **Location**: `installer/global/agents/python-mcp-specialist.md`
- [x] **Proper location**: This is correct - central source of truth

### Template-Specific Files ⚠️ (PYTHON TEMPLATE)

**Python Template Updates**:
- [x] ✅ `CLAUDE.md` - Updated with MCP section
- [ ] ❌ `agents/python-mcp-specialist.md` - NOT COPIED YET
- [x] ✅ Gap analysis done
- [x] ✅ Implementation summary created

---

## Action Items: What Needs to Be Done

### Critical (Required for Agent to Work)

1. **Copy agent to all template directories** ⚠️ **MUST DO**
   ```bash
   # Copy to all templates
   for template in default maui react python dotnet-microservice typescript-api fullstack; do
     cp installer/global/agents/python-mcp-specialist.md \
        installer/global/templates/$template/agents/
   done
   ```

2. **Verify agent files exist in templates**
   ```bash
   # Check each template has the agent
   for template in default maui react python dotnet-microservice typescript-api fullstack; do
     echo "Checking $template:"
     ls installer/global/templates/$template/agents/python-mcp-specialist.md
   done
   ```

3. **Reinstall global system**
   ```bash
   cd installer
   ./scripts/install-global.sh
   ```

4. **Verify installation**
   ```bash
   # Check global installation
   ls ~/.claude/templates/python/agents/python-mcp-specialist.md

   # Test with new project
   mkdir /tmp/test-mcp-agent
   cd /tmp/test-mcp-agent
   agentec-init python
   ls .claude/agents/python-mcp-specialist.md  # Should exist
   ```

### Optional (Recommended for Documentation)

5. **Update installer/README.md**
   - Add section about stack-specific agents
   - Mention `python-mcp-specialist` for Python projects

6. **Update EXTENDING_THE_SYSTEM.md**
   - Add `python-mcp-specialist` as a real-world example
   - Show how specialized agents work for specific stacks

---

## Testing Checklist

After completing action items:

### Agent Availability Test
- [ ] Run `agentec-init python` in test directory
- [ ] Verify `.claude/agents/python-mcp-specialist.md` exists
- [ ] Check agent content matches global version

### Documentation Test
- [ ] Python template CLAUDE.md references the agent
- [ ] MCP section provides clear guidance
- [ ] Examples are accurate and complete

### Integration Test (with Claude Code)
- [ ] Create test Python project
- [ ] Reference agent: `@python-mcp-specialist`
- [ ] Verify agent responds with MCP expertise
- [ ] Test agent provides correct patterns

---

## Current Status Summary

### ✅ Completed
1. ✅ Gap analysis document created
2. ✅ Agent specification created (`installer/global/agents/python-mcp-specialist.md`)
3. ✅ Python template CLAUDE.md updated
4. ✅ Implementation summary documented
5. ✅ Manifest.json reviewed (no changes needed)

### ❌ Not Completed (Critical)
1. ❌ **Agent NOT copied to template directories** - This is the blocker
2. ❌ Global system not reinstalled
3. ❌ Installation not verified

### ⚠️ Optional (Recommended)
1. ⚠️ installer/README.md not updated
2. ⚠️ EXTENDING_THE_SYSTEM.md not updated with example

---

## Why Template Copying Matters

**Understanding the Installation Flow**:

1. **Global Installation** (`~/.claude/`)
   - Source: `installer/global/templates/*/agents/*.md`
   - Installed by: `./scripts/install-global.sh`
   - Used when: Running `agentec-init`

2. **Project Initialization**
   - Source: `~/.claude/templates/[stack]/agents/*.md`
   - Copied to: `project/.claude/agents/*.md`
   - Command: `agentec-init python`

**The Problem**:
- ✅ We created `installer/global/agents/python-mcp-specialist.md`
- ❌ We did NOT copy it to `installer/global/templates/python/agents/`
- ❌ Therefore `install-global.sh` won't install it to `~/.claude/templates/python/`
- ❌ Therefore `agentec-init python` won't copy it to projects
- ❌ Therefore new Python projects won't have the agent

**The Solution**:
Copy the agent to all template directories, then reinstall.

---

## Quick Fix Script

```bash
#!/bin/bash
# Quick fix to add python-mcp-specialist to all templates

cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer

# Copy agent to all templates
for template in default maui react python dotnet-microservice typescript-api fullstack; do
  echo "Copying python-mcp-specialist to $template..."
  cp installer/global/agents/python-mcp-specialist.md \
     installer/global/templates/$template/agents/
done

# Verify copies
echo ""
echo "Verifying agent was copied to all templates:"
for template in default maui react python dotnet-microservice typescript-api fullstack; do
  if [ -f "installer/global/templates/$template/agents/python-mcp-specialist.md" ]; then
    echo "✅ $template: agent present"
  else
    echo "❌ $template: agent MISSING"
  fi
done

echo ""
echo "Now run: cd installer && ./scripts/install-global.sh"
```

---

## Conclusion

**Current State**: Agent created and documented, but NOT distributed to templates

**Required Action**: Copy agent to all template directories and reinstall

**Estimated Time**: 2 minutes to copy files, 1 minute to reinstall, 2 minutes to verify = 5 minutes total

**Priority**: **HIGH** - Without this step, the agent won't be available in new projects

**Next Steps**:
1. Run the quick fix script (or copy manually)
2. Verify files copied to all templates
3. Run global reinstall
4. Test with `agentec-init python`
5. Verify agent appears in `.claude/agents/`

---

**Status**: Installation Incomplete - Requires Template Distribution ⚠️
**Blocker**: Agent not copied to template directories
**Fix Complexity**: Simple - just file copying
