# Template Creation Commands - Proposal

**Status**: Draft
**Created**: 2025-10-19
**Author**: AI Engineer
**Version**: 1.0.0

## Executive Summary

This proposal introduces two new commands to dramatically simplify Agentecflow adoption for both **existing codebases** and **greenfield projects**:

1. **`/template-create`** - Analyzes existing codebase and generates a custom local template
2. **`/template-init`** - Interactive Q&A to create greenfield project templates

Both commands feature **intelligent agent discovery** from online repositories (subagents.cc, GitHub collections) and **automatic pattern extraction** to capture your team's architectural conventions.

## Problem Statement

### Current State

**Existing Codebases**:
- Teams must manually create local templates by copying global templates
- Requires deep understanding of template structure (manifest.json, settings.json, etc.)
- No automated way to capture existing architectural patterns
- Agent discovery is manual and time-consuming

**Greenfield Projects**:
- Limited to global templates (maui-appshell, react, python, etc.)
- No guided customization during template creation
- Can't easily incorporate team preferences or company standards
- No integration with community agent repositories

### Pain Points

1. **High Barrier to Entry**: Teams abandon Agentecflow because template setup is complex
2. **Pattern Drift**: Manually created templates don't accurately reflect actual codebase patterns
3. **Agent Discovery Gap**: Valuable community agents remain undiscovered
4. **Time Investment**: 2-4 hours to create a quality local template manually

## Proposed Solution

### Command 1: `/template-create` (Existing Codebase Capture)

**Purpose**: Automatically analyze an existing codebase and generate a local template that captures its patterns, architecture, and conventions.

#### Usage

```bash
# Analyze current project and create template
/template-create "mycompany-react" --scan-depth full

# Analyze with manual guidance
/template-create "mycompany-maui" --interactive

# Analyze specific directories only
/template-create "acme-api" --scan-paths "src/domain,src/services"

# Include agent discovery
/template-create "mycompany-python" --discover-agents --agent-sources "subagents.cc,github:wshobson/agents"
```

#### 8-Phase Workflow

```
Phase 1: Technology Stack Detection
├─ Scan project files for technology indicators
├─ Detect frameworks, libraries, versions
├─ Identify package managers and build systems
└─ Output: Technology profile (React 18 + TypeScript + Vite)

Phase 2: Architecture Pattern Analysis
├─ Analyze directory structure and layering
├─ Identify architectural patterns (DDD, Clean Architecture, etc.)
├─ Detect naming conventions (repositories, services, etc.)
├─ Find error handling patterns (ErrorOr, Result, Either)
└─ Output: Architecture blueprint

Phase 3: Code Pattern Extraction
├─ Extract common class patterns and templates
├─ Identify dependency injection patterns
├─ Capture testing strategies and frameworks
├─ Analyze quality standards (coverage thresholds)
└─ Output: Code templates with placeholders

Phase 4: Agent Discovery & Matching
├─ Fetch agent listings from online sources
├─ Match agents to detected technology stack
├─ Filter by detected architectural patterns
├─ Rank by relevance scores
└─ Output: Recommended agent list

Phase 5: Agent Selection (Interactive)
├─ Display categorized agent recommendations
├─ Allow user selection with preview
├─ Support bulk import by category
├─ Download and customize agent definitions
└─ Output: Selected agents for template

Phase 6: Template Generation
├─ Create manifest.json with detected metadata
├─ Generate settings.json with naming conventions
├─ Create CLAUDE.md with architectural guidance
├─ Generate code templates with placeholders
└─ Output: Complete template structure

Phase 7: Validation & Testing
├─ Validate template structure completeness
├─ Test template placeholder substitution
├─ Verify agent definitions are valid
├─ Generate sample project for verification
└─ Output: Validation report

Phase 8: Installation & Distribution
├─ Install template to installer/local/templates/
├─ Generate README with usage instructions
├─ Create distribution package (.tar.gz)
├─ Output setup commands for team
└─ Output: Ready-to-use local template
```

#### Pattern Detection Examples

**React/TypeScript Detection**:
```typescript
// Detected pattern: React component with TypeScript
// From: src/components/ProductList.tsx

export interface ProductListProps {
  products: Product[];
  onSelect: (id: string) => void;
}

export const ProductList: React.FC<ProductListProps> = ({ products, onSelect }) => {
  return (
    <div className="product-list">
      {products.map(p => (
        <ProductCard key={p.id} product={p} onClick={() => onSelect(p.id)} />
      ))}
    </div>
  );
};

// Generated template: templates/component/functional-component.tsx.template
export interface {{ComponentName}}Props {
  {{Props}}
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({ {{PropNames}} }) => {
  return (
    <div className="{{className}}">
      {{ComponentBody}}
    </div>
  );
};
```

