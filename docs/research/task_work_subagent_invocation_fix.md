# Task-Work Subagent Invocation Fix

**Problem**: Claude Code doesn't automatically invoke subagents when `/task-work TASK-XXX` is executed. Users must manually add `--use-subagents` flag and remind Claude to use the Task tool.

**Root Cause**: Command specification uses descriptive documentation style instead of imperative execution instructions that Claude Code can directly act upon.

---

## Analysis of Current Implementation

### Current Command Structure Issues

1. **Too Much Explanation, Not Enough Action**
   - Current: "Claude Code MUST automatically..."
   - Problem: These are guidelines, not direct instructions

2. **Code Examples Instead of Tool Calls**
   - Current: Python code showing logic flow
   - Problem: Claude interprets this as documentation, not executable steps

3. **Buried Execution Instructions**
   - Current: "REQUIRED TASK TOOL INVOCATIONS" section at line 99
   - Problem: Too far down, preceded by 98 lines of context

4. **Missing Direct Invocation Pattern**
   - Current: Shows example Task() calls in code blocks
   - Problem: Not formatted as immediate action items

---

## Solution: Restructured Command Format

### Key Principles

1. **Lead with Action**: First thing Claude sees should be what to do
2. **Explicit Tool Calls**: Use direct "INVOKE:" statements
3. **Minimal Preamble**: Context comes after actions
4. **Clear Sequencing**: Numbered steps with no ambiguity

### Recommended Structure

```markdown
# /task-work Command

## IMMEDIATE EXECUTION SEQUENCE

When user runs `/task-work TASK-XXX`, IMMEDIATELY execute these steps:

### Step 1: Detect Stack (15 seconds max)
READ `.claude/settings.json` → extract `project.template` value
IF file not found → detect from project files
SET stack = detected value (default: "default")

### Step 2: Load Task Context (10 seconds max)
READ `tasks/in_progress/TASK-XXX.md`
EXTRACT: requirements, acceptance criteria, BDD scenarios, epic/feature links
VERIFY task exists, exit with error if not found

### Step 3: Select Agents (5 seconds max)
BASED ON stack value, MAP to agents:
- maui → maui-usecase-specialist, maui-viewmodel-specialist, dotnet-testing-specialist
- react → react-state-specialist, react-testing-specialist
- python → python-api-specialist, python-testing-specialist
- typescript-api → nestjs-api-specialist, typescript-domain-specialist, nodejs-testing-specialist
- dotnet-microservice → dotnet-api-specialist, dotnet-domain-specialist, dotnet-testing-specialist
- default → software-architect, task-manager, test-verifier

### Step 4: Execute Agent Phases (NO DELAY - START IMMEDIATELY)

#### Phase 1: Requirements Analysis
INVOKE Task tool with:
```
subagent_type: "requirements-analyst"
description: "Analyze requirements for TASK-XXX"
prompt: "Analyze task TASK-XXX requirements and acceptance criteria.
         Extract key functional requirements, non-functional requirements,
         and testable acceptance criteria for {stack} implementation."
```

#### Phase 2: Implementation Planning
INVOKE Task tool with:
```
subagent_type: "{stack}-api-specialist" OR fallback to "software-architect"
description: "Plan implementation for TASK-XXX"
prompt: "Design {stack} implementation approach for TASK-XXX.
         Include architecture decisions, pattern selection, and component structure.
         Consider {stack}-specific best practices and testing strategies."
```

#### Phase 3: Implementation
INVOKE Task tool with:
```
subagent_type: "{stack}-domain-specialist" OR fallback to "task-manager"
description: "Implement TASK-XXX"
prompt: "Implement TASK-XXX following {stack} best practices.
         Use patterns from planning phase.
         Create production-quality code with error handling.
         Prepare codebase for testing phase."
```

#### Phase 4: Testing
INVOKE Task tool with:
```
subagent_type: "{stack}-testing-specialist" OR fallback to "test-verifier"
description: "Generate tests for TASK-XXX"
prompt: "Create comprehensive test suite for TASK-XXX.
         Include unit tests, integration tests, and edge cases.
         Target 80%+ coverage.
         Use {stack} testing frameworks and patterns.
         EXECUTE tests and report results."
