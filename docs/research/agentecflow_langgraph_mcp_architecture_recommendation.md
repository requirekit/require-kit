# Agentecflow: LangGraph + MCP Architecture Recommendation

**Date**: 2025-09-30
**Status**: Strategic Recommendation
**Decision**: LangGraph Orchestration with MCP Integration

---

## Executive Summary

Based on comprehensive analysis of:
1. **Agentecflow Overview PDF** - Complete product vision and 4-stage workflow
2. **Product Requirements** - Team-scale tooling requirements
3. **Legal AI Agent Implementation** - Proven LangGraph production patterns
4. **Claude Agent SDK Analysis** - Previous markdown-based approach limitations

**Recommendation**: Build Agentecflow as a **LangGraph-orchestrated system with MCP integrations** for team collaboration, abandoning local markdown files in favor of centralized state management with external PM tool synchronization.

---

## Key Insights from Analysis

### 1. Agentecflow Overview (PDF) Reveals True Scope

The PDF clearly shows this is **NOT a single-developer CLI tool** but rather:

- **Team-scale development platform** with human checkpoints
- **Cross-tool compatibility** (Claude Code, Gemini CLI, GitHub Copilot, Cursor)
- **External PM tool integration** (Jira, Linear, Azure DevOps, GitHub Projects)
- **AI/human collaboration** with specialized agent roles
- **Stage-gate workflow** with validation at each checkpoint

**Critical Insight**: Local markdown files are fundamentally incompatible with team collaboration and real-time PM tool synchronization.

### 2. Legal AI Agent Demonstrates Production-Ready LangGraph Patterns

The UK Probate Agent (`/Users/richardwoollcott/Projects/appmilla_github/uk-probate-agent`) provides excellent reference architecture:

#### LangGraph Workflow Excellence
```python
# Proven production pattern from legal_search_workflow.py
class LegalSearchWorkflow:
    def __init__(self, llm_model, max_documents, enable_caching, api_key):
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(LegalSearchState)

        # Multi-stage orchestration
        workflow.add_node("analyze_query", self._analyze_query_node)
        workflow.add_node("search_legislation", self._search_legislation_node)
        workflow.add_node("parse_documents", self._parse_documents_node)
        workflow.add_node("analyze_content", self._analyze_content_node)
        workflow.add_node("generate_response", self._generate_response_node)

        # Conditional routing with state management
        workflow.add_conditional_edges(...)

        return workflow.compile()
```

**Key Learnings**:
- ✅ **Stateful orchestration** - LangGraph manages complex state transitions
- ✅ **Conditional routing** - Decision points based on intermediate results
- ✅ **Error handling** - Graceful degradation with fallback responses
- ✅ **Streaming support** - Real-time response generation
- ✅ **Metrics tracking** - Performance monitoring built-in

#### Multi-Agent Orchestration Pattern
```python
# Comprehensive agent with intelligent routing
class ComprehensiveLegalAgent:
    def _determine_optimal_approach(self, query: str) -> str:
        """Semantic routing to specialized engines"""
        # Score-based decision making
        if combined_indicators:
            return "combined"
        elif research_score > reasoning_score:
            return "research"
        else:
            return "reasoning"

    def ask(self, query: str) -> LegalResponse:
        approach = self._determine_optimal_approach(query)

        if approach == "research":
            return self.research_engine.process(query)
        elif approach == "reasoning":
            return self.reasoning_engine.process(query)
        else:
            # Combined approach - sequential processing
            research_result = self.research_engine.process(query)
            return self.reasoning_engine.process(query, context=research_result)
```

**Architecture Pattern**: Central orchestrator delegates to specialized engines based on semantic query analysis.

### 3. Previous Claude Agent SDK Analysis Was Limited

The `claude_agent_sdk_integration_analysis.md` correctly identified MCP integration points BUT was constrained by:

- ❌ **Markdown-based assumptions** - Assumed local file state management
- ❌ **Single-developer focus** - Didn't address team collaboration
- ❌ **No PM tool synchronization** - Missing critical external integrations
- ❌ **Static command system** - Markdown commands lack dynamic orchestration

---

