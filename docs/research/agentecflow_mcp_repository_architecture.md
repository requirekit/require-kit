# Agentecflow MCP Repository Architecture Recommendation

**Date**: 2025-10-01
**Question**: Should all MCPs and agents be in the same repo or separate repos?
**Recommendation**: **Python Monorepo with Workspaces**

---

## TL;DR - Recommendation

✅ **Use a Python Monorepo** with the following structure:

```
agentecflow-platform/              # Single repository
├── orchestrator/                  # LangGraph orchestration engine
├── mcps/                         # All MCP servers
│   ├── requirements/             # Requirements MCP
│   ├── pm-tools/                 # PM Tools MCP (Jira, Linear, etc.)
│   ├── testing/                  # Testing MCP
│   └── deployment/               # Deployment MCP
├── shared/                       # Shared libraries
│   ├── models/                   # Pydantic models
│   ├── utils/                    # Common utilities
│   └── database/                 # Database schemas/migrations
├── api/                          # FastAPI REST API (optional)
├── tests/                        # Integration tests
└── docs/                         # Documentation
```

**Rationale**: Proven by your Legal AI Agent (`uk-probate-agent`) - monorepo works excellently for Python projects with multiple interconnected components.

---

## Analysis: Monorepo vs Multi-Repo

### Option 1: Monorepo (RECOMMENDED) ✅

**Structure**:
```
agentecflow-platform/
├── orchestrator/                         # Main LangGraph orchestrator
│   ├── src/
│   │   ├── workflows/                   # LangGraph workflows
│   │   ├── agents/                      # Agent coordination
│   │   ├── state/                       # State management
│   │   └── main.py                      # Entry point
│   ├── tests/
│   └── pyproject.toml
│
├── mcps/                                # All MCP servers
│   ├── requirements/                    # Requirements MCP Server
│   │   ├── src/
│   │   │   ├── server.py               # MCP server implementation
│   │   │   ├── tools/                  # EARS, BDD generation
│   │   │   └── resources/              # Requirement templates
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   ├── pm-tools/                       # PM Tools MCP Server
│   │   ├── src/
│   │   │   ├── server.py
│   │   │   ├── jira/                   # Jira integration
│   │   │   ├── linear/                 # Linear integration
│   │   │   ├── azure_devops/           # Azure DevOps integration
│   │   │   └── github/                 # GitHub Projects integration
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   ├── testing/                        # Testing MCP Server
│   │   ├── src/
│   │   │   ├── server.py
│   │   │   ├── pytest_runner/
│   │   │   ├── jest_runner/
│   │   │   └── playwright_runner/
│   │   ├── tests/
│   │   └── pyproject.toml
│   │
│   └── deployment/                     # Deployment MCP Server
│       ├── src/
│       │   ├── server.py
│       │   ├── docker/
│       │   ├── ci_cd/
│       │   └── qa/
│       ├── tests/
│       └── pyproject.toml
│
├── shared/                             # Shared libraries (critical!)
│   ├── models/                         # Shared Pydantic models
│   │   ├── __init__.py
│   │   ├── requirement.py              # Requirement model
│   │   ├── epic.py                     # Epic model
│   │   ├── feature.py                  # Feature model
│   │   ├── task.py                     # Task model
│   │   ├── test_result.py              # Test result model
│   │   └── state.py                    # Workflow state models
│   │
│   ├── database/                       # Database schemas
│   │   ├── models.py                   # SQLAlchemy models
│   │   ├── migrations/                 # Alembic migrations
│   │   └── connection.py               # DB connection pooling
│   │
│   └── utils/                          # Common utilities
│       ├── logging.py
│       ├── config.py
│       └── validation.py
│
├── api/                                # Optional: REST API wrapper
│   ├── src/
│   │   ├── main.py                    # FastAPI app
│   │   ├── routes/
│   │   └── middleware/
│   ├── tests/
│   └── pyproject.toml
│
├── tests/                              # Integration tests
│   ├── integration/                    # Cross-component tests
│   ├── e2e/                           # End-to-end workflows
│   └── performance/                    # Performance benchmarks
│
├── docs/                               # Documentation
│   ├── architecture/
│   ├── api/
│   └── deployment/
│
├── scripts/                            # Deployment scripts
│   ├── setup_dev.sh
│   ├── run_all_mcps.sh
│   └── deploy.sh
│
├── docker-compose.yml                  # Local development
├── pyproject.toml                      # Root project config
├── README.md
└── .github/
    └── workflows/                      # CI/CD pipelines
        ├── orchestrator.yml
        ├── mcps.yml
        └── integration-tests.yml
```

