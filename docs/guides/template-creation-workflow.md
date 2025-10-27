# Template Creation Workflow

**Purpose**: Complete guide to creating custom templates for existing codebases and greenfield projects using AI-powered pattern extraction and agent discovery.

**Learn template creation in**:
- **2 minutes**: Quick Start
- **10 minutes**: Core Concepts
- **30 minutes**: Complete Reference

---

## Quick Start (2 minutes)

### Create Template from Existing Codebase

```bash
# Analyze current project and create template
cd /path/to/your/project
/template-create "mycompany-react"

# Review generated template
ls -la installer/local/templates/mycompany-react/

# Use template for new projects
agentic-init mycompany-react
```

### Create Template for Greenfield Project

```bash
# Start interactive template creation
/template-init

# Follow Q&A prompts for:
# - Technology stack selection
# - Architecture and patterns
# - Testing strategy
# - Agent discovery

# Use generated template
agentic-init mycompany-mobile-app
```

**That's it!** Custom templates created in minutes, not hours.

**Learn More**: See "Core Concepts" below for pattern extraction and agent discovery.

---

## Core Concepts (10 minutes)

### Two Approaches to Template Creation

**1. `/template-create` - Capture Existing Patterns**

Use when you have an **existing codebase** and want to:
- Capture architectural patterns automatically
- Extract naming conventions and layer structure
- Discover community agents matching your stack
- Generate reusable template for similar projects

**2. `/template-init` - Design from Scratch**

Use when starting a **greenfield project** and want to:
- Choose technology stack and frameworks
- Define architecture and patterns upfront
- Select testing strategy and quality standards
- Discover and integrate relevant agents

### 8-Phase Pattern Extraction

The `/template-create` command follows this workflow:

```
Phase 1: Technology Stack Detection
└─ Scan files, detect frameworks, identify versions

Phase 2: Architecture Pattern Analysis
└─ Analyze layers, patterns, naming conventions

Phase 3: Code Pattern Extraction
└─ Extract class templates, DI patterns, testing

Phase 4: Agent Discovery
└─ Fetch agents from online sources, match to stack

Phase 5: Agent Selection
└─ Interactive selection with preview and filtering

Phase 6: Template Generation
└─ Create manifest, settings, CLAUDE.md, templates

Phase 7: Validation & Testing
└─ Validate structure, test placeholders, verify agents

Phase 8: Installation & Distribution
└─ Install locally, create package, output usage
```

### Agent Discovery Sources

The system discovers agents from three primary sources:

**1. subagents.cc**
- Community-curated agent marketplace
- 100+ specialized agents with ratings
- Category-based organization
- Download statistics for popularity

**2. github:wshobson/agents**
- Plugin-based agent architecture
- 63 focused plugins across 23 categories
- Comprehensive agent specifications
- Active maintenance and updates

**3. github:VoltAgent/awesome-claude-code-subagents**
- Curated awesome list format
- 116 agents in 10 categories
- Quality-vetted agent definitions
- Community contributions

### Agent Matching Algorithm

Discovered agents are scored 0-100 based on:

1. **Technology Stack (40%)**: Exact or partial tech match
2. **Architecture Patterns (30%)**: Pattern keywords in description
3. **Tool Compatibility (20%)**: Required MCP tools available
4. **Community Validation (10%)**: Downloads, favorites, recency

**Threshold**: Agents with score ≥ 60 are considered relevant.

### Template Structure

Generated templates follow this structure:

```
installer/local/templates/mycompany-stack/
├── manifest.json               # Template metadata and config
├── settings.json               # Naming conventions, layers
├── CLAUDE.md                   # Architectural guidance
├── README.md                   # Human-readable docs
├── templates/                  # Code generation templates
│   ├── domain/*.template      # Business logic templates
│   ├── repository/*.template  # Data access templates
│   ├── service/*.template     # External integration templates
│   ├── presentation/*.template # UI templates
│   └── testing/*.template     # Test templates
└── agents/                     # Stack-specific AI agents
    ├── domain-specialist.md
    ├── testing-specialist.md
    └── architecture-reviewer.md
```

**Learn More**: See "Complete Reference" below for detailed examples and customization.

---

## Complete Reference (30+ minutes)

### `/template-create` Command Reference

#### Usage

```bash
/template-create <template-name> [options]
```

#### Options

