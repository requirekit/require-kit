# Python AI Agent Project Context for Claude Code

This is a Python AI Agent project using the Agentic Flow system with production-ready patterns learned from real-world implementations.

## 🎯 Development Constraints (Surgical Coding Prompt)

**CRITICAL**: Think harder and thoroughly examine similar areas of the codebase to ensure your proposed approach fits seamlessly with the established patterns and architecture. Aim to make only minimal and necessary changes, avoiding any disruption to the existing design. Whenever possible, take advantage of components, utilities, or logic that have already been implemented to maintain consistency, reduce duplication, and streamline integration with the current system.

## ✅ Quality Gates
- **Maximum 3 files changed per feature** (enforce surgical changes)
- **Test coverage required before implementation** (minimum 80%)
- **Existing patterns must be reused** (no reinventing the wheel)
- **No new abstractions without documented justification**
- **Incremental commits after each working change**
- **Regression tests for critical paths** (prevent production issues)

## 🏗️ Technology Stack

### Core Technologies
- **Language**: Python 3.10+
- **API Framework**: FastAPI (for REST APIs and SSE streaming)
- **AI Orchestration**: LangGraph (preferred over LangChain for production)
- **LLM Integration**: LangChain (for model connectors only)
- **Validation**: Pydantic v2 (models, configs, API contracts)
- **Testing**: pytest + pytest-asyncio + pytest-bdd
- **UI Prototyping**: Streamlit (for rapid testing)
- **Database**: PostgreSQL with SQLAlchemy (when needed)
- **Caching**: Redis (for performance optimization)

### Code Quality Tools
- **Formatting**: Black (88 char line length)
- **Linting**: Ruff (fast, comprehensive)
- **Type Checking**: mypy (strict mode)
- **Security**: bandit
- **Documentation**: Sphinx with autodoc

## 📂 Project Structure

```
.
├── .claude/                # Agentic Flow configuration
│   ├── CLAUDE.md          # This file - project context
│   ├── agents/            # Sub-agent specifications
│   └── commands/          # Custom commands
├── src/
│   ├── agents/            # AI agent implementations
│   │   ├── __init__.py
│   │   └── main_agent.py  # Primary orchestration agent
│   ├── workflows/         # LangGraph workflows
│   │   ├── __init__.py
│   │   └── base_workflow.py
│   ├── tools/             # Agent tools/functions
│   │   ├── __init__.py
│   │   └── search_tool.py
│   ├── models/            # Pydantic models
│   │   ├── __init__.py
│   │   ├── requests.py   # API request models
│   │   └── responses.py  # API response models
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── llm_service.py
│   ├── api/               # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── routes/       # Route definitions
│   │   └── streaming.py  # SSE endpoints
│   ├── prompts/           # Prompt templates
│   │   ├── __init__.py
│   │   └── templates.py
│   ├── utils/             # Utilities
│   │   ├── __init__.py
│   │   ├── config.py     # Configuration management
│   │   └── logging.py    # Structured logging
│   └── main.py            # Application entry point
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── e2e/               # End-to-end tests
│   ├── regression/        # Regression test suite
│   └── conftest.py       # Pytest configuration
├── streamlit_app.py       # Streamlit UI for testing
├── docs/                  # Documentation
│   ├── requirements/      # EARS requirements
│   └── bdd/              # BDD scenarios
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Project configuration
└── docker-compose.yml   # Container orchestration
```

## 🔄 Development Patterns

### 1. Factory Pattern (Component Creation)

**ALWAYS use factory functions for component instantiation:**

```python
# src/agents/factories.py
from typing import Optional
from .main_agent import MainAgent
from ..models.config import AgentConfig

def create_agent(
    config: Optional[AgentConfig] = None,
    enable_caching: bool = True,
    enable_monitoring: bool = True
) -> MainAgent:
    """
    Factory function for creating configured agents.
    
    Args:
        config: Optional configuration override
        enable_caching: Enable Redis caching
        enable_monitoring: Enable metrics collection
    
    Returns:
        Configured MainAgent instance
    """
    if config is None:
        config = AgentConfig.from_env()
    
    agent = MainAgent(config)
    
    if enable_caching:
        agent.enable_caching()
    
    if enable_monitoring:
        agent.enable_monitoring()
    
    return agent

# Usage
agent = create_agent()  # Use factory, not direct instantiation
```

### 2. LangGraph Workflow Pattern

**Structure workflows with clear states and transitions:**