```

#### Phase 5: Code Review
INVOKE Task tool with:
```
subagent_type: "code-reviewer"
description: "Review TASK-XXX implementation"
prompt: "Review TASK-XXX implementation for quality, patterns, and {stack} best practices.
         Check: code quality, test coverage, error handling, documentation.
         Provide actionable feedback if improvements needed."
```

### Step 5: Report Results
AFTER all agents complete, GENERATE summary report with:
- Test results (passed/failed/coverage)
- Quality gate status
- Next state (IN_REVIEW or BLOCKED)
- Recommended next actions

---

## CONTEXT (Read if needed, but EXECUTE ABOVE FIRST)

[All the existing documentation about modes, patterns, examples, etc.]
```

---

## Specific Fix for Your Command

### File to Update
`installer/global/commands/task-work.md`

### New Structure

```markdown
# Task Work Command

## EXECUTION PROTOCOL

When user runs `/task-work TASK-XXX`, execute this exact sequence:

### 1. Stack Detection (Required - 10 seconds)
```bash
# Read settings file
if [ -f ".claude/settings.json" ]; then
  stack=$(jq -r '.project.template // "default"' .claude/settings.json)
else
  stack="default"
fi
echo "Detected stack: $stack"
```

### 2. Agent Selection (Required - 5 seconds)
Based on $stack, select agents:

| Stack | Agents |
|-------|--------|
| maui | maui-usecase-specialist, dotnet-testing-specialist, code-reviewer |
| react | react-state-specialist, react-testing-specialist, code-reviewer |
| python | python-api-specialist, python-testing-specialist, code-reviewer |
| typescript-api | nestjs-api-specialist, nodejs-testing-specialist, code-reviewer |
| dotnet-microservice | dotnet-api-specialist, dotnet-testing-specialist, code-reviewer |
| default | software-architect, test-verifier, code-reviewer |

### 3. Task Tool Invocations (Required - Execute Immediately)

**YOU MUST USE THE TASK TOOL FOR EACH PHASE. DO NOT ATTEMPT TO DO THE WORK YOURSELF.**

#### INVOKE 1: Requirements Analysis
```
Use Task tool:
  subagent_type: requirements-analyst
  description: Analyze TASK-XXX requirements
  prompt: Analyze requirements for TASK-XXX and extract testable criteria for {stack}
```

#### INVOKE 2: Implementation Planning
```
Use Task tool:
  subagent_type: {stack}-api-specialist (or software-architect if stack not supported)
  description: Plan TASK-XXX implementation
  prompt: Design {stack} implementation for TASK-XXX with appropriate patterns
```

#### INVOKE 3: Implementation
```
Use Task tool:
  subagent_type: {stack}-domain-specialist (or task-manager if stack not supported)
  description: Implement TASK-XXX
  prompt: Implement TASK-XXX following {stack} best practices and planned architecture
```

#### INVOKE 4: Testing
```
Use Task tool:
  subagent_type: {stack}-testing-specialist (or test-verifier if stack not supported)
  description: Test TASK-XXX
  prompt: Generate and execute comprehensive tests for TASK-XXX with 80%+ coverage
```

#### INVOKE 5: Review
```
Use Task tool:
  subagent_type: code-reviewer
  description: Review TASK-XXX
  prompt: Review TASK-XXX for quality, coverage, and {stack} best practices
```

### 4. Report Generation (Required - After all invocations complete)
Summarize results from all agent invocations and determine next state.

---

## Additional Context

[Rest of documentation - modes, examples, troubleshooting, etc.]
```

---

## Alternative: Hook-Based Approach

If the restructured command doesn't work, use a pre-command hook:

### File: `.claude/hooks/task-work-pre.sh`

```bash
#!/bin/bash
# Pre-execution hook for /task-work command
# This runs BEFORE Claude processes the command

TASK_ID=$1

# Detect stack
if [ -f ".claude/settings.json" ]; then
  STACK=$(jq -r '.project.template // "default"' .claude/settings.json)
else
  STACK="default"
fi

# Output instructions that Claude MUST follow
cat <<EOF
🎯 TASK-WORK EXECUTION INSTRUCTIONS 🎯

Task: $TASK_ID
Stack: $STACK

YOU MUST FOLLOW THIS EXACT SEQUENCE:

1. INVOKE Task tool → requirements-analyst
   Prompt: "Analyze $TASK_ID requirements for $STACK"

2. INVOKE Task tool → ${STACK}-api-specialist
   Prompt: "Plan $TASK_ID implementation for $STACK"

3. INVOKE Task tool → ${STACK}-domain-specialist
   Prompt: "Implement $TASK_ID for $STACK"

4. INVOKE Task tool → ${STACK}-testing-specialist
   Prompt: "Test $TASK_ID for $STACK with 80%+ coverage"

5. INVOKE Task tool → code-reviewer
   Prompt: "Review $TASK_ID for quality and patterns"

DO NOT SKIP ANY INVOCATIONS. USE THE TASK TOOL FOR EACH PHASE.
EOF
```

