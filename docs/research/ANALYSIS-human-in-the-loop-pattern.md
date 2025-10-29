# Analysis: Human-in-the-Loop Pattern for Task Creation

**Date**: 2025-10-28
**Context**: MyDrive MAUI Application - TASK-065 Refactoring
**Analyst**: Analysis of actual Claude Code usage pattern

---

## Executive Summary

This analysis examines a real-world human-in-the-loop workflow where Claude Code was used to break down a complex refactoring task (TASK-065) into 5 TDD-friendly subtasks, with explicit intervention points for business logic decisions. The pattern demonstrates excellent engineering discipline and should be **partially integrated** into our system.

**Key Finding**: The human-in-the-loop pattern worked exceptionally well for **business logic decisions**, but the system already handles **technical complexity** through Phase 2.5 (Architectural Review) and Phase 2.7 (Complexity Evaluation).

**Recommendation**: Enhance `/task-create` with **business decision detection**, but keep it lightweight and optional.

---

## What Happened: The TASK-065 Story

### Context
The user was working on a .NET MAUI mobile app and had:
1. Multiple code review comments with example snippets
2. A complex refactoring spanning 8 phases
3. Desire to use TDD mode (`/task-work --mode=tdd`)
4. Need to pause for business logic decisions (not just technical decisions)

### User's Workflow
```
1. Shift Claude Code into plan mode
2. Provide code review comments + example code snippets
3. Ask Claude to create a plan for /task-create
4. Claude creates TASK-065 with 8 phases (too complex)
5. User asks to break down into TDD-friendly subtasks
6. User explicitly requests: "defer business logic assumptions to human-in-the-loop"
7. Claude creates 5 subtasks (TASK-065.1 through 065.5)
8. Each subtask includes ⚠️ HUMAN LOOP INTERVENTION POINTS sections
```

### Key Quote from User
> "Look, if there's any assumptions that you're going to make, especially about business logic or whatever, you can defer it to human and loop intervention."

This reveals a **critical gap**: Our system handles technical complexity well, but doesn't explicitly surface **business logic decision points**.

---

## Analysis of Created Subtasks

### TASK-065.1: Generic Relationship Classes & Mapper Foundation

**Human Loop Intervention Points** (3 identified):

1. **Route Property Mapping**
   - Question: Should `DriverDetails.Route` map to `DriverDefaultRoute` or `DriverCurrentRoute`?
   - Type: **Business Logic Decision**
   - Impact: Determines which route is considered "primary"
   - Why it matters: Different stakeholders may have different expectations

2. **Missing DriverDetails Properties**
   - Question: Should we add `CurrentRoute` and `Device` properties to `DriverDetails`?
   - Type: **Domain Model Decision**
   - Impact: Changes entity contract (breaking change potential)
   - Options: Add properties (breaking) vs data loss vs hidden state

3. **Null Handling Strategy**
   - Question: How should mapper handle null/empty strings?
   - Type: **Data Integrity Decision**
   - Impact: Could affect downstream validation logic
   - Options: Empty → null, null → empty, leave as-is

### TASK-065.4: DriverEngine Creation

**Human Loop Intervention Points** (4 identified):

1. **Business Validation Rules**
   - Question: What validation rules should the engine enforce?
   - Type: **Business Logic Decision**
   - Impact: Determines what constitutes "valid" driver state
   - Examples: Must have route? Must have location? Device required?

2. **Error Types and Messages**
   - Question: What error codes should be returned?
   - Type: **API Contract Decision**
   - Impact: External consumers depend on consistent error codes
   - Options: Domain-specific codes vs generic codes

3. **Return Type Strategy**
   - Question: Return `ErrorOr<DriverDetails>` or `ErrorOr<bool>`?
   - Type: **Architecture Decision**
   - Impact: Affects caller ergonomics and error handling
   - Trade-offs: Convenience vs explicit retrieval

4. **Service vs Repository Data Flow**
   - Question: Should engine trust service saved correctly, or always retrieve from repository?
   - Type: **Data Consistency Decision**
   - Impact: Performance vs verification trade-off
   - Options: Trust service return vs double-retrieval

---

## Pattern Characteristics

### What Made This Pattern Effective