**.NET MAUI Detection**:
```csharp
// Detected pattern: Domain operation with ErrorOr
// From: src/Domain/Products/GetProducts.cs

public class GetProducts
{
    private readonly ILogger<GetProducts> _logger;
    private readonly IProductRepository _repository;

    public GetProducts(ILogger<GetProducts> logger, IProductRepository repository)
    {
        _logger = logger;
        _repository = repository;
    }

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        _logger.LogInformation("Executing GetProducts");
        return await _repository.GetAllAsync();
    }
}

// Generated template: templates/domain/query-operation.cs.template
public class {{OperationName}}
{
    private readonly ILogger<{{OperationName}}> _logger;
    private readonly I{{Entity}}Repository _repository;

    public {{OperationName}}(ILogger<{{OperationName}}> logger, I{{Entity}}Repository repository)
    {
        _logger = logger;
        _repository = repository;
    }

    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        _logger.LogInformation("Executing {{OperationName}}");
        return await _repository.{{RepositoryMethod}}();
    }
}
```

**Python FastAPI Detection**:
```python
# Detected pattern: FastAPI endpoint with dependency injection
# From: src/api/products.py

@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    repository: ProductRepository = Depends(get_repository)
) -> List[ProductResponse]:
    """Get all products"""
    products = await repository.get_all()
    return [ProductResponse.from_entity(p) for p in products]

# Generated template: templates/api/get-endpoint.py.template
@router.get("{{endpoint}}", response_model={{ResponseModel}})
async def {{function_name}}(
    {{Dependencies}}
) -> {{ResponseModel}}:
    """{{Description}}"""
    {{Implementation}}
```

#### Agent Discovery Integration

**Phase 4: Agent Discovery Flow**

```
┌─────────────────────────────────────────────────────────────┐
│ Agent Discovery Sources                                     │
├─────────────────────────────────────────────────────────────┤
│ 1. subagents.cc                                            │
│    - Fetch via web scraping (/browse endpoint)             │
│    - Parse YAML frontmatter + markdown content             │
│    - Extract metadata: name, description, tags, tools       │
│                                                              │
│ 2. github:wshobson/agents                                  │
│    - Clone/fetch repository structure                      │
│    - Parse .claude-plugin/marketplace.json                 │
│    - Extract agents from plugins/* directories             │
│                                                              │
│ 3. github:VoltAgent/awesome-claude-code-subagents          │
│    - Fetch categories/* directory structure                │
│    - Parse agent markdown files                            │
│    - Extract YAML frontmatter metadata                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Matching Algorithm                                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Technology Stack Matching (40% weight)                  │
│    - Exact match: +40 points (python → python-specialist)   │
│    - Partial match: +20 points (react → frontend)          │
│                                                              │
│ 2. Architecture Pattern Matching (30% weight)              │
│    - Pattern keywords in agent description                  │
│    - DDD, Clean Architecture, CQRS, etc.                   │
│                                                              │
│ 3. Tool/MCP Compatibility (20% weight)                     │
│    - Required MCP tools available                          │
│    - Integration with detected libraries                   │
│                                                              │
│ 4. Community Validation (10% weight)                       │
│    - Download count, favorites, stars                      │
│    - Recency of updates                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Interactive Selection UI                                    │
├─────────────────────────────────────────────────────────────┤
│ 🎯 RECOMMENDED AGENTS FOR YOUR STACK (React + TypeScript)   │
│                                                              │
│ ✅ Core Development (5 agents)                              │
│   [x] react-state-specialist      Score: 95  (subagents.cc) │
│   [x] typescript-domain-modeler   Score: 88  (wshobson)    │
│   [x] react-testing-specialist    Score: 85  (VoltAgent)    │
│   [ ] frontend-performance        Score: 72  (subagents.cc) │
│   [ ] accessibility-auditor       Score: 68  (VoltAgent)    │
│                                                              │
│ 🔧 Infrastructure (3 agents)                                │
│   [ ] vite-bundler-specialist     Score: 90  (wshobson)    │
│   [ ] docker-containerization     Score: 65  (VoltAgent)    │
│   [ ] github-actions-ci           Score: 62  (wshobson)    │
│                                                              │
│ 🧪 Quality & Testing (4 agents)                             │
│   [x] playwright-e2e-specialist   Score: 92  (subagents.cc) │
│   [ ] vitest-unit-tester          Score: 87  (VoltAgent)    │
│   [ ] code-coverage-enforcer      Score: 70  (wshobson)    │
│   [ ] security-scanner            Score: 68  (VoltAgent)    │
│                                                              │
│ Options:                                                     │
│   [A] Accept all recommended (score ≥ 85)                   │
│   [C] Customize selection                                   │
│   [S] Skip agent discovery                                  │
│   [P] Preview agent details                                 │
└─────────────────────────────────────────────────────────────┘
```

