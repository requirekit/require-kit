# Template Creation Commands - Executive Summary

**Status**: Draft
**Created**: 2025-10-19
**Author**: AI Engineer
**Version**: 1.0.0

---

## Overview

Two powerful new commands to dramatically simplify Agentecflow adoption for both **existing codebases** and **greenfield projects**:

1. **`/template-create`** - Capture Existing Codebase Patterns
2. **`/template-init`** - Interactive Greenfield Template Creation

Both commands feature **intelligent agent discovery** from online repositories (subagents.cc, GitHub collections) and **automatic pattern extraction** to capture your team's architectural conventions.

---

## `/template-create` - Capture Existing Codebase Patterns

### Purpose
Automatically analyze your existing codebase and generate a custom local template

### Key Features

**AI Pattern Extraction**:
- Detects naming conventions, architectural layers, error handling patterns
- Analyzes directory structure and code organization
- Extracts dependency injection patterns and testing strategies

**Intelligent Agent Discovery**:
Discovers 100+ community agents from:
- **subagents.cc** - Curated marketplace with ratings and downloads
- **github:wshobson/agents** - Plugin architecture with 63 focused plugins
- **github:VoltAgent/awesome-claude-code-subagents** - Awesome list with 116 agents

**Smart Matching**:
Scores agents 0-100 based on:
- Technology Stack Match (40%)
- Architecture Pattern Match (30%)
- Tool Compatibility (20%)
- Community Validation (10%)

**8-Phase Workflow**:
```
Phase 1: Technology Stack Detection
Phase 2: Architecture Pattern Analysis
Phase 3: Code Pattern Extraction
Phase 4: Agent Discovery
Phase 5: Agent Selection (Interactive)
Phase 6: Template Generation
Phase 7: Validation & Testing
Phase 8: Installation & Distribution
```

**Time Savings**: 75-80% reduction (from 3-5 hours to 35-40 minutes)

### Example Usage

```bash
# Analyze current project and create template
cd /path/to/your/react-app
/template-create "mycompany-react" --discover-agents

# Output: Complete template with detected patterns + 5 relevant agents
# Location: installer/local/templates/mycompany-react/
# Package: mycompany-react-v1.0.0.tar.gz
```

### Pattern Detection Examples

**React/TypeScript**:
```typescript
// Detected from: src/components/ProductList.tsx
export const ProductList: React.FC<ProductListProps> = ({ products, onSelect }) => {
  return (
    <div className="product-list">
      {products.map(p => <ProductCard key={p.id} product={p} onClick={() => onSelect(p.id)} />)}
    </div>
  );
};

// Generated template: templates/component/functional-component.tsx.template
export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({ {{PropNames}} }) => {
  return (
    <div className="{{className}}">
      {{ComponentBody}}
    </div>
  );
};
```

**.NET MAUI**:
```csharp
// Detected from: src/Domain/Products/GetProducts.cs
public class GetProducts
{
    private readonly IProductRepository _repository;

    public async Task<ErrorOr<List<Product>>> ExecuteAsync()
    {
        return await _repository.GetAllAsync();
    }
}

// Generated template: templates/domain/query-operation.cs.template
public class {{OperationName}}
{
    private readonly I{{Entity}}Repository _repository;

    public async Task<ErrorOr<{{ReturnType}}>> ExecuteAsync()
    {
        return await _repository.{{RepositoryMethod}}();
    }
}
```

---

## `/template-init` - Interactive Greenfield Template Creation

### Purpose
Guided Q&A session to create custom templates for greenfield projects

### Key Features

**9 Interactive Sections**:
1. Basic Information (name, description, version)
2. Technology Stack (framework, libraries, versions)
3. Architecture & Patterns (MVVM, Clean Architecture, DDD)
4. Layer Structure (Domain, Repository, Service, Presentation)
5. Testing Strategy (framework, approach, coverage targets)
6. Quality Standards (SOLID, DRY, YAGNI, quality gates)
7. Company Standards (logging, security, documentation)
8. Agent Discovery (automatic matching and selection)
9. Template Generation (validation, packaging, distribution)

