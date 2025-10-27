# MAUI Template Migration Plan

## Executive Summary

This document outlines the migration from MyDrive-specific MAUI template to a dual-template system:
- **Global generic templates** for new projects (Domain pattern, verb-based naming)
- **Local custom templates** for project-specific patterns (Engine pattern, custom naming)

## Goals

1. ✅ Create two generic global MAUI templates (AppShell + NavigationPage)
2. ✅ Use Domain pattern with verb-based naming (no UseCase/Engine suffix)
3. ✅ Separate Repositories (database) from Services (APIs/hardware)
4. ✅ Preserve MyDrive-specific patterns in local template
5. ✅ Enable projects to create custom local templates
6. ✅ Maintain backward compatibility

## Current State Analysis

### Existing MAUI Template (`installer/global/templates/maui/`)

**Issues**:
- ❌ MyDrive-specific namespace (`DeCUK.Mobile.MyDrive`)
- ❌ Uses `Engine` suffix (not standard clean architecture)
- ❌ Mixed in with global templates
- ❌ Not suitable for generic use

**Strengths**:
- ✅ Good ErrorOr pattern usage
- ✅ Solid MVVM implementation
- ✅ Comprehensive test examples
- ✅ Strong functional programming patterns

## Target Architecture

### Global Templates

#### Template 1: `maui-appshell`
```
maui-appshell/
├── manifest.json
├── CLAUDE.md
├── agents/
│   ├── maui-domain-specialist.md       # Business logic (verb-based)
│   ├── maui-repository-specialist.md   # Database access
│   ├── maui-service-specialist.md      # APIs and hardware
│   ├── maui-viewmodel-specialist.md    # MVVM
│   ├── maui-ui-specialist.md           # XAML/UI
│   ├── architectural-reviewer.md       # Design review
│   └── test-orchestrator.md            # Testing
├── templates/
│   ├── Domain.cs                       # Business logic template
│   ├── Repository.cs                   # Database template
│   ├── IRepository.cs                  # Repository interface
│   ├── Service.cs                      # External service template
│   ├── IService.cs                     # Service interface
│   ├── ViewModel.cs                    # ViewModel template
│   ├── Page.xaml                       # XAML page
│   ├── AppShell.xaml                   # Shell navigation
│   ├── MauiProgram.cs                  # DI setup
│   └── README.md                       # Template guide
└── settings.json                       # Template config
```

#### Template 2: `maui-navigationpage`
```
maui-navigationpage/
├── manifest.json
├── CLAUDE.md
├── agents/                             # Same as appshell
├── templates/
│   ├── Domain.cs                       # Same as appshell
│   ├── Repository.cs                   # Same as appshell
│   ├── Service.cs                      # Same as appshell
│   ├── ViewModel.cs                    # Same as appshell
│   ├── Page.xaml                       # Same as appshell
│   ├── NavigationService.cs            # NavigationPage service
│   ├── INavigationService.cs           # Navigation interface
│   ├── MauiProgram.cs                  # DI setup (different nav)
│   └── README.md                       # Template guide
└── settings.json                       # Template config
```

### Local Template (MyDrive)

```
MyDrive/.claude/templates/maui-mydrive/
├── manifest.json                       # Local template metadata
├── CLAUDE.md                           # MyDrive-specific guidance
├── agents/
│   ├── maui-engine-specialist.md       # Engine pattern specialist
│   └── [other MyDrive agents]
├── templates/
│   ├── Engine.cs                       # MyDrive Engine template
│   ├── EngineTests.cs                  # Engine test template
│   └── [other MyDrive templates]
└── settings.json                       # MyDrive template config
```

## Implementation Phases

### Phase 1: Create Global Templates ✅

**Tasks**:
1. Create `installer/global/templates/maui-appshell/`
2. Create `installer/global/templates/maui-navigationpage/`
3. Implement Domain pattern (verb-based, no suffix)
4. Separate Repository (database) from Service (API/hardware)
5. Create manifest.json for each template
6. Create comprehensive CLAUDE.md guidance

**Deliverables**:
- Two production-ready global MAUI templates
- Clear documentation on when to use each
- Domain pattern examples

### Phase 2: Create Specialized Agents 🔄

**New Agents**:

#### `maui-domain-specialist.md`
```yaml
---
name: maui-domain-specialist
description: MAUI Domain layer specialist - business logic with verb-based naming
tools: Read, Write, Analyze, Search
model: sonnet
expertise:
  - Domain layer implementation (GetProducts, CreateOrder, etc.)
  - ErrorOr pattern for functional error handling
  - Composing Repositories and Services
  - Business rule enforcement
  - No UseCase or Engine suffix
  - Clean architecture principles
---
```

#### `maui-repository-specialist.md`
```yaml
---
name: maui-repository-specialist
description: MAUI Repository specialist - database access patterns
tools: Read, Write, Analyze, Search
model: sonnet
expertise:
  - SQLite, LiteDB, Entity Framework Core
  - Repository pattern implementation
  - Database migrations
  - Query optimization
  - Offline data storage
  - ONLY database access (no API calls)
---
```