## Recommended Architecture: LangGraph Core + MCP Extensions

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Agentecflow Orchestration Layer                │
│                    (LangGraph StateGraph)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ Specification │   │ Task Definition  │   │   Engineering    │
│     Stage     │   │      Stage       │   │      Stage       │
│ (LangGraph)   │   │   (LangGraph)    │   │   (LangGraph)    │
└───────────────┘   └──────────────────┘   └──────────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────────────────────────────────────────────────────┐
│                      MCP Integration Layer                     │
├───────────────────────────────────────────────────────────────┤
│  Requirements MCP  │  PM Tools MCP  │  Testing MCP  │ Deploy  │
│  - EARS notation   │  - Jira sync   │  - pytest     │  MCP    │
│  - BDD generation  │  - Linear sync │  - Playwright │  - CI/CD│
│  - Validation      │  - Azure DevOps│  - Quality    │  - QA   │
│                    │  - GitHub      │    gates      │         │
└───────────────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  PostgreSQL   │   │   External PM    │   │   Test Results   │
│   Database    │   │      Tools       │   │    Storage       │
│ - State       │   │ - Jira/Linear    │   │ - Coverage       │
│ - Requirements│   │ - Azure DevOps   │   │ - Metrics        │
│ - Tasks/Epics │   │ - GitHub         │   │ - Quality Gates  │
└───────────────┘   └──────────────────┘   └──────────────────┘
```

### Core Components

#### 1. **LangGraph Orchestration Engine** (Python)

**Purpose**: Central state machine managing the complete Agentecflow lifecycle

**Key Features**:
- **4-Stage Workflow**: Specification → Tasks → Engineering → Deployment
- **State Management**: PostgreSQL-backed state persistence
- **Human Checkpoints**: Built-in approval gates with timeout handling
- **Agent Coordination**: Specialized agent invocation with context passing
- **Error Recovery**: Rollback and retry mechanisms

**State Model**:
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Optional
from pydantic import BaseModel

class AgentecflowState(BaseModel):
    """Complete project state"""
    project_id: str
    current_stage: str  # specification | tasks | engineering | deployment
    specification: SpecificationData
    epics: List[Epic]
    features: List[Feature]
    tasks: List[Task]
    requirements: List[Requirement]
    test_results: Dict[str, TestResult]
    pm_tool_mappings: Dict[str, str]  # local_id -> external_id
    human_approvals: List[Approval]
    workflow_history: List[StateTransition]

class AgentecflowOrchestrator:
    """Main orchestration engine"""

    def __init__(self, db_connection, mcp_clients):
        self.db = db_connection
        self.mcps = mcp_clients
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentecflowState)

        # Stage 1: Specification
        workflow.add_node("gather_requirements", self._gather_requirements_node)
        workflow.add_node("formalize_ears", self._formalize_ears_node)
        workflow.add_node("human_spec_review", self._human_checkpoint_node)

        # Stage 2: Tasks Definition
        workflow.add_node("generate_epics", self._generate_epics_node)
        workflow.add_node("generate_features", self._generate_features_node)
        workflow.add_node("generate_tasks", self._generate_tasks_node)
        workflow.add_node("sync_to_pm_tools", self._sync_pm_tools_node)
        workflow.add_node("human_task_review", self._human_checkpoint_node)

        # Stage 3: Engineering
        workflow.add_node("assign_tasks", self._task_assignment_node)
        workflow.add_node("execute_task", self._execute_task_node)
        workflow.add_node("run_tests", self._run_tests_node)
        workflow.add_node("code_review", self._code_review_node)

        # Stage 4: Deployment & QA
        workflow.add_node("deploy_to_test", self._deploy_test_node)
        workflow.add_node("run_qa_suite", self._run_qa_node)
        workflow.add_node("human_release_review", self._human_checkpoint_node)

        # Conditional routing with human checkpoints
        workflow.add_conditional_edges("human_spec_review", self._approval_routing)
        workflow.add_conditional_edges("human_task_review", self._approval_routing)
        workflow.add_conditional_edges("human_release_review", self._approval_routing)

        workflow.set_entry_point("gather_requirements")
        return workflow.compile()

    async def execute_stage(self, stage: str, project_id: str) -> AgentecflowState:
        """Execute a complete stage with checkpoints"""
        state = await self.db.load_state(project_id)
        result = await self.workflow.ainvoke(state)
        await self.db.save_state(result)
        return result
```

#### 2. **MCP Integration Layer** (Python)

**Architecture Decision: Python for All MCP Servers**

**Rationale for Python-Only MCP Stack**:

1. **Consistency with Legal AI Agent**: Proven Python LangGraph implementation provides battle-tested patterns to reuse
2. **Single Language Stack**: Entire Agentecflow system in Python (orchestrator + all MCPs + agents)
3. **Team Expertise**: Leverage existing Python proficiency and LangGraph experience from Legal AI Agent
4. **Python MCP SDK Available**: `mcp` Python package fully supports MCP server development with decorator-based APIs
5. **Pydantic Model Sharing**: Direct reuse of data models (Epic, Feature, Task, Requirement) across orchestrator and MCPs
6. **Simplified Deployment**: Single runtime environment (Python 3.10+), not Python + Node.js + multiple package managers
7. **Easier Maintenance**: One language for debugging, testing, logging, and contributor onboarding
8. **Type Safety**: Python 3.10+ with type hints and Pydantic provides excellent type safety and validation
9. **Async Integration**: Python asyncio integrates seamlessly with LangGraph async workflows and database operations
10. **Development Velocity**: Faster iteration when entire stack uses same language, libraries, and patterns

**Alternative Considered and Rejected**: TypeScript for MCP servers

**Why TypeScript Was Initially Considered**:
- Official `@modelcontextprotocol/sdk` from Anthropic is TypeScript-first
- More mature documentation and examples in TypeScript ecosystem
- Strong typing and excellent IDE support

**Why Python Was Ultimately Chosen**:
- ❌ TypeScript introduces language fragmentation (Python for orchestrator, TypeScript for MCPs)
- ❌ No significant functional advantages over Python MCP SDK for Agentecflow use case
- ❌ Added deployment complexity: two language runtimes, npm + pip, Node.js + Python
- ❌ Team would need TypeScript expertise alongside Python (slower onboarding)
- ❌ Can't directly share Pydantic models between orchestrator and MCPs (need JSON schemas)
- ❌ Different async patterns (Promises vs asyncio) complicate integration
- ✅ Legal AI Agent proves Python is production-ready for complex LangGraph orchestration
- ✅ Python MCP SDK (`mcp` package) provides all required capabilities

**Python MCP Stack**:
```
agentecflow-requirements-mcp/     # Python (EARS, BDD generation)
agentecflow-pm-tools-mcp/         # Python (Jira, Linear, Azure, GitHub sync)
agentecflow-testing-mcp/          # Python (pytest, Jest, Playwright orchestration)
agentecflow-deployment-mcp/       # Python (Docker, CI/CD automation)
```