1. **Explicit Labeling**: Each intervention point clearly marked with ⚠️
2. **Context Provided**: Current code context shown for each decision
3. **Options Listed**: Multiple options presented for each decision
4. **Impact Stated**: Why the decision matters is explained
5. **No Default Assumptions**: Claude doesn't pick a default and move on
6. **Type Classification**: Decisions categorized (business logic, domain model, architecture)

### Format Template Discovered

```markdown
## ⚠️ HUMAN LOOP INTERVENTION POINTS

### 1. [Decision Name]
**Question**: What should we do about [specific issue]?

**Current Code Context**:
```csharp
// Relevant code snippet showing current state
```

**Options**:
- A) [Option 1 with trade-offs]
- B) [Option 2 with trade-offs]
- C) [Option 3 with trade-offs]

**Decision Needed**: [Clear ask for human input]

---
```

### Types of Decisions Identified

| Type | Count | Examples | Should Pause? |
|------|-------|----------|---------------|
| **Business Logic** | 5 | Validation rules, error codes, domain constraints | ✅ Yes |
| **Domain Model** | 3 | Entity properties, data mappings, contracts | ✅ Yes |
| **Architecture** | 2 | Return types, data flow patterns | 🟡 Maybe |
| **Data Integrity** | 2 | Null handling, transformation rules | 🟡 Maybe |
| **API Contracts** | 2 | Error codes, external interfaces | ✅ Yes |

**Key Insight**: Not all intervention points are equal. Business logic and API contracts warrant mandatory pauses, while architecture decisions could be optional.

---

## Current System Capabilities

### What We Already Handle Well

1. **Technical Complexity** (Phase 2.7)
   - File count complexity
   - Pattern familiarity
   - Risk assessment
   - Dependency complexity
   - Result: Complexity score 0-10

2. **Architectural Review** (Phase 2.5)
   - SOLID principles
   - DRY violations
   - YAGNI compliance
   - Pattern consistency
   - Result: Review score 0-100

3. **Complexity-Based Routing**
   - Simple tasks (1-3): AUTO_PROCEED
   - Medium tasks (4-6): QUICK_OPTIONAL (30s timeout)
   - Complex tasks (7-10): FULL_REQUIRED (mandatory checkpoint)

4. **Test Enforcement** (Phase 4.5)
   - Compilation verification
   - Test execution
   - Auto-fix (up to 3 attempts)
   - Block if all attempts fail

5. **Plan Auditing** (Phase 5.5)
   - Scope creep detection
   - File count variance
   - LOC variance (±20%)
   - Duration variance (±30%)

### What We DON'T Handle

1. **Business Logic Decision Detection**
   - No automatic detection of business logic assumptions
   - No prompting for validation rule decisions
   - No flagging of domain model changes

2. **Domain-Specific Validation**
   - No awareness of domain constraints (e.g., "drivers must have routes")
   - No detection of entity contract changes
   - No API contract change detection

3. **Stakeholder-Level Decisions**
   - No detection of decisions requiring product owner input
   - No flagging of UX/business rule changes
   - No escalation for ambiguous requirements

---

## Gap Analysis

### Current Flow vs Desired Flow

**Current `/task-create` Flow**:
```
1. Parse title, epic, feature, requirements
2. Generate task ID
3. Extract acceptance criteria from EARS requirements
4. Evaluate complexity (Phase 2.7 logic at creation time)
5. If complexity ≥7, suggest split
6. Create task file in backlog
```

**Gaps**:
- ❌ No business logic assumption detection
- ❌ No domain model change detection
- ❌ No API contract analysis
- ❌ No "decision needed" flagging

**Desired Enhancement**:
```
1. Parse title, epic, feature, requirements
2. Generate task ID
3. Extract acceptance criteria from EARS requirements
4. Evaluate complexity
5. **NEW: Detect business decision points**
   - Entity changes (add/remove properties)
   - Validation rules (what constitutes "valid"?)
   - Error handling strategies (codes, messages)
   - Data transformation rules (null handling, mappings)
6. **NEW: Flag ambiguous requirements**
   - Multiple interpretation options
   - Missing business constraints
   - Unclear domain rules
7. If complexity ≥7 OR decision points detected, suggest split or clarification
8. Create task file with intervention points flagged
```

---

## Recommendation: Lightweight Enhancement

### Proposal: Add `--detect-decisions` Flag to `/task-create`

**Design Philosophy**: Make it **optional** and **lightweight** to avoid adding friction to simple tasks.

