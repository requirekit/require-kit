---
id: TASK-DOCS-001
title: Audit documentation structure and create content organization plan
status: completed
created: 2025-11-06T00:00:00Z
updated: 2025-11-06T15:15:00Z
completed: 2025-11-06T15:15:00Z
priority: high
tags: [documentation, mkdocs, github-pages, planning]
epic: null
feature: null
requirements: []
dependencies: []
complexity_evaluation:
  score: 3
  level: "simple"
  review_mode: "AUTO_PROCEED"
  factor_scores:
    - factor: "file_complexity"
      score: 1
      max_score: 3
      justification: "Analysis task, no file creation"
    - factor: "pattern_familiarity"
      score: 0
      max_score: 2
      justification: "Standard documentation audit"
    - factor: "risk_level"
      score: 0
      max_score: 3
      justification: "Zero risk - analysis only"
    - factor: "dependencies"
      score: 2
      max_score: 2
      justification: "Requires understanding of current doc structure"
completion_notes:
  deliverable: "docs/planning/documentation-organization-plan.md"
  file_size: "24KB (687 lines)"
  directories_inventoried: 23
  files_catalogued: 147
  navigation_sections: 11
  landing_pages_identified: 28
  priorities: "P0: 9 pages, P1: 11 pages, P2: 8 pages"
---

# Task: Audit Documentation Structure and Create Content Organization Plan

## Context

The RequireKit repository has approximately 24 subdirectories in the docs/ folder, mixing:
- **User-facing documentation** (guides/, requirements/, features/)
- **Development artifacts** (implementation-plans/, tests/, fixes/)
- **Architecture decisions** (adr/)
- **Internal research** (research/, analysis/, state/)

Setting up MkDocs + Material for GitHub Pages will provide professional documentation for users learning EARS notation, BDD/Gherkin scenarios, and epic/feature hierarchy management.

**Goal**: Create a clear plan for organizing docs into user-facing vs internal content, determining what should be prominent in the documentation site.

## Objective

Analyze the current documentation structure and create a content organization plan that separates user-facing docs (prominent) from internal development docs (still accessible but less prominent).

## Requirements

### Documentation Inventory
- [x] List all ~24 doc subdirectories with brief descriptions
- [x] Categorize each as: User-Facing, Developer/Contributor, Internal/Temporary
- [x] Identify missing key user docs (index.md, quickstart.md, etc.)
- [x] Map existing comprehensive guides to suggested simple guides

### Content Categorization

**User-Facing (Prominent)**:
- [x] Identify all guides meant for end users
- [x] Identify EARS notation documentation
- [x] Identify BDD/Gherkin generation guides
- [x] Identify epic/feature management guides
- [x] Identify requirements gathering documentation
- [x] Identify troubleshooting guides

**Developer/Contributor (Accessible)**:
- [x] Identify ADRs (architecture decision records)
- [x] Identify contributing guides
- [x] Identify architecture documentation
- [x] Identify testing documentation

**Internal/Temporary (Exclude from Site)**:
- [x] Identify implementation plans
- [x] Identify test artifacts
- [x] Identify state tracking documents
- [x] Identify research/analysis documents
- [x] Identify fix summaries

### Navigation Structure Design
- [x] Design main navigation tabs (Getting Started, Core Concepts, Advanced, etc.)
- [x] Map existing docs to navigation structure
- [x] Identify landing pages needed (aggregate existing content)
- [x] Create navigation hierarchy (3 levels max recommended)

### Gap Analysis
- [x] List missing landing pages
- [x] List missing quickstart content
- [x] List missing FAQ
- [x] List missing troubleshooting content

## Acceptance Criteria

### Documentation Inventory ✅
- [x] All ~24 subdirectories catalogued
- [x] Each directory categorized (User/Developer/Internal)
- [x] File count per directory noted
- [x] Key files in each directory identified

### Content Map ✅
- [x] User-facing docs clearly identified
- [x] Developer docs clearly identified
- [x] Internal docs clearly identified
- [x] Mapping rationale documented

### Navigation Design ✅
- [x] Multi-level navigation structure proposed
- [x] All user-facing docs mapped to navigation
- [x] No navigation deeper than 3 levels
- [x] Clear hierarchy (Home → Section → Page)

### Gap Analysis ✅
- [x] Missing pages identified
- [x] For each gap, note if: create new OR aggregate existing OR link to existing
- [x] Priority ranking (must-have vs nice-to-have)

### Deliverable ✅
- [x] Markdown document: `docs/planning/documentation-organization-plan.md`
- [x] Contains: inventory, categorization, navigation design, gap analysis
- [x] Ready to inform TASK-DOCS-002 (MkDocs configuration)

## Implementation Plan

### Phase 1: Directory Inventory
1. List all docs/ subdirectories
2. Count files in each
3. Read 1-2 sample files per directory to understand purpose
4. Categorize each directory

### Phase 2: Content Analysis
1. Identify key user-facing guides
2. Identify workflow documentation
3. Identify pattern documentation
4. Identify MCP setup guides
5. Identify developer documentation

### Phase 3: Navigation Design
1. Sketch main navigation tabs
2. Map docs to tabs
3. Identify missing landing pages
4. Design 3-level hierarchy

### Phase 4: Gap Analysis
1. Compare existing docs to ChatGPT suggestions
2. Note what exists vs what's missing
3. Decide: create new, aggregate existing, or link to existing
4. Prioritize gaps

### Phase 5: Documentation
1. Create planning document
2. Include inventory table
3. Include navigation structure diagram
4. Include gap analysis with recommendations

## Expected Deliverable Structure