**Requirements MCP Server** (Python):
```python
# agentecflow-requirements-mcp
from mcp.server import Server
from mcp.types import Tool, Resource, TextContent
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import asyncio

# Shared Pydantic models (reused from orchestrator)
from agentecflow.models import Requirement, EARSPattern, BDDScenario

class RequirementsMCPServer:
    """
    MCP server for requirements gathering, EARS formalization, and BDD generation.

    Provides tools and resources for Stage 1 (Specification) of Agentecflow workflow.
    Integrates with LangGraph orchestrator using shared Pydantic models.
    """

    def __init__(self, db_connection, llm_client):
        self.db = db_connection
        self.llm = llm_client
        self.server = Server("agentecflow-requirements")
        self._register_tools()
        self._register_resources()

    def _register_tools(self):
        """Register MCP tools for requirements management"""

        @self.server.tool()
        async def gather_requirements(
            project_id: str,
            context: str = ""
        ) -> dict:
            """
            Interactive requirements gathering with intelligent Q&A.

            Uses LLM to generate contextual questions and extract requirements
            from user responses. Supports iterative refinement.

            Args:
                project_id: Project identifier
                context: Optional context from previous interactions

            Returns:
                Gathered requirements with metadata and next steps
            """
            return await self._gather_requirements_interactive(project_id, context)

        @self.server.tool()
        async def formalize_ears(
            raw_requirements: List[str],
            project_id: str
        ) -> List[dict]:
            """
            Convert raw requirements to EARS notation.

            Analyzes natural language requirements and converts them to formal
            EARS patterns (Ubiquitous, Event-Driven, State-Driven, Unwanted, Optional).

            Args:
                raw_requirements: List of natural language requirements
                project_id: Project identifier for storage

            Returns:
                List of formalized requirements with EARS notation and pattern classification
            """
            return await self._convert_to_ears(raw_requirements, project_id)

        @self.server.tool()
        async def generate_bdd(
            requirement_id: str
        ) -> dict:
            """
            Generate BDD/Gherkin scenarios from EARS requirement.

            Creates comprehensive Given/When/Then scenarios for testing
            based on formalized EARS requirements.

            Args:
                requirement_id: Requirement identifier (e.g., REQ-001)

            Returns:
                BDD scenarios with Gherkin syntax and traceability
            """
            requirement = await self.db.get_requirement(requirement_id)
            return await self._generate_bdd_scenarios(requirement)

        @self.server.tool()
        async def validate_requirements(
            project_id: str
        ) -> dict:
            """
            Validate completeness and consistency of requirements.

            Analyzes requirement set for completeness, consistency,
            ambiguity, and EARS notation compliance.

            Args:
                project_id: Project identifier

            Returns:
                Validation results with completeness score, issues, and recommendations
            """
            requirements = await self.db.get_requirements(project_id)
            return await self._validate_completeness(requirements)

    def _register_resources(self):
        """Register MCP resources for requirements access"""

        @self.server.resource("requirements://{requirement_id}")
        async def get_requirement(uri: str) -> str:
            """Retrieve requirement by ID with EARS notation"""
            requirement_id = uri.split("/")[-1]
            req = await self.db.get_requirement(requirement_id)
            return req.to_markdown()

        @self.server.resource("ears://templates")
        async def get_ears_templates() -> str:
            """Get EARS notation templates and examples"""
            return self._get_ears_documentation()

        @self.server.resource("bdd://scenarios/{requirement_id}")
        async def get_bdd_scenarios(uri: str) -> str:
            """Retrieve BDD scenarios for a requirement"""
            requirement_id = uri.split("/")[-1]
            scenarios = await self.db.get_bdd_scenarios(requirement_id)
            return self._format_scenarios(scenarios)

        @self.server.resource("requirements://project/{project_id}")
        async def get_project_requirements(uri: str) -> str:
            """Retrieve all requirements for a project"""
            project_id = uri.split("/")[-1]
            requirements = await self.db.get_requirements(project_id)
            return self._format_requirements_list(requirements)

    async def _gather_requirements_interactive(
        self,
        project_id: str,
        context: str
    ) -> dict:
        """
        Interactive Q&A for requirements gathering.

        Uses LLM to generate intelligent, contextual questions
        based on project domain and previous answers.
        """
        # Use LLM to generate intelligent questions based on context
        questions = await self._generate_questions(project_id, context)

        requirements = []
        for question in questions:
            # This would integrate with CLI for user interaction
            # In production, this would be async streaming back to CLI
            answer = await self._prompt_user(question)
            requirements.append({
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat(),
                "confidence": 0.8  # Could use LLM to assess answer quality
            })

        # Store raw requirements
        await self.db.save_raw_requirements(project_id, requirements)

        return {
            "project_id": project_id,
            "requirements_gathered": len(requirements),
            "coverage_score": await self._assess_coverage(requirements),
            "next_step": "formalize_ears",
            "suggested_followup_questions": await self._suggest_followups(requirements)
        }

    async def _convert_to_ears(
        self,
        raw_requirements: List[str],
        project_id: str
    ) -> List[dict]:
        """
        Convert natural language to EARS notation using LLM.

        EARS Patterns:
        1. Ubiquitous: The [system] shall [behavior]
        2. Event-Driven: When [trigger], the [system] shall [response]
        3. State-Driven: While [state], the [system] shall [behavior]
        4. Unwanted: If [error], then the [system] shall [recovery]
        5. Optional: Where [feature], the [system] shall [behavior]
        """
        formalized = []

        for req in raw_requirements:
            # Use LLM to convert to EARS notation
            ears_notation = await self.llm.ainvoke([
                SystemMessage(content="""You are an expert at EARS notation for requirements engineering.

Convert requirements to one of these five EARS patterns:
1. **Ubiquitous**: The [system] shall [behavior]
2. **Event-Driven**: When [trigger], the [system] shall [response]
3. **State-Driven**: While [state], the [system] shall [behavior]
4. **Unwanted Behavior**: If [error], then the [system] shall [recovery]
5. **Optional Feature**: Where [feature], the [system] shall [behavior]

Respond with only the EARS-formatted requirement, clearly identifying the pattern used."""),
                HumanMessage(content=f"Convert to EARS notation: {req}")
            ])

            pattern = self._detect_ears_pattern(ears_notation.content)
            validated = self._validate_ears_syntax(ears_notation.content, pattern)

            requirement = Requirement(
                id=await self._generate_req_id(project_id),
                project_id=project_id,
                original=req,
                ears_notation=ears_notation.content,
                pattern=pattern,
                validated=validated,
                created_at=datetime.now()
            )

            # Store in database
            await self.db.save_requirement(requirement)

            formalized.append(requirement.dict())

        return formalized

    async def _generate_bdd_scenarios(self, requirement: Requirement) -> dict:
        """Generate BDD/Gherkin scenarios from EARS requirement"""
        # Use LLM to generate Gherkin scenarios
        scenarios = await self.llm.ainvoke([
            SystemMessage(content="""Generate comprehensive BDD/Gherkin scenarios for testing.

Format each scenario as:
Scenario: [Clear description]
  Given [precondition - system state]
  When [action - user action or event]
  Then [expected result - observable outcome]

Generate multiple scenarios covering:
- Happy path (main flow)
- Alternative paths (variations)
- Error cases (unwanted behaviors)

Ensure scenarios are testable, unambiguous, and traceable to requirement."""),
            HumanMessage(content=f"""EARS Requirement: {requirement.ears_notation}
Original Context: {requirement.original}
Pattern: {requirement.pattern}""")
        ])

        parsed_scenarios = self._parse_gherkin(scenarios.content)

        # Store BDD scenarios
        for scenario in parsed_scenarios:
            await self.db.save_bdd_scenario(
                requirement_id=requirement.id,
                scenario=scenario
            )

        return {
            "requirement_id": requirement.id,
            "scenarios": parsed_scenarios,
            "coverage": "complete",
            "test_cases_generated": len(parsed_scenarios)
        }

    def _detect_ears_pattern(self, ears_text: str) -> EARSPattern:
        """Detect which EARS pattern is used"""
        text_lower = ears_text.lower()

        if text_lower.startswith("when "):
            return EARSPattern.EVENT_DRIVEN
        elif text_lower.startswith("while "):
            return EARSPattern.STATE_DRIVEN
        elif text_lower.startswith("if ") or "if " in text_lower:
            return EARSPattern.UNWANTED
        elif text_lower.startswith("where "):
            return EARSPattern.OPTIONAL
        else:
            return EARSPattern.UBIQUITOUS

    def _validate_ears_syntax(self, ears_text: str, pattern: EARSPattern) -> bool:
        """Validate EARS notation syntax"""
        # Check for "shall" keyword (required in all EARS patterns)
        if " shall " not in ears_text.lower():
            return False

        # Pattern-specific validation
        if pattern == EARSPattern.EVENT_DRIVEN:
            return ears_text.lower().startswith("when ")
        elif pattern == EARSPattern.STATE_DRIVEN:
            return ears_text.lower().startswith("while ")
        # ... more validation logic

        return True

    async def run(self):
        """Start the MCP server"""
        async with self.server.stdio_transport():
            await self.server.serve()


# Factory function for easy instantiation
def create_requirements_mcp_server(
    db_connection,
    llm_client
) -> RequirementsMCPServer:
    """
    Factory function to create Requirements MCP server.

    Args:
        db_connection: PostgreSQL database connection
        llm_client: LangChain LLM client for EARS/BDD generation

    Returns:
        Configured RequirementsMCPServer instance
    """
    return RequirementsMCPServer(db_connection, llm_client)
```