```
--scan-depth <quick|full>
  Quick: Scan package files and common directories only
  Full: Deep scan entire project (default)

--interactive
  Enable interactive mode with pattern review

--scan-paths <paths>
  Comma-separated list of paths to scan
  Example: --scan-paths "src/domain,src/services"

--discover-agents
  Enable agent discovery (default: true)

--agent-sources <sources>
  Comma-separated list of agent sources
  Options: subagents.cc, github:wshobson/agents, github:VoltAgent/awesome-claude-code-subagents
  Default: All sources

--skip-validation
  Skip template validation step (advanced)

--output-package
  Create distribution package (.tar.gz) (default: true)
```

#### Examples

**Example 1: Quick Template from React Project**

```bash
cd /path/to/react-project
/template-create "acme-react" --scan-depth quick

# Output:
# ✅ Template Created: acme-react
# Technology: React 18 + TypeScript 5 + Vite 4
# Patterns: Functional components, Custom hooks, Context API
# Agents: 3 selected (react-state-specialist, typescript-domain-modeler, react-testing-specialist)
# Location: installer/local/templates/acme-react/
```

**Example 2: Interactive Creation with Customization**

```bash
cd /path/to/maui-app
/template-create "mycompany-maui" --interactive

# Interactive prompts:
# ❓ Detected domain pattern: {Verb}{Entity}
#    Looks correct? [Y/n] y
#
# ❓ Detected repository pattern: I{Entity}Repository / {Entity}Repository
#    Looks correct? [Y/n] y
#
# ❓ Detected error handling: ErrorOr<T>
#    Looks correct? [Y/n] y
#
# [Agent Discovery Phase]
# ✅ Found 15 agents matching .NET MAUI + MVVM + ErrorOr
# ❓ Select agents:
#    [A] Accept all recommended (score ≥ 85)
#    [C] Customize selection
# > A
```

**Example 3: Specific Directories Only**

```bash
cd /path/to/monorepo
/template-create "backend-api" --scan-paths "packages/api,packages/domain"

# Scans only specified paths, ignores rest of monorepo
```

**Example 4: Custom Agent Sources**

```bash
/template-create "python-api" --agent-sources "subagents.cc,github:wshobson/agents"

# Discovers agents from subagents.cc and wshobson/agents only
# Skips VoltAgent/awesome-claude-code-subagents
```

#### Pattern Detection Examples

**React Component Pattern**:

```typescript
// Detected from: src/components/ProductList.tsx
export interface ProductListProps {
  products: Product[];
  onSelect: (id: string) => void;
}

export const ProductList: React.FC<ProductListProps> = ({ products, onSelect }) => {
  return (
    <div className="product-list">
      {products.map(p => <ProductCard key={p.id} product={p} onClick={() => onSelect(p.id)} />)}
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

**.NET MAUI Domain Operation**:

```csharp
// Detected from: src/Domain/Products/GetProducts.cs
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

**Python FastAPI Endpoint**:

```python
# Detected from: src/api/products.py
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

#### Agent Discovery UI

```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 AGENT DISCOVERY RESULTS                                  │
│ Technology: React 18 + TypeScript 5 + Vite 4                │
│ Patterns: Functional components, Custom hooks, Context API  │
└─────────────────────────────────────────────────────────────┘

📊 Found 23 agents from 3 sources:
   - subagents.cc: 10 agents
   - github:wshobson/agents: 8 agents
   - github:VoltAgent/awesome-claude-code-subagents: 5 agents

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CORE DEVELOPMENT (7 agents)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[x] react-state-specialist                    Score: 95
    Source: subagents.cc (248 downloads)
    Expert in React state management patterns (Context, Zustand, Redux)
    Tools: Read, Write, Edit, Bash

[x] typescript-domain-modeler                 Score: 88
    Source: github:wshobson/agents
    TypeScript domain modeling with Result patterns
    Tools: Read, Write, Edit, Search

[x] react-testing-specialist                  Score: 85
    Source: github:VoltAgent/awesome-claude-code-subagents
    React Testing Library + Vitest expert
    Tools: Read, Write, Bash, Grep

[ ] frontend-performance                      Score: 72
    Source: subagents.cc (95 downloads)
    Performance optimization for React apps
    Tools: Read, Bash, Analyze

