# Requirements Gathering Q&A Session - AgenticFlow LangGraph + MCP Architecture

**Date:** 2025-10-01
**Session Type:** Dual-session requirements gathering (Session 1: gather-requirements, Session 2: research assistant)
**Purpose:** Comprehensive requirements analysis for AgenticFlow migration from markdown to LangGraph + MCP architecture

---

## Table of Contents

1. [Discovery Phase](#discovery-phase)
2. [Exploration Phase](#exploration-phase)
3. [Technical Specifications & Constraints](#technical-specifications--constraints)
4. [Final Clarifications](#final-clarifications)

---

## Discovery Phase

### Q1: What is the main purpose or goal of the feature you want to build?

**Answer:**

## Primary Goal: Transform AgenticFlow into Production-Ready LangGraph + MCP Architecture

The main purpose is to **migrate AgenticFlow from a markdown-based, single-developer CLI tool to a production-grade, team-scale development platform** using LangGraph orchestration with MCP (Model Context Protocol) integration.

### Core Capabilities to Add:

1. **LangGraph Workflow Orchestration** (replacing static markdown commands)
   - Multi-stage StateGraph workflows for all 4 AgenticFlow stages
   - Conditional routing based on context and results
   - Checkpoint/resume support for human approval gates
   - Proven pattern from UK Probate Agent showing 50-85% cost savings

2. **MCP Server Integration** (replacing local `.claude/` files)
   - Centralized MCP servers for Requirements, PM Tools, Testing, Deployment
   - Universal compatibility across Claude Code, Gemini CLI, GitHub Copilot
   - Dynamic tool discovery and capability exposure
   - Real-time configuration updates without file copying

3. **Team Collaboration Infrastructure** (replacing individual markdown files)
   - PostgreSQL-backed state management for multi-user workflows
   - Bidirectional PM tool synchronization (Jira, Linear, Azure DevOps, GitHub)
   - Progress rollup across Epic → Feature → Task hierarchy
   - Role-based access control and audit logging

4. **Production-Grade Quality** (enterprise readiness)
   - OAuth 2.1 authentication and security
   - Comprehensive error handling and fallback mechanisms
   - Model optimization for cost efficiency
   - Monitoring, logging, and observability

### Success Criteria:
- **Replace** all markdown-based commands with LangGraph workflows
- **Enable** real-time collaboration across development teams
- **Provide** universal AI tool compatibility via MCP protocol
- **Achieve** enterprise-grade reliability and security

---

## Exploration Phase

### Q2: Who are the primary users and what are their roles?

**Answer:**

### **Individual Developers**

**Primary Interactions:**
- Execute `/gather-requirements` for new feature specifications
- Run `/task-work TASK-XXX` to implement assigned tasks with AI assistance
- Use `/task-status` to check progress and quality gate results
- Interact via Claude Code, Gemini CLI, or Cursor (universal AI tool support)

**Pain Points with Markdown Approach:**
- ❌ Must manually copy `.claude/agents/*.md` files to every new project
- ❌ Agent definitions become stale - no automatic updates when team improves templates
- ❌ No visibility into what teammates are working on (isolated markdown files)
- ❌ Claude Code specific - can't use same setup with Gemini CLI or Copilot
- ❌ Quality gates are manual reminders in markdown, not enforced programmatically

**Expected Workflow Improvements:**
- ✅ **Automatic agent updates** - New patterns/agents available instantly via MCP
- ✅ **Multi-tool support** - Same workflow works in Claude Code, Gemini CLI, Cursor
- ✅ **Enforced quality gates** - Tests MUST pass before task completion (Phase 4.5 fix loop)
- ✅ **Real-time collaboration** - See teammate progress in shared task hierarchy
- ✅ **Intelligent routing** - AI selects optimal agent based on task complexity (proven in UK Probate Agent)

---

### **Development Teams (5-15 developers)**

**Primary Interactions:**
- Collaborate on Epic → Feature → Task hierarchy in real-time
- Sync progress with external PM tools (Jira/Linear/Azure DevOps)
- Share agent improvements and templates across team via centralized MCP
- Track quality metrics and test coverage across all active work

**Pain Points with Markdown Approach:**
- ❌ **Git merge conflicts** - Multiple developers editing task markdown simultaneously
- ❌ **No progress rollup** - Can't see epic completion % across all features/tasks
- ❌ **Version drift** - Each developer has slightly different agent definitions
- ❌ **Manual PM sync** - Must copy task details to Jira/Linear manually
- ❌ **No audit trail** - Can't see who changed task state or when

**Expected Workflow Improvements:**
- ✅ **PostgreSQL state management** - Single source of truth, no merge conflicts
- ✅ **Automatic progress rollup** - Epic shows real-time % from child features/tasks
- ✅ **Bidirectional PM sync** - Jira/Linear updates reflect in AgenticFlow instantly
- ✅ **Complete audit logging** - Every state change tracked with user/timestamp
- ✅ **Centralized templates** - One update to MCP server reaches all developers

---

### **Product/Project Managers**

**Primary Interactions:**
- Create Epics from requirements using `/epic-create` with auto-sync to Jira/Linear
- Generate Features via `/feature-create` linked to requirements (REQ-001, REQ-002)
- Use `/hierarchy-view` for portfolio dashboard and timeline visualization
- Monitor progress via `/portfolio-dashboard --business-value --risks --timeline`

**Pain Points with Markdown Approach:**
- ❌ **No PM tool integration** - Must recreate epic/features in Jira manually
- ❌ **Stale status** - Markdown files don't reflect actual development progress
- ❌ **No traceability** - Can't map deployed features back to original requirements
- ❌ **Missing business metrics** - No ROI tracking, resource optimization, risk assessment
- ❌ **Limited visibility** - Can't see cross-team dependencies or blockers

**Expected Workflow Improvements:**
- ✅ **One-click PM sync** - Epic created in AgenticFlow appears in Jira/Linear instantly
- ✅ **Real-time dashboards** - Executive portfolio view with business value metrics
- ✅ **Requirements traceability** - REQ-001 → EPIC-001 → FEAT-001 → TASK-001 → Code
- ✅ **Risk assessment** - AI-powered identification of blockers and timeline risks
- ✅ **Progress automation** - Task completion auto-updates epic % in external PM tools

---

### **Tech Leads/Architects**

**Primary Interactions:**
- Review architectural plans in **Phase 2.5: Architectural Review** (auto-triggered)
- Approve/reject designs based on SOLID/DRY/YAGNI compliance scores (0-100)
- Provide **Phase 2.6: Human Checkpoint** for critical/complex tasks
- Monitor technical debt and enforce quality standards via `/task-status --hierarchy`

**Pain Points with Markdown Approach:**
- ❌ **No architectural review gate** - Code written before design review possible
- ❌ **Manual enforcement** - Markdown says "follow SOLID" but doesn't verify
- ❌ **Post-implementation reviews** - Too late to change architecture after coding
- ❌ **No metrics** - Can't track technical debt or pattern compliance trends
- ❌ **Inconsistent standards** - Each developer interprets guidelines differently

**Expected Workflow Improvements:**
- ✅ **Automated Phase 2.5** - AI evaluates architecture BEFORE implementation starts
  - Score ≥80: Auto-approve
  - Score 60-79: Approve with recommendations
  - Score <60: Reject, require redesign
- ✅ **Early intervention** - Architectural issues caught at planning, not code review
- ✅ **Consistent standards** - LangGraph workflow enforces same rules for everyone
- ✅ **Quality metrics** - Track SOLID compliance, pattern usage, technical debt trends
- ✅ **Optional human gate** - Phase 2.6 triggers for security-critical or complex tasks

**Reference from UK Probate Agent:**
```python
def _determine_optimal_approach(self, query: str) -> str:
    """Intelligent routing based on semantic analysis"""
    if combined_indicators:
        return "combined"  # Use research + reasoning
    elif research_score > reasoning_score:
        return "research"  # Legislation search only
    else:
        return "reasoning"  # Legal analysis only
```
This same pattern applies to task routing in AgenticFlow.

---

### **DevOps/Platform Engineers**

**Primary Interactions:**
- Deploy via **Stage 4: Deployment & QA** MCP server
- Configure CI/CD pipelines integrated with quality gates
- Manage MCP server infrastructure (Docker, Kubernetes)
- Monitor system health via observability stack

**Pain Points with Markdown Approach:**
- ❌ **No deployment automation** - Markdown can't trigger actual deploys
- ❌ **Missing quality gates** - Tests in markdown are suggestions, not enforced
- ❌ **No infrastructure state** - Can't track deployment history or rollback
- ❌ **Manual configuration** - Each environment needs separate markdown setup
- ❌ **Limited observability** - Can't monitor workflow execution or failures

**Expected Workflow Improvements:**
- ✅ **Deployment MCP server** - Docker/CI/CD automation via programmatic API
- ✅ **Enforced quality gates** - Phase 4.5 ensures ALL tests pass before deploy
- ✅ **State persistence** - PostgreSQL tracks deployment history and audit trail
- ✅ **Environment configuration** - MCP servers handle dev/staging/prod differences
- ✅ **Full observability** - Metrics, logging, tracing for all workflow executions

---

### Q3: What are the 4 AgenticFlow stages?

**Answer:**

### **Stage 1: Specification**

**What Happens:**
1. **Interactive Requirements Gathering** (`/gather-requirements`)
   - AI-powered Q&A session extracts requirements from user
   - Contextual questions generated based on project domain
   - Iterative refinement until completeness score ≥80%

2. **EARS Formalization** (`/formalize-ears`)
   - Natural language → EARS notation conversion
   - Patterns: Ubiquitous, Event-Driven, State-Driven, Unwanted, Optional
   - Validation for compliance and testability

3. **BDD Generation** (`/generate-bdd`)
   - EARS requirements → Gherkin scenarios
   - Given/When/Then format for all requirements
   - Coverage analysis (happy path, alternatives, error cases)

**Current State:** Markdown-based with manual execution of each command

**Approval Gate:** Human review of EARS requirements and BDD scenarios (completeness check)

**Automation Level:** 70% automated (AI generates, human approves)

**LangGraph Workflow Pattern:**
```python
workflow.add_node("analyze_specification", analyze_spec_node)
workflow.add_node("generate_questions", generate_questions_node)
workflow.add_node("formalize_ears", formalize_ears_node)
workflow.add_node("generate_bdd", generate_bdd_node)
workflow.add_node("validate_completeness", validate_node)

workflow.add_conditional_edges(
    "validate_completeness",
    is_complete,
    {"complete": END, "iterate": "generate_questions"}
)
```

---

### **Stage 2: Tasks Definition**

**What Happens:**
1. **Epic Generation** (`/epic-create`)
   - AI analyzes requirements to create epic structure
   - Syncs to PM tools (Jira/Linear/Azure/GitHub) via MCP
   - Priority assignment and business value estimation

2. **Feature Breakdown** (`/feature-create`, `/feature-generate-tasks`)
   - Epic decomposed into features automatically
   - Each feature linked to requirements (REQ-001, REQ-002)
   - Task generation with acceptance criteria

3. **PM Tool Synchronization** (`/task-sync`, `/epic-sync`)
   - Bidirectional sync maintains consistency
   - Progress rollup: Task → Feature → Epic
   - External ID mapping for traceability

**Current State:** Manual epic/feature creation, no PM tool sync

**Approval Gate:** Human review of work breakdown structure (epic/feature hierarchy)

**Automation Level:** 60% automated (structure generation), 0% PM sync (will be 100%)

**LangGraph Workflow Pattern:**
```python
workflow.add_node("generate_epics", generate_epics_node)
workflow.add_node("generate_features", generate_features_node)
workflow.add_node("generate_tasks", generate_tasks_node)
workflow.add_node("sync_to_pm_tools", sync_pm_tools_node)
workflow.add_node("human_task_review", human_checkpoint_node)

workflow.add_conditional_edges(
    "human_task_review",
    approval_routing,
    {"approved": "sync_to_pm_tools", "rejected": "generate_epics"}
)
```

---

### **Stage 3: Engineering**

**What Happens:**
1. **Requirements Analysis** (Phase 1)
   - Load task context and linked requirements
   - Identify dependencies and technical constraints

2. **Implementation Planning** (Phase 2)
   - AI generates technical approach and file changes
   - Estimates complexity and time requirements

3. **🆕 Architectural Review** (Phase 2.5 - NEW)
   - AI evaluates SOLID, DRY, YAGNI compliance
   - Scoring: 0-100 scale
     - ≥80: Auto-approve (proceed to implementation)
     - 60-79: Approve with recommendations (warnings)
     - <60: Reject (require redesign)

4. **🆕 Human Checkpoint** (Phase 2.6 - OPTIONAL)
   - Triggered for critical/complex tasks
   - Tech lead reviews architectural plan
   - Manual approve/reject decision

5. **Implementation** (Phase 3)
   - Code generation based on approved plan
   - Stack-specific agents (React, Python, .NET, etc.)

6. **Testing** (Phase 4)
   - Automated test execution
   - Coverage analysis

7. **�� Fix Loop** (Phase 4.5 - NEW)
   - **Verifies code compiles** before testing
   - **Up to 3 automatic fix attempts** for failing tests
   - **Only completes when ALL tests pass (100%)**
   - No more completing with compilation errors or failing tests

8. **Code Review** (Phase 5)
   - Only runs if Phase 4.5 passes
   - Quality metrics and pattern compliance

**Current State:** Markdown reminders, manual quality gates

**Approval Gates:**
- **Phase 2.6:** Human checkpoint (optional, for critical tasks)
- **Phase 4.5:** Automated (tests must pass 100%)

**Automation Level:**
- Current: 40% (AI assists, human enforces)
- Target: 85% (automated gates, human review for critical only)

**LangGraph Workflow Pattern:**
```python
workflow.add_node("requirements_analysis", analyze_requirements)
workflow.add_node("implementation_planning", plan_implementation)
workflow.add_node("architectural_review", review_architecture)  # NEW
workflow.add_node("human_checkpoint", human_approval_gate)      # NEW
workflow.add_node("code_generation", generate_code)
workflow.add_node("test_execution", run_tests)
workflow.add_node("fix_loop", fix_failing_tests)                # NEW
workflow.add_node("code_review", review_code)

workflow.add_conditional_edges(
    "architectural_review",
    check_architecture_score,
    {"approved": "code_generation", "review": "human_checkpoint", "rejected": "implementation_planning"}
)

workflow.add_conditional_edges(
    "test_execution",
    tests_passed,
    {"pass": "code_review", "fail": "fix_loop"}
)

workflow.add_conditional_edges(
    "fix_loop",
    fix_attempt_count,
    {"retry": "code_generation", "fail": END, "pass": "code_review"}
)
```

---

### **Stage 4: Deployment & QA**

**What Happens:**
1. **Deployment Preparation** (`/task-complete --prepare-deployment`)
   - Package artifacts for deployment
   - Generate deployment manifests (Docker, K8s)

2. **Test Environment Deployment**
   - Deploy via Deployment MCP server
   - Configure environment-specific settings

3. **QA Automation**
   - Run full QA suite (E2E, integration, performance)
   - Generate validation reports

4. **Release Gate**
   - Human approval for production deployment
   - Compliance and security checklist

**Current State:** Manual deployment, no QA automation

**Approval Gate:** Human release approval (production deployment decision)

**Automation Level:** 30% automated (will be 80% with Deployment MCP)

**LangGraph Workflow Pattern:**
```python
workflow.add_node("prepare_deployment", prepare_deploy_node)
workflow.add_node("deploy_to_test", deploy_test_node)
workflow.add_node("run_qa_suite", run_qa_node)
workflow.add_node("human_release_review", human_checkpoint_node)

workflow.add_conditional_edges(
    "human_release_review",
    approval_routing,
    {"approved": "deploy_to_production", "rejected": END}
)
```

---

### Q4: PM Tool Bidirectional Synchronization

**Answer:**

### **Jira**

**Priority:** ⭐⭐⭐ Must-Have (most common enterprise PM tool)

**Sync Direction:**
- **OUT (AgenticFlow → Jira):**
  - Epic creation → Jira Epic
  - Feature creation → Jira Story (linked to Epic)
  - Task creation → Jira Sub-task (linked to Story)
  - Status updates → Jira workflow transitions (BACKLOG → In Progress → Done)
  - Progress % → Jira epic progress bar

- **IN (Jira → AgenticFlow):**
  - Status changes in Jira → Update AgenticFlow task state
  - Assignee changes → Update task assignee
  - Comments/updates → Sync to task history
  - Sprint assignment → Update task sprint metadata

**Hierarchy Mapping:**
```
AgenticFlow          Jira
EPIC-001      →      Epic (customfield_10011)
FEAT-001      →      Story (issuetype: Story, epic link)
TASK-001      →      Sub-task (issuetype: Sub-task, parent link)
```

**Real-time vs. Batch:**
- **Real-time (< 2s latency):** Epic/feature/task creation, status changes
- **Batch (5-minute intervals):** Progress rollup calculations, bulk updates
- **On-demand:** Manual `/task-sync` or `/epic-sync` command

**MCP Integration Pattern:**
```python
async def create_epic(self, title: str, description: str, requirements: List[str]) -> str:
    epic_data = {
        "fields": {
            "project": {"key": self.project_key},
            "summary": title,
            "description": description,
            "issuetype": {"name": "Epic"},
            "customfield_10011": title  # Epic Name
        }
    }
    response = await self.client.post(f"{self.base_url}/rest/api/3/issue", json=epic_data)
    return response.json()["key"]  # Returns "PROJ-123"
```

---

### **Linear**

**Priority:** ⭐⭐ Nice-to-Have (growing adoption, especially in startups)

**Sync Direction:**
- **OUT (AgenticFlow → Linear):**
  - Epic → Linear Initiative (project-level grouping)
  - Feature → Linear Issue (with initiative link)
  - Task → Linear Sub-issue (related to parent issue)
  - Status updates → Linear workflow state transitions

- **IN (Linear → AgenticFlow):**
  - State changes → Update AgenticFlow status
  - Priority changes → Update task priority
  - Cycle assignment → Update sprint/iteration metadata

**Hierarchy Mapping:**
```
AgenticFlow          Linear
EPIC-001      →      Initiative (teamId, name)
FEAT-001      →      Issue (initiativeId link)
TASK-001      →      Issue (parentId link, related)
```

**Real-time vs. Batch:**
- **Real-time via GraphQL subscriptions:** Status changes, assignee updates
- **Batch (10-minute intervals):** Progress rollup, bulk imports
- **Webhook triggers:** Linear changes push to AgenticFlow instantly

**MCP Integration Pattern:**
```python
async def create_epic(self, title: str, description: str) -> str:
    query = """
    mutation CreateInitiative($input: InitiativeCreateInput!) {
        initiativeCreate(input: $input) {
            initiative { id name }
        }
    }
    """
    variables = {
        "input": {
            "teamId": self.team_id,
            "name": title,
            "description": description
        }
    }
    response = await self.client.post("https://api.linear.app/graphql",
                                      json={"query": query, "variables": variables})
    return response.json()["data"]["initiativeCreate"]["initiative"]["id"]
```

---

### **Azure DevOps**

**Priority:** ⭐⭐⭐ Must-Have (dominant in Microsoft enterprise shops)

**Sync Direction:**
- **OUT (AgenticFlow → Azure DevOps):**
  - Epic → Azure Epic work item
  - Feature → Azure Feature work item (parent: Epic)
  - Task → Azure Task work item (parent: Feature)
  - Status updates → Work item state transitions
  - Test results → Link to Azure Test Plans

- **IN (Azure DevOps → AgenticFlow):**
  - Work item updates → Sync state changes
  - Board column moves → Status updates
  - Sprint assignment → Update iteration path
  - Pull request links → Track code changes

**Hierarchy Mapping:**
```
AgenticFlow          Azure DevOps
EPIC-001      →      Epic (Work Item Type: Epic)
FEAT-001      →      Feature (Parent: Epic, Work Item Type: Feature)
TASK-001      →      Task (Parent: Feature, Work Item Type: Task)
```

**Real-time vs. Batch:**
- **Real-time (webhooks):** Work item state changes push to AgenticFlow
- **Near real-time (1-2 min polling):** AgenticFlow → Azure updates
- **Batch (15-minute intervals):** Progress rollup, iteration metrics

**MCP Integration Pattern:**
```python
async def create_epic(self, title: str, description: str) -> str:
    work_item = {
        "op": "add",
        "path": "/fields/System.Title",
        "value": title
    }
    response = await self.client.post(
        f"{self.org_url}/{self.project}/_apis/wit/workitems/$Epic?api-version=7.0",
        json=[work_item]
    )
    return str(response.json()["id"])  # Returns work item ID
```

---

### **GitHub Issues/Projects**

**Priority:** ⭐⭐ Nice-to-Have (common in open-source, smaller teams)

**Sync Direction:**
- **OUT (AgenticFlow → GitHub):**
  - Epic → GitHub Milestone (project-level grouping)
  - Feature → GitHub Issue (with milestone link)
  - Task → GitHub Issue (with "parent" reference in body)
  - Status updates → Issue labels (backlog, in-progress, done)

- **IN (GitHub → AgenticFlow):**
  - Issue state changes (open/closed) → Status updates
  - Label changes → Update task state
  - PR merges → Auto-complete linked tasks
  - Project board column moves → Status transitions

**Hierarchy Mapping:**
```
AgenticFlow          GitHub
EPIC-001      →      Milestone (title, due date)
FEAT-001      →      Issue (milestone link, labels)
TASK-001      →      Issue (parent reference, task list item)
```

**Real-time vs. Batch:**
- **Real-time (webhooks):** Issue state changes, PR events
- **Near real-time (GraphQL):** AgenticFlow → GitHub updates
- **Batch (30-minute intervals):** Milestone progress calculations

**MCP Integration Pattern:**
```python
async def create_epic(self, title: str, description: str) -> str:
    query = """
    mutation CreateMilestone($input: CreateMilestoneInput!) {
        createMilestone(input: $input) {
            milestone { id title number }
        }
    }
    """
    variables = {
        "input": {
            "repositoryId": self.repo_id,
            "title": title,
            "description": description
        }
    }
    response = await self.client.post("https://api.github.com/graphql",
                                      json={"query": query, "variables": variables})
    return response.json()["data"]["createMilestone"]["milestone"]["number"]
```

---

### **Sync Architecture Summary**

**Data Flow Example (Epic Creation):**
```
1. User: /epic-create "User Management" export:jira,linear priority:high
2. AgenticFlow: Creates EPIC-001 in PostgreSQL
3. PM Tools MCP: Parallel sync to Jira + Linear
   - Jira: Creates PROJ-123 Epic
   - Linear: Creates Initiative init_abc123
4. Mapping stored: EPIC-001 → {jira: "PROJ-123", linear: "init_abc123"}
5. Progress rollup: Task completion → Feature % → Epic % → Jira/Linear update
```

**Real-time vs Batch Strategy:**
- **Real-time (< 2s):** User-initiated creates/updates (epic, feature, task)
- **Near real-time (1-5 min):** Automated status transitions, progress rollup
- **Batch (15-30 min):** Analytics, metrics, bulk operations
- **Webhook-driven:** External PM tool changes push to AgenticFlow instantly

---

### Q5: UK Probate Agent Reference

**Answer:**

### **Yes, it's an existing production LangGraph + AI implementation**

**Location:** `/Users/richardwoollcott/Projects/appmilla_github/uk-probate-agent`

**Description:** A sophisticated AI system for UK legal research specializing in wills, probate, and estate planning, featuring intelligent model optimization for **50-85% cost savings**.

### **Architecture Overview:**

The system provides **three complementary agent systems** using **LangGraph StateGraph orchestration**:

1. **Research Agent** - Legislation search and document retrieval
2. **Reasoning Agent** - Legal analysis using IRAC methodology
3. **Comprehensive Agent** - Combines both with intelligent routing

### **Key Patterns to Replicate in AgenticFlow:**

#### **1. LangGraph StateGraph Workflow** ✅
```python
# From: src/workflows/legal_search_workflow.py
class LegalSearchWorkflow:
    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(LegalSearchState)

        # Multi-stage orchestration
        workflow.add_node("analyze_query", self._analyze_query_node)
        workflow.add_node("search_legislation", self._search_legislation_node)
        workflow.add_node("parse_documents", self._parse_documents_node)
        workflow.add_node("analyze_content", self._analyze_content_node)
        workflow.add_node("generate_response", self._generate_response_node)

        # Conditional routing based on results
        workflow.add_conditional_edges(
            "analyze_query",
            self._should_continue_after_analysis,
            {"search": "search_legislation", "end": END}
        )

        return workflow.compile()
```

**Apply to AgenticFlow:** Same pattern for Stage 3 Engineering workflow with conditional routing between phases.

#### **2. Intelligent Agent Routing** ✅
```python
# From: src/agents/comprehensive_legal_agent.py
def _determine_optimal_approach(self, query: str) -> str:
    """Route to appropriate engine based on query analysis"""

    research_indicators = ["find", "search", "section", "act", "legislation"]
    reasoning_indicators = ["analyze", "explain", "why", "how", "implications"]

    research_score = sum(1 for ind in research_indicators if ind in query.lower())
    reasoning_score = sum(1 for ind in reasoning_indicators if ind in query.lower())

    if research_score > 0 and reasoning_score > 0:
        return "combined"  # Use both engines
    elif research_score > reasoning_score:
        return "research"
    else:
        return "reasoning"
```

**Apply to AgenticFlow:** Route tasks to appropriate agents:
- Simple CRUD → Standard agent
- Complex business logic → TDD agent with architectural review
- User-facing features → BDD agent
- Security-critical → Enhanced review + human checkpoint

#### **3. Multi-Engine Coordination** ✅
```python
# From: src/agents/comprehensive_legal_agent.py
def _use_both_engines(self, query: str, context: str, model_name: str) -> ComprehensiveResponse:
    """Use both engines for comprehensive analysis"""

    # First, get legislation context
    search_result = self.legislation_engine.search_and_analyze(query, model_name)

    # Build enhanced context from legislation
    enhanced_context = self._build_context_from_legislation(search_result, context)

    # Apply reasoning with legislation context
    reasoning_result = self.reasoning_engine.analyze_with_irac(
        query=query,
        context=enhanced_context,
        model_name=model_name
    )

    # Merge results intelligently
    return self._merge_results(search_result, reasoning_result, query)
```

**Apply to AgenticFlow:** Architectural Review (Phase 2.5) feeds into Implementation (Phase 3):
1. Architecture agent analyzes plan → generates recommendations
2. Implementation agent uses recommendations as context
3. Test agent validates against architecture constraints

#### **4. Model Optimization (50-85% Cost Savings)** ✅
```python
# From: src/utils/model_config.py
class ModelConfiguration:
    def get_model_for_query(self, query: str, context: str):
        complexity = self._assess_complexity(query, context)

        if complexity == "simple":
            return "gpt-4.1-mini", {...}  # Fast, cheap ($0.15/1M tokens)
        elif complexity == "moderate":
            return "gpt-4o", {...}         # Balanced ($2.50/1M tokens)
        else:
            return "o4-mini", {...}        # Reasoning ($15/1M tokens)
```

**Key Architectural Decision:** Use cheap models for simple tasks, expensive models only when necessary.

**Cost Savings Example:**
- **Before:** All queries use GPT-4 ($30/1M tokens) → 100 queries = $3.00
- **After:** 70% use gpt-4.1-mini ($0.15), 20% use gpt-4o ($2.50), 10% use o4-mini ($15)
  - 70 × $0.000015 = $0.00105
  - 20 × $0.000025 = $0.00050
  - 10 × $0.000150 = $0.00150
  - **Total = $0.00305** (vs $3.00) = **99% savings** on simple tasks

**Apply to AgenticFlow:**
- Requirements gathering → gpt-4o (quality matters for human interaction)
- EARS generation → gpt-4.1-mini (structured output, simple)
- BDD generation → gpt-4.1-mini (pattern-based)
- Code generation (simple) → gpt-4.1-mini
- Code generation (complex) → o4-mini (reasoning required)
- Architectural review → gpt-4o (critical evaluation)

#### **5. Streaming Response Pattern** ✅
```python
# From: src/workflows/legal_search_workflow.py
def set_streaming_callback(self, callback_func):
    self.streaming_callback = callback_func

def _generate_response_node(self, state):
    if self.streaming_callback:
        response_stream = self.llm.stream(messages)
        for chunk in response_stream:
            if chunk.content:
                self.streaming_callback(chunk.content)
```

**Apply to AgenticFlow:** Stream progress updates during `/task-work`:
- Phase 1: "Analyzing requirements..."
- Phase 2: "Planning implementation for 3 files..."
- Phase 2.5: "Evaluating architecture (SOLID score: 85/100)..."
- Phase 3: "Generating code for UserService.cs..."
- Phase 4: "Running 12 tests..."
- Phase 4.5: "Fix attempt 1/3: Addressing NullReferenceException..."

#### **6. Error Handling and Fallback** ✅
```python
# From: src/workflows/legal_search_workflow.py
def _generate_response_node(self, state):
    try:
        response = self.llm.invoke(messages)
        return LegalSearchState(..., final_response=response.content, workflow_stage="completed")
    except Exception as e:
        fallback_response = f"I encountered an error: {str(e)}\n\nWhat I found:\n- Documents: {len(state.parsed_documents)}\n- Sections: {len(state.relevant_sections)}"
        return LegalSearchState(..., final_response=fallback_response, workflow_stage="completed_with_errors")
```

**Apply to AgenticFlow:** Graceful degradation in Phase 4.5:
- Attempt 1 fails → Retry with enhanced context
- Attempt 2 fails → Retry with simpler approach
- Attempt 3 fails → Mark task as BLOCKED, notify human
- Never complete with failing tests (current gap in markdown approach)

### **Code Examples Available:**

**Core Workflows:**
- `src/workflows/legal_search_workflow.py` - LangGraph StateGraph orchestration
- `src/agents/comprehensive_legal_agent.py` - Multi-engine coordination
- `src/utils/model_config.py` - Model optimization logic
- `src/engines/` - Shared engine pattern (no duplication)

**Testing:**
- `tests/integration/test_full_workflow.py` - End-to-end workflow tests
- `tests/validation/` - Quality monitoring and accuracy measurement

**Documentation:**
- `README.md` - Architecture overview
- Production-ready patterns proven at scale

---

## Technical Specifications & Constraints

### Q8: Technology Stack Validation

**Answer:**

### **LangGraph Version**

**Target: LangGraph 0.2.x (latest stable - currently 0.2.16+)**

**Specific Features Needed:**

✅ **Checkpointing (CRITICAL)**
- Human approval gates require pause/resume capability
- Phase 2.6 (Human Checkpoint) must save state and wait for approval
- Phase 4 (Release Gate) needs persistent workflow state during review period

```python
# From UK Probate Agent pattern - checkpointing for state persistence
from langgraph.checkpoint.sqlite import SqliteSaver

# Production: Use PostgreSQL for checkpoints
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(connection_string=DATABASE_URL)
workflow = workflow.compile(checkpointer=checkpointer)

# Resume workflow after human approval
result = await workflow.ainvoke(
    state,
    config={"configurable": {"thread_id": "TASK-001"}}
)
```

✅ **Persistence (CRITICAL)**
- All workflow state must survive orchestrator restarts
- Task execution can take hours/days (waiting for approvals)
- PostgreSQL-backed persistence ensures no data loss

✅ **Streaming (HIGH PRIORITY)**
- Real-time progress updates during `/task-work`
- Phase-by-phase streaming to user (proven in UK Probate Agent)
```python
# From UK Probate Agent streaming pattern
async for event in workflow.astream(state):
    if event["type"] == "phase_complete":
        print(f"✅ {event['phase']}: {event['message']}")
```

✅ **Conditional Edges (CRITICAL)**
- Phase 2.5 routing: score ≥80 → auto-approve, <60 → reject
- Phase 4.5 routing: tests pass → code review, tests fail → fix loop
```python
workflow.add_conditional_edges(
    "architectural_review",
    lambda state: "approved" if state.score >= 80 else "rejected" if state.score < 60 else "review",
    {"approved": "implementation", "review": "human_checkpoint", "rejected": "planning"}
)
```

✅ **Sub-graphs (FUTURE)**
- Nested workflows for complex features (not MVP, but nice to have)
- Example: BDD generation sub-graph within requirements gathering workflow

---

### **PostgreSQL Schema**

**Multi-tenancy: Shared DB with Tenant Isolation (Recommended for MVP)**

**Schema Approach:**
```sql
-- Option A: Shared schema with org_id column (RECOMMENDED for MVP)
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    org_id UUID NOT NULL,  -- Organization isolation
    project_id UUID NOT NULL REFERENCES projects(id),
    task_id VARCHAR(20) NOT NULL,
    -- ... other columns
    UNIQUE(org_id, task_id)  -- TASK-001 unique per org
);

CREATE INDEX idx_tasks_org_project ON tasks(org_id, project_id);

-- Row-level security for isolation
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY org_isolation ON tasks
    USING (org_id = current_setting('app.current_org')::uuid);
```

**Why Shared DB:**
- ✅ Simpler infrastructure (one PostgreSQL instance)
- ✅ Easier backups and maintenance
- ✅ Cost-effective for MVP
- ✅ RLS (Row-Level Security) provides strong isolation

**Alternative (Future): One DB per Organization**
- Pros: Complete isolation, easier compliance (HIPAA, GDPR)
- Cons: Complex to manage 100+ databases, higher cost
- Use case: Enterprise customers with strict data sovereignty

**Data Retention Period:**

**Active Data (Hot Storage - PostgreSQL):**
- **Tasks:** 12 months (1 year of active project history)
- **Requirements:** Indefinite (reference documentation)
- **Audit Logs:** 12 months (compliance requirement)
- **Workflow Checkpoints:** 30 days (in-progress workflows)

**Archived Data (Cold Storage - S3/Blob):**
- **Tasks (>12 months):** Archive to JSON/Parquet in S3
- **Audit Logs (>12 months):** Compressed archive for compliance
- **Test Results:** 90 days (older results archived)

**Retention Policy Implementation:**
```python
# Scheduled job: archive old data
async def archive_old_tasks():
    # Tasks completed >12 months ago
    old_tasks = await db.query("""
        SELECT * FROM tasks
        WHERE status = 'COMPLETED'
        AND completed_at < NOW() - INTERVAL '12 months'
    """)

    # Export to S3
    s3_client.upload(
        f"archives/{org_id}/tasks-{year}.json.gz",
        compress_json(old_tasks)
    )

    # Delete from PostgreSQL
    await db.execute("""
        DELETE FROM tasks
        WHERE id = ANY($1)
    """, [t.id for t in old_tasks])
```

**Expected Database Size:**

**Assumptions:**
- 50 developers
- 20 tasks/developer/month = 1,000 tasks/month
- 12 months retention = 12,000 tasks
- Each task: ~5KB (JSON state, history, results) = 60MB
- Audit logs: 10 entries/task × 500 bytes = 60MB
- Requirements + BDD: 500 requirements × 2KB = 1MB

**Total Estimate: ~150MB/year (hot data)**
- Small enough for single PostgreSQL instance
- Scales to 500 developers (~750MB/year) comfortably

**Database Instance Sizing:**
- **MVP (50 users):** db.t3.medium (2 vCPU, 4GB RAM, 100GB SSD)
- **Growth (200 users):** db.m5.large (2 vCPU, 8GB RAM, 500GB SSD)
- **Enterprise (500+ users):** db.m5.xlarge + read replicas

---

### **Redis Usage**

**What Gets Cached:**

**1. LLM Responses (HIGH VALUE)**
```python
# Cache key: hash(prompt + model + temperature)
cache_key = f"llm:{hash(prompt)}:{model}:{temp}"
ttl = 3600  # 1 hour

# EARS generation: same requirements → same EARS
if cached := redis.get(f"ears:{hash(requirements)}"):
    return cached
else:
    result = await llm.generate_ears(requirements)
    redis.setex(f"ears:{hash(requirements)}", 86400, result)  # 24h TTL
```

**2. PM Tool Queries (MEDIUM VALUE)**
```python
# Jira epic status: cache for 5 minutes (reduce API calls)
cache_key = f"jira:epic:{epic_id}:status"
if cached := redis.get(cache_key):
    return cached
else:
    status = await jira_client.get_epic_status(epic_id)
    redis.setex(cache_key, 300, status)  # 5 min TTL
```

**3. Agent Routing Decisions (LOW VALUE, but fast)**
```python
# Query complexity assessment: cache for 1 hour
cache_key = f"routing:{hash(query)}"
if cached := redis.get(cache_key):
    return cached  # "research", "reasoning", or "combined"
else:
    approach = await determine_optimal_approach(query)
    redis.setex(cache_key, 3600, approach)  # 1h TTL
```

**4. Architectural Review Scores (HIGH VALUE)**
```python
# Similar code patterns → similar scores (avoid re-evaluation)
code_hash = hash(implementation_plan)
cache_key = f"arch_review:{code_hash}"
if cached := redis.get(cache_key):
    return json.loads(cached)
else:
    score = await architectural_reviewer.evaluate(plan)
    redis.setex(cache_key, 86400, json.dumps(score))  # 24h TTL
```

**TTL Strategy:**

| Cache Type | TTL | Rationale |
|------------|-----|-----------|
| **EARS Generation** | 24 hours | Requirements rarely change within a day |
| **BDD Scenarios** | 24 hours | Scenarios tied to stable requirements |
| **Architectural Review** | 24 hours | Code patterns repeat across team |
| **PM Tool Queries** | 5 minutes | Balance freshness vs. API rate limits |
| **LLM Routing Decisions** | 1 hour | Query patterns stable short-term |
| **Test Results** | 10 minutes | Tests run frequently, need freshness |
| **User Sessions** | 30 minutes | Active workflow state |

**Cache Invalidation:**
- **Requirements updated** → Invalidate EARS and BDD cache
- **Task status changed** → Invalidate PM tool cache
- **Code modified** → Invalidate architectural review cache
- **Manual flush:** `redis-cli FLUSHDB` (for testing/debugging)

**Redis Instance Sizing:**
- **MVP:** 1GB Redis (sufficient for 50 users)
- **Growth:** 4GB Redis with persistence (RDB snapshots every 5 min)
- **Enterprise:** 16GB Redis Cluster (high availability)

---

### **Authentication**

**OAuth 2.1 Providers (Priority Order):**

✅ **1. GitHub (HIGH PRIORITY - Developer-focused)**
- Most developers already have GitHub accounts
- Easy integration with GitHub Projects/Issues
- OAuth flow: `https://github.com/login/oauth/authorize`
```python
# OAuth 2.1 with PKCE (required by spec)
auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=repo,read:org&code_challenge={code_challenge}&code_challenge_method=S256"
```

✅ **2. Google Workspace (HIGH PRIORITY - Enterprise)**
- Enterprise organizations use Google for email/calendar
- SSO integration with Google Workspace
- OAuth flow: `https://accounts.google.com/o/oauth2/v2/auth`

✅ **3. Azure AD / Microsoft Entra (HIGH PRIORITY - Enterprise)**
- Microsoft enterprise customers (Azure DevOps users)
- Integration with Microsoft ecosystem
- OAuth flow: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize`

✅ **4. Okta (MEDIUM PRIORITY - Enterprise SSO)**
- Large enterprises using Okta for identity management
- SAML 2.0 support (in addition to OAuth 2.1)

❌ **NOT MVP:** Facebook, Twitter, LinkedIn (not developer tools)

**Service-to-Service Auth (MCP Servers):**

**Option A: JWT with Service Principals (RECOMMENDED)**
```python
# MCP server validates JWT from orchestrator
from jose import jwt

def validate_service_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            audience="agentecflow-mcp",
            issuer="agentecflow-orchestrator"
        )
        return payload["service"] == "orchestrator"
    except jwt.JWTError:
        return False

# Orchestrator includes JWT in MCP requests
headers = {
    "Authorization": f"Bearer {service_jwt}",
    "X-Request-ID": request_id
}
```

**Option B: mTLS (Mutual TLS) for Production**
- Each MCP server has TLS certificate
- Orchestrator validates server cert, server validates orchestrator cert
- Higher security, more complex setup
- Use for production, not MVP

**Option C: API Keys (Simplest, less secure)**
- Each MCP server has static API key
- Orchestrator includes `X-API-Key` header
- ⚠️ Risk: Key leakage, no rotation, no expiry
- Use only for local development

**Auth Flow Example:**
```
1. User logs in via GitHub OAuth → JWT token (user context)
2. Orchestrator receives user JWT → Validates signature
3. Orchestrator generates service JWT (service context)
4. Orchestrator calls MCP server with service JWT
5. MCP server validates service JWT → Executes tool
6. MCP server logs action with user context (from original JWT)
```

---

### **MCP Protocol Version**

**Yes, using official Model Context Protocol from Anthropic**

**Specification:** https://spec.modelcontextprotocol.io/
**Current Version:** 2024-11-05 (latest stable)

**Transport Strategy:**

**MVP: Stdio Transport (Universal Compatibility)**
```json
// .mcp.json (Claude Code project configuration)
{
  "mcpServers": {
    "agentecflow-requirements": {
      "command": "python",
      "args": ["-m", "agentecflow_mcp.requirements"],
      "env": {
        "DATABASE_URL": "postgresql://...",
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

**Pros:**
- ✅ Works with Claude Code, Gemini CLI, Cursor (all support stdio)
- ✅ Simple deployment (no server infrastructure)
- ✅ Local execution (fast, secure)

**Cons:**
- ❌ Can't share across team (each developer runs own instance)
- ❌ No remote access
- ❌ Process-per-user (resource intensive for large teams)

**Future: HTTP/WebSocket Transport (Team-Scale)**
```json
// .mcp.json (remote MCP server)
{
  "mcpServers": {
    "agentecflow-requirements": {
      "url": "https://mcp.company.com/requirements",
      "transport": "http",
      "auth": {
        "type": "bearer",
        "token": "${AGENTECFLOW_TOKEN}"
      }
    }
  }
}
```

**Pros:**
- ✅ Centralized server (one instance for entire team)
- ✅ Remote access (works from anywhere)
- ✅ Better resource utilization
- ✅ Easier monitoring and logging

**Cons:**
- ❌ Network latency (100-500ms vs <10ms for stdio)
- ❌ More complex security (OAuth, rate limiting)
- ❌ Requires infrastructure (load balancer, auto-scaling)

**Migration Path:**
1. **Phase 1 (MVP):** Stdio for individual developers
2. **Phase 2 (Team):** HTTP for centralized MCP servers
3. **Phase 3 (Enterprise):** WebSocket for real-time bi-directional communication

**Protocol Features Used:**
- ✅ **Tools** (primary): `gather_requirements`, `formalize_ears`, `create_epic`, `sync_to_jira`
- ✅ **Resources** (secondary): `requirements://REQ-001`, `epics://EPIC-001/hierarchy`
- ❌ **Prompts** (not MVP): Reusable prompt templates (future enhancement)

---

### Q9: Quality Gates Implementation Details

**Answer:**

### **Scoring Algorithm (Phase 2.5 Architectural Review)**

**Hybrid Approach: Static Analysis + LLM Evaluation (RECOMMENDED)**

**Step 1: Static Analysis (40% of score)**
```python
# Tools: Ruff (linter), Radon (complexity), mypy (type checking)
import subprocess
import json

def static_analysis_score(file_paths: List[str]) -> float:
    scores = {
        "ruff": 0,      # Code quality (max 15 points)
        "radon": 0,     # Cyclomatic complexity (max 15 points)
        "mypy": 0,      # Type safety (max 10 points)
    }

    # Ruff: 0 violations = 15 points, scale down for violations
    ruff_result = subprocess.run(
        ["ruff", "check", "--output-format=json", *file_paths],
        capture_output=True, text=True
    )
    violations = len(json.loads(ruff_result.stdout))
    scores["ruff"] = max(0, 15 - violations)

    # Radon: Average complexity < 5 = 15 points, scale down
    radon_result = subprocess.run(
        ["radon", "cc", "-j", *file_paths],
        capture_output=True, text=True
    )
    avg_complexity = calculate_avg_complexity(json.loads(radon_result.stdout))
    scores["radon"] = max(0, 15 - (avg_complexity - 5) * 3)

    # mypy: 0 type errors = 10 points
    mypy_result = subprocess.run(
        ["mypy", "--json", *file_paths],
        capture_output=True, text=True
    )
    type_errors = len(json.loads(mypy_result.stdout))
    scores["mypy"] = max(0, 10 - type_errors)

    return sum(scores.values())  # Max 40 points
```

**Step 2: LLM-Based Evaluation (60% of score)**
```python
# SOLID/DRY/YAGNI principles evaluation
async def llm_architecture_score(implementation_plan: str, requirements: str) -> float:
    prompt = f"""
You are a senior software architect evaluating an implementation plan.

REQUIREMENTS:
{requirements}

IMPLEMENTATION PLAN:
{implementation_plan}

Evaluate the plan on these principles (10 points each, max 60 points):

1. **Single Responsibility (SRP):** Each class/module has one reason to change
   - 10 = Perfect, 5 = Some violations, 0 = Major violations

2. **Open/Closed Principle (OCP):** Open for extension, closed for modification
   - 10 = Well-designed abstractions, 5 = Some tight coupling, 0 = Hard to extend

3. **Liskov Substitution (LSP):** Subtypes substitutable for base types
   - 10 = Correct inheritance, 5 = Some violations, 0 = Broken contracts

4. **Interface Segregation (ISP):** Clients not forced to depend on unused interfaces
   - 10 = Minimal interfaces, 5 = Some fat interfaces, 0 = Bloated interfaces

5. **Dependency Inversion (DIP):** Depend on abstractions, not concretions
   - 10 = Proper DI, 5 = Some concrete dependencies, 0 = Tightly coupled

6. **DRY (Don't Repeat Yourself):** No code duplication
   - 10 = No duplication, 5 = Minor duplication, 0 = Major duplication

Respond with ONLY a JSON object:
{{
    "srp_score": 8,
    "ocp_score": 7,
    "lsp_score": 9,
    "isp_score": 8,
    "dip_score": 6,
    "dry_score": 9,
    "reasoning": "Detailed explanation of each score...",
    "recommendations": ["Use dependency injection for...", "Extract interface for..."]
}}
"""

    # Use gpt-4o for quality evaluation (proven in UK Probate Agent)
    response = await llm.ainvoke([HumanMessage(content=prompt)], model="gpt-4o")
    scores = json.loads(response.content)

    total = sum([
        scores["srp_score"],
        scores["ocp_score"],
        scores["lsp_score"],
        scores["isp_score"],
        scores["dip_score"],
        scores["dry_score"]
    ])  # Max 60 points

    return total, scores["reasoning"], scores["recommendations"]
```

**Final Score Calculation:**
```python
def calculate_architecture_score(plan: ImplementationPlan) -> ArchitectureScore:
    # Static analysis (40%)
    static_score = static_analysis_score(plan.file_paths)

    # LLM evaluation (60%)
    llm_score, reasoning, recommendations = await llm_architecture_score(
        plan.implementation_details,
        plan.requirements
    )

    # Total score (0-100)
    total_score = static_score + llm_score

    # Determine action
    if total_score >= 80:
        action = "APPROVED"
    elif total_score >= 60:
        action = "APPROVED_WITH_WARNINGS"
    else:
        action = "REJECTED"

    return ArchitectureScore(
        total_score=total_score,
        static_analysis_score=static_score,
        llm_evaluation_score=llm_score,
        action=action,
        reasoning=reasoning,
        recommendations=recommendations
    )
```

**Example Output:**
```json
{
    "total_score": 78,
    "static_analysis_score": 35,
    "llm_evaluation_score": 43,
    "action": "APPROVED_WITH_WARNINGS",
    "reasoning": "Good adherence to SOLID principles overall. Minor DIP violation: UserService directly depends on SqlUserRepository instead of IUserRepository interface. Some code duplication in validation logic.",
    "recommendations": [
        "Extract IUserRepository interface and inject via constructor",
        "Create shared ValidationHelper class to eliminate duplicated validation logic",
        "Consider breaking UserService into UserQueryService and UserCommandService (CQRS pattern)"
    ]
}
```

---

### **Thresholds (Configurable per Project)**

**Yes, thresholds are configurable** via project settings:

```yaml
# .agentecflow/config.yml
quality_gates:
  architectural_review:
    enabled: true
    auto_approve_threshold: 80      # Default: 80
    warning_threshold: 60           # Default: 60
    model: "gpt-4o"                 # Model for LLM evaluation

    # Per-project overrides
    strict_mode: false              # If true: auto_approve = 85, warning = 70

    # Category weights (advanced)
    weights:
      static_analysis: 0.4          # 40%
      llm_evaluation: 0.6           # 60%

    # Critical projects
    require_human_review: false     # If true: always trigger Phase 2.6
```

**Configuration Scenarios:**

**1. Strict Project (Security/Finance):**
```yaml
quality_gates:
  architectural_review:
    auto_approve_threshold: 90     # Very high bar
    warning_threshold: 75
    require_human_review: true     # Always review, even if score ≥90
```

**2. Prototype/Experimental Project:**
```yaml
quality_gates:
  architectural_review:
    auto_approve_threshold: 60     # Lower bar for speed
    warning_threshold: 40
    model: "gpt-4.1-mini"          # Cheaper model
```

**3. Disabled (Manual Review Only):**
```yaml
quality_gates:
  architectural_review:
    enabled: false                 # Skip Phase 2.5 entirely
```

**Runtime Override:**
```bash
# Command-line override for specific task
/task-work TASK-001 --arch-review-threshold 85

# Disable for one-off task
/task-work TASK-001 --skip-arch-review
```

---

### **Phase 4.5 (Fix Loop) Configuration**

**Attempt Limit: Configurable (default 3)**

```yaml
# .agentecflow/config.yml
quality_gates:
  test_enforcement:
    enabled: true
    max_fix_attempts: 3            # Default: 3, range: 1-5
    compilation_timeout_seconds: 60
    test_timeout_seconds: 300

    # Failure handling
    on_final_failure:
      action: "BLOCK_AND_NOTIFY"   # Options: BLOCK_AND_NOTIFY, AUTO_SUBTASK, ALLOW_PARTIAL
      notify_users: ["tech_lead", "task_assignee"]
```

**Attempt 4 Behavior (Configurable):**

**Option A: BLOCK_AND_NOTIFY (RECOMMENDED for MVP)**
```python
if attempt_count > max_attempts:
    # Mark task as BLOCKED
    await db.update_task_status(task_id, "BLOCKED")

    # Create notification
    await notify(
        users=["tech_lead", "task_assignee"],
        message=f"Task {task_id} blocked: Tests failed after {max_attempts} attempts",
        context={
            "task_id": task_id,
            "failure_summary": failure_summary,
            "suggested_actions": ["Review test failures", "Manual debugging required"]
        }
    )

    # Stop workflow
    return END
```

**Option B: AUTO_SUBTASK (Advanced)**
```python
if attempt_count > max_attempts:
    # Create subtask for manual investigation
    subtask = await create_subtask(
        parent_task_id=task_id,
        title=f"Debug test failures in {task_id}",
        description=f"Automated fix attempts failed. Manual investigation required.\n\nFailures:\n{failure_summary}",
        assignee=current_user,
        priority="HIGH"
    )

    # Link original task to subtask
    await db.link_tasks(task_id, subtask.id, relationship="BLOCKED_BY")

    return END
```

**Option C: ALLOW_PARTIAL (NOT RECOMMENDED - only for non-critical)**
```python
if attempt_count > max_attempts:
    # Allow completion with test failures (with big warning)
    await db.update_task_status(task_id, "COMPLETED_WITH_FAILURES")

    logger.warning(f"Task {task_id} completed with {failed_count} failing tests")

    # Require manual sign-off
    await require_approval(
        task_id=task_id,
        reason="Tests failed, manual review required before merge"
    )
```

**Failure Type Distinction:**

**Yes, Phase 4.5 distinguishes failure types:**

```python
class FailureType(Enum):
    COMPILATION_ERROR = "compilation_error"
    TEST_FAILURE = "test_failure"
    TIMEOUT = "timeout"
    RUNTIME_ERROR = "runtime_error"
    ASSERTION_ERROR = "assertion_error"

async def fix_loop_strategy(failure_type: FailureType, attempt: int) -> str:
    """Different strategies for different failure types"""

    if failure_type == FailureType.COMPILATION_ERROR:
        # Compilation errors: aggressive fixes
        if attempt == 1:
            return "fix_syntax_and_imports"
        elif attempt == 2:
            return "regenerate_with_type_hints"
        else:
            return "request_human_help"

    elif failure_type == FailureType.TEST_FAILURE:
        # Test failures: iterative refinement
        if attempt == 1:
            return "fix_obvious_logic_errors"
        elif attempt == 2:
            return "review_test_expectations"
        else:
            return "partial_implementation_acceptable"

    elif failure_type == FailureType.TIMEOUT:
        # Timeouts: optimization focus
        if attempt == 1:
            return "optimize_algorithms"
        elif attempt == 2:
            return "increase_timeout_limit"  # Temporary
        else:
            return "require_performance_review"

    elif failure_type == FailureType.ASSERTION_ERROR:
        # Assertion errors: test vs code mismatch
        if attempt == 1:
            return "align_implementation_with_tests"
        elif attempt == 2:
            return "review_test_validity"  # Maybe test is wrong?
        else:
            return "escalate_to_tech_lead"
```

**Example Fix Loop Execution:**
```
Attempt 1: NullReferenceException in UserService.cs
→ Strategy: Add null checks
→ Result: FAILED (compilation error - missing using statement)

Attempt 2: Compilation error - 'ILogger' not found
→ Strategy: Add missing imports
→ Result: FAILED (test failure - expected 5 users, got 3)

Attempt 3: Test failure - user count mismatch
→ Strategy: Review query logic, fix WHERE clause
→ Result: SUCCESS (all tests pass)
```

---

### **Test Coverage Requirements**

**Yes, coverage is measured and enforced:**

**Coverage Tools:**
- **Python:** `pytest-cov` with `coverage.py` backend
- **TypeScript:** `Jest` with `--coverage` flag
- **.NET:** `dotnet test --collect:"XPlat Code Coverage"`

**Enforcement Level: Configurable**

```yaml
# .agentecflow/config.yml
quality_gates:
  test_coverage:
    enabled: true
    enforcement_level: "feature"   # Options: file, feature, project

    # Thresholds
    line_coverage_min: 80          # Default: 80%
    branch_coverage_min: 75        # Default: 75%

    # Exclusions
    exclude_patterns:
      - "*/tests/*"
      - "*/migrations/*"
      - "*/__init__.py"
      - "*/generated/*"

    # Failure handling
    on_coverage_failure:
      action: "BLOCK"              # Options: BLOCK, WARN, IGNORE
      generate_missing_tests: true # Auto-generate tests for uncovered code
```

**Enforcement Options:**

**Option A: Per-File Enforcement (STRICTEST)**
```python
# Every modified file must have ≥80% coverage
def check_coverage_per_file(coverage_data: Dict) -> bool:
    for file_path, file_coverage in coverage_data.items():
        if file_coverage["line_percent"] < 80:
            raise CoverageError(
                f"{file_path}: {file_coverage['line_percent']}% coverage (min: 80%)"
            )
    return True
```

**Option B: Per-Feature Enforcement (BALANCED - RECOMMENDED)**
```python
# All files in feature must average ≥80% coverage
def check_coverage_per_feature(feature: Feature, coverage_data: Dict) -> bool:
    feature_files = feature.get_modified_files()

    total_lines = sum(coverage_data[f]["total_lines"] for f in feature_files)
    covered_lines = sum(coverage_data[f]["covered_lines"] for f in feature_files)

    coverage_percent = (covered_lines / total_lines) * 100

    if coverage_percent < 80:
        raise CoverageError(
            f"Feature {feature.id}: {coverage_percent:.1f}% coverage (min: 80%)"
        )

    return True
```

**Option C: Project-Level Enforcement (FLEXIBLE)**
```python
# Overall project coverage must be ≥80%
def check_coverage_overall(coverage_data: Dict) -> bool:
    total_coverage = coverage_data["totals"]["percent_covered"]

    if total_coverage < 80:
        logger.warning(
            f"Project coverage: {total_coverage:.1f}% (target: 80%)"
        )
        # Don't block, just warn

    return True  # Always pass at project level
```

**Coverage Report Example:**
```
=== Test Coverage Report ===
File: src/services/user_service.py
  Lines: 120 / 150 (80.0%) ✅
  Branches: 45 / 60 (75.0%) ✅

File: src/services/order_service.py
  Lines: 85 / 120 (70.8%) ❌ BELOW THRESHOLD
  Branches: 30 / 50 (60.0%) ❌ BELOW THRESHOLD

Missing Coverage:
  - Line 45-52: Error handling not tested
  - Line 78-82: Edge case not covered

Suggested Tests:
  - test_order_service_handles_invalid_payment()
  - test_order_service_validates_quantity_limits()
```

**Auto-Generate Missing Tests (Future Enhancement):**
```python
# If coverage < threshold, generate tests for uncovered code
if coverage_percent < 80:
    missing_tests = await generate_missing_tests(
        file_path=file_path,
        uncovered_lines=uncovered_lines,
        existing_tests=existing_tests
    )

    await write_test_file(f"tests/test_{file_name}", missing_tests)

    # Re-run tests
    coverage_percent = await run_tests_with_coverage(file_path)
```

---

### Q10: MCP Server Architecture

**Answer:**

### **MCP Server Discovery**

**Hybrid Approach: Static Configuration + Dynamic Capabilities Query (RECOMMENDED)**

**Step 1: Static Configuration (Server List)**
```json
// .mcp.json (per-project or user-level)
{
  "mcpServers": {
    "agentecflow-requirements": {
      "command": "python",
      "args": ["-m", "agentecflow_mcp.requirements"],
      "env": {"DATABASE_URL": "postgresql://..."}
    },
    "agentecflow-pm-tools": {
      "command": "python",
      "args": ["-m", "agentecflow_mcp.pm_tools"]
    },
    "agentecflow-testing": {
      "command": "python",
      "args": ["-m", "agentecflow_mcp.testing"]
    },
    "agentecflow-deployment": {
      "command": "python",
      "args": ["-m", "agentecflow_mcp.deployment"]
    }
  }
}
```

**Step 2: Dynamic Discovery (Tool Capabilities)**
```python
# At runtime: Query each server for available tools
async def discover_mcp_tools() -> Dict[str, List[Tool]]:
    tools_by_server = {}

    for server_name, server_config in mcp_config["mcpServers"].items():
        # Connect to server
        client = await MCPClient.connect(server_config)

        # Query capabilities (MCP protocol: list_tools request)
        tools = await client.list_tools()

        tools_by_server[server_name] = tools

        logger.info(f"Discovered {len(tools)} tools from {server_name}")

    return tools_by_server

# Example result:
{
    "agentecflow-requirements": [
        {"name": "gather_requirements", "description": "..."},
        {"name": "formalize_ears", "description": "..."},
        {"name": "generate_bdd", "description": "..."}
    ],
    "agentecflow-pm-tools": [
        {"name": "create_epic", "description": "..."},
        {"name": "sync_to_jira", "description": "..."},
        {"name": "sync_to_linear", "description": "..."}
    ]
}
```

**Advantages:**
- ✅ **Static config:** Easy to manage, version-controlled
- ✅ **Dynamic discovery:** Handles tool updates without config changes
- ✅ **Tool introspection:** Client knows exact capabilities at runtime
- ✅ **Fallback:** If dynamic query fails, use cached tool list

**Alternative (Not Recommended): Fully Static**
- Pre-defined tool list in code
- ❌ Requires redeployment for new tools
- ❌ No version compatibility detection

---

### **MCP Server Deployment**

**Separate Processes/Containers per MCP Server (RECOMMENDED for Production)**

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│               LangGraph Orchestrator                     │
│  - Workflow execution                                    │
│  - State management (PostgreSQL)                         │
│  - MCP client connections                                │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬───────────┐
        ▼                 ▼                 ▼           ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Requirements │  │  PM Tools    │  │   Testing    │  │  Deployment  │
│  MCP Server  │  │  MCP Server  │  │  MCP Server  │  │  MCP Server  │
├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
│ - EARS gen   │  │ - Jira sync  │  │ - pytest     │  │ - Docker     │
│ - BDD gen    │  │ - Linear     │  │ - Jest       │  │ - K8s        │
│ - Validation │  │ - Azure      │  │ - Playwright │  │ - CI/CD      │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

**Deployment (Docker Compose):**
```yaml
# docker-compose.yml
services:
  orchestrator:
    image: agentecflow/orchestrator:latest
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
    depends_on:
      - requirements-mcp
      - pm-tools-mcp
      - testing-mcp
      - deployment-mcp

  requirements-mcp:
    image: agentecflow/requirements-mcp:latest
    environment:
      - DATABASE_URL=postgresql://...
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    deploy:
      replicas: 2  # Horizontal scaling

  pm-tools-mcp:
    image: agentecflow/pm-tools-mcp:latest
    environment:
      - JIRA_URL=${JIRA_URL}
      - LINEAR_API_KEY=${LINEAR_API_KEY}
    deploy:
      replicas: 2

  testing-mcp:
    image: agentecflow/testing-mcp:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # For test containers
    deploy:
      replicas: 3  # Testing is CPU-intensive

  deployment-mcp:
    image: agentecflow/deployment-mcp:latest
    environment:
      - KUBE_CONFIG=${KUBE_CONFIG}
    deploy:
      replicas: 1  # Deployments are sequential
```

**Scaling Strategy:**

**Stateless MCP Servers (Can Run Multiple Instances):**
- ✅ **Requirements MCP:** Stateless (LLM calls only) → Scale to N instances
- ✅ **PM Tools MCP:** Mostly stateless (API calls) → Scale to N instances
- ✅ **Testing MCP:** Stateless (ephemeral test containers) → Scale to N instances

**Stateful MCP Servers (Single Instance or Leader Election):**
- ⚠️ **Deployment MCP:** Stateful (deployment locks) → Single instance or leader election

**Load Balancing:**
```python
# Round-robin across MCP instances
class MCPClientPool:
    def __init__(self, server_instances: List[str]):
        self.instances = server_instances
        self.current_index = 0

    async def call_tool(self, tool_name: str, params: dict):
        # Get next instance (round-robin)
        instance = self.instances[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.instances)

        # Call tool on selected instance
        client = await MCPClient.connect(instance)
        return await client.call_tool(tool_name, params)

# Usage
requirements_pool = MCPClientPool([
    "requirements-mcp-1:8000",
    "requirements-mcp-2:8000"
])

result = await requirements_pool.call_tool("gather_requirements", {...})
```

**Alternative (Not Recommended for Production): All-in-One Process**
```python
# Single process with all tools (OK for development, NOT production)
class AgentecflowMCPServer:
    def __init__(self):
        self.requirements_tools = RequirementsTools()
        self.pm_tools = PMTools()
        self.testing_tools = TestingTools()
        self.deployment_tools = DeploymentTools()

    def register_tools(self, server: Server):
        # Register all tools in one process
        self.requirements_tools.register(server)
        self.pm_tools.register(server)
        self.testing_tools.register(server)
        self.deployment_tools.register(server)
```

**Why Separate is Better:**
- ✅ **Independent scaling:** Scale testing MCP separately from requirements MCP
- ✅ **Fault isolation:** Testing MCP crash doesn't affect requirements MCP
- ✅ **Technology flexibility:** Use different languages per MCP (Python, Node.js, Go)
- ✅ **Security boundaries:** Deployment MCP has K8s access, others don't

---

### **Tool Invocation Pattern**

**Option B: LangGraph Node Integration (RECOMMENDED)**

```python
# Pattern from UK Probate Agent: External tools as LangGraph nodes
from langgraph.graph import StateGraph, END

class TaskExecutionWorkflow:
    def __init__(self, mcp_clients: Dict[str, MCPClient]):
        self.mcp = mcp_clients
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(TaskExecutionState)

        # MCP tools as workflow nodes
        workflow.add_node("gather_requirements", self._requirements_node)
        workflow.add_node("formalize_ears", self._ears_node)
        workflow.add_node("sync_to_jira", self._jira_sync_node)
        workflow.add_node("run_tests", self._testing_node)

        # Conditional routing based on MCP results
        workflow.add_conditional_edges(
            "run_tests",
            lambda state: "passed" if state.test_results.all_passed else "failed",
            {"passed": "sync_to_jira", "failed": "fix_loop"}
        )

        return workflow.compile()

    async def _requirements_node(self, state: TaskExecutionState):
        """Invoke Requirements MCP tool as LangGraph node"""
        result = await self.mcp["requirements"].call_tool(
            "gather_requirements",
            {"query": state.user_input, "context": state.context}
        )

        state.requirements = result["ears_requirements"]
        state.workflow_stage = "requirements_gathered"
        return state

    async def _ears_node(self, state: TaskExecutionState):
        """Invoke EARS formalization as node"""
        result = await self.mcp["requirements"].call_tool(
            "formalize_ears",
            {"requirements": state.requirements}
        )

        state.ears_notation = result["ears_notation"]
        state.workflow_stage = "ears_formalized"
        return state

    async def _jira_sync_node(self, state: TaskExecutionState):
        """Invoke Jira sync as node"""
        result = await self.mcp["pm_tools"].call_tool(
            "sync_to_jira",
            {
                "epic_id": state.epic_id,
                "task_id": state.task_id,
                "status": state.status,
                "progress": state.progress
            }
        )

        state.jira_issue_id = result["jira_issue_id"]
        state.workflow_stage = "synced_to_jira"
        return state

    async def _testing_node(self, state: TaskExecutionState):
        """Invoke testing as node"""
        result = await self.mcp["testing"].call_tool(
            "run_test_suite",
            {
                "project_path": state.project_path,
                "test_files": state.test_files
            }
        )

        state.test_results = result
        state.workflow_stage = "tests_executed"
        return state
```

**Why LangGraph Node Pattern:**
- ✅ **Conditional routing:** Can route based on MCP tool results (test pass/fail → different paths)
- ✅ **State management:** LangGraph manages state across MCP invocations
- ✅ **Checkpointing:** Can pause/resume workflow at MCP boundaries
- ✅ **Error recovery:** LangGraph handles MCP failures with retries/fallbacks
- ✅ **Observability:** Full workflow execution trace including MCP calls

**Alternative: LangChain Tool Integration (Option C)**
```python
# Works, but less control over workflow orchestration
from langchain.tools import BaseTool
from langchain.agents import create_react_agent

class MCPTool(BaseTool):
    """Wrap MCP tool as LangChain tool"""
    name = "create_epic"
    description = "Create epic in PM tool"

    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client

    async def _arun(self, title: str, description: str):
        return await self.mcp.call_tool("create_epic", {
            "title": title,
            "description": description
        })

# Usage with ReAct agent
tools = [
    MCPTool(name="create_epic", mcp_client=pm_tools_mcp),
    MCPTool(name="sync_to_jira", mcp_client=pm_tools_mcp)
]

agent = create_react_agent(llm, tools)
result = await agent.ainvoke({"input": "Create epic for user authentication"})
```

**Why Not LangChain Tools (for Agentecflow):**
- ❌ Less control over execution flow (ReAct agent decides tool order)
- ❌ No built-in checkpointing (can't pause for human approval)
- ❌ Harder to implement quality gates (testing → fix loop → retry)
- ✅ OK for simple chains, NOT for complex workflows

---

### **Error Handling in MCP**

**Multi-Layer Error Handling: MCP Server + LangGraph Orchestrator**

**Layer 1: MCP Server Error Handling**
```python
# MCP server catches and categorizes errors
@mcp_server.tool()
async def create_epic(title: str, description: str, sync_to: str) -> dict:
    try:
        if sync_to == "jira":
            result = await jira_client.create_epic(title, description)
            return {"status": "success", "epic_id": result["key"]}

    except JiraAPIError as e:
        if e.status_code == 429:  # Rate limit
            return {
                "status": "error",
                "error_type": "rate_limit",
                "retry_after": e.retry_after,
                "message": "Jira API rate limit exceeded"
            }
        elif e.status_code >= 500:  # Jira server error
            return {
                "status": "error",
                "error_type": "server_error",
                "retryable": True,
                "message": f"Jira server error: {e.message}"
            }
        else:  # Client error (bad request)
            return {
                "status": "error",
                "error_type": "client_error",
                "retryable": False,
                "message": f"Invalid request: {e.message}"
            }

    except NetworkError as e:
        return {
            "status": "error",
            "error_type": "network_error",
            "retryable": True,
            "message": "Network connection failed"
        }
```

**Layer 2: LangGraph Orchestrator Error Handling**
```python
async def _jira_sync_node(self, state: TaskExecutionState):
    """LangGraph node with retry logic"""

    max_retries = 3
    retry_delay = [2, 5, 10]  # Exponential backoff

    for attempt in range(max_retries):
        result = await self.mcp["pm_tools"].call_tool("create_epic", {...})

        if result["status"] == "success":
            state.jira_epic_id = result["epic_id"]
            return state

        elif result["error_type"] == "rate_limit":
            # Wait for rate limit reset
            wait_time = int(result["retry_after"])
            logger.warning(f"Rate limited, waiting {wait_time}s...")
            await asyncio.sleep(wait_time)
            continue

        elif result["error_type"] == "server_error" and result["retryable"]:
            # Retry with backoff
            logger.warning(f"Server error (attempt {attempt+1}/{max_retries}), retrying...")
            await asyncio.sleep(retry_delay[attempt])
            continue

        elif result["error_type"] == "client_error":
            # Don't retry client errors
            logger.error(f"Client error: {result['message']}")
            state.errors.append(result["message"])
            return state  # Continue workflow with error logged

        else:
            # Unknown error
            logger.error(f"Unknown error: {result}")
            break

    # All retries exhausted
    state.workflow_stage = "jira_sync_failed"
    state.errors.append(f"Failed to sync to Jira after {max_retries} attempts")

    return state  # Continue workflow (degraded mode)
```

**Layer 3: Conditional Routing Based on Errors**
```python
def _should_continue_after_jira_sync(state: TaskExecutionState) -> str:
    """Route based on Jira sync result"""

    if state.jira_epic_id:
        return "success"  # Continue to next stage

    elif "jira_sync_failed" in state.errors:
        # Queue for later sync (degraded mode)
        logger.warning("Jira sync failed, queuing for retry...")
        queue_for_retry(state.epic_id, "jira_sync")
        return "queue"  # Continue workflow without Jira sync

    else:
        return "success"  # No Jira sync requested

workflow.add_conditional_edges(
    "sync_to_jira",
    _should_continue_after_jira_sync,
    {
        "success": "next_stage",
        "queue": "next_stage",  # Continue without blocking
    }
)
```

**Layer 4: Queue for Later Processing**
```python
# Failed operations queued for async retry
class RetryQueue:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def enqueue(self, operation: str, params: dict, max_retries: int = 10):
        """Add failed operation to retry queue"""
        retry_item = {
            "operation": operation,
            "params": params,
            "attempts": 0,
            "max_retries": max_retries,
            "next_retry": time.time() + 60  # Retry in 1 minute
        }

        await self.redis.lpush("retry_queue", json.dumps(retry_item))

    async def process_queue(self):
        """Background worker processes retry queue"""
        while True:
            item_json = await self.redis.rpop("retry_queue")
            if not item_json:
                await asyncio.sleep(10)
                continue

            item = json.loads(item_json)

            if item["attempts"] >= item["max_retries"]:
                logger.error(f"Max retries exhausted: {item['operation']}")
                # Store in dead letter queue for manual intervention
                await self.redis.lpush("dead_letter_queue", item_json)
                continue

            # Wait until next retry time
            wait_time = item["next_retry"] - time.time()
            if wait_time > 0:
                await asyncio.sleep(wait_time)

            # Retry operation
            try:
                result = await self.mcp[item["operation_server"]].call_tool(
                    item["operation"],
                    item["params"]
                )

                if result["status"] == "success":
                    logger.info(f"Retry successful: {item['operation']}")
                else:
                    # Re-queue with increased delay
                    item["attempts"] += 1
                    item["next_retry"] = time.time() + (60 * (2 ** item["attempts"]))  # Exponential backoff
                    await self.redis.lpush("retry_queue", json.dumps(item))

            except Exception as e:
                logger.error(f"Retry failed: {e}")
                item["attempts"] += 1
                await self.redis.lpush("retry_queue", json.dumps(item))
```

**Error Handling Summary:**
- **Immediate retry:** Network errors, rate limits (with backoff)
- **Queue for later:** Server errors after max retries
- **Fail fast:** Client errors (invalid requests)
- **Graceful degradation:** Continue workflow without failed operation
- **Manual intervention:** Dead letter queue for persistent failures

---

## Final Clarifications

### Q16: Performance Requirements

**Answer:**

### **Workflow Execution Time Targets**

**Stage 1: Requirements Gathering**

**Target: 2-5 minutes for interactive Q&A**

**Breakdown:**
- Initial spec analysis: 10-15 seconds (LLM analyzes input)
- Question generation: 5-10 seconds per iteration (3-5 iterations typical)
- EARS formalization: 20-30 seconds (batch LLM processing)
- BDD generation: 30-45 seconds (per requirement, parallel processing)
- **Total: 2-5 minutes** (depending on iteration count)

**Implementation:**
```python
# Performance targets per stage
PERFORMANCE_TARGETS = {
    "analyze_specification": 15,      # seconds
    "generate_questions": 10,         # per iteration
    "formalize_ears": 30,            # batch processing
    "generate_bdd": 45,              # parallel generation
    "max_total_time": 300            # 5 minutes hard limit
}

# Timeout enforcement
async def requirements_workflow_with_timeout(spec: str):
    try:
        result = await asyncio.wait_for(
            requirements_workflow.execute(spec),
            timeout=PERFORMANCE_TARGETS["max_total_time"]
        )
        return result
    except asyncio.TimeoutError:
        logger.error("Requirements gathering exceeded 5 minute limit")
        # Return partial results
        return partial_requirements
```

**Optimization Strategy (from UK Probate Agent):**
- Use **gpt-4.1-mini** for question generation (fast, cheap)
- Use **gpt-4o** for EARS formalization (quality matters)
- **Parallel BDD generation** for multiple requirements
```python
# Parallel processing pattern
async def generate_bdd_parallel(requirements: List[Requirement]) -> List[BDDScenario]:
    tasks = [generate_bdd_for_requirement(req) for req in requirements]
    return await asyncio.gather(*tasks)  # Parallel execution
```

---

**Stage 2: Task Breakdown**

**Target: <30 seconds for epic → features → tasks**

**Breakdown:**
- Epic analysis: 5-8 seconds (LLM extracts themes)
- Feature generation: 10-15 seconds (5-10 features typical)
- Task breakdown: 10-15 seconds (parallel per feature)
- PM tool sync: 2-5 seconds (async, non-blocking)
- **Total: 25-30 seconds**

**Implementation:**
```python
# Stage 2 performance targets
async def task_breakdown_workflow(epic: Epic):
    start_time = time.time()

    # Step 1: Analyze epic (5-8s)
    themes = await llm.extract_themes(epic.description)

    # Step 2: Generate features in parallel (10-15s)
    feature_tasks = [
        llm.generate_feature(theme, epic.requirements)
        for theme in themes
    ]
    features = await asyncio.gather(*feature_tasks)

    # Step 3: Generate tasks in parallel (10-15s)
    task_generation_jobs = [
        llm.break_into_tasks(feature)
        for feature in features
    ]
    all_tasks = await asyncio.gather(*task_generation_jobs)

    # Step 4: PM sync (async, don't wait)
    asyncio.create_task(sync_to_pm_tools(epic, features, all_tasks))

    elapsed = time.time() - start_time
    logger.info(f"Task breakdown completed in {elapsed:.1f}s (target: <30s)")

    if elapsed > 30:
        logger.warning(f"⚠️ Exceeded target: {elapsed:.1f}s > 30s")

    return {"epic": epic, "features": features, "tasks": all_tasks}
```

**Optimization:**
- **Batch LLM requests** (5 features in one request vs 5 separate)
- **Async PM sync** (don't block on Jira/Linear API)
- **Cache similar epics** (if epic description similar → reuse structure)

---

**Stage 3: Engineering (Task Execution)**

**Targets:**
- **Simple task:** <10 minutes (CRUD, basic API endpoint)
- **Complex task:** <30 minutes (business logic, multiple files, extensive tests)

**Phase Breakdown (Simple Task):**
```
Phase 1: Requirements Analysis      →  30s
Phase 2: Implementation Planning     →  45s
Phase 2.5: Architectural Review      →  60s (LLM evaluation)
Phase 3: Code Generation             →  120s (2 minutes)
Phase 4: Test Execution              →  90s (pytest/jest)
Phase 4.5: Fix Loop (if needed)      →  180s (3 attempts × 60s)
Phase 5: Code Review                 →  45s (static analysis)
─────────────────────────────────────────
TOTAL (simple):                       8-10 minutes
```

**Phase Breakdown (Complex Task):**
```
Phase 1: Requirements Analysis       →  60s
Phase 2: Implementation Planning     →  120s (complex design)
Phase 2.5: Architectural Review      →  90s
Phase 2.6: Human Checkpoint          →  variable (minutes to hours)
Phase 3: Code Generation             →  300s (5 minutes, multiple files)
Phase 4: Test Execution              →  180s (3 minutes)
Phase 4.5: Fix Loop                  →  360s (6 minutes, multiple attempts)
Phase 5: Code Review                 →  90s
─────────────────────────────────────────
TOTAL (complex, no human wait):      20-30 minutes
```

**Performance Enforcement:**
```python
# Per-phase timeout configuration
PHASE_TIMEOUTS = {
    "requirements_analysis": 120,      # 2 minutes max
    "implementation_planning": 180,    # 3 minutes max
    "architectural_review": 120,       # 2 minutes max
    "code_generation": 600,            # 10 minutes max
    "test_execution": 300,             # 5 minutes max
    "fix_loop": 600,                   # 10 minutes max (3 attempts)
    "code_review": 120                 # 2 minutes max
}

async def execute_phase_with_timeout(phase_name: str, phase_func, state):
    timeout = PHASE_TIMEOUTS[phase_name]

    try:
        result = await asyncio.wait_for(
            phase_func(state),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        logger.error(f"Phase {phase_name} exceeded {timeout}s timeout")
        # Mark task as BLOCKED
        state.status = "BLOCKED"
        state.errors.append(f"{phase_name} timeout")
        return state
```

---

**Stage 4: Deployment**

**Target: <5 minutes to test environment**

**Breakdown:**
- Package artifacts: 30-60s (Docker build or artifact creation)
- Deploy to test env: 90-120s (K8s apply or container start)
- Health checks: 30-60s (wait for service ready)
- Run smoke tests: 60-90s (basic validation)
- **Total: 3-5 minutes**

**Implementation:**
```python
# Stage 4 performance targets
async def deploy_to_test_environment(task: Task):
    start_time = time.time()

    # Step 1: Package (30-60s)
    artifacts = await package_application(task.project_path)

    # Step 2: Deploy (90-120s)
    deployment = await deploy_to_k8s(
        artifacts,
        environment="test",
        timeout=120
    )

    # Step 3: Health checks (30-60s)
    await wait_for_healthy(deployment, timeout=60)

    # Step 4: Smoke tests (60-90s)
    smoke_results = await run_smoke_tests(deployment.url)

    elapsed = time.time() - start_time
    logger.info(f"Deployment completed in {elapsed:.1f}s (target: <300s)")

    return {
        "deployment_id": deployment.id,
        "url": deployment.url,
        "duration": elapsed,
        "smoke_tests": smoke_results
    }
```

**Optimization:**
- **Pre-built base images** (reduce Docker build time)
- **Parallel health checks** (don't wait sequentially)
- **Incremental deploys** (only deploy changed services)

---

### **Concurrency Limits**

**Max Concurrent Workflows per User**

**Limit: 3 active workflows per user (configurable)**

**Rationale:**
- Prevents resource exhaustion from runaway workflows
- Encourages focus (finish current work before starting new)
- Limits blast radius if user's workflows fail

**Implementation:**
```python
# Per-user workflow limit
class WorkflowOrchestrator:
    def __init__(self):
        self.active_workflows: Dict[str, List[str]] = {}  # user_id → [workflow_ids]
        self.max_workflows_per_user = 3

    async def start_workflow(self, user_id: str, workflow_type: str, params: dict):
        # Check concurrent limit
        active_count = len(self.active_workflows.get(user_id, []))

        if active_count >= self.max_workflows_per_user:
            raise ConcurrencyLimitError(
                f"User {user_id} has {active_count} active workflows (max: {self.max_workflows_per_user})"
            )

        # Start workflow
        workflow_id = str(uuid.uuid4())
        workflow = await self._execute_workflow(workflow_type, params)

        # Track active workflow
        if user_id not in self.active_workflows:
            self.active_workflows[user_id] = []
        self.active_workflows[user_id].append(workflow_id)

        return workflow

    async def complete_workflow(self, user_id: str, workflow_id: str):
        # Remove from active list
        if user_id in self.active_workflows:
            self.active_workflows[user_id].remove(workflow_id)
```

**Configuration Override:**
```yaml
# .agentecflow/config.yml
concurrency:
  max_workflows_per_user: 3        # Default: 3
  max_workflows_per_team: 50       # Team-level limit
  max_workflows_global: 500        # System-wide limit
```

---

**Max Concurrent LLM Requests per Instance**

**Limit: 50 concurrent LLM requests (rate limit consideration)**

**OpenAI Rate Limits (Enterprise Tier):**
- **RPM (Requests Per Minute):** 10,000 (GPT-4)
- **TPM (Tokens Per Minute):** 2,000,000
- **Concurrency:** 100 concurrent requests

**Agentecflow Strategy: 50% of OpenAI limit (50 concurrent)**

**Rationale:**
- Leave headroom for other services using same OpenAI account
- Prevent cascading failures if rate limit hit
- Allow burst capacity for urgent requests

**Implementation:**
```python
# LLM request semaphore
class LLMRateLimiter:
    def __init__(self, max_concurrent: int = 50):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.request_count = 0
        self.rate_limit_hits = 0

    async def execute_llm_request(self, llm_func, *args, **kwargs):
        async with self.semaphore:  # Acquire slot
            self.request_count += 1

            try:
                result = await llm_func(*args, **kwargs)
                return result

            except RateLimitError as e:
                self.rate_limit_hits += 1
                logger.warning(f"Rate limit hit (total: {self.rate_limit_hits})")

                # Exponential backoff
                wait_time = min(60, 2 ** self.rate_limit_hits)
                await asyncio.sleep(wait_time)

                # Retry
                return await llm_func(*args, **kwargs)

# Usage
llm_limiter = LLMRateLimiter(max_concurrent=50)

async def generate_code(prompt: str):
    return await llm_limiter.execute_llm_request(
        llm.ainvoke,
        [HumanMessage(content=prompt)]
    )
```

**Monitoring:**
```python
# Track LLM usage metrics
metrics = {
    "requests_total": llm_limiter.request_count,
    "rate_limit_hits": llm_limiter.rate_limit_hits,
    "concurrent_requests_current": 50 - llm_limiter.semaphore._value,
    "concurrent_requests_max": 50
}

# Alert if hitting limits frequently
if llm_limiter.rate_limit_hits > 10:
    alert("High LLM rate limit hits - consider increasing concurrency limit or upgrading OpenAI tier")
```

---

**Max Concurrent Test Executions**

**Limit: 10 concurrent test suites (CI/CD resource constraint)**

**Rationale:**
- Test execution is CPU/memory intensive
- Parallel tests compete for Docker containers, database connections
- Limit prevents resource exhaustion on CI/CD infrastructure

**Implementation:**
```python
# Test execution semaphore
class TestExecutionManager:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_tests: Dict[str, TestExecution] = {}

    async def run_test_suite(self, task_id: str, test_files: List[str]):
        async with self.semaphore:  # Acquire test slot
            logger.info(f"Running tests for {task_id} (slot {10 - self.semaphore._value}/10)")

            # Execute tests in isolated container
            test_result = await self._run_in_container(task_id, test_files)

            return test_result

    async def _run_in_container(self, task_id: str, test_files: List[str]):
        # Isolated test execution
        container = await docker_client.containers.run(
            image="test-runner:latest",
            command=["pytest", *test_files, "--tb=short", "--json-report"],
            volumes={
                f"/tasks/{task_id}": {"bind": "/app", "mode": "ro"}
            },
            mem_limit="2g",
            cpu_quota=100000,  # 1 CPU core
            auto_remove=True
        )

        # Wait for completion
        exit_code = await container.wait()
        logs = await container.logs()

        return TestResult.parse(logs)

# Configuration
test_manager = TestExecutionManager(max_concurrent=10)
```

**Queueing for Fairness:**
```python
# FIFO queue for test requests
test_queue = asyncio.Queue()

async def queue_test_request(task_id: str, test_files: List[str]):
    await test_queue.put({"task_id": task_id, "test_files": test_files})

async def test_execution_worker():
    """Background worker processing test queue"""
    while True:
        request = await test_queue.get()

        # Execute test (blocks until slot available)
        result = await test_manager.run_test_suite(
            request["task_id"],
            request["test_files"]
        )

        # Notify task completion
        await notify_task_test_complete(request["task_id"], result)

        test_queue.task_done()

# Start workers
for _ in range(10):  # 10 worker threads
    asyncio.create_task(test_execution_worker())
```

---

### **Database Query Performance**

**Target: <100ms for 95th percentile queries**

**Query Categories:**

**1. Hot Path Queries (must be <50ms):**
```sql
-- Task status lookup (most frequent)
SELECT * FROM tasks WHERE task_id = 'TASK-001' AND org_id = 'org-uuid';

-- Index optimization
CREATE INDEX idx_tasks_lookup ON tasks(org_id, task_id) INCLUDE (status, assignee, updated_at);

-- Explain plan target: Index Only Scan, ~5-10ms
```

**2. Reporting Queries (target <100ms):**
```sql
-- Epic progress rollup
SELECT
    e.epic_id,
    COUNT(t.id) as total_tasks,
    SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks,
    (SUM(CASE WHEN t.status = 'COMPLETED' THEN 1 ELSE 0 END)::float / COUNT(t.id) * 100) as progress_pct
FROM epics e
JOIN features f ON f.epic_id = e.id
JOIN tasks t ON t.feature_id = f.id
WHERE e.org_id = 'org-uuid' AND e.epic_id = 'EPIC-001'
GROUP BY e.epic_id;

-- Index optimization
CREATE INDEX idx_tasks_status_rollup ON tasks(feature_id, status) WHERE status IS NOT NULL;

-- Materialized view for complex rollups (refresh every 5 min)
CREATE MATERIALIZED VIEW epic_progress_mv AS
SELECT ...;
REFRESH MATERIALIZED VIEW CONCURRENTLY epic_progress_mv;
```

**3. Analytical Queries (target <500ms, run async):**
```sql
-- Team velocity analysis (last 30 days)
SELECT
    DATE_TRUNC('day', completed_at) as date,
    COUNT(*) as tasks_completed,
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_completion_time_sec
FROM tasks
WHERE org_id = 'org-uuid'
  AND status = 'COMPLETED'
  AND completed_at > NOW() - INTERVAL '30 days'
GROUP BY DATE_TRUNC('day', completed_at)
ORDER BY date;

-- Run async, cache results
```

**Performance Monitoring:**
```python
# Query performance tracking
import time
from functools import wraps

def track_query_performance(query_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            # Record metric
            metrics.histogram(
                "db_query_duration_ms",
                duration_ms,
                tags={"query": query_name}
            )

            # Alert if slow
            if duration_ms > 100:
                logger.warning(f"Slow query: {query_name} took {duration_ms:.1f}ms")

            return result
        return wrapper
    return decorator

# Usage
@track_query_performance("get_task_by_id")
async def get_task(task_id: str):
    return await db.fetchrow("SELECT * FROM tasks WHERE task_id = $1", task_id)
```

---

**PM Tool Sync Latency**

**Target: <2 seconds for create_epic**

**Breakdown:**
- Jira API call: 500-1000ms (network + processing)
- Linear GraphQL: 300-600ms
- Database update: 50-100ms (store external ID mapping)
- **Total: <2 seconds**

**Implementation:**
```python
# PM sync with timeout
async def create_epic_with_sync(epic: Epic, sync_to: List[str]):
    # Create in database first (always succeeds)
    db_epic = await db.create_epic(epic)

    # Sync to PM tools (with timeout)
    sync_tasks = []

    if "jira" in sync_to:
        sync_tasks.append(
            asyncio.wait_for(
                jira_client.create_epic(epic),
                timeout=2.0
            )
        )

    if "linear" in sync_to:
        sync_tasks.append(
            asyncio.wait_for(
                linear_client.create_initiative(epic),
                timeout=2.0
            )
        )

    # Execute in parallel
    try:
        results = await asyncio.gather(*sync_tasks, return_exceptions=True)

        # Store external IDs
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"PM sync failed for {sync_to[i]}: {result}")
            else:
                await db.store_external_id(
                    db_epic.id,
                    tool=sync_to[i],
                    external_id=result["id"]
                )

        return db_epic

    except asyncio.TimeoutError:
        logger.error("PM sync timeout (>2s)")
        # Epic still created in DB, sync can retry later
        return db_epic
```

**Latency Optimization:**
- **Parallel sync:** Jira + Linear in parallel (not sequential)
- **Async fire-and-forget:** Don't block user on sync completion
- **Retry queue:** Failed syncs queued for background retry

---

### Q17: Data Model & Relationships

**Answer:**

### **Epic → Feature → Task Hierarchy**

**Can a feature belong to multiple epics?**

**NO - Strict 1:1 relationship (feature belongs to exactly one epic)**

**Rationale:**
- Simplifies progress rollup (feature % → epic %)
- Prevents ambiguous ownership (which epic "owns" the feature?)
- Aligns with standard PM tool hierarchies (Jira Story → Epic, Linear Issue → Initiative)

**Schema Enforcement:**
```sql
CREATE TABLE features (
    id UUID PRIMARY KEY,
    epic_id UUID NOT NULL REFERENCES epics(id) ON DELETE CASCADE,
    feature_id VARCHAR(20) NOT NULL,
    -- ... other columns
    UNIQUE(org_id, feature_id)
);

-- One feature → one epic (enforced by foreign key)
```

**Workaround for Cross-Epic Features:**
If a feature conceptually spans multiple epics, create **linked features** (one per epic):
```python
# Cross-epic feature pattern
epic_a = Epic(id="EPIC-001", title="User Management")
epic_b = Epic(id="EPIC-002", title="Security")

# Create feature in primary epic
feature_auth = Feature(
    id="FEAT-001",
    epic_id="EPIC-001",  # Primary epic
    title="User Authentication"
)

# Create linked feature in secondary epic
feature_auth_security = Feature(
    id="FEAT-002",
    epic_id="EPIC-002",  # Secondary epic
    title="Authentication Security (linked to FEAT-001)",
    linked_feature_id="FEAT-001"  # Reference to primary
)
```

---

**Can a task belong to multiple features?**

**NO - Strict 1:1 relationship (task belongs to exactly one feature)**

**Rationale:**
- Clear ownership and accountability
- Simplifies progress tracking
- Prevents duplicate work counting

**Schema Enforcement:**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    epic_id UUID NOT NULL REFERENCES epics(id) ON DELETE CASCADE,  -- Denormalized for performance
    task_id VARCHAR(20) NOT NULL,
    -- ... other columns
    UNIQUE(org_id, task_id)
);
```

**Workaround for Cross-Feature Tasks:**
If a task impacts multiple features, create **subtasks** or **linked tasks**:
```python
# Cross-feature task pattern
task_api = Task(
    id="TASK-001",
    feature_id="FEAT-001",  # Primary feature
    title="Implement authentication API"
)

# Linked task in related feature
task_ui = Task(
    id="TASK-002",
    feature_id="FEAT-002",
    title="Update login UI to use new API",
    depends_on=["TASK-001"]  # Dependency link
)
```

---

**Max depth of hierarchy?**

**3 Levels: Epic → Feature → Task (no subtasks in MVP)**

**Rationale:**
- Matches industry-standard PM tools (Jira: Epic → Story → Sub-task)
- Prevents over-planning (tasks should be <1 day of work)
- Simplifies rollup calculations

**Future Extension: Subtasks (Post-MVP)**
```sql
-- Optional subtasks table (not MVP)
CREATE TABLE subtasks (
    id UUID PRIMARY KEY,
    parent_task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    subtask_id VARCHAR(20) NOT NULL,
    title TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    UNIQUE(org_id, subtask_id)
);
```

**Hierarchy Depth Validation:**
```python
# Enforce max depth
def validate_hierarchy_depth(epic: Epic):
    if epic.features:
        for feature in epic.features:
            if feature.tasks:
                for task in feature.tasks:
                    if hasattr(task, 'subtasks') and task.subtasks:
                        raise ValidationError(
                            "Hierarchy too deep: Epic → Feature → Task → Subtask not allowed in MVP"
                        )
```

---

### **Requirements Linking**

**Can one requirement link to multiple features?**

**YES - Many-to-Many relationship**

**Rationale:**
- Complex requirements often span multiple features
- Example: "The system shall support user authentication" (REQ-001) impacts:
  - FEAT-001: Login UI
  - FEAT-002: Auth API
  - FEAT-003: Session Management

**Schema:**
```sql
-- Many-to-many junction table
CREATE TABLE feature_requirements (
    id UUID PRIMARY KEY,
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    requirement_id UUID NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(feature_id, requirement_id)  -- Prevent duplicates
);

CREATE INDEX idx_feature_requirements_feature ON feature_requirements(feature_id);
CREATE INDEX idx_feature_requirements_requirement ON feature_requirements(requirement_id);
```

**Usage:**
```python
# Link requirement to multiple features
requirement = Requirement(id="REQ-001", ears_notation="The system shall...")

await db.link_requirement_to_feature("REQ-001", "FEAT-001")  # Login UI
await db.link_requirement_to_feature("REQ-001", "FEAT-002")  # Auth API
await db.link_requirement_to_feature("REQ-001", "FEAT-003")  # Sessions

# Query features for requirement
features = await db.get_features_for_requirement("REQ-001")
# Returns: [FEAT-001, FEAT-002, FEAT-003]
```

---

**Can one feature satisfy multiple requirements?**

**YES - Many-to-Many relationship (same junction table)**

**Example:**
```python
# Feature satisfies multiple requirements
feature = Feature(id="FEAT-001", title="User Login")

# Links
await db.link_requirement_to_feature("REQ-001", "FEAT-001")  # Authentication
await db.link_requirement_to_feature("REQ-005", "FEAT-001")  # Audit logging
await db.link_requirement_to_feature("REQ-012", "FEAT-001")  # Session management

# Query requirements for feature
requirements = await db.get_requirements_for_feature("FEAT-001")
# Returns: [REQ-001, REQ-005, REQ-012]
```

---

**Traceability: Bidirectional links?**

**YES - Bidirectional traceability is CRITICAL**

**Use Cases:**
- **Forward trace:** REQ-001 → Which features implement this? (impact analysis)
- **Backward trace:** FEAT-001 → Which requirements does this satisfy? (coverage analysis)

**Implementation:**
```python
# Forward traceability (requirement → features)
async def get_feature_coverage(requirement_id: str) -> Dict:
    features = await db.execute("""
        SELECT f.*
        FROM features f
        JOIN feature_requirements fr ON fr.feature_id = f.id
        WHERE fr.requirement_id = (
            SELECT id FROM requirements WHERE requirement_id = $1
        )
    """, requirement_id)

    return {
        "requirement_id": requirement_id,
        "features": features,
        "coverage": "COMPLETE" if len(features) > 0 else "MISSING"
    }

# Backward traceability (feature → requirements)
async def get_requirement_satisfaction(feature_id: str) -> Dict:
    requirements = await db.execute("""
        SELECT r.*
        FROM requirements r
        JOIN feature_requirements fr ON fr.requirement_id = r.id
        WHERE fr.feature_id = (
            SELECT id FROM features WHERE feature_id = $1
        )
    """, feature_id)

    return {
        "feature_id": feature_id,
        "requirements": requirements,
        "satisfaction": "COMPLETE" if all(r.validated for r in requirements) else "PARTIAL"
    }
```

**Traceability Matrix (for compliance):**
```python
# Generate traceability matrix
async def generate_traceability_matrix(project_id: str) -> pd.DataFrame:
    data = []

    requirements = await db.get_requirements(project_id)

    for req in requirements:
        features = await get_feature_coverage(req.requirement_id)

        for feature in features["features"]:
            tasks = await db.get_tasks_for_feature(feature.feature_id)

            data.append({
                "Requirement": req.requirement_id,
                "EARS": req.ears_notation,
                "Feature": feature.feature_id,
                "Tasks": ", ".join([t.task_id for t in tasks]),
                "Status": feature.status,
                "Coverage": "✅" if feature.status == "COMPLETED" else "⏳"
            })

    return pd.DataFrame(data)

# Export to Excel for stakeholders
matrix = await generate_traceability_matrix("project-uuid")
matrix.to_excel("traceability_matrix.xlsx", index=False)
```

---

### **State Transitions**

**Valid Task States:**

```
BACKLOG → IN_PROGRESS → IN_REVIEW → COMPLETED
             ↓              ↓
          BLOCKED        BLOCKED → IN_PROGRESS (after unblock)
                                      ↓
                                  ARCHIVED (after 12 months)
```

**State Definitions:**
- **BACKLOG:** Created but not started (default state)
- **IN_PROGRESS:** Actively being worked on (`/task-work` in progress)
- **BLOCKED:** Failed quality gates or dependency issue (Phase 4.5 failures)
- **IN_REVIEW:** All quality gates passed, awaiting human review
- **COMPLETED:** Finished and approved
- **ARCHIVED:** Completed >12 months ago, moved to cold storage

**Schema:**
```sql
CREATE TYPE task_status AS ENUM (
    'BACKLOG',
    'IN_PROGRESS',
    'BLOCKED',
    'IN_REVIEW',
    'COMPLETED',
    'ARCHIVED'
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    status task_status NOT NULL DEFAULT 'BACKLOG',
    -- ... other columns
);
```

---

**Can tasks skip states?**

**Mostly NO - Sequential transitions enforced (with exceptions)**

**Valid Transitions:**
```python
VALID_TRANSITIONS = {
    "BACKLOG": ["IN_PROGRESS"],
    "IN_PROGRESS": ["BLOCKED", "IN_REVIEW", "BACKLOG"],  # Can go back to backlog
    "BLOCKED": ["IN_PROGRESS"],  # Unblock → resume
    "IN_REVIEW": ["COMPLETED", "IN_PROGRESS"],  # Review fail → back to progress
    "COMPLETED": ["ARCHIVED"],
    "ARCHIVED": []  # Terminal state
}

# Validation
def validate_transition(current_status: str, new_status: str) -> bool:
    if new_status not in VALID_TRANSITIONS.get(current_status, []):
        raise InvalidTransitionError(
            f"Cannot transition from {current_status} to {new_status}"
        )
    return True
```

**Exceptions (Admin Override):**
```python
# Tech leads/admins can force state transitions
def force_transition(task_id: str, new_status: str, user_role: str, reason: str):
    if user_role not in ["admin", "tech_lead"]:
        raise PermissionError("Only admins/tech leads can force state transitions")

    # Log override
    await db.log_state_override(
        task_id=task_id,
        from_status=task.status,
        to_status=new_status,
        overridden_by=user_id,
        reason=reason
    )

    # Execute transition (bypassing validation)
    await db.update_task_status(task_id, new_status)
```

**Use Cases for Skipping:**
- **BACKLOG → COMPLETED:** Task obsolete (requirement changed) - Admin override
- **IN_PROGRESS → ARCHIVED:** Project cancelled - Admin override
- **BLOCKED → COMPLETED:** Issue resolved externally - Tech lead override

---

**Who can transition between states?**

**Role-Based Transition Permissions:**

```python
TRANSITION_PERMISSIONS = {
    "BACKLOG → IN_PROGRESS": ["assignee", "tech_lead", "admin"],
    "IN_PROGRESS → BLOCKED": ["system", "assignee"],  # System auto-blocks on test failure
    "IN_PROGRESS → IN_REVIEW": ["system"],  # Auto when quality gates pass
    "BLOCKED → IN_PROGRESS": ["assignee", "tech_lead"],
    "IN_REVIEW → COMPLETED": ["tech_lead", "admin"],  # Requires approval
    "IN_REVIEW → IN_PROGRESS": ["tech_lead", "assignee"],  # Rejected in review
    "COMPLETED → ARCHIVED": ["system"],  # Auto after 12 months

    # Emergency overrides
    "* → *": ["admin"]  # Admins can force any transition
}

# Permission check
async def can_transition(task: Task, new_status: str, user_id: str) -> bool:
    user = await db.get_user(user_id)
    transition_key = f"{task.status} → {new_status}"

    allowed_roles = TRANSITION_PERMISSIONS.get(transition_key, [])

    # Check if user is assignee
    if "assignee" in allowed_roles and task.assignee_id == user_id:
        return True

    # Check user role
    if user.role in allowed_roles:
        return True

    return False

# Usage
if await can_transition(task, "COMPLETED", current_user_id):
    await db.update_task_status(task.id, "COMPLETED")
else:
    raise PermissionError(f"User {current_user_id} cannot mark task as COMPLETED")
```

**State Transition Logging:**
```sql
-- Audit trail for all state changes
CREATE TABLE state_transitions (
    id UUID PRIMARY KEY,
    task_id UUID NOT NULL REFERENCES tasks(id),
    from_status task_status NOT NULL,
    to_status task_status NOT NULL,
    triggered_by UUID REFERENCES users(id),  -- NULL if system-triggered
    trigger_type VARCHAR(20) NOT NULL,  -- 'user', 'system', 'admin_override'
    reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_state_transitions_task ON state_transitions(task_id);
```

**System-Triggered Transitions:**
```python
# Phase 4.5: Auto-block on test failure
if test_results.failed_count > 0 and attempt_count >= max_attempts:
    await db.transition_task_status(
        task_id=task.id,
        from_status="IN_PROGRESS",
        to_status="BLOCKED",
        triggered_by=None,  # System trigger
        trigger_type="system",
        reason=f"Tests failed after {max_attempts} attempts"
    )

# Phase 5: Auto-review on quality gate pass
if quality_gates_passed:
    await db.transition_task_status(
        task_id=task.id,
        from_status="IN_PROGRESS",
        to_status="IN_REVIEW",
        triggered_by=None,
        trigger_type="system",
        reason="All quality gates passed"
    )
```

---

## Document Summary

This comprehensive Q&A session captures detailed requirements for the AgenticFlow LangGraph + MCP architecture migration, covering:

- **Discovery Phase:** Primary goals, user roles, problem statement
- **Exploration Phase:** 4-stage workflow, PM tool synchronization, UK Probate Agent reference patterns
- **Technical Specifications:** Technology stack validation, quality gates, MCP architecture, performance requirements, data model design

**Key Takeaways:**
1. Proven LangGraph patterns from UK Probate Agent (50-85% cost savings)
2. PostgreSQL-backed state management with team collaboration
3. MCP server architecture for universal AI tool compatibility
4. Automated quality gates (Phase 2.5 Architectural Review, Phase 4.5 Fix Loop)
5. Bidirectional PM tool synchronization (Jira, Linear, Azure DevOps, GitHub)
6. Production-ready deployment with enterprise security and observability

**Next Steps:** Continue with remaining questions (Q18-Q21) covering UX, migration strategy, MVP scope, and risk mitigation.