**Agent Discovery Implementation**:

```python
# installer/global/commands/lib/agent_discovery.py

from dataclasses import dataclass
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import subprocess

@dataclass
class AgentMetadata:
    name: str
    description: str
    source: str  # "subagents.cc", "github:wshobson/agents", etc.
    category: str
    tools: List[str]
    score: int  # Relevance score 0-100
    content: str  # Full agent markdown content
    author: Optional[str] = None
    downloads: Optional[int] = None
    url: Optional[str] = None

class AgentDiscovery:
    def __init__(self, sources: List[str]):
        self.sources = sources
        self.agents: List[AgentMetadata] = []

    async def discover(self) -> List[AgentMetadata]:
        """Discover agents from all configured sources"""
        for source in self.sources:
            if source == "subagents.cc":
                await self._discover_subagents_cc()
            elif source.startswith("github:"):
                repo = source.replace("github:", "")
                await self._discover_github_repo(repo)

        return self.agents

    async def _discover_subagents_cc(self):
        """Scrape subagents.cc for agent listings"""
        response = requests.get("https://subagents.cc/browse")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse agent cards from browse page
        # Extract name, description, tags, download count
        # Fetch full content for each agent
        pass

    async def _discover_github_repo(self, repo: str):
        """Clone and parse GitHub agent repository"""
        if repo == "wshobson/agents":
            await self._discover_wshobson_agents()
        elif repo == "VoltAgent/awesome-claude-code-subagents":
            await self._discover_voltagen_agents()

    async def _discover_wshobson_agents(self):
        """Parse wshobson/agents repository structure"""
        # Clone repo to temp directory
        # Parse .claude-plugin/marketplace.json
        # Extract agents from plugins/*/agents/*.md
        pass

    async def _discover_voltagen_agents(self):
        """Parse VoltAgent/awesome-claude-code-subagents repository"""
        # Fetch categories/ directory structure
        # Parse each category's agent markdown files
        # Extract YAML frontmatter and content
        pass

    def match_to_stack(
        self,
        technology: str,
        patterns: List[str],
        tools: List[str]
    ) -> List[AgentMetadata]:
        """Match discovered agents to detected technology stack"""
        scored_agents = []

        for agent in self.agents:
            score = 0

            # Technology matching (40%)
            if technology.lower() in agent.name.lower() or \
               technology.lower() in agent.description.lower():
                score += 40

            # Pattern matching (30%)
            for pattern in patterns:
                if pattern.lower() in agent.description.lower():
                    score += 30
                    break

            # Tool compatibility (20%)
            common_tools = set(agent.tools) & set(tools)
            if common_tools:
                score += 20

            # Community validation (10%)
            if agent.downloads and agent.downloads > 100:
                score += 10

            agent.score = score
            if score >= 60:  # Threshold for relevance
                scored_agents.append(agent)

        # Sort by score descending
        return sorted(scored_agents, key=lambda a: a.score, reverse=True)

    def categorize(self, agents: List[AgentMetadata]) -> Dict[str, List[AgentMetadata]]:
        """Categorize agents by function"""
        categories = {
            "Core Development": [],
            "Infrastructure": [],
            "Quality & Testing": [],
            "Data & AI": [],
            "Design & UX": [],
            "Security": [],
            "Other": []
        }

        for agent in agents:
            # Categorize based on agent.category or description keywords
            category = self._infer_category(agent)
            if category in categories:
                categories[category].append(agent)
            else:
                categories["Other"].append(agent)

        return categories

    def _infer_category(self, agent: AgentMetadata) -> str:
        """Infer category from agent metadata"""
        keywords = {
            "Core Development": ["development", "coding", "programming", "language"],
            "Infrastructure": ["devops", "deployment", "docker", "kubernetes", "ci/cd"],
            "Quality & Testing": ["testing", "quality", "test", "coverage", "qa"],
            "Data & AI": ["data", "ml", "ai", "machine learning", "analytics"],
            "Design & UX": ["design", "ux", "ui", "frontend", "figma"],
            "Security": ["security", "auth", "encryption", "vulnerability"]
        }

        description = agent.description.lower()
        for category, kws in keywords.items():
            if any(kw in description for kw in kws):
                return category

        return "Other"
```

#### Output Example

