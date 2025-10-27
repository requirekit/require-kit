# AI Engineer Quick Reference Guide - v2.0

## 🚀 Quick Start Commands

### Installation
```bash
# Install globally (one-time)
curl -sSL https://raw.githubusercontent.com/appmilla/agentic-flow/main/installer/scripts/install.sh | bash

# Initialize projects with enterprise capabilities
agentecflow init react               # React with TypeScript, Vite, Playwright
agentecflow init python              # Python with FastAPI, pytest, LangGraph
agentecflow init dotnet-microservice # .NET microservices with FastEndpoints
agentecflow init maui                # .NET MAUI mobile with MVVM
agentecflow init typescript-api      # NestJS TypeScript backend API
agentecflow init fullstack           # React + Python full-stack
agentecflow init default             # Language-agnostic template
```

## 🏢 Enterprise Features (New in v2.0)

### Epic → Feature → Task Hierarchy
- **Epic Management**: Strategic planning with PM tool integration
- **Feature Management**: Bridge between strategy and implementation
- **Task Management**: Developer-focused implementation workflow
- **Portfolio Dashboard**: Executive oversight and metrics

### PM Tool Integration
- **Jira**: Automatic epic/feature/task creation and sync
- **Linear**: Initiative and issue management
- **GitHub Projects**: Milestone and issue tracking
- **Azure DevOps**: Work item hierarchy management

### Agentecflow Stages
- **Stage 1**: Requirements & Planning → Epic Creation
- **Stage 2**: Feature & Task Definition → Automatic Generation
- **Stage 3**: Engineering & Implementation → Quality Gates
- **Stage 4**: Deployment & QA → Progress Rollup

## 📚 Stack Features Summary

### React Stack
**Production Patterns Included:**
- ✅ Error boundaries for resilient error handling
- ✅ SSE hooks for real-time streaming
- ✅ Performance optimization (memoization, debouncing)
- ✅ Accessibility patterns (WCAG 2.1 AA)
- ✅ Advanced testing (visual regression, performance)
- ✅ Security patterns (input sanitization)

**Key Files:**
- `CLAUDE.md` - Complete development context
- `PATTERNS.md` - Production-tested patterns
- Templates for hooks, components, services

### Python Stack
**Production Patterns Included:**
- ✅ Surgical coding philosophy (minimal changes)
- ✅ Factory pattern throughout
- ✅ LangGraph workflow orchestration
- ✅ SSE streaming with completion events
- ✅ MCP server integration
- ✅ Regression test markers

**Key Files:**
- `CLAUDE.md` - Surgical coding prompts
- Templates for endpoints, agents, workflows
- Comprehensive test templates

### .NET Microservice Stack
**Production Patterns Included:**
- ✅ FastEndpoints with REPR pattern
- ✅ Either monad for functional error handling
- ✅ OpenTelemetry observability
- ✅ Domain-driven design structure
- ✅ Health check endpoints
- ✅ Integration testing focus

**Project Structure:**
```
ServiceName.API/
├── Domain/         # Entities and errors
├── Endpoints/      # FastEndpoints
├── Services/       # Business logic
├── Infrastructure/ # Cross-cutting concerns
└── Validators/     # FluentValidation

ServiceName.Tests/
├── Unit/          # Service tests
└── Integration/   # API tests
```

### .NET MAUI Stack
**Production Patterns Included:**
- ✅ MVVM with UseCase pattern
- ✅ Functional error handling (Either monad)
- ✅ Outside-In TDD approach
- ✅ Cache-aside pattern
- ✅ Loading scope pattern
- ✅ Navigation service

**Project Structure:**
```
AppName/
├── Core/         # Models and interfaces
├── UseCases/     # Business logic
├── Services/     # Infrastructure
├── ViewModels/   # MVVM
├── Views/        # XAML pages
└── Tests/        # Integration tests
```

### TypeScript API Stack (New)
**Production Patterns Included:**
- ✅ NestJS with modular architecture
- ✅ Result patterns for error handling
- ✅ Domain modeling with TypeScript
- ✅ Comprehensive testing with Jest
- ✅ OpenAPI documentation generation
- ✅ Dependency injection containers

**Project Structure:**
```
src/
├── modules/        # Feature modules
├── common/         # Shared utilities
├── database/       # Database configuration
├── auth/          # Authentication module
└── config/        # Application configuration

test/
├── unit/          # Unit tests
├── integration/   # API tests
└── e2e/          # End-to-end tests
```

### Full Stack Template (New)
**Production Patterns Included:**
- ✅ React frontend + Python backend
- ✅ Shared TypeScript types
- ✅ API-first design with OpenAPI
- ✅ Full-stack testing strategy
- ✅ Monorepo structure with workspaces
- ✅ Consistent error handling patterns

**Project Structure:**
```
frontend/          # React application
├── src/
├── tests/
└── package.json

backend/           # Python API
├── app/
├── tests/
└── requirements.txt

shared/           # Shared types and utilities
└── types/
```

## 🎯 Quality Gates

### All Stacks Include:
| Gate | Threshold | Enforcement |
|------|-----------|-------------|
| Code Coverage | 80-90% | Required |
| Complexity | ≤10 | Required |
| Test Pass Rate | 100% | Required |
| Performance | Stack-specific | Warning |

### Stack-Specific Requirements:

**React:**
- Render time <100ms
- Accessibility score 100%
- Bundle size <500KB

**Python:**
- Max 3 files per feature
- All endpoints use Pydantic
- SSE streams send completion

