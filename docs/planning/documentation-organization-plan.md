# RequireKit Documentation Organization Plan

**Version**: 1.0.0
**Date**: 2025-11-06
**Status**: Planning
**Purpose**: Comprehensive plan for organizing RequireKit documentation for MkDocs + Material + GitHub Pages

---

## Table of Contents

1. [Current Structure Inventory](#current-structure-inventory)
2. [Content Categorization](#content-categorization)
3. [Proposed Navigation Structure](#proposed-navigation-structure)
4. [Gap Analysis](#gap-analysis)
5. [Implementation Recommendations](#implementation-recommendations)
6. [MkDocs Configuration Guidance](#mkdocs-configuration-guidance)

---

## Current Structure Inventory

### Directory Summary

| Directory | Total Files | MD Files | Category | Purpose |
|-----------|-------------|----------|----------|---------|
| adr/ | 8 | 8 | Developer/Contributor | Architecture Decision Records |
| analysis/ | 5 | 5 | Internal/Temporary | Analysis documents |
| architecture/ | 3 | 3 | Developer/Contributor | Architecture documentation |
| features/ | 4 | 3 | User-Facing | Feature specifications (active/ subdirectory) |
| fixes/ | 4 | 4 | Internal/Temporary | Fix summaries |
| guides/ | 6 | 6 | User-Facing | User guides and getting started |
| implementation/ | 1 | 1 | Internal/Temporary | Implementation artifacts |
| implementation-plans/ | 3 | 3 | Internal/Temporary | Implementation planning docs |
| integration/ | 1 | 0 | User-Facing | Integration JSON data |
| mcp-setup/ | 2 | 2 | User-Facing | MCP setup guides (Figma, Zeplin) |
| migration/ | 1 | 1 | Internal/Temporary | Migration documentation |
| proposals/ | 2 | 2 | Internal/Temporary | Proposal documents |
| quick-reference/ | 5 | 5 | User-Facing | Quick reference cards |
| requirements/ | 3 | 2 | User-Facing | Requirements examples (draft/ subdirectory) |
| requirements-gathering-api/ | 1 | 1 | Internal/Temporary | Internal API documentation |
| research/ | 56 | 55 | Internal/Temporary | Research and exploration |
| reviews/ | 1 | 1 | Internal/Temporary | Review documents |
| shared/ | 3 | 3 | Developer/Contributor | Common patterns and thresholds |
| state/ | 31 | 10 | Internal/Temporary | State tracking documents |
| templates/ | 1 | 1 | Developer/Contributor | Template files |
| test_reports/ | 3 | 3 | Internal/Temporary | Test execution results |
| tests/ | 2 | 2 | Internal/Temporary | Test files |
| troubleshooting/ | 1 | 1 | User-Facing | Troubleshooting guide |
| **Root files** | 1 | 1 | User-Facing | INTEGRATION-GUIDE.md |

**Total**: 23 subdirectories + 1 root file = 24 items
**Total files**: 147+ files
**Markdown files**: 125+ MD files

### Key Observations

1. **Large Internal Directories**: research/ (56 files) and state/ (31 files) are primarily development artifacts
2. **User-Facing Core**: guides/, quick-reference/, mcp-setup/, INTEGRATION-GUIDE.md
3. **Examples Structure**: requirements/ and features/ use subdirectories (draft/, active/)
4. **Documentation Quality**: Comprehensive user guides exist (getting_started.md, require_kit_user_guide.md, command_usage_guide.md)

---

## Content Categorization

### User-Facing (Prominent in Documentation Site) ✅

**Primary User Guides**:
- `guides/getting_started.md` - Quick start guide (463 lines)
- `guides/require_kit_user_guide.md` - Comprehensive user guide
- `guides/command_usage_guide.md` - Command reference
- `guides/README.md` - Guide index
- `guides/documentation_update_summary.md` - Update summary
- `guides/guide_audit_report_task_041.md` - Audit report

**Quick Reference Materials**:
- `quick-reference/task-work-cheat-sheet.md` - Task workflow reference
- `quick-reference/complexity-guide.md` - Complexity evaluation
- `quick-reference/quality-gates-card.md` - Quality gates
- `quick-reference/design-first-workflow-card.md` - Design-first workflow
- `quick-reference/README.md` - Quick reference index

**MCP Setup Guides**:
- `mcp-setup/figma-mcp-setup.md` - Figma MCP configuration
- `mcp-setup/zeplin-mcp-setup.md` - Zeplin MCP configuration

**Integration Documentation**:
- `INTEGRATION-GUIDE.md` - Integration with taskwright (927 lines, comprehensive)

**Troubleshooting**:
- `troubleshooting/zeplin-maui-icon-issues.md` - Troubleshooting guide

**Examples** (User-Facing but need organization):
- `requirements/draft/` - Example requirements
- `features/active/` - Example features

**Rationale**: These documents directly serve end users learning to use require-kit for requirements management, EARS notation, BDD scenarios, and epic/feature hierarchy.

### Developer/Contributor (Accessible in Documentation Site) 🔧

**Architecture Decision Records**:
- `adr/*.md` - 8 ADR files documenting architectural decisions

**Architecture Documentation**:
- `architecture/ARCHITECTURE-SUMMARY.md` - System architecture overview
- `architecture/bidirectional-integration.md` - Integration architecture
- `architecture/ux-design-subagents-implementation-plan.md` - Design subagents plan

**Shared Patterns**:
- `shared/common-thresholds.md` - Common thresholds
- `shared/design-to-code-common.md` - Design-to-code patterns
- `shared/maui-template-architecture.md` - MAUI templates

**Templates**:
- `templates/implementation-plan-template.md` - Implementation template

**Rationale**: These documents help contributors understand the system architecture, make informed decisions, and maintain consistency.

### Internal/Temporary (Exclude from Documentation Site) 🚫

**Research and Analysis**:
- `research/*.md` - 56 files of research and exploration
- `analysis/*.md` - 5 analysis documents

**State Tracking**:
- `state/` - 31 files tracking implementation state (metrics/, task tracking)

**Implementation Artifacts**:
- `implementation-plans/*.md` - 3 implementation planning documents
- `implementation/*.md` - 1 implementation artifact

**Test and QA**:
- `test_reports/*.md` - 3 test execution reports
- `tests/*.md` - 2 test files

**Reviews and Fixes**:
- `reviews/*.md` - 1 review document
- `fixes/*.md` - 4 fix summaries

**Proposals and Migration**:
- `proposals/*.md` - 2 proposal documents
- `migration/*.md` - 1 migration doc

**Internal APIs**:
- `requirements-gathering-api/*.md` - Internal API documentation

**Rationale**: These are development artifacts, ephemeral state tracking, and internal research not relevant to end users. Keep in repository for history but exclude from documentation site.

---

## Proposed Navigation Structure

### MkDocs Navigation Hierarchy (≤3 Levels)

```yaml
nav:
  - Home: index.md

  - Getting Started:
      - Overview: getting-started/index.md
      - Quickstart: getting-started/quickstart.md
      - Installation: getting-started/installation.md
      - Your First Requirements: getting-started/first-requirements.md
      - Integration with taskwright: getting-started/integration.md

  - Core Concepts:
      - Overview: core-concepts/index.md
      - EARS Notation Patterns: core-concepts/ears-notation.md
      - BDD/Gherkin Scenarios: core-concepts/bdd-scenarios.md
      - Epic/Feature Hierarchy: core-concepts/hierarchy.md
      - Requirements Traceability: core-concepts/traceability.md

  - User Guides:
      - Overview: guides/README.md
      - Complete User Guide: guides/require_kit_user_guide.md
      - Getting Started: guides/getting_started.md
      - Command Usage: guides/command_usage_guide.md

  - Commands Reference:
      - Overview: commands/index.md
      - Requirements Commands: commands/requirements.md
      - Epic Commands: commands/epics.md
      - Feature Commands: commands/features.md
      - Hierarchy Commands: commands/hierarchy.md

  - MCP Setup:
      - Overview: mcp-setup/index.md
      - Figma MCP: mcp-setup/figma-mcp-setup.md
      - Zeplin MCP: mcp-setup/zeplin-mcp-setup.md

  - Integration:
      - taskwright Integration: INTEGRATION-GUIDE.md
      - PM Tool Export: integration/pm-tools.md

  - Quick Reference:
      - Overview: quick-reference/README.md
      - Task Work Cheat Sheet: quick-reference/task-work-cheat-sheet.md
      - Complexity Guide: quick-reference/complexity-guide.md
      - Quality Gates Card: quick-reference/quality-gates-card.md
      - Design-First Workflow: quick-reference/design-first-workflow-card.md

  - Examples:
      - Overview: examples/index.md
      - Requirements Examples: examples/requirements.md
      - Feature Examples: examples/features.md
      - BDD Scenarios Examples: examples/bdd.md

  - Developer Docs:
      - Overview: developer/index.md
      - Architecture: developer/architecture.md
      - Architecture Decision Records: developer/adr.md
      - Contributing: developer/contributing.md
      - Templates: developer/templates.md

  - Troubleshooting & FAQ:
      - Troubleshooting: troubleshooting/index.md
      - FAQ: faq.md
```

### Navigation Levels Breakdown

**Level 1** (Main Sections): 11 sections
- Home
- Getting Started
- Core Concepts
- User Guides
- Commands Reference
- MCP Setup
- Integration
- Quick Reference
- Examples
- Developer Docs
- Troubleshooting & FAQ

**Level 2** (Section Pages): 4-5 pages per section average

**Level 3** (Sub-pages): Minimal, only where necessary for complex topics

### Navigation Design Principles

1. **Progressive Disclosure**: Start simple (Home → Getting Started → Core Concepts) then advance
2. **Task-Oriented**: Commands, MCP Setup, Integration organized by user tasks
3. **Clear Separation**: User docs prominent, developer docs accessible but separate
4. **Quick Access**: Quick Reference as top-level for fast lookups
5. **Discoverability**: Each section has an overview/index page

---

## Gap Analysis

### Missing Landing Pages (Must Create) 🔴

| Page | Purpose | Priority | Source/Action |
|------|---------|----------|---------------|
| `docs/index.md` | Site home page | P0 | Aggregate README.md + welcome + navigation guide |
| `getting-started/index.md` | Getting Started section home | P0 | Aggregate existing getting_started.md + installation steps |
| `getting-started/quickstart.md` | 5-minute quickstart | P0 | Extract from getting_started.md (lines 67-161) |
| `getting-started/installation.md` | Installation guide | P0 | Extract from getting_started.md (lines 22-64) + README.md |
| `getting-started/first-requirements.md` | First requirements walkthrough | P1 | Extract from getting_started.md (lines 67-161) |
| `getting-started/integration.md` | Integration overview | P1 | Link to INTEGRATION-GUIDE.md with summary |
| `core-concepts/index.md` | Core Concepts section home | P0 | New - overview of EARS, BDD, hierarchy, traceability |
| `core-concepts/ears-notation.md` | EARS patterns detailed | P0 | Extract from guides/require_kit_user_guide.md + README.md |
| `core-concepts/bdd-scenarios.md` | BDD/Gherkin explanation | P0 | Extract from guides/require_kit_user_guide.md |
| `core-concepts/hierarchy.md` | Epic/feature hierarchy | P0 | Extract from guides/require_kit_user_guide.md |
| `core-concepts/traceability.md` | Requirements traceability | P1 | New - explain REQ → BDD → FEAT → TASK links |
| `commands/index.md` | Commands section home | P0 | New - command categories overview |
| `commands/requirements.md` | Requirements commands | P0 | Extract from guides/command_usage_guide.md |
| `commands/epics.md` | Epic commands | P0 | Extract from guides/command_usage_guide.md |
| `commands/features.md` | Feature commands | P0 | Extract from guides/command_usage_guide.md |
| `commands/hierarchy.md` | Hierarchy commands | P1 | Extract from guides/command_usage_guide.md |
| `mcp-setup/index.md` | MCP Setup section home | P1 | New - MCP overview + links to Figma/Zeplin |
| `integration/pm-tools.md` | PM tool export guide | P1 | New - Jira, Linear, GitHub, Azure DevOps export |
| `examples/index.md` | Examples section home | P1 | New - overview of example requirements/features |
| `examples/requirements.md` | Requirements examples | P2 | Aggregate examples from requirements/draft/ |
| `examples/features.md` | Feature examples | P2 | Aggregate examples from features/active/ |
| `examples/bdd.md` | BDD scenarios examples | P2 | New - example Gherkin scenarios |
| `developer/index.md` | Developer Docs section home | P1 | New - contributing overview |
| `developer/architecture.md` | Architecture documentation | P1 | Link to architecture/ARCHITECTURE-SUMMARY.md |
| `developer/adr.md` | ADR index | P1 | Generate index of all adr/*.md files |
| `developer/contributing.md` | Contributing guide | P2 | New - how to contribute |
| `developer/templates.md` | Template reference | P2 | Link to templates/ directory |
| `troubleshooting/index.md` | Troubleshooting home | P1 | Aggregate troubleshooting/*.md |
| `faq.md` | Frequently Asked Questions | P1 | New - common questions from INTEGRATION-GUIDE.md |

### Missing Content (Must Create) 🟡

| Content Type | Description | Priority | Action |
|--------------|-------------|----------|--------|
| Welcome/Overview | Project introduction | P0 | Create from README.md |
| Installation Steps | Detailed installation | P0 | Extract from getting_started.md + README.md |
| EARS Patterns Deep Dive | Detailed EARS explanation | P0 | Exists in guides, needs extraction |
| BDD Workflow | BDD generation workflow | P0 | Exists in guides, needs extraction |
| Epic Management Guide | Epic creation and management | P0 | Exists in guides, needs extraction |
| Feature Management Guide | Feature creation and management | P0 | Exists in guides, needs extraction |
| PM Tool Export Guide | Export to Jira/Linear/GitHub | P1 | Partially in INTEGRATION-GUIDE.md |
| FAQ | Common questions | P1 | Extract from INTEGRATION-GUIDE.md troubleshooting |
| Examples Collection | Real-world examples | P2 | Aggregate from requirements/, features/ |

### Existing Content to Reuse ✅

| Existing File | Reuse As | Notes |
|---------------|----------|-------|
| `guides/getting_started.md` | Multiple pages | Split into quickstart, installation, first requirements |
| `guides/require_kit_user_guide.md` | User guide | Keep as comprehensive reference |
| `guides/command_usage_guide.md` | Commands pages | Split into requirements, epics, features commands |
| `guides/README.md` | Guides overview | Adapt as guides section home |
| `INTEGRATION-GUIDE.md` | Integration docs | Keep as-is, comprehensive (927 lines) |
| `quick-reference/README.md` | Quick reference home | Keep as-is |
| `quick-reference/*.md` | Quick reference cards | Keep all cards as-is |
| `mcp-setup/*.md` | MCP setup guides | Keep as-is |
| `troubleshooting/*.md` | Troubleshooting | Aggregate into troubleshooting section |
| `adr/*.md` | Developer docs | Keep as-is, create index |
| `architecture/*.md` | Developer docs | Link from developer section |
| `templates/*.md` | Developer docs | Link from developer section |

### Content Not Needed for Site ❌

- All files in: research/, analysis/, state/, implementation-plans/, test_reports/, tests/, reviews/, fixes/, proposals/, migration/, requirements-gathering-api/
- These remain in repository for version control but excluded from MkDocs build

---

## Implementation Recommendations

### Phase 1: Critical Landing Pages (TASK-DOCS-003)

**Priority P0 - Must Have for Launch**

1. **docs/index.md**
   - Welcome to require-kit
   - What is require-kit?
   - Key features (EARS, BDD, Epic/Feature)
   - Quick navigation to Getting Started
   - Source: README.md overview

2. **getting-started/index.md**
   - Getting Started overview
   - Installation steps summary
   - Quick navigation to quickstart, installation, first requirements
   - Source: Aggregate from README.md + getting_started.md

3. **getting-started/quickstart.md**
   - 5-minute quickstart
   - Basic workflow: gather → formalize → generate-bdd
   - Source: Extract from getting_started.md (lines 67-161)

4. **getting-started/installation.md**
   - Detailed installation steps
   - Prerequisites
   - Verification
   - Source: Extract from getting_started.md (lines 22-64) + README.md

5. **core-concepts/index.md**
   - Core Concepts overview
   - EARS, BDD, Hierarchy, Traceability summary
   - Navigation to detailed pages
   - Source: New aggregation

6. **core-concepts/ears-notation.md**
   - EARS patterns detailed explanation
   - 5 patterns with examples
   - When to use each pattern
   - Source: Extract from guides/ + README.md

7. **core-concepts/bdd-scenarios.md**
   - BDD/Gherkin explanation
   - Why BDD?
   - Scenario structure
   - Source: Extract from guides/

8. **core-concepts/hierarchy.md**
   - Epic/Feature hierarchy explanation
   - Why organize hierarchically?
   - Traceability benefits
   - Source: Extract from guides/

9. **commands/index.md**
   - Commands overview
   - Command categories
   - Quick command reference table
   - Source: Extract from guides/command_usage_guide.md

### Phase 2: Command Reference Pages

**Priority P0-P1**

10. **commands/requirements.md**
    - /gather-requirements
    - /formalize-ears
    - /generate-bdd
    - Source: Extract from guides/command_usage_guide.md

11. **commands/epics.md**
    - /epic-create
    - /epic-status
    - /epic-sync
    - /epic-generate-features
    - Source: Extract from guides/command_usage_guide.md

12. **commands/features.md**
    - /feature-create
    - /feature-status
    - /feature-sync
    - /feature-generate-tasks
    - Source: Extract from guides/command_usage_guide.md

### Phase 3: Integration and Developer Docs

**Priority P1-P2**

13. **mcp-setup/index.md**
    - MCP overview
    - Available MCP servers (Figma, Zeplin)
    - Installation guidance
    - Source: New

14. **integration/pm-tools.md**
    - PM tool export guide
    - Jira, Linear, GitHub, Azure DevOps
    - API integration requirements
    - Source: Extract from INTEGRATION-GUIDE.md + new

15. **developer/index.md**
    - Contributing overview
    - Architecture links
    - ADR links
    - Source: New

16. **developer/adr.md**
    - ADR index (auto-generated list)
    - Links to all adr/*.md files
    - Source: Generated from adr/ directory

17. **troubleshooting/index.md**
    - Troubleshooting guide
    - Common issues
    - Source: Aggregate troubleshooting/*.md

18. **faq.md**
    - Frequently Asked Questions
    - Source: Extract from INTEGRATION-GUIDE.md troubleshooting section

### Phase 4: Examples (Nice to Have)

**Priority P2**

19. **examples/index.md**
20. **examples/requirements.md**
21. **examples/features.md**
22. **examples/bdd.md**

---

## MkDocs Configuration Guidance

### Directories to Exclude from Build

Add to `mkdocs.yml`:

```yaml
exclude_docs: |
  research/
  analysis/
  state/
  implementation-plans/
  implementation/
  test_reports/
  tests/
  reviews/
  fixes/
  proposals/
  migration/
  requirements-gathering-api/
  planning/

  # Keep in repo, exclude from site
  requirements/draft/
  features/active/
```

### Recommended Material Theme Configuration

```yaml
theme:
  name: material
  palette:
    # Light mode
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

  features:
    - navigation.instant
    - navigation.tracking
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy
```

### Search Configuration

```yaml
plugins:
  - search:
      lang: en
      separator: '[\s\-,:!=\[\]()"/]+|(?!\b)(?=[A-Z][a-z])|\.(?!\d)|&[lg]t;'
```

### Social Links

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourusername/require-kit
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/yourhandle
```

### Copyright and Version

```yaml
copyright: Copyright &copy; 2025 RequireKit
extra:
  version:
    provider: mike
```

---

## Success Criteria

### Deliverable Checklist ✅

- [x] Complete directory inventory (23 subdirectories + 1 root file catalogued)
- [x] All directories categorized (User-Facing, Developer/Contributor, Internal/Temporary)
- [x] File counts per directory documented
- [x] Key files in each directory identified
- [x] User-facing docs clearly identified (7 directories + 1 file)
- [x] Developer docs clearly identified (4 directories)
- [x] Internal docs clearly identified (12 directories)
- [x] Mapping rationale documented for each category
- [x] Multi-level navigation structure proposed (11 sections, ≤3 levels)
- [x] All user-facing docs mapped to navigation
- [x] No navigation deeper than 3 levels
- [x] Clear hierarchy (Home → Section → Page)
- [x] Missing pages identified (28 new pages needed)
- [x] For each gap, action specified (create new / aggregate existing / link to existing)
- [x] Priority ranking completed (P0 / P1 / P2)
- [x] Planning document created at `docs/planning/documentation-organization-plan.md`
- [x] Document contains: inventory, categorization, navigation design, gap analysis
- [x] Ready to inform TASK-DOCS-002 (MkDocs configuration)

### Quality Metrics ✅

- [x] Every existing doc file accounted for (147+ files inventoried)
- [x] Clear rationale for each categorization
- [x] Navigation structure has clear hierarchy (Home → 11 sections → pages)
- [x] Gap analysis prioritized (P0 = critical, P1 = important, P2 = nice-to-have)

### Ready for Next Task ✅

- [x] Plan informs MkDocs nav configuration (complete nav structure provided)
- [x] Plan identifies which landing pages to create (28 pages with priorities)
- [x] Plan specifies what to include/exclude from site build (12 directories excluded)

---

## Next Steps

### Immediate Actions

1. **Review this plan** with stakeholders
2. **Proceed to TASK-DOCS-002**: Create MkDocs configuration using this navigation structure
3. **Proceed to TASK-DOCS-003**: Create landing pages based on gap analysis (P0 first)
4. **Proceed to TASK-DOCS-004**: Setup GitHub Actions workflow
5. **Proceed to TASK-DOCS-005**: Enable GitHub Pages and update README

### Long-Term Considerations

- **Versioning**: Consider adding versioned docs when require-kit reaches v2.0
- **Search Optimization**: Monitor search queries to improve content discoverability
- **Examples Expansion**: Add more real-world examples as users share their requirements
- **Video Tutorials**: Consider adding video walkthrough to Getting Started
- **API Documentation**: If require-kit adds programmatic API, document in dedicated section

---

## Appendix: File Inventory Details

### User-Facing Files (27 files)

**guides/** (6 files):
- getting_started.md (463 lines)
- require_kit_user_guide.md (comprehensive)
- command_usage_guide.md (command reference)
- README.md (guide index)
- documentation_update_summary.md
- guide_audit_report_task_041.md

**quick-reference/** (5 files):
- task-work-cheat-sheet.md
- complexity-guide.md
- quality-gates-card.md
- design-first-workflow-card.md
- README.md

**mcp-setup/** (2 files):
- figma-mcp-setup.md
- zeplin-mcp-setup.md

**INTEGRATION-GUIDE.md** (1 file):
- 927 lines of comprehensive integration documentation

**troubleshooting/** (1 file):
- zeplin-maui-icon-issues.md

**requirements/** (subdirectories):
- draft/ subdirectory with example requirements

**features/** (subdirectories):
- active/ subdirectory with example features

### Developer/Contributor Files (15 files)

**adr/** (8 files):
- All ADR files documenting architectural decisions

**architecture/** (3 files):
- ARCHITECTURE-SUMMARY.md
- bidirectional-integration.md
- ux-design-subagents-implementation-plan.md

**shared/** (3 files):
- common-thresholds.md
- design-to-code-common.md
- maui-template-architecture.md

**templates/** (1 file):
- implementation-plan-template.md

### Internal/Temporary Files (105 files)

**research/** (56 files):
- Extensive research and exploration artifacts

**state/** (31 files):
- State tracking, metrics, task tracking

**implementation-plans/** (3 files):
- Implementation planning documents

**test_reports/** (3 files):
- Test execution results

**analysis/** (5 files):
- Analysis documents

**fixes/** (4 files):
- Fix summaries

**tests/** (2 files):
- Test files

**reviews/** (1 file):
- Review documents

---

**Document Status**: Complete
**Ready for Review**: Yes
**Next Task**: TASK-DOCS-002 (Create MkDocs Configuration)