**PM Tools MCP Server** (Python):
```python
# agentecflow-pm-tools-mcp
from mcp.server import Server
from mcp.types import Tool, Resource
import asyncio

class PMToolsMCPServer:
    """MCP server for external PM tool synchronization"""

    def __init__(self):
        self.jira_client = JiraClient()
        self.linear_client = LinearClient()
        self.azure_devops_client = AzureDevOpsClient()
        self.github_client = GitHubClient()

    async def sync_epic(self, epic: Epic, tool: str) -> str:
        """Sync epic to external PM tool"""
        if tool == "jira":
            return await self.jira_client.create_epic(epic)
        elif tool == "linear":
            return await self.linear_client.create_project(epic)
        elif tool == "azure_devops":
            return await self.azure_devops_client.create_epic(epic)
        elif tool == "github":
            return await self.github_client.create_milestone(epic)

    async def sync_feature(self, feature: Feature, tool: str, parent_id: str):
        """Sync feature to external PM tool with parent relationship"""
        if tool == "jira":
            return await self.jira_client.create_story(feature, epic_id=parent_id)
        # ... other implementations

    async def rollup_progress(self, epic_id: str, tool: str):
        """Calculate and sync progress rollup"""
        local_epic = await self.db.get_epic(epic_id)
        total_tasks = len(local_epic.tasks)
        completed_tasks = sum(1 for t in local_epic.tasks if t.status == "COMPLETED")

        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Update external tool
        if tool == "jira":
            await self.jira_client.update_epic_progress(local_epic.external_id, progress)
```

