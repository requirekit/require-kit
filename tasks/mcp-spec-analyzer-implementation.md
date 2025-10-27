# Task: Implement MCP Specification Analyzer Server

## Overview
Build a proof-of-concept MCP server for packaging the agentic specification analysis workflow, using Python as the primary technology stack based on the technology analysis.

## Background
- Current workflow successfully analyzes specifications and creates requirements
- Need to package this as an MCP server for use with Claude Code, Cline, and other CLI tools
- Python chosen over Node.js for superior text processing, AI integration, and performance
- Will support both CLI integration initially and WebUI in future phases

## Technology Stack Decision
**Primary: Python** 
- Better text processing and NLP capabilities
- Rich AI/ML ecosystem (LangChain, spaCy, transformers)
- Good performance for specification analysis
- Clean, maintainable code
- Active community MCP support

**Optional: Minimal Node.js adapter** (only if protocol compatibility issues arise)

## Implementation Phases

### Phase 1: Python MCP Server POC (Week 1-2)

#### Task 1.1: Project Setup
```bash
# Create project structure
mkdir mcp-spec-analyzer-python
cd mcp-spec-analyzer-python

# Initialize Python project
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Create requirements.txt
cat > requirements.txt << EOF
mcp==0.1.0  # or latest version
pydantic==2.5.0
fastapi==0.104.0
uvicorn==0.24.0
pytest==7.4.0
pytest-asyncio==0.21.0
spacy==3.7.0
langchain==0.1.0
EOF

pip install -r requirements.txt
```

#### Task 1.2: Core MCP Server Implementation
Create `mcp_server.py`:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import asyncio
import json
from datetime import datetime

class SpecificationRequest(BaseModel):
    """Request model with runtime validation"""
    specification: str = Field(..., min_length=1, max_length=100000)
    format: Optional[str] = Field(None, pattern="^(user_story|technical|api|requirements)$")
    output_format: str = Field("files", pattern="^(json|markdown|files)$")
    options: Dict = Field(default_factory=dict)

class SpecAnalyzerServer:
    def __init__(self):
        self.server = Server("spec-analyzer", "1.0.0")
        self.setup_tools()
    
    def setup_tools(self):
        @self.server.tool()
        async def analyze_specification(request: SpecificationRequest):
            """Comprehensive specification analysis workflow"""
            result = await self.process_specification(request)
            
            if request.output_format == "json":
                return {"type": "text", "text": json.dumps(result, indent=2)}
            else:
                return {"type": "text", "text": self.format_markdown(result)}
    
    async def process_specification(self, request: SpecificationRequest):
        # Implementation here
        pass
    
    async def run(self):
        async with stdio_server() as streams:
            await self.server.run(
                streams.read_stream,
                streams.write_stream,
                self.server.create_initialization_options()
            )

if __name__ == "__main__":
    server = SpecAnalyzerServer()
    asyncio.run(server.run())
```

#### Task 1.3: Docker Configuration
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for NLP libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application
COPY . .

# Python optimizations
ENV PYTHONUNBUFFERED=1
ENV PYTHONOPTIMIZE=2

CMD ["python", "mcp_server.py"]
```

#### Task 1.4: CLI Integration Testing
Configure for Claude Desktop:
```json
{
  "mcpServers": {
    "spec-analyzer": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {}
    }
  }
}
```

### Phase 2: Core Features Implementation (Week 3-4)

#### Task 2.1: Specification Processing Module
Create `processors/specification_analyzer.py`:
```python
import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ParsedSpecification:
    sections: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    raw_text: str

class SpecificationAnalyzer:
    def __init__(self):
        self.patterns = {
            'user_story': r'As a .+ I want .+ so that .+',
            'requirement': r'[Tt]he system (shall|should|must)',
            'acceptance_criteria': r'Given .+ When .+ Then .+'
        }
    
    async def parse(self, spec: str, format: Optional[str] = None) -> ParsedSpecification:
        """Parse specification into structured format"""
        # Auto-detect format if not specified
        if not format:
            format = self.detect_format(spec)
        
        sections = self.extract_sections(spec)
        metadata = self.extract_metadata(spec)
        
        return ParsedSpecification(
            sections=sections,
            metadata=metadata,
            raw_text=spec
        )
    
    def detect_format(self, spec: str) -> str:
        """Auto-detect specification format"""
        for format_type, pattern in self.patterns.items():
            if re.search(pattern, spec, re.IGNORECASE):
                return format_type
        return 'technical'
```

#### Task 2.2: Requirements Generator
Create `processors/requirements_generator.py`:
```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Requirement:
    id: str
    type: str  # functional, non-functional, technical
    description: str
    priority: str  # high, medium, low
    acceptance_criteria: List[str]

class RequirementsGenerator:
    async def generate(self, parsed_spec: ParsedSpecification) -> List[Requirement]:
        """Generate requirements from parsed specification"""
        requirements = []
        
        for idx, section in enumerate(parsed_spec.sections):
            req = Requirement(
                id=f"REQ-{idx+1:03d}",
                type=self.classify_requirement(section),
                description=self.extract_description(section),
                priority=self.determine_priority(section),
                acceptance_criteria=self.extract_criteria(section)
            )
            requirements.append(req)
        
        return requirements
```