```
✅ Template Created: mycompany-react

📋 Template Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Technology: React 18.2 + TypeScript 5.1 + Vite 4.4
Architecture: Component-Based with Domain-Driven Design
Patterns Detected:
  - Functional components with TypeScript interfaces
  - Custom hooks for state management
  - React Query for data fetching
  - Context API for global state
  - Vitest + React Testing Library

Template Structure:
  ✓ manifest.json (React, TypeScript, Vite metadata)
  ✓ settings.json (naming conventions, layer config)
  ✓ CLAUDE.md (architectural guidance)
  ✓ README.md (usage instructions)
  ✓ templates/ (5 code templates)
    - component/functional-component.tsx.template
    - hook/custom-hook.ts.template
    - context/context-provider.tsx.template
    - test/component-test.tsx.template
    - api/react-query-hook.ts.template
  ✓ agents/ (3 selected agents)
    - react-state-specialist.md (score: 95)
    - typescript-domain-modeler.md (score: 88)
    - react-testing-specialist.md (score: 85)

📦 Distribution Package
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: installer/local/templates/mycompany-react/
Package: mycompany-react-v1.0.0.tar.gz (145 KB)

Team Distribution:
  # Option 1: Git repository
  git add installer/local/templates/mycompany-react/
  git commit -m "feat: Add MyCompany React template v1.0.0"
  git push

  # Option 2: Package distribution
  cp mycompany-react-v1.0.0.tar.gz /shared/templates/
  tar -xzf mycompany-react-v1.0.0.tar.gz -C installer/local/templates/

Usage:
  agentic-init mycompany-react

Validation:
  ✓ Template structure valid
  ✓ All placeholders functional
  ✓ Sample project generated successfully
  ✓ 3 agents validated and ready
```

---

### Command 2: `/template-init` (Greenfield Interactive Creation)

**Purpose**: Guided Q&A session to create a custom template for greenfield projects, incorporating technology choices, patterns, and team preferences.

#### Usage

```bash
# Start interactive template creation
/template-init

# Start with pre-configured technology
/template-init --technology react

# Use specific base template
/template-init --from maui-appshell

# Include agent discovery
/template-init --discover-agents
```

#### Interactive Q&A Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Agentecflow Template Creator                                │
│ Let's create a custom template for your greenfield project  │
└─────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1: Basic Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Template name (lowercase, hyphens):
> mycompany-mobile-app

❓ Description:
> Mobile app template for MyCompany iOS/Android apps with MVVM

