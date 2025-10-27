# Updated settings.json Configuration

Add this configuration to your `.claude/settings.json` file:

```json
{
  "agent_orchestration": {
    "enabled": true,
    "rules_file": "methodology/05-agent-orchestration.md",
    "auto_select": {
      "by_file_extension": {
        ".py": {
          "primary": "python-api-specialist",
          "testing": "python-testing-specialist",
          "ai": "python-langchain-specialist"
        },
        ".tsx": {
          "primary": "react-component-specialist",
          "state": "react-state-specialist",
          "testing": "react-testing-specialist"
        },
        ".ts": {
          "primary": "react-component-specialist",
          "testing": "react-testing-specialist"
        },
        ".cs": {
          "primary": "dotnet-api-specialist",
          "domain": "dotnet-domain-specialist",
          "testing": "dotnet-testing-specialist"
        },
        ".xaml": {
          "primary": "maui-ui-specialist",
          "viewmodel": "maui-viewmodel-specialist",
          "testing": "qa-tester"
        },
        ".sql": {
          "primary": "database-specialist",
          "review": "code-reviewer"
        },
        "Dockerfile": {
          "primary": "devops-specialist",
          "security": "security-specialist"
        },
        ".yml": {
          "primary": "devops-specialist",
          "review": "code-reviewer"
        }
      },
      "by_task_type": {
        "architecture": ["software-architect"],
        "testing": ["qa-tester"],
        "security": ["security-specialist"],
        "database": ["database-specialist"],
        "deployment": ["devops-specialist"],
        "requirements": ["requirements-analyst"],
        "review": ["code-reviewer"],
        "ai_workflow": ["python-langchain-specialist"],
        "api_development": ["{stack}-api-specialist"],
        "bug_fix": ["qa-tester", "{stack}-specialist"],
        "performance": ["software-architect", "devops-specialist"]
      }
    },
    "coordination_mode": "sequential",
    "default_sequence": [
      "requirements-analyst",
      "software-architect",
      "{stack}-specialist",
      "qa-tester",
      "code-reviewer"
    ],
    "quality_gates": {
      "code_quality": {
        "enabled": true,
        "linting": "required",
        "complexity_threshold": 10,
        "duplication_threshold": 5
      },
      "testing": {
        "enabled": true,
        "coverage_threshold": 80,
        "unit_tests": "required",
        "integration_tests": "recommended"
      },
      "documentation": {
        "enabled": true,
        "api_docs": "required",
        "code_comments": "recommended",
        "readme_updates": "required"
      },
      "security": {
        "enabled": true,
        "vulnerability_scan": "required",
        "secrets_scan": "required"
      }
    },
    "handoff_protocol": {
      "context_preservation": true,
      "documentation_required": true,
      "quality_check": true,
      "review_required": false
    }
  }
}
```

## Configuration Explanation

### agent_orchestration
Main configuration block for the orchestration system.

### auto_select
Defines automatic agent selection rules:
- **by_file_extension**: Maps file types to appropriate specialists
- **by_task_type**: Maps task types to agent sequences

### coordination_mode
How agents work together:
- `sequential`: One after another
- `parallel`: Simultaneously
- `hierarchical`: Lead agent coordinates others

### default_sequence
Standard agent flow for tasks without specific routing.

### quality_gates
Defines quality standards that must be met:
- **code_quality**: Linting, complexity, duplication
- **testing**: Coverage thresholds and requirements
- **documentation**: Required documentation updates
- **security**: Security scanning requirements

### handoff_protocol
Rules for passing work between agents:
- **context_preservation**: Maintain context between handoffs
- **documentation_required**: Document decisions and changes
- **quality_check**: Verify quality gates before handoff
- **review_required**: Require review before proceeding