#### Task 2.3: Task Creator
Create `processors/task_creator.py`:
```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Task:
    id: str
    title: str
    description: str
    type: str  # feature, bug, improvement, task
    estimated_hours: float
    requirements: List[str]  # Related requirement IDs
    acceptance_criteria: List[str]

class TaskCreator:
    async def create(self, requirements: List[Requirement], max_tasks: int = 10) -> List[Task]:
        """Create actionable tasks from requirements"""
        tasks = []
        
        for req in requirements[:max_tasks]:
            # Create one or more tasks per requirement
            task_count = self.determine_task_count(req)
            
            for i in range(task_count):
                task = Task(
                    id=f"TASK-{len(tasks)+1:03d}",
                    title=self.generate_title(req, i),
                    description=self.generate_description(req),
                    type=self.determine_type(req),
                    estimated_hours=self.estimate_hours(req),
                    requirements=[req.id],
                    acceptance_criteria=req.acceptance_criteria
                )
                tasks.append(task)
        
        return tasks
```

### Phase 3: Advanced Features (Week 5-6)

#### Task 3.1: WebUI Support via MCPO
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    container_name: mcp-spec-analyzer
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./output:/app/output
    networks:
      - mcp-network

  mcpo-proxy:
    image: python:3.11-slim
    container_name: mcpo-proxy
    command: >
      sh -c "pip install mcpo && 
             mcpo --port 8000 --host 0.0.0.0 -- 
             docker exec mcp-spec-analyzer python /app/mcp_server.py"
    ports:
      - "8000:8000"
    depends_on:
      - mcp-server
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

#### Task 3.2: Authentication & Rate Limiting
Create `middleware/auth.py`:
```python
from typing import Dict, Optional
import hashlib
import time
from dataclasses import dataclass

@dataclass
class APIKey:
    key: str
    permissions: List[str]
    rate_limit: int  # requests per hour
    usage: int
    reset_time: float

class AuthManager:
    def __init__(self):
        self.api_keys: Dict[str, APIKey] = {}
    
    def generate_api_key(self, permissions: List[str]) -> str:
        """Generate new API key"""
        key = f"mcp_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]}"
        self.api_keys[key] = APIKey(
            key=key,
            permissions=permissions,
            rate_limit=100,
            usage=0,
            reset_time=time.time() + 3600
        )
        return key
    
    async def validate_request(self, api_key: str) -> bool:
        """Validate API key and check rate limits"""
        if api_key not in self.api_keys:
            return False
        
        key_data = self.api_keys[api_key]
        
        # Reset counter if window expired
        if time.time() > key_data.reset_time:
            key_data.usage = 0
            key_data.reset_time = time.time() + 3600
        
        # Check rate limit
        if key_data.usage >= key_data.rate_limit:
            raise Exception("Rate limit exceeded")
        
        key_data.usage += 1
        return True
```

#### Task 3.3: Testing Suite
Create `tests/test_mcp_server.py`:
```python
import pytest
import asyncio
from mcp_server import SpecAnalyzerServer
from processors.specification_analyzer import SpecificationAnalyzer

@pytest.mark.asyncio
async def test_specification_parsing():
    analyzer = SpecificationAnalyzer()
    spec = "As a user, I want to login to the system so that I can access my account"
    
    result = await analyzer.parse(spec)
    
    assert result.metadata['format'] == 'user_story'
    assert len(result.sections) > 0

@pytest.mark.asyncio
async def test_mcp_tool_registration():
    server = SpecAnalyzerServer()
    tools = server.server.get_tools()
    
    assert 'analyze_specification' in [t.name for t in tools]

@pytest.mark.asyncio
async def test_end_to_end_analysis():
    server = SpecAnalyzerServer()
    request = {
        "specification": "Build a user authentication system",
        "output_format": "json"
    }
    
    result = await server.process_specification(request)
    
    assert 'requirements' in result
    assert 'tasks' in result
    assert len(result['tasks']) > 0
```

### Phase 4: Production Deployment

#### Task 4.1: Cloud Deployment (AWS)
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URL
docker build -t mcp-spec-analyzer .
docker tag mcp-spec-analyzer:latest $ECR_URL/mcp-spec-analyzer:latest
docker push $ECR_URL/mcp-spec-analyzer:latest

# Deploy with ECS or Lambda
```

#### Task 4.2: Monitoring & Logging
```python
import logging
from pythonjsonlogger import jsonlogger

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

## Success Criteria

1. ✅ Python MCP server successfully processes specifications
2. ✅ Works with Claude Desktop, Cline, and VS Code
3. ✅ Docker containerization working
4. ✅ Returns both files and structured data
5. ✅ Comprehensive test coverage (>80%)
6. ✅ Documentation complete
7. ✅ Ready for WebUI integration via MCPO

## Deliverables

1. **Python MCP Server** - Core implementation
2. **Docker Configuration** - Containerization
3. **Test Suite** - Unit and integration tests
4. **Documentation** - Setup and usage guide
5. **CLI Configurations** - For Claude Desktop, Cline, VS Code
6. **MCPO Integration** - REST API bridge for future WebUI

## Timeline

- **Week 1-2**: Core Python MCP server implementation
- **Week 3-4**: Feature implementation and testing
- **Week 5-6**: Advanced features and production readiness

## Notes

- Python chosen over Node.js for better text processing and AI integration
- Minimal Node.js adapter only if protocol compatibility issues arise
- Focus on clean, maintainable code over premature optimization
- Prioritize working POC before adding advanced features

## Resources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCPO Proxy Documentation](https://github.com/mcpo/mcpo)
- [Python MCP Examples](https://github.com/modelcontextprotocol/servers)
- [Docker Best Practices for Python](https://docs.docker.com/language/python/)

---

*Created: 2025-01-15*
*Status: Ready for Implementation*
*Assignee: TBD*