**Testing MCP Server** (Python):
```python
# agentecflow-testing-mcp
class TestingMCPServer:
    """MCP server for test execution and quality gates"""

    def __init__(self):
        self.test_runners = {
            "pytest": PyTestRunner(),
            "jest": JestRunner(),
            "playwright": PlaywrightRunner(),
            "xunit": XUnitRunner()
        }

    async def execute_test_suite(self, project_path: str, stack: str) -> TestResult:
        """Auto-detect and execute appropriate test suite"""
        runner = self._detect_test_runner(project_path, stack)

        result = await runner.run_tests(project_path)

        return TestResult(
            passed=result.passed,
            failed=result.failed,
            coverage=result.coverage,
            duration=result.duration,
            quality_gates=self._evaluate_quality_gates(result)
        )

    async def validate_coverage(self, coverage_data: dict, thresholds: dict) -> bool:
        """Validate coverage against thresholds"""
        return (
            coverage_data["line_coverage"] >= thresholds.get("line", 80) and
            coverage_data["branch_coverage"] >= thresholds.get("branch", 75)
        )

    def _evaluate_quality_gates(self, result: TestResult) -> QualityGateResult:
        """Evaluate all quality gates"""
        return QualityGateResult(
            tests_passed=result.failed == 0,
            coverage_met=result.coverage.line >= 80,
            performance_acceptable=result.duration < 300,
            overall_passed=all([...])
        )
```

#### 3. **State Persistence Layer** (PostgreSQL)

**Database Schema**:
```sql
-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    current_stage VARCHAR(50) NOT NULL,
    technology_stack VARCHAR(50),
    pm_tool VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Epics table
CREATE TABLE epics (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    epic_id VARCHAR(20) UNIQUE NOT NULL, -- EPIC-001
    external_id VARCHAR(100), -- Jira/Linear/etc ID
    title TEXT NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20),
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    progress DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Features table
CREATE TABLE features (
    id UUID PRIMARY KEY,
    epic_id UUID REFERENCES epics(id),
    feature_id VARCHAR(20) UNIQUE NOT NULL, -- FEAT-001
    external_id VARCHAR(100),
    title TEXT NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    requirement_ids TEXT[], -- Array of requirement IDs
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    feature_id UUID REFERENCES features(id),
    epic_id UUID REFERENCES epics(id),
    task_id VARCHAR(20) UNIQUE NOT NULL, -- TASK-001
    external_id VARCHAR(100),
    title TEXT NOT NULL,
    description TEXT,
    acceptance_criteria TEXT[],
    status VARCHAR(20) NOT NULL,
    assignee VARCHAR(100),
    test_results JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Requirements table
CREATE TABLE requirements (
    id UUID PRIMARY KEY,
    requirement_id VARCHAR(20) UNIQUE NOT NULL, -- REQ-001
    project_id UUID REFERENCES projects(id),
    ears_notation TEXT NOT NULL,
    bdd_scenarios TEXT[],
    status VARCHAR(20) NOT NULL,
    validated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- State transitions (audit log)
CREATE TABLE state_transitions (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    from_stage VARCHAR(50),
    to_stage VARCHAR(50),
    triggered_by VARCHAR(100), -- user or agent
    approval_status VARCHAR(20),
    transition_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- PM tool mappings
CREATE TABLE pm_tool_mappings (
    id UUID PRIMARY KEY,
    local_id VARCHAR(50) NOT NULL,
    local_type VARCHAR(20) NOT NULL, -- epic, feature, task
    external_id VARCHAR(100) NOT NULL,
    external_tool VARCHAR(50) NOT NULL, -- jira, linear, azure_devops, github
    last_synced TIMESTAMP,
    sync_status VARCHAR(20),
    UNIQUE(local_id, external_tool)
);

-- Indexes for performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_epics_project ON epics(project_id);
CREATE INDEX idx_features_epic ON features(epic_id);
CREATE INDEX idx_pm_mappings_local ON pm_tool_mappings(local_id, local_type);
```

#### 4. **Agent Coordination System** (Python)

**Specialized Agents** (following Legal AI Agent patterns):
```python
# Specification Agent
class SpecificationAgent:
    """Interactive requirements gathering with EARS formalization"""

    def __init__(self, llm, mcp_client):
        self.llm = llm
        self.requirements_mcp = mcp_client
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(SpecificationState)

        workflow.add_node("interactive_qa", self._interactive_qa_node)
        workflow.add_node("extract_requirements", self._extract_requirements_node)
        workflow.add_node("formalize_ears", self._formalize_ears_node)
        workflow.add_node("generate_bdd", self._generate_bdd_node)
        workflow.add_node("validate", self._validate_node)

        return workflow.compile()

    async def gather_requirements(self, project_id: str, context: str) -> List[Requirement]:
        """Orchestrate complete requirements gathering"""
        state = SpecificationState(project_id=project_id, context=context)
        result = await self.workflow.ainvoke(state)
        return result.requirements

# Task Definition Agent
class TaskDefinitionAgent:
    """Generate epic/feature/task hierarchy from requirements"""

    def __init__(self, llm, mcp_client):
        self.llm = llm
        self.pm_tools_mcp = mcp_client

    async def generate_epic(self, requirements: List[Requirement]) -> Epic:
        """Generate epic from requirements"""
        # Use LLM to analyze requirements and create epic
        epic_data = await self.llm.ainvoke([
            SystemMessage(content="You are an expert at creating project epics..."),
            HumanMessage(content=f"Requirements: {requirements}")
        ])

        epic = Epic.parse(epic_data.content)

        # Sync to external PM tool via MCP
        external_id = await self.pm_tools_mcp.sync_epic(epic, tool="jira")
        epic.external_id = external_id

        return epic

# Engineering Agent
class EngineeringAgent:
    """Task implementation with quality gates"""

    def __init__(self, llm, testing_mcp):
        self.llm = llm
        self.testing_mcp = testing_mcp
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(EngineeringState)

        workflow.add_node("analyze_task", self._analyze_task_node)
        workflow.add_node("implement", self._implement_node)
        workflow.add_node("generate_tests", self._generate_tests_node)
        workflow.add_node("run_tests", self._run_tests_node)
        workflow.add_node("quality_gates", self._quality_gates_node)
        workflow.add_node("code_review", self._code_review_node)

        # Conditional routing based on test results
        workflow.add_conditional_edges(
            "quality_gates",
            self._gate_routing,
            {
                "passed": "code_review",
                "failed": "implement",  # Retry
                "blocked": END
            }
        )

        return workflow.compile()
```