**Technology-Aware**:
Pre-configured question sets for:
- React (TypeScript, Vite, Tailwind)
- Python (FastAPI, pytest, SQLAlchemy)
- .NET MAUI (C#, XAML, MVVM)
- TypeScript API (NestJS, Domain-Driven Design)
- .NET Microservice (FastEndpoints, Clean Architecture)

**Agent Integration**:
Built-in agent discovery and selection during creation

**Quick Mode**:
Sensible defaults with minimal prompts for rapid setup

**Flexible**:
Start from scratch or customize existing templates

### Example Usage

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

### Interactive Q&A Flow

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2: Technology Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Primary technology:
  1. React (TypeScript, Vite, Tailwind)
  2. Python (FastAPI, pytest, SQLAlchemy)
  3. .NET MAUI (C#, XAML, MVVM)
  4. TypeScript API (NestJS, Domain-Driven Design)
  5. .NET Microservice (FastEndpoints, Clean Architecture)

> 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: Architecture & Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Application architecture:
  1. MVVM (Model-View-ViewModel)
  2. Clean Architecture (Domain, Application, Infrastructure)
  3. Domain-Driven Design (DDD)

> 1

❓ Domain operations naming:
  1. Verb-based (GetProducts, CreateOrder)
  2. CQRS (Queries/Commands)
  3. Custom (specify)

> 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 8: Agent Discovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Discovering agents for: .NET MAUI, MVVM, ErrorOr...

✅ Found 15 relevant agents from 3 sources

📊 RECOMMENDED AGENTS (score ≥ 80):

✅ Core Development (3 agents)
  [x] maui-domain-specialist      Score: 95  (subagents.cc)
  [x] dotnet-testing-specialist   Score: 88  (wshobson)
  [ ] csharp-code-reviewer        Score: 82  (VoltAgent)

❓ Select agents:
  [A] Accept all recommended (score ≥ 85)
  [C] Customize selection
  [S] Skip agent discovery

> A
```

---

## Agent Discovery System

### Agent Matching Algorithm

Discovered agents are scored 0-100 based on:

1. **Technology Stack Match (40%)**
   - Exact match: +40 points (python → python-specialist)
   - Partial match: +20 points (react → frontend)

2. **Architecture Pattern Match (30%)**
   - Pattern keywords in agent description
   - DDD, Clean Architecture, CQRS, MVVM, etc.

3. **Tool Compatibility (20%)**
   - Required MCP tools available
   - Integration with detected libraries

4. **Community Validation (10%)**
   - Download count, favorites, stars
   - Recency of updates

**Threshold**: Agents with score ≥ 60 are considered relevant.

### Interactive Selection UI

```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 AGENT DISCOVERY RESULTS                                  │
│ Technology: React 18 + TypeScript 5 + Vite 4                │
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
    Expert in React state management patterns
    Tools: Read, Write, Edit, Bash

[x] typescript-domain-modeler                 Score: 88
    Source: github:wshobson/agents
    TypeScript domain modeling with Result patterns
    Tools: Read, Write, Edit, Search

[x] react-testing-specialist                  Score: 85
    Source: github:VoltAgent/awesome-claude-code-subagents
    React Testing Library + Vitest expert
    Tools: Read, Write, Bash, Grep

Options:
  [A] Accept all recommended (score ≥ 85) - 3 agents
  [C] Customize selection
  [S] Skip agent discovery
  [P] Preview agent details
```

### Agent Discovery Sources

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

---

## Generated Template Structure

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

---

## Use Cases

### Use Case 1: Existing Codebase → Template

**Scenario**: You have a React app with custom patterns and want to create a reusable template.

```bash
# You have a React app with custom patterns
cd /my-react-app
/template-create "mycompany-react"

# Result: Template with your exact patterns + relevant agents
# Time: 35-40 minutes (vs 3-5 hours manually)
```

**Output**:
```
✅ Template Created: mycompany-react

Technology: React 18 + TypeScript 5 + Vite 4
Patterns: Functional components, Custom hooks, Context API
Agents: 3 selected
  - react-state-specialist (score: 95)
  - typescript-domain-modeler (score: 88)
  - react-testing-specialist (score: 85)

Location: installer/local/templates/mycompany-react/
Package: mycompany-react-v1.0.0.tar.gz (145 KB)
```

### Use Case 2: Greenfield → Template

**Scenario**: Starting a new .NET MAUI app and want to establish patterns upfront.

```bash
# Starting a new .NET MAUI app
/template-init --technology maui

# Q&A guides you through architecture decisions
# Discovers and selects MAUI-specific agents
# Creates ready-to-use template
```

**Output**:
```
✅ Template Created: mycompany-mobile-app

Technology: .NET 8 MAUI + MVVM + ErrorOr
Architecture: MVVM with AppShell navigation
Agents: 4 selected
  - maui-domain-specialist (score: 95)
  - dotnet-testing-specialist (score: 88)
  - erroror-pattern-specialist (score: 92)
  - maui-deployment-specialist (score: 85)

Location: installer/local/templates/mycompany-mobile-app/
```

### Use Case 3: Team Distribution

**Scenario**: Share template with team via git.

```bash
# Share template via git
git add installer/local/templates/mycompany-react/
git commit -m "feat: Add company React template v1.0.0"
git tag mycompany-react-v1.0.0
git push origin main --tags

# Team members pull and use
git pull origin main
agentic-init mycompany-react
```

### Use Case 4: Template Versioning

**Scenario**: Update template with new patterns and agents.

```bash
# Update existing template
/template-create "mycompany-react"

# Prompt:
# ⚠️  Template 'mycompany-react' already exists
# Options:
#   [M] Merge (preserve customizations, update patterns)
#   [O] Overwrite (lose customizations)
#   [C] Cancel

> M

# Result: Template updated to v1.1.0 with new patterns
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

### Phase 1: Pattern Extraction (Weeks 1-2)
- [ ] Implement technology stack detection
- [ ] Build architecture pattern analyzer
- [ ] Create code pattern extraction engine
- [ ] Develop naming convention inference
- [ ] Build layer structure detector

### Phase 2: Agent Discovery (Weeks 3-4)
- [ ] Implement subagents.cc scraper
- [ ] Build GitHub repository parsers (wshobson, VoltAgent)
- [ ] Create agent matching algorithm
- [ ] Develop interactive selection UI
- [ ] Build agent download and customization

### Phase 3: Template Generation (Weeks 5-6)
- [ ] Create manifest.json generator
- [ ] Build settings.json generator
- [ ] Implement CLAUDE.md generator
- [ ] Develop code template generator with placeholders
- [ ] Build validation and testing engine

### Phase 4: Interactive Greenfield Creator (Weeks 7-8)
- [ ] Design Q&A flow for `/template-init`
- [ ] Implement section-by-section prompting
- [ ] Build technology-specific question sets
- [ ] Integrate agent discovery into Q&A flow
- [ ] Create template generation from Q&A responses

### Phase 5: Testing & Documentation (Weeks 9-10)
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

**Total Timeline**: 11 weeks

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

## Key Innovations

### 1. Multi-Source Agent Discovery
First system to aggregate agents from multiple community sources (subagents.cc, GitHub collections) with intelligent matching.

### 2. AI Pattern Extraction
Automatically detects architectural patterns from existing codebases without manual configuration.

### 3. Interactive Template Creation
Guided Q&A flow makes greenfield template creation accessible to all developers.

### 4. Template Distribution
Built-in support for git-based distribution and versioning.

---

## Next Steps

1. **Review the full proposal**: [Template Creation Commands Proposal](./template-creation-commands.md)
2. **Explore the workflow guide**: [Template Creation Workflow Guide](../guides/template-creation-workflow.md)
3. **Decide on implementation**: Prioritize phases, allocate resources
4. **Prototype agent discovery**: Start with one source (subagents.cc) as MVP
5. **Gather feedback**: Share with early adopters for validation

---

## Related Documentation

- [Template Creation Commands - Full Proposal](./template-creation-commands.md)
- [Template Creation Workflow Guide](../guides/template-creation-workflow.md)
- [Creating Local Templates](../guides/creating-local-templates.md)
- [MAUI Template Selection](../guides/maui-template-selection.md)

---

**This dramatically lowers the barrier to Agentecflow adoption while leveraging the community's agent ecosystem!**

---

**Last Updated**: 2025-10-19
**Version**: 1.0.0
**Maintained By**: AI Engineer Team