```python
# src/workflows/base_workflow.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from operator import add

class WorkflowState(TypedDict):
    """Typed state for workflow execution."""
    messages: Annotated[Sequence[str], add]
    current_step: str
    context: dict
    errors: list
    results: dict

def create_workflow() -> StateGraph:
    """Factory for creating configured workflows."""
    workflow = StateGraph(WorkflowState)
    
    # Define nodes (steps)
    workflow.add_node("analyze", analyze_input)
    workflow.add_node("process", process_data)
    workflow.add_node("validate", validate_results)
    workflow.add_node("respond", generate_response)
    
    # Define edges (transitions)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "process")
    workflow.add_conditional_edges(
        "process",
        should_validate,
        {
            "validate": "validate",
            "respond": "respond"
        }
    )
    workflow.add_edge("validate", "respond")
    workflow.add_edge("respond", END)
    
    return workflow.compile()
```

### 3. Comprehensive Error Handling

**Every external call must have error handling:**

```python
# src/utils/error_handling.py
from typing import TypeVar, Callable, Optional, Any
from functools import wraps
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

T = TypeVar('T')

class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class APIError(AgentError):
    """API-related errors."""
    pass

def with_error_handling(
    default_return: Optional[Any] = None,
    log_errors: bool = True,
    raise_on_error: bool = False
):
    """Decorator for comprehensive error handling."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                if raise_on_error:
                    raise AgentError(f"Failed to execute {func.__name__}: {str(e)}") from e
                return default_return
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                if raise_on_error:
                    raise AgentError(f"Failed to execute {func.__name__}: {str(e)}") from e
                return default_return
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Usage with retry logic
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
@with_error_handling(raise_on_error=True)
async def call_external_api(url: str) -> dict:
    """Make external API call with retry and error handling."""
    # Implementation here
    pass
```

### 4. SSE Streaming Pattern

**Implement Server-Sent Events for real-time AI responses:**

```python
# src/api/streaming.py
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import json
import asyncio

router = APIRouter()

async def generate_stream(query: str) -> AsyncGenerator[str, None]:
    """Generate SSE stream for AI responses."""
    try:
        # Initialize agent
        agent = create_agent()
        
        # Process with streaming
        async for chunk in agent.process_streaming(query):
            # Format as SSE
            data = {
                "event": "message",
                "data": json.dumps({"content": chunk})
            }
            yield f"data: {json.dumps(data)}\n\n"
        
        # Send completion event
        yield f"data: {json.dumps({'event': 'done'})}\n\n"
        
    except Exception as e:
        # Send error event
        error_data = {
            "event": "error",
            "data": json.dumps({"error": str(e)})
        }
        yield f"data: {json.dumps(error_data)}\n\n"

@router.post("/stream")
async def stream_response(request: dict):
    """SSE endpoint for streaming AI responses."""
    return StreamingResponse(
        generate_stream(request["query"]),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Connection": "keep-alive",
        }
    )
```

### 5. Pydantic Model Patterns

**Define clear, validated data models:**

```python
# src/models/requests.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class AgentRequest(BaseModel):
    """Base request model for agent interactions."""
    
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation tracking")
    max_tokens: int = Field(default=500, ge=1, le=4000, description="Maximum response tokens")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Response randomness")
    
    @validator('query')
    def validate_query(cls, v):
        """Ensure query is not just whitespace."""
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the requirements for a valid will?",
                "context": {"jurisdiction": "UK"},
                "session_id": "sess_123",
                "max_tokens": 500,
                "temperature": 0.7
            }
        }

class AgentResponse(BaseModel):
    """Standard response model for agent interactions."""
    
    answer: str = Field(..., description="Agent's response")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    sources: List[str] = Field(default_factory=list, description="Source references")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    session_id: Optional[str] = Field(None, description="Session identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "A valid will requires...",
                "confidence": 0.95,
                "sources": ["Wills Act 1837"],
                "metadata": {"processing_time": 1.2},
                "session_id": "sess_123",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
```

### 6. Multi-Agent Orchestration

**Coordinate multiple specialized agents:**

```python
# src/agents/orchestrator.py
from typing import Dict, Any, List
from .specialist_agents import ResearchAgent, AnalysisAgent, ValidationAgent

class OrchestratorAgent:
    """Orchestrates multiple specialist agents."""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.validation_agent = ValidationAgent()
    
    async def process_complex_query(self, query: str) -> Dict[str, Any]:
        """Process query using multiple agents."""
        
        # Phase 1: Research
        research_results = await self.research_agent.gather_information(query)
        
        # Phase 2: Analysis
        analysis = await self.analysis_agent.analyze(
            query=query,
            context=research_results
        )
        
        # Phase 3: Validation
        validated_response = await self.validation_agent.validate(
            analysis=analysis,
            sources=research_results.get("sources", [])
        )
        
        return {
            "response": validated_response,
            "confidence": self._calculate_confidence(validated_response),
            "sources": research_results.get("sources", []),
            "metadata": {
                "agents_used": ["research", "analysis", "validation"],
                "processing_stages": 3
            }
        }
```