❓ Template version (semver):
> 1.0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2: Technology Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Primary technology:
  1. React (TypeScript, Vite, Tailwind)
  2. Python (FastAPI, pytest, SQLAlchemy)
  3. .NET MAUI (C#, XAML, MVVM)
  4. TypeScript API (NestJS, Domain-Driven Design)
  5. .NET Microservice (FastEndpoints, Clean Architecture)
  6. Full Stack (React + Python)
  7. Other (specify)

> 3

❓ .NET version:
  1. .NET 8 (LTS)
  2. .NET 9

> 1

❓ Additional frameworks/libraries (comma-separated):
> CommunityToolkit.Mvvm, ErrorOr, Refit, Serilog

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: Architecture & Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Application architecture:
  1. MVVM (Model-View-ViewModel)
  2. Clean Architecture (Domain, Application, Infrastructure, Presentation)
  3. Domain-Driven Design (DDD)
  4. Layered Architecture
  5. Microservices
  6. Other (specify)

> 1

❓ Navigation pattern:
  1. AppShell (Shell-based with flyout and tabs)
  2. NavigationPage (Stack-based navigation)

> 1

❓ Error handling pattern:
  1. ErrorOr (functional, no exceptions)
  2. Result pattern (functional result types)
  3. Either monad
  4. Traditional exceptions

> 1

❓ Domain operations naming:
  1. Verb-based (GetProducts, CreateOrder)
  2. CQRS (Queries/Commands)
  3. UseCase suffix (GetProductsUseCase)
  4. Custom (specify)

> 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4: Layer Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Include Domain layer?
> yes

  ❓ Domain operations naming pattern:
  > {Verb}{Entity}

  ❓ Prohibited suffixes (comma-separated):
  > UseCase, Engine, Handler, Processor

❓ Include Repository layer (database access)?
> yes

  ❓ Repository naming pattern:
  > I{Entity}Repository / {Entity}Repository

❓ Include Service layer (external systems)?
> yes

  ❓ Service naming pattern:
  > I{Purpose}Service / {Purpose}Service

❓ Include Presentation layer (UI)?
> yes

  ❓ Page naming pattern:
  > {Feature}Page

  ❓ ViewModel naming pattern:
  > {Feature}ViewModel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5: Testing Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Testing framework:
  1. xUnit
  2. NUnit
  3. MSTest

> 1

❓ Mocking library:
  1. NSubstitute
  2. Moq
  3. FakeItEasy

> 1

❓ Assertion library:
  1. FluentAssertions
  2. Shouldly
  3. xUnit assertions

> 1

❓ Testing strategy:
  1. Outside-In TDD (acceptance tests → unit tests)
  2. Inside-Out TDD (unit tests → integration tests)
  3. BDD (Gherkin scenarios → implementation)
  4. Standard (write tests after implementation)

> 1

❓ Coverage targets:
  Line coverage (%):
  > 80

  Branch coverage (%):
  > 75

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6: Quality Standards
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Code quality principles (select multiple):
  [x] SOLID principles
  [x] DRY (Don't Repeat Yourself)
  [x] YAGNI (You Aren't Gonna Need It)
  [ ] KISS (Keep It Simple, Stupid)
  [ ] Clean Code principles

❓ Required quality gates (select multiple):
  [x] All tests passing
  [x] Coverage targets met
  [x] No compiler warnings
  [ ] Static analysis passing
  [ ] Security scan passing
  [x] Code review completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7: Company Standards (Optional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Add company-specific patterns?
> yes

  ❓ Company name:
  > MyCompany

  ❓ Logging library:
  > Serilog

  ❓ Security library (optional):
  > MyCompany.Security

  ❓ Error tracking library (optional):
  > MyCompany.ErrorTracking

  ❓ Documentation links (comma-separated):
  > https://wiki.mycompany.com/architecture, https://wiki.mycompany.com/coding-standards

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 8: Agent Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Discover community agents for your stack?
> yes

  🔍 Discovering agents for: .NET MAUI, MVVM, ErrorOr...

  ✅ Found 15 relevant agents from 3 sources:
     - subagents.cc (6 agents)
     - github:wshobson/agents (5 agents)
     - github:VoltAgent/awesome-claude-code-subagents (4 agents)

  📊 RECOMMENDED AGENTS (score ≥ 80):

  ✅ Core Development (3 agents)
    [x] maui-domain-specialist      Score: 95  (subagents.cc)
    [x] dotnet-testing-specialist   Score: 88  (wshobson)
    [ ] csharp-code-reviewer        Score: 82  (VoltAgent)

  ✅ Quality & Testing (2 agents)
    [x] erroror-pattern-specialist  Score: 92  (wshobson)
    [ ] xaml-ui-tester              Score: 78  (VoltAgent)

  ✅ Infrastructure (1 agent)
    [ ] maui-deployment-specialist  Score: 85  (subagents.cc)

  ❓ Select agents:
    [A] Accept all recommended (score ≥ 85)
    [C] Customize selection
    [S] Skip agent discovery

  > A

  ✅ Selected 4 agents for template

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 9: Template Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 Generating template structure...

  ✓ Created manifest.json
  ✓ Created settings.json
  ✓ Generated CLAUDE.md with architectural guidance
  ✓ Generated README.md with usage instructions
  ✓ Created templates/ directory with 12 code templates:
    - domain/query-operation.cs.template
    - domain/command-operation.cs.template
    - repository/repository-interface.cs.template
    - repository/repository-implementation.cs.template
    - service/service-interface.cs.template
    - service/service-implementation.cs.template
    - presentation/page.xaml.template
    - presentation/page.xaml.cs.template
    - presentation/viewmodel.cs.template
    - testing/domain-test.cs.template
    - testing/repository-test.cs.template
    - testing/viewmodel-test.cs.template
  ✓ Downloaded and customized 4 agent definitions

🧪 Validating template...

  ✓ Template structure complete
  ✓ Placeholder substitution working
  ✓ Agents validated
  ✓ Sample project generated successfully

✅ Template Created: mycompany-mobile-app

📦 Template Location
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
installer/local/templates/mycompany-mobile-app/

Distribution Package:
  mycompany-mobile-app-v1.0.0.tar.gz (178 KB)

Usage:
  agentic-init mycompany-mobile-app

Next Steps:
  1. Test template: agentic-init mycompany-mobile-app --output /tmp/test-app
  2. Commit to git: git add installer/local/templates/mycompany-mobile-app/
  3. Distribute to team via git or package manager
```

---

## Technical Implementation

### Agent Discovery Architecture

```python
# installer/global/commands/lib/agent_discovery.py

from typing import List, Dict, Optional
from dataclasses import dataclass
import requests
import subprocess
import tempfile
import os

@dataclass
class AgentSource:
    name: str
    type: str  # "web", "github"
    url: str
    parser_class: str

class AgentDiscoveryEngine:
    """
    Multi-source agent discovery with intelligent matching
    """

    SOURCES = [
        AgentSource(
            name="subagents.cc",
            type="web",
            url="https://subagents.cc",
            parser_class="SubagentsCCParser"
        ),
        AgentSource(
            name="github:wshobson/agents",
            type="github",
            url="https://github.com/wshobson/agents.git",
            parser_class="WshobsonAgentsParser"
        ),
        AgentSource(
            name="github:VoltAgent/awesome-claude-code-subagents",
            type="github",
            url="https://github.com/VoltAgent/awesome-claude-code-subagents.git",
            parser_class="VoltAgentAwesomeParser"
        )
    ]

    def __init__(self, sources: Optional[List[str]] = None):
        if sources:
            self.sources = [s for s in self.SOURCES if s.name in sources]
        else:
            self.sources = self.SOURCES

    async def discover_all(self) -> List[AgentMetadata]:
        """Discover agents from all configured sources"""
        all_agents = []

        for source in self.sources:
            try:
                parser = self._get_parser(source)
                agents = await parser.discover()
                all_agents.extend(agents)
            except Exception as e:
                print(f"Warning: Failed to discover from {source.name}: {e}")

        return all_agents

    def _get_parser(self, source: AgentSource):
        """Get appropriate parser for agent source"""
        if source.parser_class == "SubagentsCCParser":
            return SubagentsCCParser(source.url)
        elif source.parser_class == "WshobsonAgentsParser":
            return WshobsonAgentsParser(source.url)
        elif source.parser_class == "VoltAgentAwesomeParser":
            return VoltAgentAwesomeParser(source.url)
        else:
            raise ValueError(f"Unknown parser: {source.parser_class}")

class SubagentsCCParser:
    """Parse agents from subagents.cc"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def discover(self) -> List[AgentMetadata]:
        """
        Scrape subagents.cc for agent listings
        1. Fetch /browse page
        2. Extract agent cards with metadata
        3. Fetch individual agent pages for full content
        """
        agents = []

        # Fetch browse page
        response = requests.get(f"{self.base_url}/browse")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse agent cards (implementation depends on actual HTML structure)
        # This is a placeholder - actual implementation would parse the DOM
        agent_cards = soup.find_all('div', class_='agent-card')

        for card in agent_cards:
            agent = self._parse_agent_card(card)
            if agent:
                agents.append(agent)

        return agents

    def _parse_agent_card(self, card) -> Optional[AgentMetadata]:
        """Parse individual agent card from browse page"""
        # Extract name, description, tags, download count
        # Fetch full content from agent detail page
        # Return AgentMetadata instance
        pass

class WshobsonAgentsParser:
    """Parse agents from wshobson/agents GitHub repository"""

    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    async def discover(self) -> List[AgentMetadata]:
        """
        Clone wshobson/agents repository and parse structure
        1. Clone to temp directory
        2. Parse .claude-plugin/marketplace.json
        3. Extract agents from plugins/*/agents/*.md
        """
        agents = []

        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone repository
            subprocess.run(
                ["git", "clone", "--depth", "1", self.repo_url, tmpdir],
                check=True
            )

            # Parse marketplace.json for plugin metadata
            marketplace_path = os.path.join(tmpdir, ".claude-plugin", "marketplace.json")
            with open(marketplace_path) as f:
                marketplace = json.load(f)

            # Iterate through plugins
            plugins_dir = os.path.join(tmpdir, "plugins")
            for plugin in os.listdir(plugins_dir):
                plugin_path = os.path.join(plugins_dir, plugin)
                agents_dir = os.path.join(plugin_path, "agents")

                if os.path.exists(agents_dir):
                    for agent_file in os.listdir(agents_dir):
                        if agent_file.endswith(".md"):
                            agent = self._parse_agent_file(
                                os.path.join(agents_dir, agent_file),
                                plugin
                            )
                            if agent:
                                agents.append(agent)

        return agents

    def _parse_agent_file(self, filepath: str, plugin: str) -> Optional[AgentMetadata]:
        """Parse agent markdown file"""
        # Extract YAML frontmatter
        # Parse markdown content
        # Return AgentMetadata instance
        pass

class VoltAgentAwesomeParser:
    """Parse agents from VoltAgent/awesome-claude-code-subagents"""

    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    async def discover(self) -> List[AgentMetadata]:
        """
        Clone VoltAgent/awesome-claude-code-subagents and parse
        1. Clone to temp directory
        2. Iterate through categories/* directories
        3. Parse agent markdown files with YAML frontmatter
        """
        agents = []

        with tempfile.TemporaryDirectory() as tmpdir:
            # Clone repository
            subprocess.run(
                ["git", "clone", "--depth", "1", self.repo_url, tmpdir],
                check=True
            )

            # Iterate through categories
            categories_dir = os.path.join(tmpdir, "categories")
            for category_dir in os.listdir(categories_dir):
                category_path = os.path.join(categories_dir, category_dir)

                if os.path.isdir(category_path):
                    for agent_file in os.listdir(category_path):
                        if agent_file.endswith(".md"):
                            agent = self._parse_agent_file(
                                os.path.join(category_path, agent_file),
                                category_dir
                            )
                            if agent:
                                agents.append(agent)

        return agents

    def _parse_agent_file(self, filepath: str, category: str) -> Optional[AgentMetadata]:
        """Parse agent markdown file with YAML frontmatter"""
        # Extract YAML frontmatter
        # Parse markdown content
        # Return AgentMetadata instance
        pass
```

### Pattern Extraction Engine

```python
# installer/global/commands/lib/pattern_extraction.py

from typing import List, Dict, Optional
import ast
import re

class PatternExtractor:
    """
    Analyze codebase and extract architectural patterns
    """

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.patterns = {}

    def extract_all(self) -> Dict[str, any]:
        """Extract all patterns from codebase"""
        return {
            "naming_conventions": self.extract_naming_conventions(),
            "layers": self.extract_layer_structure(),
            "error_handling": self.extract_error_handling_patterns(),
            "dependency_injection": self.extract_di_patterns(),
            "testing": self.extract_testing_patterns(),
        }

    def extract_naming_conventions(self) -> Dict[str, str]:
        """Detect naming patterns from existing code"""
        # Analyze class names, method names, file names
        # Infer patterns like {Verb}{Entity}, I{Entity}Repository, etc.
        pass

    def extract_layer_structure(self) -> List[Dict[str, any]]:
        """Detect architectural layers and their organization"""
        # Analyze directory structure
        # Identify layers (Domain, Repository, Service, Presentation)
        # Determine namespace patterns
        pass

    def extract_error_handling_patterns(self) -> Dict[str, str]:
        """Detect error handling approach"""
        # Look for ErrorOr, Result, Either usage
        # Analyze exception patterns
        # Determine dominant approach
        pass

    def extract_di_patterns(self) -> Dict[str, str]:
        """Detect dependency injection patterns"""
        # Analyze constructor injection usage
        # Identify DI container (Microsoft.Extensions, Autofac, etc.)
        # Determine lifetime patterns (transient, scoped, singleton)
        pass

    def extract_testing_patterns(self) -> Dict[str, any]:
        """Detect testing strategy and frameworks"""
        # Identify test framework (xUnit, NUnit, pytest, Jest)
        # Detect mocking library
        # Analyze test organization
        # Calculate coverage targets
        pass
```

---

## Benefits

### Time Savings

**Current State** (Manual Template Creation):
- Research template structure: 30-45 minutes
- Copy and customize global template: 45-60 minutes
- Create code templates: 60-90 minutes
- Find and integrate agents: 30-45 minutes
- Validate and test: 30-45 minutes
- **Total: 3.5-5 hours per template**

**With `/template-create`**:
- Run command: 5 minutes
- Review and customize generated template: 15-20 minutes
- Select agents from discovery: 10 minutes
- Validate: 5 minutes
- **Total: 35-40 minutes per template**

**Time Saved: 2.5-4 hours (75-80% reduction)**

### Quality Improvements

1. **Pattern Accuracy**: Automatically captures actual codebase patterns vs. manual interpretation
2. **Agent Discovery**: Access to 100+ community agents vs. manual search
3. **Consistency**: Generated templates follow established structure vs. ad-hoc customization
4. **Validation**: Automated template validation catches errors early

### Adoption Acceleration

1. **Lower Barrier**: Single command vs. multi-step manual process
2. **Confidence**: AI-generated templates reflect actual codebase accurately
3. **Discoverability**: Built-in agent discovery exposes valuable community resources
4. **Team Onboarding**: Greenfield template creation guides best practices

---

## Implementation Plan

### Phase 1: Pattern Extraction (Week 1-2)

- [ ] Implement technology stack detection
- [ ] Build architecture pattern analyzer
- [ ] Create code pattern extraction engine
- [ ] Develop naming convention inference
- [ ] Build layer structure detector

### Phase 2: Agent Discovery (Week 3-4)

- [ ] Implement subagents.cc scraper
- [ ] Build GitHub repository parsers (wshobson, VoltAgent)
- [ ] Create agent matching algorithm
- [ ] Develop interactive selection UI
- [ ] Build agent download and customization

### Phase 3: Template Generation (Week 5-6)

- [ ] Create manifest.json generator
- [ ] Build settings.json generator
- [ ] Implement CLAUDE.md generator
- [ ] Develop code template generator with placeholders
- [ ] Build validation and testing engine

### Phase 4: Interactive Greenfield Creator (Week 7-8)

- [ ] Design Q&A flow for `/template-init`
- [ ] Implement section-by-section prompting
- [ ] Build technology-specific question sets
- [ ] Integrate agent discovery into Q&A flow
- [ ] Create template generation from Q&A responses

### Phase 5: Testing & Documentation (Week 9-10)

- [ ] End-to-end testing with real codebases
- [ ] Create comprehensive documentation
- [ ] Build example templates
- [ ] User acceptance testing with dev teams
- [ ] Performance optimization

### Phase 6: Release (Week 11)

- [ ] Final QA and bug fixes
- [ ] Release notes and migration guide
- [ ] Community announcement
- [ ] Gather early feedback

---

## Success Metrics

### Quantitative

- **Template Creation Time**: <40 minutes (target: 75% reduction)
- **Pattern Accuracy**: >90% of patterns correctly identified
- **Agent Discovery**: 100+ agents indexed across sources
- **Adoption Rate**: 50% of teams create custom template within 1 month
- **User Satisfaction**: NPS score ≥ 8/10

### Qualitative

- Teams report "easy to get started with Agentecflow"
- Developers discover valuable agents they didn't know existed
- Custom templates accurately reflect team conventions
- Reduced support requests for template customization

---

## Risks & Mitigations

### Risk: Web scraping instability

**Impact**: High (agent discovery breaks if source sites change)

**Mitigation**:
- Implement robust error handling and fallbacks
- Cache discovered agents locally
- Provide manual agent import as backup
- Monitor sources for changes with automated checks

### Risk: Pattern extraction inaccuracy

**Impact**: Medium (incorrect patterns lead to poor templates)

**Mitigation**:
- Provide interactive review and correction
- Show confidence scores for detected patterns
- Allow manual override of all detected patterns
- Include validation step before template finalization

### Risk: Complexity overwhelms users

**Impact**: Medium (too many options, questions, agents)

**Mitigation**:
- Provide "quick mode" with sensible defaults
- Use progressive disclosure (show advanced options only if requested)
- Offer "accept recommendations" shortcuts
- Create video tutorials and examples

---

## Alternatives Considered

### Alternative 1: Manual template creation (current state)

**Pros**:
- Full control
- No new code to maintain
- Works today

**Cons**:
- Time-consuming (3-5 hours)
- Error-prone
- Limited pattern accuracy
- No agent discovery

**Decision**: Rejected - too much friction for adoption

### Alternative 2: Template marketplace

**Pros**:
- Community-contributed templates
- Browse and download pre-made templates
- Social validation (ratings, downloads)

**Cons**:
- Doesn't solve "capture existing codebase" problem
- Still requires customization
- Maintenance burden for marketplace infrastructure

**Decision**: Possible future enhancement, not core solution

### Alternative 3: AI code generation without templates

**Pros**:
- No template creation needed
- AI generates code directly

**Cons**:
- Loses pattern consistency
- No reusability across projects
- Harder to maintain conventions
- Doesn't leverage Agentecflow template system

**Decision**: Rejected - templates are core to Agentecflow methodology

---

## Open Questions

1. **Agent Curation**: Should we curate/rank agents, or show all discovered agents?
2. **Update Strategy**: How do we handle updates to discovered agents?
3. **Licensing**: How do we handle licensing for community agents?
4. **Private Agents**: Should we support private/company-internal agent repositories?
5. **Agent Versioning**: How do we handle versioning for downloaded agents?
6. **Offline Mode**: Should pattern extraction work without internet (no agent discovery)?

---

## Appendices

### Appendix A: Agent Source API Analysis

**subagents.cc**:
- No public API documented
- Web scraping required
- Rate limiting unknown
- Authentication: Not required

**github:wshobson/agents**:
- GitHub API available
- Rate limit: 5000 req/hour (authenticated)
- Authentication: GitHub personal access token (optional)
- Structure: Well-defined plugin architecture

**github:VoltAgent/awesome-claude-code-subagents**:
- GitHub API available
- Rate limit: 5000 req/hour (authenticated)
- Authentication: GitHub personal access token (optional)
- Structure: Category-based organization

### Appendix B: Example Generated Template

See separate file: `examples/generated-template-example.json`

### Appendix C: Competitive Analysis

**Comparison with similar tools**:
- **Yeoman**: Generator framework, but no AI pattern extraction
- **Cookiecutter**: Template engine, but no agent discovery
- **Scaffold**: Code generation, but technology-specific
- **Agentecflow /template-create**: ✅ AI pattern extraction + agent discovery + template generation

---

**End of Proposal**