**.NET Microservice:**
- P95 response <200ms
- All operations return Either
- OpenTelemetry required

**.NET MAUI:**
- Page load <500ms
- ViewModels contain no logic
- Integration tests required

## 🛠 Enterprise Development Workflow

### Stage 1: Requirements & Planning
```bash
# In Claude Code
/gather-requirements    # Interactive Q&A session
/formalize-ears        # Convert to EARS notation
/epic-create           # Create epic with PM tool integration
```

### Stage 2: Feature & Task Definition
```bash
/feature-create        # Create feature with epic linkage
/generate-bdd          # Create BDD scenarios from requirements
/task-create           # Create implementation tasks
# or
/feature-generate-tasks # Auto-generate tasks from EARS/BDD
```

### Stage 3: Engineering & Implementation
```bash
# Universal command for all stacks
/task-work TASK-XXX [--mode=standard|tdd|bdd]
# Automatically handles implementation + testing + quality gates

# Progress monitoring
/task-status           # View task progress with hierarchy context
/task-sync            # Sync progress to PM tools
```

**Stack-specific development commands:**
```bash
# React
npm run dev            # Start development
npm test              # Run tests
npm run build         # Production build

# Python
python -m venv venv   # Create environment
pip install -r requirements.txt
uvicorn main:app --reload

# TypeScript API
npm install           # Install dependencies
npm run start:dev     # Start in development
npm run test         # Run tests

# .NET Microservice
dotnet build
dotnet run
dotnet test

# .NET MAUI
dotnet build
dotnet run --framework net8.0-android
dotnet test --filter Category=Integration

# Full Stack
# Frontend
cd frontend && npm run dev
# Backend
cd backend && uvicorn main:app --reload
```

### Stage 4: Deployment & QA
```bash
/task-complete TASK-XXX    # Complete with validation + progress rollup
/hierarchy-view           # View complete project hierarchy
/portfolio-dashboard      # Executive portfolio overview
```

## 📋 Key Patterns by Stack

### React Patterns
```typescript
// Error Boundary
<ErrorBoundary fallback={<ErrorFallback />}>
  <Component />
</ErrorBoundary>

// SSE Hook
const { data, error, isConnected } = useSSE('/api/stream');

// Performance
const MemoizedComponent = memo(Component);
const debouncedSearch = useDebouncedCallback(search, 300);
```

### Python Patterns
```python
# Factory Pattern
def create_agent_factory(config: AgentConfig):
    return Agent(config)

# LangGraph Workflow
workflow = StateGraph(State)
workflow.add_node("process", process_node)
workflow.add_edge("process", "validate")

# SSE Streaming
async def stream_response():
    yield "data: Starting\n\n"
    # ... processing
    yield "event: done\ndata: {}\n\n"
```

### .NET Patterns
```csharp
// Either Monad
public async Task<Either<Error, Product>> GetProductAsync(Guid id)
{
    return await TryAsync(async () => 
    {
        var product = await _repository.GetByIdAsync(id);
        return product != null 
            ? Right<Error, Product>(product)
            : Left<Error, Product>(new NotFoundError());
    })
    .IfFail(ex => Left<Error, Product>(new ServiceError(ex.Message)));
}

// FastEndpoint
public class GetProduct : Endpoint<GetRequest, GetResponse>
{
    public override void Configure()
    {
        Get("/api/products/{id}");
    }
}
```

### MAUI Patterns
```csharp
// UseCase
public async Task<Either<Error, Data>> ExecuteAsync(object? param)
{
    // Try cache first
    var cached = await _cache.GetAsync<Data>(key);
    if (cached != null) return cached;
    
    // Fetch from API
    return await _api.GetAsync<Data>(endpoint);
}

// ViewModel
[RelayCommand]
private async Task LoadData()
{
    using (var _ = new LoadingScope(this))
    {
        var result = await _useCase.ExecuteAsync();
        result.Match(
            Right: data => Data = data,
            Left: error => ShowError(error)
        );
    }
}
```

## 🔍 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `agentecflow: command not found` | Run `source ~/.bashrc` or add to PATH |
| NuGet package conflicts | Ensure all target .NET 8.0 |
| Either monad errors | Add `using static LanguageExt.Prelude;` |
| React SSE not closing | Ensure `event: done` is sent |
| Python tests not found | Check pytest.ini configuration |

## 📚 Documentation Links

- [Full System Documentation](README.md)
- [.NET Stacks Guide](docs/NET_STACKS_INTEGRATION.md)
- [Template Integration Summary](docs/TEMPLATE_INTEGRATION_SUMMARY.md)
- [Setup Guide](installer/SETUP_GUIDE.md)
- [Installation Guide](installer/INSTALLATION_GUIDE.md)

## 🎯 Best Practices

### Universal
1. Always use the templates as starting points
2. Follow the quality gates strictly
3. Test from the outside in
4. Use factory patterns for consistency
5. Handle errors functionally, not with exceptions

### Stack-Specific
- **React**: Prioritize accessibility and performance
- **Python**: Keep changes surgical, reuse patterns
- **NET Microservice**: Use Either monad everywhere
- **NET MAUI**: Keep ViewModels thin, logic in UseCases

## 🚀 Next Steps

1. Choose your stack and initialize a project
2. Review the stack's CLAUDE.md file
3. Start with `/gather-requirements`
4. Follow the EARS → BDD → Implementation flow
5. Use quality gates to ensure standards

---

*This guide covers the enhanced AI Engineer system with production-tested patterns from multiple successful projects.*
