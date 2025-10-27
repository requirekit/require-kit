---
id: TASK-011I
title: Update installer to support local template directories
status: completed
created: 2025-10-12T10:30:00Z
updated: 2025-10-17T00:00:00Z
completed: 2025-10-17T00:00:00Z
priority: medium
tags: [installer, templates, local-templates, maui-migration, phase-4]
epic: null
feature: null
requirements: []
external_ids:
  epic_jira: null
  epic_linear: null
  jira: null
  linear: null
bdd_scenarios: []
test_results:
  status: passed
  total_tests: 12
  passed: 12
  failed: 0
  coverage:
    line: 85
    branch: 90
  last_run: "2025-10-13T00:00:00Z"
dependencies: []
related_documents:
  - docs/workflows/maui-template-migration-plan.md
  - installer/scripts/install.sh
  - installer/scripts/init-claude-project.sh
complexity_evaluation:
  score: 4
  level: "moderate"
  review_mode: "FULL_REQUIRED"
  factor_scores:
    - factor: "file_complexity"
      score: 1
      max_score: 3
      justification: "2 files to modify (~180 LOC total changes)"
    - factor: "pattern_familiarity"
      score: 0
      max_score: 2
      justification: "Familiar bash patterns (Chain of Responsibility, Validation)"
    - factor: "risk_level"
      score: 3
      max_score: 3
      justification: "Critical security risk - path traversal vulnerability requires mandatory review"
    - factor: "dependencies"
      score: 0
      max_score: 2
      justification: "No external dependencies (pure bash, coreutils only)"
  force_triggers:
    - "security_keywords"
  trigger_details: "Path traversal vulnerability identified in architectural review"
architectural_review:
  score: 87
  status: "approved"
  approved_at: "2025-10-13T00:00:00Z"
  principles:
    solid: 44
    dry: 23
    yagni: 20
  critical_issues:
    - priority: "HIGH"
      category: "security"
      description: "Missing input validation for path traversal attacks"
      fix_time_minutes: 5
design_approval:
  status: "approved"
  approved_at: "2025-10-13T00:00:00Z"
  approved_by: "user"
  review_mode: "full_required"
  checkpoint_duration_seconds: 0
previous_state: backlog
state_transition_reason: "Automatic transition for task-work execution"
---

# Task: Update installer to support local template directories

## Context

This is Phase 4 of the MAUI Template Migration Plan. The goal is to enable projects to have their own custom templates in `.claude/templates/` that override global templates, allowing:

1. MyDrive project to maintain its Engine pattern locally
2. New projects to use generic Domain pattern globally
3. Any project to customize templates without affecting other projects

The template priority resolution should be: **local → global → default**

## Objective

Enhance the installer and initialization scripts to:
- Discover local templates in `.claude/templates/`
- Implement template priority resolution (local overrides global)
- Update all CLI commands to recognize local templates
- Add validation and diagnostics for local templates

## Requirements

### Template Discovery
- Add function to discover local templates in `.claude/templates/`
- Scan both global (`~/.agentecflow/templates/`) and local (`.claude/templates/`) directories
- Return template list with clear indication of source (local vs global)

### Template Priority Resolution
- **Priority Order**: local → global → default
- If template exists in `.claude/templates/`, use that version
- Otherwise, fallback to `~/.agentecflow/templates/`
- If neither exist, fallback to `default` template
- Clear logging of which template source is being used

### Init Script Updates
- Update `init-claude-project.sh` to check local templates first
- Add `resolve_template()` function with priority logic
- Log template resolution source for transparency
- Validate local templates before using them

### Doctor Command Updates
- Add local template verification to `agentecflow doctor`
- Show which templates are available locally
- Display template priority for each template
- Warn about invalid local templates

### Bash Completion Updates
- Update completion script to include local templates
- Dynamically discover local templates if in project directory
- Show both local and global templates in completion suggestions

### Template Listing
- Update `agentec-init help` to show local templates
- Distinguish local from global templates in output
- Show local template priority in listings

### Validation
- Add validation function for local template structure
- Check for required files (manifest.json, CLAUDE.md, agents/, templates/)
- Provide helpful error messages for invalid templates
- Allow graceful fallback to global template if local is invalid

### Error Handling
- Clear error messages when local template is invalid
- Fallback to global template if local template fails validation
- Log warnings for missing required template components
- Prevent crashes from malformed local templates

## Acceptance Criteria

### Functional Requirements
- [x] Local templates discovered correctly from `.claude/templates/`
- [x] Template priority works: local overrides global
- [x] `agentec-init` resolves templates in correct order
- [x] `agentecflow doctor` shows local template status
- [x] Bash completion includes local templates
- [x] Template listing distinguishes local vs global
- [x] Invalid templates show helpful error messages