## 🧪 Testing Strategy

### Test-Driven Development with Regression Prevention

```python
# tests/regression/test_critical_paths.py
import pytest
from src.agents import create_agent

class TestCriticalPaths:
    """Regression tests for critical functionality."""
    
    @pytest.mark.critical
    async def test_agent_initialization(self):
        """Ensure agent initializes correctly - prevents production issues."""
        agent = create_agent()
        assert agent is not None
        assert agent.is_ready()
    
    @pytest.mark.critical
    async def test_streaming_completion_event(self):
        """Ensure SSE streams complete properly - known production issue."""
        agent = create_agent()
        events = []
        
        async for event in agent.process_streaming("test query"):
            events.append(event)
        
        # Must have completion event
        assert any(e.get("event") == "done" for e in events)
    
    @pytest.mark.parametrize("query,expected_confidence", [
        ("simple question", 0.8),
        ("complex legal query", 0.9),
    ])
    async def test_confidence_thresholds(self, query, expected_confidence):
        """Ensure confidence scoring works correctly."""
        agent = create_agent()
        response = await agent.process(query)
        assert response.confidence >= expected_confidence

# Run critical tests before deployment
# pytest tests/regression/ -m critical
```

### BDD Testing Pattern

```python
# tests/features/agent_processing.feature
Feature: Agent Query Processing
    As a user
    I want to ask questions to the AI agent
    So that I get accurate, sourced responses

    Scenario: Simple query processing
        Given an initialized agent
        When I ask "What is a will?"
        Then I should receive a response within 5 seconds
        And the response should have confidence > 0.7
        And the response should include sources

# tests/step_defs/test_agent_processing.py
from pytest_bdd import scenarios, given, when, then
import pytest

scenarios('../features/agent_processing.feature')

@given('an initialized agent')
def agent(create_agent):
    return create_agent()

@when('I ask "<query>"')
async def ask_query(agent, query):
    return await agent.process(query)

@then('I should receive a response within <timeout> seconds')
def check_response_time(response, timeout):
    assert response.metadata["processing_time"] < timeout
```

## 🔧 MCP Server Development

### Building MCP Servers for AI Workflows

If your project involves building **MCP (Model Context Protocol) servers** that expose tools and resources for AI development workflows, you should engage the **`python-mcp-specialist`** agent.

**When to Use MCP Servers**:
- Building tool servers for Claude Code, Gemini CLI, or other AI development tools
- Exposing domain-specific tools (requirements management, testing, deployment, etc.)
- Integrating external systems (Jira, Linear, Azure DevOps, GitHub) with AI workflows
- Creating reusable tool libraries that work across multiple AI platforms

**MCP Server Architecture**:
```python
# Example MCP server structure
from mcp.server import Server
from mcp.types import Tool, Resource
from typing import Dict, Any

class MyMCPServer:
    """MCP server exposing domain-specific tools."""

    def __init__(self, config: dict):
        self.server = Server("my-mcp-server")
        self._register_tools()
        self._register_resources()

    def _register_tools(self):
        """Register MCP tools using decorators."""

        @self.server.tool()
        async def process_data(input_data: dict) -> dict:
            """
            Process data using domain logic.

            Args:
                input_data: Input data to process

            Returns:
                Processed results
            """
            return await self._process_data_impl(input_data)

    def _register_resources(self):
        """Register MCP resources for direct access."""

        @self.server.resource("data://{resource_id}")
        async def get_data(uri: str) -> str:
            """Retrieve data by ID."""
            resource_id = uri.split("/")[-1]
            return await self._fetch_data(resource_id)

    async def run(self):
        """Start MCP server with stdio transport."""
        async with self.server.stdio_transport():
            await self.server.serve()
```

**Integration with LangGraph Orchestrators**:
```python
from langgraph.graph import StateGraph
from mcp.client import Client

class Orchestrator:
    def __init__(self):
        # Connect to MCP servers
        self.mcp_client = Client("my-mcp-server")
        self.workflow = self._create_workflow()

    async def _process_node(self, state):
        """LangGraph node calling MCP tool."""
        result = await self.mcp_client.call_tool(
            "process_data",
            {"input_data": state.data}
        )
        state.results = result
        return state
```