### Implementation Approach

```bash
# Standard task creation (unchanged)
/task-create "Fix login bug" epic:EPIC-001 feature:FEAT-001.2

# Enhanced mode for complex tasks
/task-create "Refactor driver architecture" epic:EPIC-001 feature:FEAT-001.2 --detect-decisions
```

### What `--detect-decisions` Would Do

1. **Analyze Task Description + Requirements**
   - Look for keywords: "validation", "error handling", "mapping", "transform"
   - Detect entity changes: "add property", "remove field", "update contract"
   - Identify ambiguity: "might", "could", "should we", "unclear"

2. **Generate Decision Points Section**
   - Add `## ⚠️ DECISION POINTS` section to task file
   - List detected decision points with context
   - Provide options when obvious alternatives exist

3. **Flag Task for Review**
   - Add `has_decision_points: true` to frontmatter
   - Add tag: `[decisions-needed]`
   - Suggest using `--design-only` mode for complex cases

### Enhanced Task File Structure

```markdown
---
id: TASK-065.2
title: Repository Layer Refactoring
status: backlog
priority: high
has_decision_points: true
decision_points_count: 3
tags: [architecture, repository, decisions-needed]
---

# Task: Repository Layer Refactoring

## Description
[Task description]

## ⚠️ DECISION POINTS

### 1. Is UpdateDriversRoute Actually Needed?
**Context**: Method exists but purpose is unclear from code review.

**Question**: Should this method be:
- A) Removed (not needed)
- B) Kept and documented
- C) Refactored into DriverEngine

**Impact**: Affects repository interface design.

**Decision Needed Before Implementation**: Yes

---

### 2. Duplicate Driver Handling Strategy
**Context**: Repository might save duplicate drivers.

**Question**: Should repository:
- A) Update existing driver (upsert)
- B) Skip if driver exists (no-op)
- C) Throw error on duplicate

**Impact**: Affects data integrity guarantees.

**Decision Needed Before Implementation**: Yes

---

### 3. Single Driver Assumption Validation
**Context**: Code assumes only one driver exists.

**Question**: Should we:
- A) Enforce single driver constraint in DB
- B) Return first driver (current behavior)
- C) Return error if multiple exist

**Impact**: Affects error handling and data model.

**Decision Needed Before Implementation**: Yes

---

## Acceptance Criteria
[Rest of task content]
```

### Integration with `/task-work`

When `/task-work` encounters a task with `has_decision_points: true`:

```
🚦 TASK-065.2 has 3 decision points flagged

DECISION POINT 1/3: Is UpdateDriversRoute Actually Needed?
[Display context and options]

Your decision [A/B/C/Skip]: _

---

OPTIONS:
- [A/B/C] - Make decision now
- [Skip] - Defer decision (will pause during implementation)
- [All] - Defer all decisions and implement with assumptions documented
```

### Benefits

1. **No Friction for Simple Tasks**: Optional flag doesn't slow down normal workflow
2. **Explicit Decision Tracking**: Decisions are documented in task file
3. **Early Detection**: Catch ambiguities before implementation
4. **Better Planning**: Product owners can review decisions upfront
5. **Reduced Rework**: Fewer mid-implementation pivots

### Risks

1. **False Positives**: Might detect "decisions" that aren't actually ambiguous
2. **Added Complexity**: Another concept for users to learn
3. **Maintenance**: Requires good heuristics to detect decision points

---

## Alternative: Enhance Phase 2.8 Instead

Instead of adding to `/task-create`, we could enhance **Phase 2.8 (Human Checkpoint)** to surface these decision points:

**Current Phase 2.8**:
- Triggered when complexity ≥7 or architectural review flags issues
- Displays implementation plan
- Options: Approve/Modify/Simplify/Reject/Postpone

**Enhanced Phase 2.8**:
- Triggered when complexity ≥7 OR **decision points detected**
- Displays implementation plan + **decision points**
- Options: Approve/Modify/**Make Decisions**/Simplify/Reject/Postpone

**Advantage**: Keeps `/task-create` simple, enhances existing checkpoint
**Disadvantage**: Decisions not visible until `/task-work` is invoked

---

## Recommendations

### Tier 1: Implement Immediately

1. **Document the Pattern** ✅ (This analysis)
   - Share TASK-065 as example workflow
   - Create template for "⚠️ DECISION POINTS" section
   - Add to best practices guide