#### `maui-service-specialist.md`
```yaml
---
name: maui-service-specialist
description: MAUI Service specialist - external systems integration
tools: Read, Write, Analyze, Search
model: sonnet
expertise:
  - HTTP API clients (RestSharp, Refit)
  - Hardware services (GPS, Camera, Sensors)
  - Cache services (in-memory, persistent)
  - Authentication services
  - ONLY external systems (no database access)
---
```

**Tasks**:
1. Create new agents with clear responsibilities
2. Update agent collaboration patterns
3. Remove or deprecate old usecase-specialist
4. Update orchestration patterns

**Deliverables**:
- 3 new specialized agents
- Updated agent orchestration
- Clear handoff patterns

### Phase 3: Migrate MyDrive to Local Template 📦

**Tasks**:
1. Create `.claude/templates/maui-mydrive/` in MyDrive project
2. Copy current `maui/` template to local template
3. Preserve Engine pattern and DeCUK namespace
4. Update manifest.json with local scope
5. Update MyDrive's `.claude/settings.json` to reference local template
6. Test MyDrive workflow with local template

**Migration Script** (`scripts/migrate-mydrive-template.sh`):
```bash
#!/bin/bash
# Migrate MyDrive to use local custom template

set -e

MYDRIVE_PROJECT="/Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive"
SOURCE_TEMPLATE="installer/global/templates/maui"
LOCAL_TEMPLATE="$MYDRIVE_PROJECT/.claude/templates/maui-mydrive"

echo "Migrating MyDrive to local template..."

# 1. Create local template directory
mkdir -p "$LOCAL_TEMPLATE"/{agents,templates}

# 2. Copy current MAUI template
cp -r "$SOURCE_TEMPLATE"/* "$LOCAL_TEMPLATE/"

# 3. Create local manifest
cat > "$LOCAL_TEMPLATE/manifest.json" << EOF
{
  "name": "maui-mydrive",
  "description": "MyDrive-specific MAUI template with Engine pattern",
  "version": "1.0.0",
  "scope": "local",
  "base": "maui-appshell",
  "customizations": {
    "domain_pattern": "Engine",
    "namespace_pattern": "DeCUK.Mobile.MyDrive",
    "domain_namespace": "Engines"
  }
}
EOF

# 4. Update MyDrive settings.json
cat > "$MYDRIVE_PROJECT/.claude/settings.json" << EOF
{
  "template": "maui-mydrive",
  "template_priority": ["local", "global"],
  "customizations": {
    "namespace_root": "DeCUK.Mobile.MyDrive",
    "domain_namespace": "Engines",
    "domain_suffix": "Engine"
  }
}
EOF

echo "✅ MyDrive migrated to local template"
echo "Location: $LOCAL_TEMPLATE"
```

**Deliverables**:
- MyDrive local template
- Migration script
- Updated MyDrive .claude configuration
- Verification tests

### Phase 4: Update Installer for Local Templates 🔧

**Changes to `installer/scripts/install.sh`**:

1. **Update template discovery**:
```bash
# Add function to discover local templates
discover_templates() {
    local templates=()

    # Global templates
    for template in "$INSTALL_DIR/templates"/*; do
        if [ -d "$template" ]; then
            templates+=("$(basename "$template")")
        fi
    done

    # Local templates (if in project directory)
    if [ -d ".claude/templates" ]; then
        for template in ".claude/templates"/*; do
            if [ -d "$template" ]; then
                templates+=("$(basename "$template") (local)")
            fi
        done
    fi

    echo "${templates[@]}"
}
```

2. **Add local template support to init script**:
```bash
# Update agentec-init to check local templates first
resolve_template() {
    local template_name=$1

    # Check local template first
    if [ -d ".claude/templates/$template_name" ]; then
        echo ".claude/templates/$template_name"
        return 0
    fi

    # Check global template
    if [ -d "$AGENTECFLOW_HOME/templates/$template_name" ]; then
        echo "$AGENTECFLOW_HOME/templates/$template_name"
        return 0
    fi

    # Fallback to default
    echo "$AGENTECFLOW_HOME/templates/default"
}
```

3. **Update completion scripts**:
```bash
# Update bash completion to include local templates
_agentec_init() {
    local cur templates
    cur="${COMP_WORDS[COMP_CWORD]}"

    # Global templates
    templates="default react python maui-appshell maui-navigationpage dotnet-microservice fullstack typescript-api"

    # Add local templates if in project
    if [ -d ".claude/templates" ]; then
        local local_templates=$(ls -1 .claude/templates/)
        templates="$templates $local_templates"
    fi

    COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
}
```

**Deliverables**:
- Updated installer with local template support
- Template priority resolution
- Updated CLI commands
- Updated completion scripts

### Phase 5: Documentation 📚

**Documents to Create**:

1. **Template Selection Guide** (`docs/guides/maui-template-selection.md`)
   - When to use AppShell vs NavigationPage
   - When to create local templates
   - Migration strategies