**Engage `python-mcp-specialist` for**:
- MCP server architecture and design
- Tool and resource registration patterns
- Transport layer configuration (stdio, HTTP, WebSocket)
- Integration with LangGraph orchestrators
- Testing strategies for MCP servers
- Claude Code configuration
- Error handling and observability

### Optional MCP Code Checker Configuration

For code quality checking, integrate the MCP Code Checker:

```json
{
  "mcpServers": {
    "python_code_checker": {
      "command": "python",
      "args": [
        "-m",
        "mcp_code_checker",
        "--project-dir",
        ".",
        "--python-executable",
        ".venv/bin/python"
      ]
    }
  }
}
```

## 📊 Performance & Monitoring

### Structured Logging

```python
# src/utils/logging.py
import structlog
from typing import Any, Dict

def setup_logging():
    """Configure structured logging."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

logger = structlog.get_logger()

# Usage
logger.info("agent_initialized", agent_id="123", config={"model": "gpt-4"})
logger.error("api_call_failed", error=str(e), retry_count=3)
```

### Performance Monitoring

```python
# src/monitoring/metrics.py
from typing import Callable
from functools import wraps
import time
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
request_count = Counter('agent_requests_total', 'Total requests processed')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')
active_sessions = Gauge('agent_active_sessions', 'Number of active sessions')

def monitor_performance(func: Callable) -> Callable:
    """Decorator to monitor function performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        request_count.inc()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            request_duration.observe(duration)
    
    return wrapper
```

## 🚀 Quick Start Commands

### Development Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install package in development mode

# Setup pre-commit hooks
pre-commit install

# Run initial tests
pytest tests/ -v

# Start development server
uvicorn src.main:app --reload --port 8000

# Start Streamlit UI (in separate terminal)
streamlit run streamlit_app.py
```

### Testing Commands
```bash
# Run all tests with coverage
pytest tests/ --cov=src --cov-report=html

# Run only critical regression tests
pytest tests/regression/ -m critical

# Run BDD tests
pytest tests/features/

# Run with specific markers
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Only integration tests

# Run type checking
mypy src/ --strict

# Run security checks
bandit -r src/

# Format code
black src/ tests/
ruff check src/ tests/ --fix
```

### Agent-Specific Commands

In your IDE with Claude integration:

```
/create-agent AgentName        # Generate new agent with factory
/create-workflow WorkflowName   # Generate LangGraph workflow
/create-tool ToolName          # Generate agent tool
/add-streaming endpoint_name   # Add SSE streaming endpoint
/add-error-handling function   # Wrap function with error handling
/create-pydantic-model Model   # Generate Pydantic model with validation
/add-regression-test feature   # Create regression test for feature
```

## 🏆 Best Practices

1. **Always use factories** - Never instantiate components directly
2. **Implement comprehensive error handling** - Every external call needs protection
3. **Write tests first** - TDD prevents issues and clarifies requirements
4. **Use Pydantic everywhere** - Validation prevents runtime errors
5. **Stream responses when possible** - Better UX for AI interactions
6. **Log structured data** - Makes debugging and monitoring easier
7. **Cache expensive operations** - Use Redis for repeated queries
8. **Version your prompts** - Track prompt changes like code
9. **Monitor everything** - You can't improve what you don't measure
10. **Keep changes surgical** - Small, focused changes reduce risk

## 🚨 Common Pitfalls to Avoid

1. **Don't use LangChain for orchestration** - Use LangGraph instead
2. **Don't skip error handling** - It will fail in production
3. **Don't hardcode configurations** - Use environment variables
4. **Don't ignore streaming completion** - SSE needs proper termination
5. **Don't create new patterns** - Reuse existing factories and patterns
6. **Don't skip regression tests** - They prevent known issues
7. **Don't use synchronous I/O in async functions** - Use async throughout
8. **Don't ignore type hints** - They prevent many runtime errors
9. **Don't commit without tests** - Untested code is broken code
10. **Don't over-engineer** - Start simple, iterate based on needs

## 📚 Additional Resources

- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic V2 Migration](https://docs.pydantic.dev/latest/migration/)
- [Streamlit for ML Apps](https://streamlit.io/)
- [pytest-bdd Guide](https://pytest-bdd.readthedocs.io/)

## 🔄 Continuous Improvement

This template is based on real-world experience from production AI agent development. Update it with new patterns and lessons learned from your implementations. Remember: the goal is to build reliable, maintainable, and performant AI agents that solve real problems.

---

**Remember the Prime Directive**: Make minimal changes, reuse existing patterns, and always test before implementing.