### Integration with CLI Tools (Claude Code, Gemini, etc.)

**Universal CLI Adapter**:
```python
# Universal adapter for multi-tool support
class AgentecflowCLIAdapter:
    """Adapter for Claude Code, Gemini CLI, GitHub Copilot, Cursor"""

    def __init__(self, orchestrator: AgentecflowOrchestrator):
        self.orchestrator = orchestrator

    async def handle_command(self, command: str, args: dict, tool: str) -> dict:
        """Route command to orchestrator"""

        # Map CLI command to orchestrator method
        command_map = {
            "/gather-requirements": self.orchestrator.gather_requirements,
            "/formalize-ears": self.orchestrator.formalize_ears,
            "/epic-create": self.orchestrator.create_epic,
            "/feature-create": self.orchestrator.create_feature,
            "/task-work": self.orchestrator.execute_task,
            "/task-sync": self.orchestrator.sync_to_pm_tools,
            "/hierarchy-view": self.orchestrator.get_hierarchy,
            "/portfolio-dashboard": self.orchestrator.get_portfolio_metrics
        }

        handler = command_map.get(command)
        if not handler:
            return {"error": f"Unknown command: {command}"}

        # Execute with tool-specific context
        result = await handler(**args, invoked_by=tool)

        # Format response for specific tool
        return self._format_for_tool(result, tool)

    def _format_for_tool(self, result: dict, tool: str) -> dict:
        """Format response based on CLI tool capabilities"""
        if tool == "claude-code":
            # Claude Code supports rich markdown with file references
            return {
                "markdown": self._rich_markdown(result),
                "file_references": result.get("files_modified", [])
            }
        elif tool == "gemini-cli":
            # Gemini CLI format
            return {
                "text": self._plain_text(result)
            }
        else:
            # Generic format
            return result
```

### Human Checkpoint Implementation

**Interactive Approval System**:
```python
class HumanCheckpointNode:
    """Implement human approval checkpoints"""

    async def _human_checkpoint_node(self, state: AgentecflowState) -> AgentecflowState:
        """Pause workflow for human review"""

        # Generate approval request
        approval_request = ApprovalRequest(
            project_id=state.project_id,
            stage=state.current_stage,
            checkpoint_type=self._get_checkpoint_type(state.current_stage),
            data_for_review=self._prepare_review_data(state),
            timeout_minutes=1440  # 24 hours
        )

        # Save approval request to database
        await self.db.save_approval_request(approval_request)

        # Notify relevant stakeholders
        await self.notification_service.notify_approval_required(
            approval_request,
            recipients=self._get_approvers(state.current_stage)
        )

        # Wait for approval (with timeout)
        approval = await self._wait_for_approval(
            approval_request.id,
            timeout=approval_request.timeout_minutes * 60
        )

        if approval.status == "approved":
            state.human_approvals.append(approval)
            state.current_stage = self._next_stage(state.current_stage)
        elif approval.status == "rejected":
            state.current_stage = self._previous_stage(state.current_stage)
            state.workflow_history.append(
                StateTransition(
                    from_stage=state.current_stage,
                    to_stage=self._previous_stage(state.current_stage),
                    reason="Rejected by human reviewer",
                    rejected_data=approval.feedback
                )
            )
        else:  # timeout
            # Handle timeout based on policy
            state.workflow_history.append(
                StateTransition(
                    from_stage=state.current_stage,
                    to_stage="paused",
                    reason="Approval timeout"
                )
            )

        return state
```

---

## Why This Architecture vs. Previous Approaches

### ❌ Why NOT Local Markdown Files

**Problems with Markdown-based State**:
1. **No real-time sync** - Files can't sync across team members in real-time
2. **Merge conflicts** - Multiple developers create Git conflicts
3. **No atomic updates** - Race conditions with concurrent edits
4. **Limited querying** - Can't efficiently query "show all blocked tasks across all epics"
5. **No PM tool integration** - Can't bidirectionally sync with Jira/Linear/Azure DevOps
6. **Audit trail gaps** - No complete history of who changed what when
7. **No rollback** - Can't easily revert to previous project state

**Team Collaboration Issues**:
```
Developer A: Updates TASK-042.md locally
Developer B: Also updates TASK-042.md locally
Git merge: CONFLICT in tasks/in_progress/TASK-042.md

PM Tool (Jira): Task marked as "Done" by PM
Local markdown: Still shows "IN_PROGRESS"
Result: Developers working on completed tasks
```

### ✅ Why LangGraph + PostgreSQL + MCP

**Advantages**:
1. **Real-time state** - Database ensures single source of truth
2. **Atomic transactions** - ACID guarantees prevent race conditions
3. **Complex queries** - SQL enables sophisticated reporting
4. **PM tool sync** - MCPs handle bidirectional synchronization
5. **Complete audit trail** - Every state change tracked
6. **Rollback support** - Can revert to any previous state
7. **Multi-user** - Designed for team collaboration from day one

**Team Collaboration Solution**:
```
Developer A: Updates task via CLI → PostgreSQL transaction
Developer B: Queries task status → Gets latest from database
PM Tool (Jira): Task updated → MCP syncs to PostgreSQL
All developers: See consistent state immediately
```