### Advantages of Monorepo ✅

#### 1. **Shared Code Reuse** (Critical for MCP Architecture)
```python
# All components import from shared/
from shared.models import Requirement, Epic, Task, TestResult
from shared.database import get_connection
from shared.utils import setup_logging

# Orchestrator uses shared models
class AgentecflowOrchestrator:
    def process(self, state: AgentecflowState) -> AgentecflowState:
        # Uses shared models
        pass

# Requirements MCP uses SAME models
class RequirementsMCPServer:
    async def formalize_ears(self, raw: str) -> Requirement:
        # Uses shared Requirement model - guaranteed compatibility
        pass

# PM Tools MCP uses SAME models
class PMToolsMCPServer:
    async def sync_to_jira(self, epic: Epic) -> str:
        # Uses shared Epic model - guaranteed compatibility
        pass
```

**Benefit**: Single source of truth for data models. Change once, reflect everywhere.

#### 2. **Atomic Changes Across Components**
```bash
# Single PR changes orchestrator + MCP in lockstep
git commit -m "Add priority field to Epic model
- Update shared/models/epic.py
- Update orchestrator to use priority
- Update pm-tools MCP to sync priority to Jira
- Update tests across all components"
```

**Benefit**: No version coordination hell. Changes are atomic.

#### 3. **Simplified Dependency Management**
```toml
# Root pyproject.toml
[tool.poetry]
name = "agentecflow-platform"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.10"
langgraph = "^0.2.0"
mcp = "^1.0.0"
pydantic = "^2.0.0"
fastapi = "^0.110.0"
sqlalchemy = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
black = "^24.0.0"
mypy = "^1.8.0"

# All subprojects inherit from root
# orchestrator/pyproject.toml just references ../shared
# mcps/requirements/pyproject.toml just references ../../shared
```

**Benefit**: One `poetry install` gets everything. No version mismatches.

#### 4. **Unified Testing**
```bash
# Run all tests from root
pytest tests/                  # Integration tests
pytest orchestrator/tests/     # Orchestrator unit tests
pytest mcps/requirements/tests/ # Requirements MCP tests
pytest mcps/pm-tools/tests/    # PM Tools MCP tests

# Or run everything
pytest -v
```

**Benefit**: CI/CD runs all tests in one pipeline. Catch integration issues early.

#### 5. **Single Development Environment**
```bash
# Clone once
git clone https://github.com/your-org/agentecflow-platform.git
cd agentecflow-platform

# Install once
poetry install

# Run everything locally
docker-compose up  # Starts orchestrator + all MCPs + PostgreSQL + Redis
```

**Benefit**: New developers onboard in minutes, not hours.

#### 6. **Proven by Your Legal AI Agent**

Your `uk-probate-agent` uses monorepo structure:
```
uk-probate-agent/           # Single repo
├── src/
│   ├── agents/            # Multiple agents
│   ├── engines/           # Research, reasoning engines
│   ├── workflows/         # LangGraph workflows
│   ├── tools/             # Shared tools
│   ├── models/            # Shared models
│   └── services/          # External services
├── api_server.py          # FastAPI server
└── tests/
```

**It works beautifully.** Why change a winning formula?

### Disadvantages of Monorepo (Manageable)

#### 1. **Larger Repository Size**
- **Impact**: ~100-500MB repo size (not huge for modern git)
- **Mitigation**: Use sparse checkout if needed

#### 2. **Potential for Tighter Coupling**
- **Impact**: Risk of shared code becoming a ball of mud
- **Mitigation**: Clear boundaries in `shared/` with documented interfaces