### Quality Requirements
- [x] All installer tests passing
- [x] Template resolution logic well-documented
- [x] Error messages are actionable and clear
- [x] Backward compatibility maintained (existing projects work)

### Documentation Requirements
- [x] Installation script comments updated
- [x] Template priority documented in comments
- [x] Examples of local template usage provided
- [x] Migration script includes template discovery

## Implementation Plan

### 1. Add Template Discovery Function (`install.sh`)

```bash
# Add function to discover all available templates
discover_templates() {
    local templates=()

    # Global templates
    if [ -d "$AGENTECFLOW_HOME/templates" ]; then
        for template in "$AGENTECFLOW_HOME/templates"/*; do
            if [ -d "$template" ]; then
                templates+=("$(basename "$template"):global")
            fi
        done
    fi

    # Local templates (if in project directory)
    if [ -d ".claude/templates" ]; then
        for template in ".claude/templates"/*; do
            if [ -d "$template" ]; then
                local name=$(basename "$template")
                templates+=("$name:local")
            fi
        done
    fi

    echo "${templates[@]}"
}
```

### 2. Add Template Resolution Function (`init-claude-project.sh`)

```bash
# Resolve template with priority: local → global → default
resolve_template() {
    local template_name=$1
    local resolved_path=""
    local resolved_source=""

    # Check local template first (highest priority)
    if [ -d ".claude/templates/$template_name" ]; then
        resolved_path=".claude/templates/$template_name"
        resolved_source="local"
        print_info "Using local template: $template_name"
    # Check global template
    elif [ -d "$AGENTECFLOW_HOME/templates/$template_name" ]; then
        resolved_path="$AGENTECFLOW_HOME/templates/$template_name"
        resolved_source="global"
        print_info "Using global template: $template_name"
    # Fallback to default
    else
        resolved_path="$AGENTECFLOW_HOME/templates/default"
        resolved_source="fallback"
        print_warning "Template '$template_name' not found, using default"
    fi

    # Validate template structure
    if ! validate_template "$resolved_path"; then
        print_error "Invalid template structure at: $resolved_path"
        if [ "$resolved_source" = "local" ]; then
            print_warning "Falling back to global template"
            resolved_path="$AGENTECFLOW_HOME/templates/$template_name"
            resolved_source="global-fallback"
        else
            return 1
        fi
    fi

    echo "$resolved_path:$resolved_source"
}

# Validate template structure
validate_template() {
    local template_path=$1
    local valid=true

    # Check for required files
    if [ ! -f "$template_path/CLAUDE.md" ]; then
        print_warning "Template missing CLAUDE.md: $template_path"
        valid=false
    fi

    if [ ! -f "$template_path/manifest.json" ]; then
        print_warning "Template missing manifest.json: $template_path"
        valid=false
    fi

    # Warnings only (not fatal)
    if [ ! -d "$template_path/agents" ]; then
        print_info "Template has no agents directory: $template_path"
    fi

    if [ ! -d "$template_path/templates" ]; then
        print_info "Template has no templates directory: $template_path"
    fi

    if [ "$valid" = true ]; then
        return 0
    else
        return 1
    fi
}
```

### 3. Update Doctor Command (`install.sh` - `agentecflow doctor`)

```bash
# In the doctor command, add local template section
echo ""
echo "Local Templates:"
if [ -d ".claude/templates" ]; then
    local local_count=$(ls -1d .claude/templates/*/ 2>/dev/null | wc -l)
    if [ $local_count -gt 0 ]; then
        echo -e "  ${GREEN}✓${NC} Found $local_count local templates"
        for template in .claude/templates/*/; do
            if [ -d "$template" ]; then
                local name=$(basename "$template")
                echo "    - $name (overrides global)"
            fi
        done
    else
        echo -e "  ${BLUE}ℹ${NC} No local templates (using global templates)"
    fi
else
    echo -e "  ${BLUE}ℹ${NC} Not in a project directory"
fi
```

### 4. Update Bash Completion (`install.sh` - completions)

```bash
# Update bash completion to include local templates
_agentec_init() {
    local cur templates
    cur="${COMP_WORDS[COMP_CWORD]}"

    # Global templates
    templates="default react python maui-appshell maui-navigationpage dotnet-microservice fullstack typescript-api"

    # Add local templates if in project
    if [ -d ".claude/templates" ]; then
        local local_templates=$(ls -1 .claude/templates/ 2>/dev/null)
        templates="$templates $local_templates"
    fi

    COMPREPLY=( $(compgen -W "${templates}" -- ${cur}) )
}
```

### 5. Update Init Script to Use Resolution

