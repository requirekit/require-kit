---
id: TASK-001A
title: "Repository Setup and Basic Structure"
created: 2025-10-19
status: backlog
priority: high
complexity: 3
parent_task: TASK-001
subtasks: []
estimated_hours: 1
---

# TASK-001A: Repository Setup and Basic Structure

## Description

Create new GitHub repository `agentecflow` with basic structure, README, LICENSE, and branch protection rules.

## Acceptance Criteria

- [ ] Repository created at GitHub.com
- [ ] Basic directory structure created
- [ ] README.md written (lite-focused, 5-min quickstart)
- [ ] LICENSE file (MIT license)
- [ ] .gitignore configured
- [ ] Branch protection enabled on main
- [ ] Repository public and accessible

## Implementation Steps

### 1. Create Repository on GitHub

```bash
# Via GitHub CLI
gh repo create agentecflow --public --description "Lightweight AI-Assisted Development with Quality Gates"

# Or create manually via GitHub web UI
```

### 2. Clone and Initialize

```bash
git clone https://github.com/yourusername/agentecflow.git
cd agentecflow
```

### 3. Create Directory Structure

```bash
mkdir -p installer/global/{commands,agents,instructions,templates}
mkdir -p installer/scripts
mkdir -p docs
mkdir -p tests
mkdir -p .github/workflows
```

### 4. Create .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
*.log

# Task workspace (when used in projects)
tasks/
.claude/
```

### 5. Create LICENSE (MIT)

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 6. Create README.md

See detailed content in "README Template" section below.

### 7. Enable Branch Protection

```bash
# Via GitHub CLI
gh api repos/yourusername/agentecflow/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":[]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false}'

# Or configure via GitHub web UI:
# Settings > Branches > Add rule for 'main'
# ✓ Require pull request reviews before merging
# ✓ Dismiss stale pull request approvals when new commits are pushed
```

### 8. Initial Commit

```bash
git add .
git commit -m "Initial commit: Repository structure and documentation"
git push origin main
```

## README Template

```markdown
# Agentecflow

**Lightweight AI-assisted development with built-in quality gates.**

Stop shipping broken code. Get architectural review before implementation and automatic test enforcement after. Simple task workflow, no ceremony.

## What You Get

- **Phase 2.5 - Architectural Review**: Evaluates SOLID, DRY, YAGNI principles before you write code
- **Phase 4.5 - Test Enforcement**: Automatically fixes failing tests, ensures 100% pass rate
- **Specialized Agents**: Stack-specific AI agents for React, Python, .NET MAUI, TypeScript, etc.
- **Quality Gates**: Coverage thresholds, compilation checks, code review automation
- **State Management**: Automatic task lifecycle tracking (backlog → in_progress → in_review → completed)

## 5-Minute Quickstart

### Install

```bash
git clone https://github.com/yourusername/agentecflow.git
cd agentecflow
chmod +x installer/scripts/install.sh
./installer/scripts/install.sh
```

### Initialize Your Project

```bash
cd your-project
agentecflow init react  # or: python, maui, typescript-api, dotnet-microservice
```

### Create and Complete a Task

```bash
# Create a task
/task-create "Add user avatar upload feature"

# Work on it (with quality gates)
/task-work TASK-001

# Complete when all tests pass
/task-complete TASK-001
```

That's it. No EARS notation, no BDD scenarios, no epic hierarchy. Just tasks with quality guarantees.

## What Makes This Different?

Most AI coding tools generate code without guardrails. Agentecflow adds:

1. **Architectural Review (Phase 2.5)** - Catches design issues before implementation
   - Evaluates SOLID principles, DRY violations, YAGNI concerns
   - Scoring: 0-100 (≥80 auto-approve, 60-79 approve with recommendations, <60 reject)
   - Optional human checkpoint for critical tasks

2. **Test Enforcement (Phase 4.5)** - Never complete with failing tests
   - Verifies code compiles before testing
   - Up to 3 automatic fix attempts for failing tests
   - Task only completes when ALL tests pass (100%)

3. **Specialized Stack Agents** - Better code quality
   - React: State management, testing patterns, component design
   - Python: FastAPI patterns, pytest best practices, async/await
   - .NET MAUI: MVVM, Domain layer, functional error handling
   - TypeScript: NestJS, Result patterns, domain modeling

## When to Use Agentecflow

**Use when**:
- You want AI assistance with quality guardrails
- You're tired of AI generating code that doesn't compile
- You want architectural review before implementation
- You want task tracking without project management overhead

**Don't use when**:
- You need formal requirements management (see [agentecflow-requirements](https://github.com/yourusername/agentecflow-requirements))
- You need epic/feature hierarchy
- You need PM tool synchronization (Jira, Linear, GitHub Projects)

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [Quality Gates Explained](docs/QUALITY-GATES.md) - Phase 2.5, 4.5 in detail
- [Stack Templates](docs/STACK-TEMPLATES.md) - Customize for your stack

## Supported Technology Stacks

- **React** - TypeScript, Next.js, Tailwind CSS, Vite, Vitest, Playwright
- **Python** - FastAPI, pytest, LangGraph, Pydantic, Streamlit
- **TypeScript API** - NestJS, Result patterns, domain modeling
- **.NET MAUI (AppShell)** - Mobile apps with AppShell navigation, MVVM, ErrorOr
- **.NET MAUI (NavigationPage)** - Mobile apps with NavigationPage stack, MVVM, ErrorOr
- **.NET Microservice** - FastEndpoints, Either monad, OpenTelemetry
- **Default** - Language-agnostic base for any stack

## Design Integration (Optional)

Convert Figma/Zeplin designs to pixel-perfect code with visual regression testing:

- `/figma-to-react` - Figma → React components with Playwright testing
- `/zeplin-to-maui` - Zeplin → .NET MAUI XAML with platform testing

## Philosophy

1. **Simple by default** - Complex when needed
2. **Quality over speed** - But both when possible
3. **Markdown-driven** - Human and AI readable
4. **Git-native** - Everything version controlled
5. **No vendor lock-in** - Plain markdown files

## Contributing

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT - See [LICENSE](LICENSE)

## Related Projects

- [agentecflow-requirements](https://github.com/yourusername/agentecflow-requirements) - Full requirements management system
- [agentecflow-platform](https://github.com/yourusername/agentecflow-platform) - Enterprise team collaboration features

## Credits

Built with [Claude Code](https://claude.ai/code).
```

## Verification

```bash
# Repository structure check
tree -L 3 -a

# Expected output:
# .
# ├── .git/
# ├── .github/
# │   └── workflows/
# ├── .gitignore
# ├── LICENSE
# ├── README.md
# ├── docs/
# ├── installer/
# │   ├── global/
# │   │   ├── agents/
# │   │   ├── commands/
# │   │   ├── instructions/
# │   │   └── templates/
# │   └── scripts/
# └── tests/

# Repository access check
gh repo view yourusername/agentecflow
```

## Estimated Time

1 hour

## Notes

- README.md emphasizes **pragmatic developers**, not enterprise
- No mention of EARS, BDD, epics, features
- Clear positioning: "No ceremony, just quality gates"
- Links to agentecflow-requirements for those who need full system