### ✅ Why LangGraph (Not Claude Agent SDK Task Tool)

**LangGraph Advantages for Agentecflow**:

1. **Explicit State Management** - Complete visibility into workflow state
2. **Conditional Routing** - Decision points based on intermediate results
3. **Streaming Support** - Real-time progress updates to users
4. **Checkpoint/Resume** - Pause and resume workflows (critical for human checkpoints)
5. **Sub-graphs** - Nested workflows for complex orchestration
6. **Production Ready** - Battle-tested in Legal AI Agent with excellent results

**Example from Legal AI Agent**:
```python
# This pattern works beautifully for Agentecflow stages
workflow.add_conditional_edges(
    "human_spec_review",
    self._approval_routing,
    {
        "approved": "generate_epics",      # Continue to Stage 2
        "rejected": "gather_requirements",  # Return to Stage 1
        "timeout": "pause_workflow"        # Pause until approval
    }
)
```

---

## Implementation Roadmap

### Phase 1: Core Orchestration (Weeks 1-4)

**Deliverables**:
1. PostgreSQL schema and database setup
2. LangGraph orchestrator for Stage 1 (Specification)
3. Requirements MCP server with EARS/BDD generation
4. Basic CLI adapter for Claude Code
5. Human checkpoint infrastructure

**Success Criteria**:
- Can gather requirements and formalize to EARS
- Human can review and approve/reject specifications
- State persists correctly in PostgreSQL
- Requirements MCP tools work from Claude Code

### Phase 2: Task Management (Weeks 5-8)

**Deliverables**:
1. LangGraph orchestrator for Stage 2 (Tasks Definition)
2. PM Tools MCP server with Jira + Linear support
3. Epic/Feature/Task generation from requirements
4. Bidirectional synchronization with external PM tools
5. Progress rollup calculations

**Success Criteria**:
- Can generate complete epic/feature/task hierarchy
- Tasks sync to Jira and Linear correctly
- Progress rolls up from tasks → features → epics
- External PM tool changes sync back to Agentecflow

### Phase 3: Engineering Workflow (Weeks 9-12)

**Deliverables**:
1. LangGraph orchestrator for Stage 3 (Engineering)
2. Testing MCP server with multi-stack support
3. Quality gate evaluation system
4. Code review agent integration
5. Task assignment and tracking

**Success Criteria**:
- Can execute complete task workflow
- Tests run automatically and results stored
- Quality gates enforce standards
- Failed gates block progression

### Phase 4: Deployment & Multi-Tool (Weeks 13-16)

**Deliverables**:
1. LangGraph orchestrator for Stage 4 (Deployment & QA)
2. Deployment MCP server with Docker/CI/CD support
3. CLI adapters for Gemini CLI, GitHub Copilot, Cursor
4. Portfolio dashboard and reporting
5. Complete documentation

**Success Criteria**:
- Full 4-stage workflow works end-to-end
- Works from Claude Code, Gemini CLI, Cursor
- Deployment automation functional
- Production-ready documentation

---

## Technology Stack

### Core Infrastructure
- **Orchestration**: Python 3.10+ with LangGraph 0.2+
- **Database**: PostgreSQL 15+ with JSONB support
- **MCP Servers**: **Python only** (all MCP servers in Python for consistency)
- **LLM Integration**: OpenAI API via LangChain
- **Caching**: Redis (optional, for performance)

### Development Tools
- **Testing**: pytest, pytest-asyncio (Python stack only)
- **Database Migrations**: Alembic for schema versioning
- **API Framework**: FastAPI for HTTP endpoints (if needed)
- **Containerization**: Docker + Docker Compose

### Why Python-Only Stack

**Decision**: All components in Python (orchestrator + all 4 MCP servers + agents)

**Key Benefits**:
1. ✅ Single language runtime (Python 3.10+)
2. ✅ Direct Pydantic model sharing across all components
3. ✅ Consistent async patterns (asyncio throughout)
4. ✅ Proven by Legal AI Agent production implementation
5. ✅ Faster development (no context switching between languages)
6. ✅ Simpler deployment (one Dockerfile, one dependency manager)
7. ✅ Easier contributor onboarding (Python-only expertise required)

**Rejected Alternative**: TypeScript for MCP servers
- ❌ Would require Node.js + Python runtimes
- ❌ Can't share Pydantic models directly
- ❌ Different async patterns (Promises vs asyncio)
- ❌ Two package managers (npm + pip)
- ❌ No significant advantages for Agentecflow use case

### External Integrations
- **PM Tools**: Jira REST API, Linear GraphQL, Azure DevOps REST, GitHub GraphQL
- **CI/CD**: GitHub Actions, Azure Pipelines, GitLab CI
- **Deployment**: Docker, Kubernetes, cloud platforms

---

## Migration from Current System

### Gradual Migration Strategy

**Phase A: Parallel Run** (4 weeks)
- Deploy new LangGraph system alongside markdown system
- Dual-write to both systems
- Compare results for validation
- Fix discrepancies

**Phase B: Cutover** (2 weeks)
- Switch primary system to LangGraph
- Markdown files become read-only archives
- Monitor for issues

**Phase C: Deprecation** (2 weeks)
- Remove markdown file dependencies
- Update all documentation
- Train users on new system

### Data Migration Tools