[ ] accessibility-auditor                     Score: 68
    Source: github:VoltAgent/awesome-claude-code-subagents
    WCAG 2.1 AA compliance auditing
    Tools: Read, WebFetch, Analyze

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 INFRASTRUCTURE (4 agents)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] vite-bundler-specialist                   Score: 90
    Source: github:wshobson/agents
    Vite configuration and optimization expert
    Tools: Read, Write, Edit, Bash

[ ] docker-containerization                   Score: 65
    Source: github:VoltAgent/awesome-claude-code-subagents
    Containerization for frontend apps
    Tools: Read, Write, Bash

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 QUALITY & TESTING (5 agents)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[x] playwright-e2e-specialist                 Score: 92
    Source: subagents.cc (312 downloads)
    End-to-end testing with Playwright
    Tools: Read, Write, Bash, Playwright

[ ] vitest-unit-tester                        Score: 87
    Source: github:VoltAgent/awesome-claude-code-subagents
    Vitest unit testing patterns
    Tools: Read, Write, Bash

[ ] code-coverage-enforcer                    Score: 70
    Source: github:wshobson/agents
    Enforce coverage thresholds
    Tools: Read, Bash, Analyze

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
  [A] Accept all recommended (score ≥ 85) - 5 agents
  [C] Customize selection (toggle individual agents)
  [S] Skip agent discovery
  [P] Preview agent details (enter number to preview)
  [F] Filter by score threshold (current: 85)

Your choice: _
```

---

### `/template-init` Command Reference

#### Usage

```bash
/template-init [options]
```

#### Options

```
--technology <tech>
  Pre-select technology stack
  Options: react, python, maui, typescript-api, dotnet-microservice

--from <template>
  Start from existing template
  Example: --from maui-appshell

--discover-agents
  Enable agent discovery (default: true)

--quick
  Quick mode with sensible defaults, minimal prompts

--output <path>
  Custom output path for template
  Default: installer/local/templates/
```

#### Interactive Q&A Sections

The `/template-init` command guides you through 9 sections:

**Section 1: Basic Information**
- Template name
- Description
- Version
- Author

**Section 2: Technology Stack**
- Primary technology (React, Python, .NET MAUI, etc.)
- Framework versions
- Additional libraries

**Section 3: Architecture & Patterns**
- Application architecture (MVVM, Clean Architecture, DDD)
- Navigation pattern
- Error handling pattern
- Domain operations naming

**Section 4: Layer Structure**
- Domain layer configuration
- Repository layer configuration
- Service layer configuration
- Presentation layer configuration

**Section 5: Testing Strategy**
- Testing framework
- Mocking library
- Assertion library
- Testing approach (TDD, BDD, etc.)
- Coverage targets

**Section 6: Quality Standards**
- Code quality principles (SOLID, DRY, YAGNI)
- Required quality gates
- Recommended quality gates

**Section 7: Company Standards (Optional)**
- Company name
- Logging library
- Security library
- Error tracking library
- Documentation links

**Section 8: Agent Discovery**
- Discover community agents
- Review and select agents
- Customize agent configurations

**Section 9: Template Generation**
- Generate template structure
- Validate template
- Create distribution package
- Output usage instructions

#### Examples

**Example 1: Quick Mode with Defaults**

```bash
/template-init --technology react --quick

# Uses sensible defaults for React:
# - React 18 + TypeScript + Vite
# - Functional components
# - Vitest + React Testing Library
# - 80% line coverage, 75% branch coverage
# - SOLID principles
# - Discovers and auto-selects agents (score ≥ 85)
```

**Example 2: Full Interactive Session**

```bash
/template-init

# Guides through all 9 sections with detailed prompts
# Allows full customization of every option
# Includes agent discovery and selection
```

**Example 3: Start from Existing Template**

```bash
/template-init --from maui-appshell

# Starts with maui-appshell as base
# Prompts for customizations
# Inherits structure but allows modifications
```

---

## Advanced Topics

### Custom Agent Sources

You can add custom agent sources:

```bash
# Add private GitHub repository
/template-create "myapp" --agent-sources "github:mycompany/private-agents"

# Add local agent directory
/template-create "myapp" --agent-sources "file://~/.agentecflow/custom-agents"
```

### Template Customization After Generation

Generated templates can be customized manually:

```bash
# Edit manifest.json
vim installer/local/templates/mycompany-react/manifest.json

# Customize code templates
vim installer/local/templates/mycompany-react/templates/component/functional-component.tsx.template