2. **Enhance Phase 2.8** (LOW EFFORT, HIGH VALUE)
   - Add decision point detection to planning phase
   - Surface decisions during human checkpoint
   - Allow inline decision capture

3. **Update TDD/BDD Mode Documentation**
   - Explain when to use human-in-the-loop pattern
   - Provide examples of decision point formatting
   - Link to TASK-065 as case study

### Tier 2: Evaluate Further

4. **Add `--detect-decisions` Flag to `/task-create`** (MEDIUM EFFORT)
   - Implement lightweight heuristics for decision detection
   - Add decision points section to task template
   - Integrate with Phase 2.8 checkpoint

5. **Create Decision Point Library** (FUTURE)
   - Common decision patterns by domain (API design, data modeling, validation)
   - Reusable templates for decision documentation
   - Decision outcome tracking for retrospectives

### Tier 3: Research

6. **LLM-Powered Decision Detection** (RESEARCH)
   - Use Claude to analyze task descriptions for ambiguity
   - Generate decision point questions automatically
   - Validate against EARS requirements for completeness

---

## Conclusion

The TASK-065 human-in-the-loop pattern demonstrates **excellent engineering discipline** and should be encouraged. However, the pattern is most valuable for **business logic decisions**, which our current system (focused on technical complexity) doesn't explicitly handle.

**Recommended Action**:
1. Document this pattern as a best practice ✅
2. Enhance Phase 2.8 to include decision point detection (Low effort, high value)
3. Consider `--detect-decisions` flag if demand justifies complexity

**Key Insight**: The user's request reveals a **different class of decisions** (business logic, domain rules, API contracts) that warrant human intervention beyond just technical complexity. Our system should help surface these decisions early, but make it **optional and lightweight** to avoid adding friction.

---

## Appendix: Decision Point Heuristics

### Keywords That Suggest Business Logic Decisions

- **Validation**: "validate", "check", "ensure", "must", "required"
- **Error Handling**: "error code", "exception", "failure", "recovery"
- **Data Mapping**: "map", "transform", "convert", "translate"
- **Domain Rules**: "business rule", "constraint", "policy", "allowed"
- **Ambiguity**: "might", "could", "should we", "unclear", "TBD"

### Patterns That Suggest Decision Points

1. **Entity Changes**: Adding/removing properties to domain entities
2. **Contract Changes**: Modifying API signatures or return types
3. **Validation Logic**: Defining what constitutes "valid" state
4. **Error Codes**: Choosing error codes and messages
5. **Null Handling**: Deciding how to handle null/empty values
6. **Data Flow**: Choosing between service vs repository as source of truth

### Confidence Levels

- **High Confidence**: Entity property additions, API contract changes
- **Medium Confidence**: Validation rules, error handling strategies
- **Low Confidence**: Null handling, data transformation edge cases

Only flag **high confidence** decision points by default. Allow users to opt-in to lower confidence levels with `--detect-decisions=verbose`.

---

## Example: Enhanced Task Creation Output

```bash
/task-create "Refactor driver repository" epic:EPIC-001 feature:FEAT-001.2 --detect-decisions

🔍 Analyzing task for decision points...

⚠️  3 DECISION POINTS DETECTED

BUSINESS LOGIC:
  1. UpdateDriversRoute method necessity (impacts repository interface)
  2. Duplicate driver handling strategy (impacts data integrity)

DOMAIN MODEL:
  3. Single driver assumption validation (impacts error handling)

✅ Task Created: TASK-065.2

📋 Task Details
Title: Refactor driver repository
Priority: high
Status: backlog
Tags: [architecture, repository, decisions-needed]
Decision Points: 3 (see task file for details)

⚠️  RECOMMENDATION: Review decision points before starting implementation

Options:
1. Make decisions now (review task file and document decisions)
2. Use /task-work --design-only to plan implementation first
3. Proceed with /task-work (will pause at Phase 2.8 for decisions)

📁 File Location
tasks/backlog/TASK-065.2/TASK-065.2-repository-refactoring.md

Next Steps:
1. Review ⚠️ DECISION POINTS section in task file
2. Document decisions or defer to Phase 2.8
3. When ready: /task-work TASK-065.2
```

---

**Analysis Complete**: Ready for discussion and prioritization.