2. **Local Template Creation Guide** (`docs/guides/creating-local-templates.md`)
   - Step-by-step instructions
   - Customization options
   - Version control best practices

3. **Domain Pattern Guide** (`docs/patterns/domain-layer-pattern.md`)
   - Verb-based naming conventions
   - Repository vs Service separation
   - ErrorOr pattern usage
   - Testing strategies

4. **Migration Guide** (`docs/migration/engine-to-domain.md`)
   - MyDrive example
   - Pattern translations
   - Common pitfalls

**Deliverables**:
- 4 comprehensive guides
- Code examples
- Migration checklists

## Verification Checklist

### Global Templates
- [ ] `maui-appshell` template created
- [ ] `maui-navigationpage` template created
- [ ] Domain pattern implemented (verb-based naming)
- [ ] Repository (database) and Service (API) separation
- [ ] ErrorOr pattern usage
- [ ] CLAUDE.md guidance complete
- [ ] Manifest.json properly configured
- [ ] All agents created and tested

### Local Template Support
- [ ] MyDrive local template created
- [ ] Local template preserves Engine pattern
- [ ] Migration script tested
- [ ] Installer supports local templates
- [ ] Template priority resolution works
- [ ] CLI commands updated
- [ ] Completion scripts updated

### Documentation
- [ ] Template selection guide complete
- [ ] Local template creation guide complete
- [ ] Domain pattern guide complete
- [ ] Migration guide complete
- [ ] Architecture doc complete
- [ ] All examples tested

### Testing
- [ ] Create new project with `maui-appshell`
- [ ] Create new project with `maui-navigationpage`
- [ ] Verify MyDrive works with local template
- [ ] Test template priority resolution
- [ ] Test local template customization
- [ ] Verify all agents function correctly

## Timeline Estimate

| Phase | Estimated Time | Priority |
|-------|----------------|----------|
| Phase 1: Global Templates | 4 hours | HIGH |
| Phase 2: Specialized Agents | 3 hours | HIGH |
| Phase 3: MyDrive Migration | 2 hours | HIGH |
| Phase 4: Installer Updates | 3 hours | MEDIUM |
| Phase 5: Documentation | 3 hours | MEDIUM |
| **Total** | **15 hours** | |

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking MyDrive workflow | HIGH | Thorough testing, local template isolation |
| Confusion between patterns | MEDIUM | Clear documentation, naming conventions |
| Installation complexity | LOW | Comprehensive installer updates, fallbacks |
| Agent orchestration issues | MEDIUM | Updated orchestration patterns, testing |

## Success Criteria

1. ✅ Two working global MAUI templates (AppShell + NavigationPage)
2. ✅ MyDrive continues working with local template
3. ✅ Clear Domain pattern implementation
4. ✅ Repository/Service separation
5. ✅ Comprehensive documentation
6. ✅ All tests passing
7. ✅ Installer supports local templates
8. ✅ Zero breaking changes for existing projects

## Next Steps

1. **Immediate**: Start Phase 1 (Create global templates)
2. **Follow-up**: Create specialized agents (Phase 2)
3. **Then**: Migrate MyDrive (Phase 3)
4. **Finally**: Update installer and docs (Phases 4-5)

## Questions for Review

1. ✅ Domain pattern vs Engine pattern confirmed?
2. ✅ Repository (database) vs Service (API/hardware) separation confirmed?
3. ✅ Two navigation templates (AppShell + NavigationPage) confirmed?
4. ❓ Any other local template patterns to consider?
5. ❓ Should we deprecate old `maui/` template or keep for compatibility?

## Rollback Procedure

If issues arise after deleting the old `maui` template, use this git-based recovery:

### Quick Rollback
```bash
# Rollback to checkpoint (pre-deletion state)
git reset --hard 8e393d206f1882b462552080ed53fc5c01cc30c0

# Or, restore just the old template
git checkout 8e393d206f1882b462552080ed53fc5c01cc30c0 -- installer/global/templates/maui/
```

### Checkpoint Information
- **Checkpoint Commit**: `8e393d206f1882b462552080ed53fc5c01cc30c0`
- **Branch**: `task-011h-delete-old-maui-template`
- **Created**: During TASK-011H implementation
- **Contents**: Pre-deletion state with old template intact

### Recovery Steps
1. Identify issue (broken MyDrive workflow, missing template, etc.)
2. Restore old template using git checkout command above
3. Revert script changes if needed
4. Test MyDrive workflow
5. Document issue for future resolution

### Verification After Rollback
- Old `maui` template exists at `installer/global/templates/maui/`
- Scripts reference old `maui` template in completions
- MyDrive workflow functions correctly
- New templates (`maui-appshell`, `maui-navigationpage`) still exist

## Approval

- [ ] Architecture approved
- [ ] Timeline approved
- [ ] Ready to proceed with implementation

---

**Document Version**: 1.1
**Last Updated**: 2025-10-13
**Author**: AI Engineer Team
**Status**: READY FOR IMPLEMENTATION