#### 3. **CI/CD Complexity**
- **Impact**: Need intelligent CI to only test changed components
- **Mitigation**: Use GitHub Actions path filters:
```yaml
on:
  push:
    paths:
      - 'orchestrator/**'
      - 'shared/**'
```

---

## Option 2: Multi-Repo (NOT RECOMMENDED) ❌

**Structure**:
```
agentecflow-orchestrator/       # Separate repo
agentecflow-requirements-mcp/   # Separate repo
agentecflow-pm-tools-mcp/       # Separate repo
agentecflow-testing-mcp/        # Separate repo
agentecflow-deployment-mcp/     # Separate repo
agentecflow-shared-models/      # Separate repo (the killer)
```

### Disadvantages of Multi-Repo

#### 1. **Version Coordination Nightmare**
```bash
# Orchestrator depends on shared-models v1.2.0
# Requirements MCP depends on shared-models v1.1.5
# PM Tools MCP depends on shared-models v1.2.1

# Result: Type mismatches at runtime 🔥
orchestrator sends: Epic(priority="high")  # v1.2.0 has priority
pm-tools MCP receives: Epic(???)           # v1.1.5 doesn't have priority
```

**This is a disaster waiting to happen.**

#### 2. **Cross-Repo Changes Require Multiple PRs**
```
# Want to add priority to Epic?

PR1: agentecflow-shared-models
  - Add priority field to Epic model
  - Wait for review, merge, release

PR2: agentecflow-orchestrator
  - Update dependency to shared-models v1.3.0
  - Use priority field
  - Wait for review, merge

PR3: agentecflow-pm-tools-mcp
  - Update dependency to shared-models v1.3.0
  - Sync priority to Jira
  - Wait for review, merge

# Total time: 3x longer, 3x the context switching
```

#### 3. **Dependency Hell**
```toml
# agentecflow-orchestrator/pyproject.toml
[tool.poetry.dependencies]
agentecflow-shared-models = "^1.2.0"

# agentecflow-requirements-mcp/pyproject.toml
[tool.poetry.dependencies]
agentecflow-shared-models = "^1.1.0"

# Result: Which version wins? Depends on install order 🎲
```

#### 4. **Complex Local Development**
```bash
# Developer workflow (painful):
git clone agentecflow-orchestrator
git clone agentecflow-requirements-mcp
git clone agentecflow-pm-tools-mcp
git clone agentecflow-testing-mcp
git clone agentecflow-deployment-mcp
git clone agentecflow-shared-models

# Now set up links...
cd agentecflow-orchestrator
poetry add --editable ../agentecflow-shared-models

cd ../agentecflow-requirements-mcp
poetry add --editable ../agentecflow-shared-models

# Repeat for each repo 😭
```

#### 5. **Testing Integration Issues Late**
```
# Unit tests pass in isolation ✅
pytest agentecflow-orchestrator/tests/  # All pass
pytest agentecflow-pm-tools-mcp/tests/  # All pass

# Integration fails in production 💥
orchestrator.sync_epic(epic) → pm_tools_mcp.process(epic)
# TypeError: Epic missing field 'priority' (version mismatch)
```

**You find out in production, not in CI.**

---

## Hybrid Option 3: Monorepo with Independent Deployment (POSSIBLE)

If you're worried about monorepo deployment complexity:

**Structure**: Monorepo (as in Option 1)
**Deployment**: Independent services

```yaml
# docker-compose.yml (development)
services:
  orchestrator:
    build: ./orchestrator
    ports: ["8000:8000"]

  requirements-mcp:
    build: ./mcps/requirements
    ports: ["8001:8001"]

  pm-tools-mcp:
    build: ./mcps/pm-tools
    ports: ["8002:8002"]

# Each can be deployed independently in production
# But they share the same codebase and models
```

**Benefits**:
- ✅ Monorepo development experience
- ✅ Independent scaling in production
- ✅ Shared models guarantee compatibility
- ✅ Atomic changes across components

---

## Industry Examples

### Monorepo Success Stories

**1. Google** - Entire codebase in one repo (billions of lines)
**2. Facebook/Meta** - Monorepo for React, React Native, Jest, etc.
**3. Vercel** - Next.js, Turbo, Svelte in monorepo
**4. Anthropic** - Claude Desktop (MCP SDK) uses monorepo