```bash
# In copy_smart_template() function
copy_smart_template() {
    local detected_type=$(detect_project_type)
    local effective_template="$TEMPLATE"

    # Override template if we detected a specific type
    if [ "$TEMPLATE" = "default" ] && [ "$detected_type" != "unknown" ]; then
        case "$detected_type" in
            maui) effective_template="maui" ;;
            # ... other cases
        esac
        print_info "Auto-selected template: $effective_template"
    fi

    # Use template resolution function
    local resolution=$(resolve_template "$effective_template")
    local template_dir=$(echo "$resolution" | cut -d: -f1)
    local template_source=$(echo "$resolution" | cut -d: -f2)

    if [ -z "$template_dir" ]; then
        print_error "Failed to resolve template: $effective_template"
        return 1
    fi

    print_success "Resolved template: $effective_template (source: $template_source)"

    # Rest of copy logic...
}
```

## Testing Strategy

### Test Scenarios

1. **Global Template Only**
   - No local templates exist
   - Should use global template
   - Completion shows only global templates

2. **Local Template Override**
   - Create `.claude/templates/maui-mydrive/`
   - Should use local template over global
   - Doctor shows local template with override indication

3. **Invalid Local Template**
   - Create malformed local template
   - Should show validation error
   - Should fallback to global template

4. **Template Discovery**
   - Run `agentecflow doctor` in project with local templates
   - Should list all local templates
   - Should indicate which override global

5. **Completion Integration**
   - Tab-complete `agentec-init ` in project
   - Should show both local and global templates

6. **Template Resolution Priority**
   - Create both local and global templates with same name
   - Should use local version
   - Should log which source is used

### Test Commands

```bash
# Test 1: Doctor command shows local templates
cd /path/to/project-with-local-templates
agentecflow doctor

# Test 2: Init with local template
cd /path/to/project-with-local-templates
agentec-init maui-mydrive

# Test 3: Bash completion
cd /path/to/project-with-local-templates
agentec-init [TAB][TAB]

# Test 4: Validation
mkdir -p .claude/templates/invalid-template
agentec-init invalid-template  # Should show error and fallback
```

## Related Documentation

- **Migration Plan**: `docs/workflows/maui-template-migration-plan.md`
- **Phase 4 Details**: See "Phase 4: Update Installer for Local Templates" section
- **Installer Script**: `installer/scripts/install.sh`
- **Init Script**: `installer/scripts/init-claude-project.sh`

## Success Metrics

- **Discoverability**: Users can find local templates via doctor command
- **Transparency**: Template resolution source is clearly logged
- **Reliability**: Invalid local templates don't break initialization
- **Usability**: Bash completion makes local templates easy to use
- **Backward Compatibility**: Existing projects work without changes

## Notes

### Design Decisions

1. **Priority Order**: Local → Global → Default
   - Allows project-specific customization
   - Maintains global defaults for new projects
   - Provides safe fallback

2. **Validation Strategy**: Warn, don't fail
   - Missing agents/templates is warning, not error
   - Only CLAUDE.md and manifest.json are required
   - Allows gradual template building

3. **Completion Strategy**: Dynamic discovery
   - Scans local templates at completion time
   - No need to regenerate completion scripts
   - Always up-to-date

4. **Doctor Command**: Full transparency
   - Shows all local templates
   - Indicates which override global
   - Provides clear status for troubleshooting

### Future Enhancements

1. **Template Inheritance**: Local templates could extend global templates
2. **Template Versioning**: Track which version of global template local is based on
3. **Template Validation**: More comprehensive structure validation
4. **Template Sync**: Command to update local template from global changes

## Dependencies

### Required Before
- None (standalone task)

### Enables After Completion
- MAUI template migration Phase 3 (MyDrive local template)
- Custom template creation for other projects
- Template experimentation without affecting globals

## Estimated Complexity

**Score**: 6/10 (Medium)

**Breakdown**:
- File Complexity: 2/3 (4-6 files to modify)
- Pattern Familiarity: 1/2 (familiar bash patterns)
- Risk Level: 1/3 (medium risk with fallbacks)
- Dependencies: 2/2 (multiple script interactions)

**Estimated Duration**: 3-4 hours

**Timeline Breakdown**:
- Template discovery function: 30 minutes
- Template resolution with validation: 1 hour
- Update init script: 1 hour
- Update doctor command: 30 minutes
- Update bash completion: 30 minutes
- Testing all scenarios: 1 hour

## Priority Justification

**MEDIUM** priority because:
- Enables Phase 3 of MAUI migration (MyDrive local template)
- Provides valuable project customization capability
- Not blocking existing functionality (global templates still work)
- Foundational for template system flexibility
- Medium complexity with clear implementation path