### Register Hook

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "pre-command": {
      "task-work": ".claude/hooks/task-work-pre.sh"
    }
  }
}
```

---

## Testing the Fix

### Before Fix (Current Behavior)
```
User: /task-work TASK-024
Claude: [Reads command] [Analyzes task] [Implements directly without subagents]
Result: ❌ No subagent invocations
```

### After Fix (Expected Behavior)
```
User: /task-work TASK-024
Claude: [Reads command] [Sees immediate execution sequence]
Claude: [Invokes Task tool → requirements-analyst]
Claude: [Invokes Task tool → nestjs-api-specialist]
Claude: [Invokes Task tool → typescript-domain-specialist]
Claude: [Invokes Task tool → nodejs-testing-specialist]
Claude: [Invokes Task tool → code-reviewer]
Claude: [Reports combined results]
Result: ✅ All subagents invoked automatically
```

---

## Why This Will Work

### Psychology of Claude Code Processing

1. **First 100 tokens matter most**: Leading with actions ensures immediate execution
2. **Tool invocation patterns**: Formatted as direct tool calls, not explanations
3. **Sequential clarity**: Numbered steps with no branching logic
4. **Imperative voice**: "INVOKE Task tool" not "Claude should invoke"
5. **Repetition**: Multiple reminders to use Task tool, not do work directly

### Key Differences from Current

| Current | Fixed |
|---------|-------|
| "Claude Code MUST automatically..." | "INVOKE Task tool with:" |
| Python code examples | Direct tool call syntax |
| Buried at line 99 | First thing after title |
| Descriptive documentation | Imperative commands |
| Conditional logic | Sequential steps |

---

## Implementation Steps

### Option 1: Restructure Command (Recommended)

1. Back up current `installer/global/commands/task-work.md`
2. Rewrite with "EXECUTION PROTOCOL" leading
3. Move documentation to bottom
4. Test with real task

### Option 2: Add Pre-Command Hook

1. Create `.claude/hooks/task-work-pre.sh`
2. Make executable: `chmod +x .claude/hooks/task-work-pre.sh`
3. Register in `.claude/settings.json`
4. Test with real task

### Option 3: Hybrid Approach (Most Robust)

1. Restructure command for clarity
2. Add pre-command hook as safety net
3. Both reinforce subagent invocation
4. Test with multiple stacks

---

## Success Criteria

After implementing fix:

- ✅ `/task-work TASK-024` automatically invokes 5 agents
- ✅ No manual `--use-subagents` flag required
- ✅ No reminder text needed
- ✅ Works across all supported stacks
- ✅ Consistent behavior every time

---

## Maintenance Notes

### If It Still Doesn't Work

1. **Check agent availability**: Ensure agents exist in `.claude/agents/`
2. **Verify naming**: Agent names must match exactly
3. **Test Task tool manually**: Try invoking Task tool directly
4. **Check Claude Code version**: Ensure Task tool is supported
5. **Review logs**: Check for error messages during command execution

### Future Improvements

1. **Add validation step**: Check if agents exist before invoking
2. **Implement fallback chain**: Primary → Secondary → Default agent
3. **Add progress indicators**: Show which phase is executing
4. **Cache stack detection**: Don't re-detect every time
5. **Parallel invocation**: Run independent phases concurrently

---

## Conclusion

The fix requires **restructuring the command to lead with imperative actions** rather than descriptive documentation. Claude Code needs to see direct tool invocation patterns immediately, not explanations of what should happen.

The key insight: **Claude Code follows the first clear instructions it sees**. If those instructions are "Read this, then do that," it works. If they're "Here's how the system should work," it doesn't.