```python
# Migration script: Markdown → PostgreSQL
class MarkdownMigrationTool:
    """Migrate existing markdown-based projects to PostgreSQL"""

    async def migrate_project(self, project_path: str):
        """Migrate a single project"""

        # Read markdown files
        epics = await self._parse_markdown_epics(f"{project_path}/docs/epics")
        features = await self._parse_markdown_features(f"{project_path}/docs/features")
        tasks = await self._parse_markdown_tasks(f"{project_path}/tasks")
        requirements = await self._parse_markdown_requirements(f"{project_path}/docs/requirements")

        # Create database records
        project = await self.db.create_project(name=project_path)

        for epic in epics:
            db_epic = await self.db.create_epic(project.id, epic)

            for feature in epic.features:
                db_feature = await self.db.create_feature(db_epic.id, feature)

                for task in feature.tasks:
                    await self.db.create_task(db_feature.id, task)

        # Verify migration
        await self._verify_migration(project.id, project_path)
```

---

## Success Metrics

### Technical Metrics
- **Response Time**: < 5 seconds for most operations
- **Sync Latency**: < 2 seconds to external PM tools
- **Uptime**: 99.9% for orchestration engine
- **Test Coverage**: > 90% for core workflows
- **Database Performance**: < 100ms for 95th percentile queries

### Business Metrics
- **Team Adoption**: > 80% within 3 months
- **Project Setup Time**: 50% reduction vs. manual setup
- **Requirements Traceability**: 95% coverage
- **Automated Testing**: 85% of tests generated from requirements
- **PM Tool Sync Accuracy**: 99% bidirectional accuracy

### User Experience Metrics
- **Time to First Task**: < 30 minutes from specification
- **Human Checkpoint Response**: < 24 hours average
- **Quality Gate Pass Rate**: > 75% first-time pass
- **Cross-Tool Compatibility**: Works from 4+ CLI tools

---

## Risk Mitigation

### Technical Risks

**Risk**: LangGraph state management complexity
- **Mitigation**: Extensive testing with Legal AI Agent patterns; comprehensive logging; fallback mechanisms

**Risk**: PostgreSQL becomes bottleneck
- **Mitigation**: Connection pooling; read replicas; query optimization; caching layer

**Risk**: MCP server failures
- **Mitigation**: Circuit breakers; retry logic; graceful degradation; local fallbacks

### Business Risks

**Risk**: User resistance to change from markdown
- **Mitigation**: Gradual migration; training sessions; clear benefits communication; parallel run period

**Risk**: External PM tool API changes
- **Mitigation**: Abstraction layers; versioned integrations; fallback modes; community support

**Risk**: Vendor lock-in to specific LLM provider
- **Mitigation**: LangChain abstraction; model swappability; open-source alternatives

---

## Comparison: Legal AI Agent vs. Agentecflow

### Similarities (Proven Patterns to Reuse)

| Pattern | Legal AI Agent | Agentecflow Application |
|---------|---------------|------------------------|
| **LangGraph Workflow** | Multi-stage legal research pipeline | 4-stage project workflow (Spec → Tasks → Engineering → Deploy) |
| **State Management** | Pydantic models with workflow state | Project/Epic/Feature/Task state in PostgreSQL |
| **Conditional Routing** | Research vs. Reasoning path selection | Approval routing, quality gate decisions |
| **Tool Orchestration** | Legislation search, XML parsing, validation | Requirements MCP, PM Tools MCP, Testing MCP |
| **Error Handling** | Graceful degradation with fallbacks | Retry mechanisms, human escalation |
| **Streaming** | Real-time AI response streaming | Progress updates during long-running operations |
| **Specialized Agents** | Research agent, Reasoning agent, Comprehensive agent | Specification agent, Task agent, Engineering agent |

### Key Differences

| Aspect | Legal AI Agent | Agentecflow |
|--------|---------------|-------------|
| **User Base** | Single user legal research | Multi-user team collaboration |
| **State Storage** | In-memory / session-based | PostgreSQL persistent storage |
| **External Integration** | Read-only (legislation.gov.uk) | Bidirectional (Jira/Linear/Azure/GitHub) |
| **Human Interaction** | Continuous (Q&A conversation) | Gated checkpoints (approval/rejection) |
| **Workflow Complexity** | Single workflow, multiple paths | 4 major stages, nested sub-workflows |
| **Deployment Model** | Standalone application | Distributed system with MCPs |

---

## Conclusion

**Recommendation**: Build Agentecflow with **LangGraph orchestration + PostgreSQL state + MCP integrations**.

**Key Decision Factors**:
1. ✅ **Proven Architecture** - Legal AI Agent demonstrates LangGraph production viability
2. ✅ **Team Collaboration** - PostgreSQL enables real multi-user coordination
3. ✅ **External Integration** - MCPs provide clean PM tool synchronization
4. ✅ **Scalability** - Database-backed state scales to enterprise needs
5. ✅ **Cross-Tool Support** - CLI adapters enable Claude Code, Gemini, Cursor, Copilot

**What to Abandon**:
- ❌ Local markdown files for state management
- ❌ Single-developer CLI assumptions
- ❌ Static command specifications without orchestration

**What to Build**:
- ✅ LangGraph StateGraph for each of 4 stages
- ✅ PostgreSQL schema with complete project state
- ✅ MCP servers for Requirements, PM Tools, Testing, Deployment
- ✅ Universal CLI adapter for multi-tool support
- ✅ Human checkpoint infrastructure with timeout handling

**Next Step**: Begin Phase 1 implementation - Core Orchestration with Stage 1 (Specification) LangGraph workflow and Requirements MCP server.

---

**References**:
- Legal AI Agent: `/Users/richardwoollcott/Projects/appmilla_github/uk-probate-agent`
- Agentecflow Overview: `docs/research/Agentecflow overview.pdf`
- Product Requirements: `docs/research/agentecflow_product_requirements_and_implementation_summary.md`
- Candidate Epics: `docs/research/candidate_epics.md`