### Python Monorepo Tools

**1. Poetry Workspaces** (Recommended)
```toml
# Root pyproject.toml
[tool.poetry]
name = "agentecflow-platform"

[tool.poetry.dependencies]
orchestrator = {path = "orchestrator", develop = true}
requirements-mcp = {path = "mcps/requirements", develop = true}
pm-tools-mcp = {path = "mcps/pm-tools", develop = true}
shared = {path = "shared", develop = true}
```

**2. Pants Build** (For larger scale)
- Used by Twitter, Foursquare
- Excellent for Python monorepos

**3. Bazel** (Overkill for this project)
- Used by Google
- Too complex for Agentecflow scale

---

## Recommendation Summary

### ✅ Use Monorepo Because:

1. **Your Legal AI Agent proves it works** - Same pattern, same scale
2. **Shared Pydantic models** - Single source of truth
3. **Atomic changes** - One PR changes orchestrator + MCPs
4. **Simplified development** - One clone, one install, one test command
5. **Guaranteed compatibility** - No version mismatch hell
6. **Faster iteration** - No cross-repo coordination overhead

### 🎯 Recommended Structure:

```
agentecflow-platform/              # Single repository
├── orchestrator/                  # LangGraph orchestration
├── mcps/                         # All MCP servers (4 total)
│   ├── requirements/
│   ├── pm-tools/
│   ├── testing/
│   └── deployment/
├── shared/                       # Shared Pydantic models (critical!)
│   ├── models/
│   ├── database/
│   └── utils/
├── tests/                        # Integration tests
└── docker-compose.yml           # Local development
```

### 📦 Deployment Options (Both Supported):

**Option A**: Single deployment (orchestrator includes all MCPs)
**Option B**: Independent microservices (each MCP separately deployed)

**Monorepo supports both.** You decide at deployment time, not development time.

---

## Getting Started

### Initial Setup

```bash
# Create monorepo
mkdir agentecflow-platform
cd agentecflow-platform
git init

# Initialize with Poetry
poetry init

# Create structure
mkdir -p orchestrator/src orchestrator/tests
mkdir -p mcps/requirements/src mcps/requirements/tests
mkdir -p mcps/pm-tools/src mcps/pm-tools/tests
mkdir -p mcps/testing/src mcps/testing/tests
mkdir -p mcps/deployment/src mcps/deployment/tests
mkdir -p shared/models shared/database shared/utils
mkdir -p tests/integration tests/e2e
mkdir -p docs/architecture
mkdir -p scripts

# Install dependencies
poetry add langgraph mcp pydantic fastapi sqlalchemy
poetry add --group dev pytest pytest-asyncio black mypy ruff

# Start coding!
```

### First Component

Start with **orchestrator + requirements MCP + shared models**:

```python
# shared/models/requirement.py
from pydantic import BaseModel, Field
from typing import Literal

class Requirement(BaseModel):
    id: str
    text: str
    pattern: Literal["ubiquitous", "event", "state", "unwanted", "optional"]
    priority: int
    status: str

# orchestrator/src/workflows/specification.py
from langgraph.graph import StateGraph
from shared.models import Requirement

class SpecificationWorkflow:
    def __init__(self):
        self.workflow = self._create_workflow()

# mcps/requirements/src/server.py
from mcp.server import Server
from shared.models import Requirement

class RequirementsMCPServer:
    async def formalize_ears(self, text: str) -> Requirement:
        # Uses shared model
        return Requirement(...)
```

**All three components use the SAME Requirement model. Perfect compatibility. Zero version issues.**

---

## Conclusion

**Use a Python monorepo.** It's proven by your Legal AI Agent, recommended by industry best practices, and eliminates the version coordination nightmare that would cripple a multi-repo MCP architecture.

Start simple (orchestrator + one MCP), scale gradually, deploy independently if needed. The monorepo gives you maximum flexibility with minimum coordination overhead.

**Next Step**: I can help you set up the initial monorepo structure and create the first component (orchestrator + requirements MCP + shared models). Ready to proceed?