# Add custom agents
vim installer/local/templates/mycompany-react/agents/custom-specialist.md
```

### Agent Metadata Customization

Downloaded agents can be customized before installation:

```json
// agents/react-state-specialist.md frontmatter
---
name: react-state-specialist
description: Expert in React state management patterns
customized_by: MyCompany
custom_tools:
  - mycompany-analytics
custom_constraints:
  - "ALWAYS use MyCompany logging wrapper"
  - "NEVER use Zustand (company standard is Context API)"
---

[Original agent content...]

## MyCompany Customizations

### Required Patterns
- Use CompanyContextProvider wrapper
- Integrate with MyCompany analytics
- Follow MyCompany state management guidelines
```

### Template Versioning

Templates support semantic versioning and changelogs:

```json
// manifest.json
{
  "version": "1.2.3",
  "changelog": [
    {
      "version": "1.2.3",
      "date": "2025-10-19",
      "changes": [
        "Updated TypeScript to 5.3",
        "Added vitest-ui integration",
        "Fixed component template placeholder bug"
      ]
    },
    {
      "version": "1.2.0",
      "date": "2025-10-15",
      "changes": [
        "Added custom hook template",
        "Integrated react-query patterns",
        "Updated agent: react-testing-specialist to v2.1"
      ]
    }
  ]
}
```

### Distribution Strategies

**Git Repository** (Recommended):
```bash
# Commit template to version control
git add installer/local/templates/mycompany-react/
git commit -m "feat: Add MyCompany React template v1.0.0"
git tag mycompany-react-v1.0.0
git push origin main --tags

# Team members pull updates
git pull origin main
```

**Package Distribution**:
```bash
# Create tarball
cd installer/local/templates/
tar -czf mycompany-react-v1.0.0.tar.gz mycompany-react/

# Distribute via internal package manager or network share
cp mycompany-react-v1.0.0.tar.gz /shared/templates/

# Team members extract
tar -xzf /shared/templates/mycompany-react-v1.0.0.tar.gz -C installer/local/templates/
```

**Template Registry** (Enterprise):
```bash
# Publish to internal registry
agentic template publish installer/local/templates/mycompany-react

# Team members install
agentic template install mycompany-react@1.0.0

# Update to latest
agentic template update mycompany-react
```

---

## FAQ

### Q: Can I create templates for monorepos?

**A**: Yes, use `--scan-paths` to target specific packages:

```bash
cd /path/to/monorepo
/template-create "backend-api" --scan-paths "packages/api,packages/domain"
```

### Q: How do I update an existing template?

**A**: Re-run `/template-create` with the same name:

```bash
/template-create "mycompany-react"

# Prompt:
# ⚠️  Template 'mycompany-react' already exists
# Options:
#   [O] Overwrite (lose customizations)
#   [M] Merge (preserve customizations, update patterns)
#   [C] Cancel
```

### Q: Can I share templates between teams?

**A**: Yes, use git or package distribution:

```bash
# Team A creates template
git add installer/local/templates/shared-react/
git push origin main

# Team B pulls template
git pull origin main

# Both teams use template
agentic-init shared-react
```

### Q: How do I remove a downloaded agent?

**A**: Delete agent file from template:

```bash
rm installer/local/templates/mycompany-react/agents/unwanted-agent.md

# Update manifest.json
vim installer/local/templates/mycompany-react/manifest.json
# Remove agent from "agents" array
```

### Q: Can I discover agents without creating a template?

**A**: Not currently, but you can explore online sources:
- Browse: https://subagents.cc
- Browse: https://github.com/wshobson/agents
- Browse: https://github.com/VoltAgent/awesome-claude-code-subagents

Future enhancement: `/agent-discover` command for standalone agent discovery.

### Q: What if pattern detection is inaccurate?

**A**: Use `--interactive` mode to review and correct:

```bash
/template-create "myapp" --interactive

# Interactive prompts:
# ❓ Detected domain pattern: {Verb}{Entity}
#    Looks correct? [Y/n] n
#
# ❓ Enter correct pattern:
# > {Entity}{Action}
```

---

## Related Documentation

- [Creating Local Templates](./creating-local-templates.md) - Manual template customization guide
- [MAUI Template Selection](./maui-template-selection.md) - Choosing between MAUI templates
- [Domain Layer Pattern](../patterns/domain-layer-pattern.md) - Domain operation patterns
- [Template Creation Commands Proposal](../proposals/template-creation-commands.md) - Full technical proposal

---

**Last Updated**: 2025-10-19
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