```markdown
# RequireKit Documentation Organization Plan

## Current Structure Inventory

| Directory | Files | Category | Purpose |
|-----------|-------|----------|---------|
| requirements/ | X | User-Facing | EARS requirements |
| features/ | X | User-Facing | Feature specifications |
| integration/ | X | User-Facing | Integration guides |
| quick-reference/ | X | User-Facing | Quick reference materials |
| ... | ... | ... | ... |

## Categorization

### User-Facing (Prominent in Site)
- requirements/ - EARS notation requirements
- features/ - Feature specifications and examples
- integration/ - Taskwright integration guides
- quick-reference/ - Quick reference materials
- ...

### Developer/Contributor (Accessible in Site)
- adr/ - Architecture decision records
- troubleshooting/ - Troubleshooting guides
- ...

### Internal/Temporary (Exclude from Site)
- implementation-plans/ - Implementation artifacts
- tests/ - Test execution results
- state/ - State tracking documents
- ...

## Proposed Navigation Structure

```
Home (index.md)
├── Getting Started
│   ├── Quickstart
│   ├── Installation (link to README section)
│   └── Integration with Taskwright
├── Core Concepts
│   ├── EARS Notation Patterns
│   ├── BDD/Gherkin Generation
│   ├── Epic/Feature Hierarchy
│   └── Requirements Traceability
├── Guides
│   ├── Requirements Gathering
│   ├── Formalizing Requirements
│   └── Generating BDD Scenarios
...
```

## Gap Analysis

### Missing Landing Pages
- [ ] docs/index.md - Site home (aggregate README + links)
- [ ] docs/getting-started/index.md - Getting started section home
- ...

### Missing Content
- [ ] docs/faq.md - Frequently asked questions
- ...

### Existing Content to Reuse
- ✅ Existing requirements examples
- ✅ Existing feature specifications
- ✅ Integration documentation
- ...
```

## Success Criteria

### Deliverables
- [x] Planning document created at `docs/planning/documentation-organization-plan.md`
- [x] All 23 subdirectories + 1 root file inventoried
- [x] Navigation structure designed
- [x] Gap analysis completed

### Quality Metrics
- [x] Every existing doc file accounted for (147+ files)
- [x] Clear rationale for each categorization
- [x] Navigation structure has clear hierarchy (11 sections, ≤3 levels)
- [x] Gap analysis prioritized (P0: 9, P1: 11, P2: 8)

### Ready for Next Task
- [x] Plan informs MkDocs nav configuration
- [x] Plan identifies which landing pages to create
- [x] Plan specifies what to include/exclude from site build

## Completion Summary

### What Was Delivered

1. **Complete Directory Inventory**
   - 23 subdirectories + 1 root file catalogued
   - 147+ total files (125+ markdown files)
   - File counts for each directory
   - Largest directories: research/ (56 files), state/ (31 files)

2. **Content Categorization**
   - **User-Facing**: 7 directories + 1 file (guides/, quick-reference/, mcp-setup/, troubleshooting/, INTEGRATION-GUIDE.md, requirements/, features/)
   - **Developer/Contributor**: 4 directories (adr/, architecture/, shared/, templates/)
   - **Internal/Temporary**: 12 directories (research/, state/, implementation-plans/, test_reports/, tests/, reviews/, fixes/, proposals/, migration/, requirements-gathering-api/, analysis/, implementation/)

3. **Navigation Structure Design**
   - 11 main sections with ≤3 level hierarchy
   - Clear paths: Home → Getting Started → Core Concepts → User Guides → Commands → MCP Setup → Integration → Quick Reference → Examples → Developer Docs → Troubleshooting
   - All user-facing content mapped to navigation

4. **Gap Analysis**
   - 28 missing landing pages identified
   - Prioritized: 9 P0 (critical), 11 P1 (important), 8 P2 (nice-to-have)
   - Content sources specified for each page (extract vs aggregate vs create new)

5. **Implementation Recommendations**
   - Phased approach for creating landing pages
   - MkDocs configuration guidance (exclude patterns, theme settings)
   - Detailed guidance for TASK-DOCS-002 and TASK-DOCS-003

### Key Deliverable

**File**: `docs/planning/documentation-organization-plan.md`
- **Size**: 24KB (687 lines)
- **Sections**: 6 major sections with detailed tables and recommendations
- **Ready for**: TASK-DOCS-002 (MkDocs configuration), TASK-DOCS-003 (Landing pages)

## Notes

### Key Decisions Needed

1. **What to exclude from site build?**
   - Recommendation: Exclude implementation/, test_reports/, fixes/, research/
   - Keep in repo but use MkDocs exclude pattern

2. **How to handle integration docs?**
   - RequireKit can work standalone or with taskwright
   - Make integration optional but clear in navigation

3. **Versioned docs?**
   - User said "keep it simple, no versioning for now"
   - Plan for single version initially

4. **Custom domain?**
   - Decision pending (separate task)
   - Plan should work with both GitHub Pages default and custom domain

### Reusability for Taskwright

This task format was copied from Taskwright repo and adapted for RequireKit. The audit process is similar but the content focuses on requirements management rather than task execution.

## Timeline Estimate

**Estimated Duration**: 1-2 hours
**Actual Duration**: ~1.5 hours

### Breakdown:
- Directory inventory: 30 minutes
- Content analysis: 30 minutes
- Navigation design: 20 minutes
- Gap analysis: 20 minutes
- Documentation: 20 minutes

## Related Documents

- `/docs/` - All existing documentation
- ChatGPT conversation about MkDocs setup
- README.md - Current user-facing documentation
- `docs/planning/documentation-organization-plan.md` - Deliverable

## Next Steps After Completion

After this task completes:
1. Move to TASK-DOCS-002: Create MkDocs configuration
2. Use this plan to design mkdocs.yml nav structure
3. Use gap analysis to create TASK-DOCS-003: Create landing pages
