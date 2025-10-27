# TASK-016: Migration Script Technical Design Document

## Executive Summary

This document provides a production-ready technical design for implementing a bash-based file migration system to reorganize completed task files into subfolders. The script will migrate 62 files in the ai-engineer project and establish a maintainable structure for both ai-engineer and MyDrive projects.

**Key Objectives:**
- Migrate 54+ task summary files from root to `tasks/completed/TASK-XXX/` subfolders
- Migrate 6+ coverage files to `coverage/reports/` with organized naming
- Preserve git history for all file moves
- Update relative links in markdown files
- Implement idempotent, rollback-capable migration
- Prevent future root pollution through configuration

**Estimated Effort:** 320 LOC, 12-16 hours development + testing

---

## 1. Architecture Overview

### 1.1 High-Level Component Design

```
migrate-completed-tasks.sh (Main Orchestrator)
├── lib/
│   ├── core.sh                 # Core utilities, logging, error handling
│   ├── project_detection.sh    # Detect MyDrive vs ai-engineer
│   ├── file_discovery.sh       # Pattern-based file finding
│   ├── task_id_parser.sh       # Extract task IDs from filenames
│   ├── backup_manager.sh       # Backup creation and rollback
│   ├── git_operations.sh       # Git mv wrapper, history preservation
│   ├── link_updater.sh         # Markdown link path adjustment
│   ├── name_standardizer.sh    # Filename normalization
│   └── validator.sh            # Post-migration validation
├── tests/
│   ├── unit/
│   │   ├── test_task_id_parser.bats
│   │   ├── test_link_updater.bats
│   │   └── test_name_standardizer.bats
│   └── integration/
│       ├── test_migration_flow.bats
│       ├── test_idempotency.bats
│       └── test_edge_cases.bats
└── .migration-lock            # Lock file for concurrent execution prevention
```

### 1.2 Execution Flow Diagram

```
[START]
   ↓
[Parse CLI Arguments] → [Show Help/Version]
   ↓
[Validate Prerequisites]
   ├─ Check bash 4.0+
   ├─ Check git repo
   ├─ Check required commands (git, find, sed, awk)
   └─ Check lock file (prevent concurrent runs)
   ↓
[Detect Project Type] → [MyDrive | ai-engineer]
   ↓
[Create Backup] → [Compress current state to .tar.gz]
   ↓
[Discover Files]
   ├─ Find task files by pattern
   ├─ Extract task IDs
   └─ Group files by task ID
   ↓
[Validate Discovery] → [Show summary, prompt confirmation if --interactive]
   ↓
[Migrate Task Files]
   ├─ Create task subfolders
   ├─ Standardize filenames
   ├─ Git mv files with history
   └─ Update relative links
   ↓
[Migrate Coverage Files] (ai-engineer only)
   ├─ Create coverage/reports/
   ├─ Standardize coverage filenames
   ├─ Git mv coverage files
   └─ Create .gitignore
   ↓
[Migrate Analysis Files] (ai-engineer only)
   ├─ Create docs/archive/
   └─ Git mv analysis files
   ↓
[Post-Migration Validation]
   ├─ Check for broken links
   ├─ Verify git status
   └─ Generate migration report
   ↓
[Cleanup]
   ├─ Remove lock file
   └─ Display summary
   ↓
[END]
```

### 1.3 Data Flow Architecture

```
Input Files (Scattered)
      ↓
  Discovery Phase
      ↓
Task ID Extraction → Grouping by Task ID
      ↓
File Association Map
  {
    "TASK-003B-4": [
      "./TASK-003B-4-COMPLEXITY-ANALYSIS.md",
      "./TASK-003B-4-IMPLEMENTATION-PLAN.md",
      ...
    ],
    "TASK-003E": [...],
    ...
  }
      ↓
  Backup Creation
      ↓
  Migration Phase
      ↓
Git Operations (preserving history)
      ↓
Link Update Phase
      ↓
Validation Phase
      ↓
Output: Organized Structure
  tasks/completed/TASK-XXX/
  coverage/reports/
  docs/archive/
```

---

## 2. Detailed Component Specifications

### 2.1 Main Entry Point: `migrate-completed-tasks.sh`

**Responsibilities:**
- Command-line argument parsing
- Orchestrate execution phases
- Lock file management
- Top-level error handling

**Function Signature:**
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Version and metadata
readonly VERSION="1.0.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LIB_DIR="${SCRIPT_DIR}/lib"
readonly LOCK_FILE=".migration-lock"

# Main execution function
# Arguments:
#   $@ - Command-line arguments
# Returns:
#   0 - Success
#   1 - Validation failure
#   2 - Migration failure
#   3 - Backup failure
main() {
  local dry_run=false
  local interactive=false
  local force=false
  local skip_backup=false

  parse_arguments "$@"
  validate_prerequisites
  create_lock_file

  trap cleanup_on_exit EXIT
  trap handle_error ERR

  if [[ "$dry_run" == true ]]; then
    execute_dry_run
  else
    execute_migration
  fi
}

main "$@"
```

**Command-Line Interface:**
```bash
Usage: migrate-completed-tasks.sh [OPTIONS]

OPTIONS:
  --execute, -e          Execute migration (default: dry-run preview)
  --interactive, -i      Prompt for confirmation before each phase
  --force, -f            Skip safety checks (use with caution)
  --skip-backup          Skip backup creation (not recommended)
  --rollback FILE        Rollback to a previous backup
  --validate-only        Only validate current state, no changes
  --help, -h             Show this help message
  --version, -v          Show version information

EXAMPLES:
  # Preview changes without executing
  ./migrate-completed-tasks.sh

  # Execute migration with interactive confirmation
  ./migrate-completed-tasks.sh --execute --interactive

  # Rollback to previous state
  ./migrate-completed-tasks.sh --rollback backup-20251017-120000.tar.gz

  # Validate existing structure
  ./migrate-completed-tasks.sh --validate-only
```

**Estimated LOC:** 120 lines

---

### 2.2 Core Utilities: `lib/core.sh`

**Responsibilities:**
- Logging functions (info, warn, error, success)
- Error handling utilities
- Color output support
- Path manipulation helpers

**Key Functions:**

```bash
# Logging with color support
# Arguments:
#   $1 - Log level (INFO|WARN|ERROR|SUCCESS)
#   $2 - Message
log() {
  local level=$1
  shift
  local message="$*"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local color_code=""

  case "$level" in
    INFO)    color_code="\033[0;36m" ;;  # Cyan
    WARN)    color_code="\033[0;33m" ;;  # Yellow
    ERROR)   color_code="\033[0;31m" ;;  # Red
    SUCCESS) color_code="\033[0;32m" ;;  # Green
  esac

  echo -e "${color_code}[${timestamp}] [${level}] ${message}\033[0m"
}

# Abort execution with error message
# Arguments:
#   $1 - Error message
#   $2 - Exit code (optional, default: 1)
die() {
  log ERROR "$1"
  exit "${2:-1}"
}

# Confirm user action (interactive mode)
# Arguments:
#   $1 - Prompt message
# Returns:
#   0 - User confirmed (yes)
#   1 - User declined (no)
confirm() {
  local prompt="$1"
  local response

  read -r -p "${prompt} [y/N] " response
  case "$response" in
    [yY][eE][sS]|[yY]) return 0 ;;
    *) return 1 ;;
  esac
}

# Get absolute path (resolves symlinks)
# Arguments:
#   $1 - Relative or absolute path
# Returns:
#   Absolute path string
get_absolute_path() {
  local path="$1"
  echo "$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
}
```

**Estimated LOC:** 80 lines

---

### 2.3 Project Detection: `lib/project_detection.sh`

**Responsibilities:**
- Detect if current project is MyDrive or ai-engineer
- Determine project-specific patterns and directories

**Key Functions:**

```bash
# Detect project type based on directory structure
# Arguments:
#   None (uses current directory)
# Returns:
#   "mydrive" - MyDrive project
#   "ai-engineer" - AI Engineer project
#   "" - Unknown project
detect_project_type() {
  local cwd=$(pwd)

  # Check for ai-engineer specific markers
  if [[ -f "installer/global/manifest.json" ]] && \
     [[ -d "installer/global/commands" ]] && \
     [[ -d "installer/global/agents" ]]; then
    echo "ai-engineer"
    return 0
  fi

  # Check for MyDrive specific markers
  if [[ -f "DeCUK.Mobile.MyDrive.sln" ]] || \
     [[ -d "src/DeCUK.Mobile.MyDrive" ]]; then
    echo "mydrive"
    return 0
  fi

  # Unknown project
  echo ""
  return 1
}

# Get project-specific patterns for file discovery
# Arguments:
#   $1 - Project type (mydrive|ai-engineer)
# Returns:
#   JSON-like structure with patterns
get_project_patterns() {
  local project_type=$1

  case "$project_type" in
    ai-engineer)
      cat <<'EOF'
{
  "task_files": {
    "root": ".",
    "patterns": ["TASK-*.md", "TASK_*.md"]
  },
  "coverage_files": {
    "root": ".",
    "patterns": ["coverage*.json"]
  },
  "analysis_files": {
    "root": ".",
    "patterns": ["TASK_DUPLICATION_*.md", "TASK_NUMBERING_*.md"]
  }
}
EOF
      ;;
    mydrive)
      cat <<'EOF'
{
  "task_files": {
    "root": "tasks/completed",
    "patterns": ["TASK-*.md"]
  },
  "related_files": {
    "root": "docs",
    "patterns": ["tasks/TASK-*.md", "implementation-notes/TASK-*.md"]
  }
}
EOF
      ;;
  esac
}
```

**Estimated LOC:** 60 lines

---

### 2.4 File Discovery: `lib/file_discovery.sh`

**Responsibilities:**
- Find task-related files using patterns
- Support both MyDrive and ai-engineer patterns
- Filter out already-migrated files

**Key Functions:**

```bash
# Discover task files based on project-specific patterns
# Arguments:
#   $1 - Project type (mydrive|ai-engineer)
# Returns:
#   Array of discovered file paths (one per line)
discover_task_files() {
  local project_type=$1
  local discovered_files=()

  case "$project_type" in
    ai-engineer)
      # Find task summary files in root
      while IFS= read -r file; do
        # Skip if already in tasks/completed subfolder
        if [[ ! "$file" =~ ^tasks/completed/TASK-[^/]+/ ]]; then
          discovered_files+=("$file")
        fi
      done < <(find . -maxdepth 1 -type f \( -name "TASK-*.md" -o -name "TASK_*.md" \))
      ;;

    mydrive)
      # Find task files in completed folder (flat)
      while IFS= read -r file; do
        discovered_files+=("$file")
      done < <(find tasks/completed -maxdepth 1 -type f -name "TASK-*.md")

      # Find related files in docs
      while IFS= read -r file; do
        discovered_files+=("$file")
      done < <(find docs/tasks docs/implementation-notes -type f -name "TASK-*.md" 2>/dev/null || true)
      ;;
  esac

  # Output discovered files
  printf '%s\n' "${discovered_files[@]}"
}

# Discover coverage files (ai-engineer only)
# Arguments:
#   None
# Returns:
#   Array of coverage file paths
discover_coverage_files() {
  find . -maxdepth 1 -type f -name "coverage*.json"
}

# Discover analysis files (ai-engineer only)
# Arguments:
#   None
# Returns:
#   Array of analysis file paths
discover_analysis_files() {
  find . -maxdepth 1 -type f \( -name "TASK_DUPLICATION_*.md" -o -name "TASK_NUMBERING_*.md" \)
}

# Check if file is already migrated
# Arguments:
#   $1 - File path
# Returns:
#   0 - Already migrated
#   1 - Not migrated
is_already_migrated() {
  local file=$1

  # Check if file is already in a task subfolder
  if [[ "$file" =~ ^tasks/completed/TASK-[^/]+/.+ ]]; then
    return 0
  fi

  # Check if file is already in coverage/reports/
  if [[ "$file" =~ ^coverage/reports/.+ ]]; then
    return 0
  fi

  # Check if file is already in docs/archive/
  if [[ "$file" =~ ^docs/archive/.+ ]]; then
    return 0
  fi

  return 1
}
```

**Estimated LOC:** 90 lines

---

### 2.5 Task ID Parser: `lib/task_id_parser.sh`

**Responsibilities:**
- Extract task IDs from filenames
- Handle edge cases (TASK-003B-4, TASK_DUPLICATION_ANALYSIS)
- Normalize task ID format

**Key Functions:**

```bash
# Extract task ID from filename
# Arguments:
#   $1 - Filename (e.g., "TASK-003B-4-COMPLEXITY-ANALYSIS.md")
# Returns:
#   Task ID (e.g., "TASK-003B-4") or empty string if not found
extract_task_id() {
  local filename=$1
  local basename=$(basename "$filename" .md)

  # Pattern 1: TASK-XXX (simple numeric)
  if [[ "$basename" =~ ^(TASK-[0-9]+) ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi

  # Pattern 2: TASK-XXX[A-Z] (with letter suffix)
  if [[ "$basename" =~ ^(TASK-[0-9]+[A-Z]) ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi

  # Pattern 3: TASK-XXX[A-Z]-N (with letter and number)
  if [[ "$basename" =~ ^(TASK-[0-9]+[A-Z]-[0-9]+) ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi

  # Pattern 4: TASK_XXX (underscore format)
  if [[ "$basename" =~ ^(TASK_[A-Z_]+) ]]; then
    # These are analysis files, not task files
    echo ""
    return 1
  fi

  # No match
  echo ""
  return 1
}

# Group files by task ID
# Arguments:
#   $@ - List of file paths
# Returns:
#   Associative array as JSON-like structure
#   {
#     "TASK-003": ["file1", "file2"],
#     "TASK-004": ["file3"]
#   }
group_files_by_task_id() {
  local files=("$@")
  declare -A task_groups

  for file in "${files[@]}"; do
    local task_id=$(extract_task_id "$file")

    if [[ -n "$task_id" ]]; then
      if [[ -z "${task_groups[$task_id]:-}" ]]; then
        task_groups[$task_id]="$file"
      else
        task_groups[$task_id]="${task_groups[$task_id]}|$file"
      fi
    fi
  done

  # Output as JSON-like structure
  for task_id in "${!task_groups[@]}"; do
    echo "$task_id:${task_groups[$task_id]}"
  done
}

# Validate task ID format
# Arguments:
#   $1 - Task ID
# Returns:
#   0 - Valid
#   1 - Invalid
is_valid_task_id() {
  local task_id=$1

  if [[ "$task_id" =~ ^TASK-[0-9]+([A-Z](-[0-9]+)?)?$ ]]; then
    return 0
  fi

  return 1
}
```

**Estimated LOC:** 85 lines

---

### 2.6 Backup Manager: `lib/backup_manager.sh`

**Responsibilities:**
- Create compressed backups before migration
- Support rollback to previous state
- Validate backup integrity

**Key Functions:**

```bash
# Create backup of current state
# Arguments:
#   None
# Returns:
#   Backup filename (e.g., "backup-20251017-120000.tar.gz")
create_backup() {
  local timestamp=$(date '+%Y%m%d-%H%M%S')
  local backup_file="backup-${timestamp}.tar.gz"
  local backup_dir=".migration-backups"

  mkdir -p "$backup_dir"

  log INFO "Creating backup: ${backup_dir}/${backup_file}"

  # Include all potentially affected files
  local files_to_backup=(
    "tasks/completed"
    "docs/tasks"
    "docs/implementation-notes"
    "coverage*.json"
    "TASK*.md"
  )

  # Create compressed archive
  tar -czf "${backup_dir}/${backup_file}" \
    --exclude=".git" \
    --exclude="node_modules" \
    --exclude="__pycache__" \
    "${files_to_backup[@]}" 2>/dev/null || true

  if [[ -f "${backup_dir}/${backup_file}" ]]; then
    log SUCCESS "Backup created: ${backup_dir}/${backup_file}"
    echo "${backup_dir}/${backup_file}"
    return 0
  else
    die "Failed to create backup" 3
  fi
}

# Rollback to previous backup
# Arguments:
#   $1 - Backup file path
# Returns:
#   0 - Success
#   1 - Failure
rollback_backup() {
  local backup_file=$1

  if [[ ! -f "$backup_file" ]]; then
    die "Backup file not found: $backup_file" 1
  fi

  log WARN "Rolling back to backup: $backup_file"

  # Extract backup (will overwrite current files)
  tar -xzf "$backup_file" || die "Failed to extract backup" 1

  log SUCCESS "Rollback completed successfully"
  return 0
}

# List available backups
# Arguments:
#   None
# Returns:
#   List of backup files with timestamps
list_backups() {
  local backup_dir=".migration-backups"

  if [[ ! -d "$backup_dir" ]]; then
    log INFO "No backups found"
    return 1
  fi

  log INFO "Available backups:"
  ls -lh "${backup_dir}"/*.tar.gz 2>/dev/null || log INFO "No backups found"
}
```

**Estimated LOC:** 75 lines

---

### 2.7 Git Operations: `lib/git_operations.sh`

**Responsibilities:**
- Wrapper for git mv with error handling
- Verify git repository status
- Preserve file history

**Key Functions:**

```bash
# Move file using git mv (preserves history)
# Arguments:
#   $1 - Source file path
#   $2 - Destination file path
# Returns:
#   0 - Success
#   1 - Failure
git_move_file() {
  local source=$1
  local dest=$2

  # Validate source exists
  if [[ ! -f "$source" ]]; then
    log ERROR "Source file not found: $source"
    return 1
  fi

  # Create destination directory if needed
  local dest_dir=$(dirname "$dest")
  mkdir -p "$dest_dir"

  # Execute git mv
  if git mv "$source" "$dest" 2>/dev/null; then
    log INFO "Moved: $source → $dest"
    return 0
  else
    log ERROR "Failed to move: $source → $dest"
    return 1
  fi
}

# Check if current directory is a git repository
# Arguments:
#   None
# Returns:
#   0 - Is git repo
#   1 - Not git repo
is_git_repository() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

# Get git repository root
# Arguments:
#   None
# Returns:
#   Repository root path
get_git_root() {
  git rev-parse --show-toplevel
}

# Check for uncommitted changes
# Arguments:
#   None
# Returns:
#   0 - Clean working tree
#   1 - Uncommitted changes present
has_uncommitted_changes() {
  if git diff-index --quiet HEAD -- 2>/dev/null; then
    return 1
  fi
  return 0
}

# Stage moved files for commit
# Arguments:
#   None
# Returns:
#   0 - Success
stage_all_changes() {
  git add -A
  log INFO "Staged all changes for commit"
}
```

**Estimated LOC:** 70 lines

---

### 2.8 Link Updater: `lib/link_updater.sh`

**Responsibilities:**
- Update relative links in markdown files
- Adjust paths based on directory depth change
- Handle both inline and reference-style links

**Key Functions:**

```bash
# Update relative links in markdown file
# Arguments:
#   $1 - File path
#   $2 - Depth change (number of directory levels moved down)
# Returns:
#   0 - Success
#   1 - Failure
update_markdown_links() {
  local file=$1
  local depth_change=${2:-1}

  if [[ ! -f "$file" ]]; then
    log ERROR "File not found: $file"
    return 1
  fi

  log INFO "Updating links in: $file"

  # Calculate prefix to add (../ for each level)
  local prefix=""
  for ((i=0; i<depth_change; i++)); do
    prefix="../${prefix}"
  done

  # Backup original file
  cp "$file" "${file}.linkbak"

  # Update inline links: [text](path)
  sed -i.tmp "s|\](\.\.\/|\](${prefix}../|g" "$file"
  sed -i.tmp "s|\](\([^h][^t][^t][^p]\)|\](${prefix}\1|g" "$file"

  # Update reference-style links: [ref]: path
  sed -i.tmp "s|^\[.*\]: \.\./|&${prefix}|g" "$file"

  # Clean up temporary files
  rm -f "${file}.tmp" "${file}.linkbak"

  log SUCCESS "Updated links in: $file"
  return 0
}

# Detect relative links in markdown file
# Arguments:
#   $1 - File path
# Returns:
#   List of relative link paths
detect_relative_links() {
  local file=$1

  # Extract links using regex
  grep -oP '\]\(\K[^)]+(?=\))' "$file" | grep -v '^http' || true
}

# Validate all links in markdown file
# Arguments:
#   $1 - File path
# Returns:
#   0 - All links valid
#   1 - Broken links found
validate_links() {
  local file=$1
  local file_dir=$(dirname "$file")
  local broken_links=()

  while IFS= read -r link; do
    # Skip absolute URLs
    if [[ "$link" =~ ^https?:// ]]; then
      continue
    fi

    # Resolve relative path
    local target="${file_dir}/${link}"

    if [[ ! -f "$target" && ! -d "$target" ]]; then
      broken_links+=("$link")
    fi
  done < <(detect_relative_links "$file")

  if [[ ${#broken_links[@]} -gt 0 ]]; then
    log WARN "Broken links in $file:"
    printf '  - %s\n' "${broken_links[@]}"
    return 1
  fi

  return 0
}
```

**Estimated LOC:** 90 lines

---

### 2.9 Name Standardizer: `lib/name_standardizer.sh`

**Responsibilities:**
- Standardize filenames within task subfolders
- Apply naming conventions consistently
- Handle edge cases (underscores, uppercase, special chars)

**Key Functions:**

```bash
# Standardize filename for task subfolder
# Arguments:
#   $1 - Original filename
#   $2 - Task ID (for context)
# Returns:
#   Standardized filename
standardize_filename() {
  local original=$1
  local task_id=$2
  local basename=$(basename "$original" .md)

  # Remove task ID prefix (TASK-003B-4-IMPLEMENTATION-SUMMARY → IMPLEMENTATION-SUMMARY)
  local without_prefix="${basename#${task_id}-}"

  # Convert to lowercase
  local lowercase=$(echo "$without_prefix" | tr '[:upper:]' '[:lower:]')

  # Replace underscores with hyphens
  local normalized="${lowercase//_/-}"

  # Apply standardization rules
  case "$normalized" in
    *implementation*)
      echo "implementation-summary.md"
      ;;
    *completion*)
      echo "completion-summary.md"
      ;;
    *complexity*)
      echo "complexity-evaluation.md"
      ;;
    *design*)
      echo "design-summary.md"
      ;;
    *test-result*)
      echo "test-results.md"
      ;;
    *before-after*)
      echo "before-after-comparison.md"
      ;;
    *continuation*)
      echo "continuation-guide.md"
      ;;
    *day-[0-9]*)
      # Preserve day numbering
      echo "$normalized.md"
      ;;
    *)
      # Keep original name if no match
      echo "${normalized}.md"
      ;;
  esac
}

# Standardize coverage filename
# Arguments:
#   $1 - Original coverage filename
# Returns:
#   Standardized coverage filename
standardize_coverage_filename() {
  local original=$1
  local basename=$(basename "$original" .json)

  # Patterns:
  # coverage-task006.json → task-006-coverage.json
  # coverage_task_003e.json → task-003e-coverage.json
  # coverage_integration.json → integration-coverage.json

  if [[ "$basename" =~ ^coverage-task([0-9]+)$ ]]; then
    local num="${BASH_REMATCH[1]}"
    echo "task-$(printf "%03d" "$num")-coverage.json"
  elif [[ "$basename" =~ ^coverage_task_(.+)$ ]]; then
    local suffix="${BASH_REMATCH[1]}"
    echo "task-${suffix}-coverage.json"
  elif [[ "$basename" =~ ^coverage_(.+)$ ]]; then
    local suffix="${BASH_REMATCH[1]}"
    echo "${suffix}-coverage.json"
  else
    echo "${basename}-coverage.json"
  fi
}

# Standardize analysis filename
# Arguments:
#   $1 - Original analysis filename
# Returns:
#   Standardized analysis filename
standardize_analysis_filename() {
  local original=$1
  local basename=$(basename "$original" .md)

  # Convert to lowercase and replace underscores
  echo "$(echo "$basename" | tr '[:upper:]' '[:lower:]' | tr '_' '-').md"
}
```

**Estimated LOC:** 85 lines

---

### 2.10 Validator: `lib/validator.sh`

**Responsibilities:**
- Post-migration validation
- Check for broken links
- Verify file integrity
- Generate validation report

**Key Functions:**

```bash
# Validate migration results
# Arguments:
#   None
# Returns:
#   0 - All validations passed
#   1 - Validation failures found
validate_migration() {
  log INFO "Starting post-migration validation..."

  local issues=()

  # Check 1: Verify no task files remain in root
  if find . -maxdepth 1 -name "TASK-*.md" | grep -q .; then
    issues+=("Task files still present in root directory")
  fi

  # Check 2: Verify no coverage files remain in root
  if find . -maxdepth 1 -name "coverage*.json" | grep -q .; then
    issues+=("Coverage files still present in root directory")
  fi

  # Check 3: Validate all migrated task folders have at least one file
  while IFS= read -r task_dir; do
    local file_count=$(find "$task_dir" -type f | wc -l)
    if [[ $file_count -eq 0 ]]; then
      issues+=("Empty task directory: $task_dir")
    fi
  done < <(find tasks/completed -mindepth 1 -maxdepth 1 -type d)

  # Check 4: Validate links in all migrated files
  while IFS= read -r file; do
    if ! validate_links "$file"; then
      issues+=("Broken links in: $file")
    fi
  done < <(find tasks/completed -type f -name "*.md")

  # Check 5: Verify git status (no untracked files)
  if git status --porcelain | grep -q "^??"; then
    issues+=("Untracked files detected (possible migration error)")
  fi

  # Report results
  if [[ ${#issues[@]} -eq 0 ]]; then
    log SUCCESS "All validation checks passed ✓"
    return 0
  else
    log ERROR "Validation failures detected:"
    printf '  - %s\n' "${issues[@]}"
    return 1
  fi
}

# Generate migration report
# Arguments:
#   $1 - Task groups (associative array as string)
#   $2 - Coverage files count
#   $3 - Analysis files count
# Returns:
#   None (prints report)
generate_migration_report() {
  local task_count=$(echo "$1" | wc -l)
  local coverage_count=$2
  local analysis_count=$3

  cat <<EOF

═══════════════════════════════════════════════════════════
                   MIGRATION REPORT
═══════════════════════════════════════════════════════════

📊 Summary:
  ✓ Tasks migrated: $task_count
  ✓ Coverage files organized: $coverage_count
  ✓ Analysis files archived: $analysis_count

📂 Directory Structure:
  ✓ tasks/completed/TASK-XXX/ (organized by task)
  ✓ coverage/reports/ (coverage files)
  ✓ docs/archive/ (analysis files)

🔍 Validation:
  ✓ No files remaining in root
  ✓ All links validated
  ✓ Git history preserved

📝 Next Steps:
  1. Review migrated files
  2. Commit changes: git commit -m "Reorganize completed task files"
  3. Push changes: git push
  4. Delete backup if satisfied: rm -f .migration-backups/backup-*.tar.gz

═══════════════════════════════════════════════════════════

EOF
}
```

**Estimated LOC:** 95 lines

---

## 3. Implementation Phases

### Phase A: CLI and Infrastructure (3 hours)

**Deliverables:**
- `migrate-completed-tasks.sh` main script
- `lib/core.sh` with logging and error handling
- Command-line argument parsing
- Lock file mechanism

**Testing:**
```bash
# Unit tests
./tests/unit/test_cli_parsing.bats
./tests/unit/test_logging.bats

# Expected outcomes
✓ Help message displays correctly
✓ Version flag works
✓ Lock file prevents concurrent execution
✓ Logging functions work with colors
```

**Estimated LOC:** 200 lines

---

### Phase B: File Discovery (2 hours)

**Deliverables:**
- `lib/project_detection.sh`
- `lib/file_discovery.sh`
- `lib/task_id_parser.sh`

**Testing:**
```bash
# Unit tests
./tests/unit/test_project_detection.bats
./tests/unit/test_file_discovery.bats
./tests/unit/test_task_id_parser.bats

# Test cases
✓ Detect ai-engineer project correctly
✓ Detect MyDrive project correctly
✓ Extract task IDs: TASK-003, TASK-003B, TASK-003B-4
✓ Group files by task ID correctly
✓ Filter out already-migrated files
```

**Estimated LOC:** 235 lines

---

### Phase C: Backup Management (2 hours)

**Deliverables:**
- `lib/backup_manager.sh`
- Backup creation with compression
- Rollback functionality

**Testing:**
```bash
# Unit tests
./tests/unit/test_backup_manager.bats

# Test cases
✓ Create backup successfully
✓ Backup includes all relevant files
✓ Rollback restores previous state
✓ List backups correctly
```

**Estimated LOC:** 75 lines

---

### Phase D: Git Operations (2 hours)

**Deliverables:**
- `lib/git_operations.sh`
- Git mv wrapper with error handling
- Repository validation

**Testing:**
```bash
# Unit tests
./tests/unit/test_git_operations.bats

# Test cases
✓ Git mv preserves file history
✓ Create destination directories automatically
✓ Handle git mv failures gracefully
✓ Detect uncommitted changes
```

**Estimated LOC:** 70 lines

---

### Phase E: Link Management (2 hours)

**Deliverables:**
- `lib/link_updater.sh`
- Markdown link detection and update
- Link validation

**Testing:**
```bash
# Unit tests
./tests/unit/test_link_updater.bats

# Test cases
✓ Update relative links correctly (+1 ../)
✓ Preserve absolute URLs
✓ Handle reference-style links
✓ Detect broken links
✓ Validate updated links
```

**Estimated LOC:** 90 lines

---

### Phase F: Name Standardization (1.5 hours)

**Deliverables:**
- `lib/name_standardizer.sh`
- Filename normalization rules
- Coverage and analysis filename handling

**Testing:**
```bash
# Unit tests
./tests/unit/test_name_standardizer.bats

# Test cases
✓ Standardize: *implementation* → implementation-summary.md
✓ Standardize: *completion* → completion-summary.md
✓ Standardize: coverage-task006.json → task-006-coverage.json
✓ Handle edge cases: spaces, unicode, uppercase
```

**Estimated LOC:** 85 lines

---

### Phase G: Validation and Reporting (2 hours)

**Deliverables:**
- `lib/validator.sh`
- Post-migration validation checks
- Migration report generation

**Testing:**
```bash
# Unit tests
./tests/unit/test_validator.bats

# Test cases
✓ Detect files remaining in root
✓ Identify broken links
✓ Validate git status
✓ Generate comprehensive report
```

**Estimated LOC:** 95 lines

---

## 4. Key Algorithms

### 4.1 Task ID Extraction with Edge Cases

**Algorithm:**
```
INPUT: filename (string)
OUTPUT: task_id (string) or empty string

1. Remove file extension (.md)
2. Apply regex patterns in priority order:
   a. TASK-NNN (simple numeric) → "TASK-003"
   b. TASK-NNNL (with letter) → "TASK-003B"
   c. TASK-NNNL-N (with letter and number) → "TASK-003B-4"
3. If no match, return empty string
4. Validate format using is_valid_task_id()
5. Return normalized task ID

EDGE CASES:
- TASK-003B-4-IMPLEMENTATION-SUMMARY.md → TASK-003B-4
- TASK_DUPLICATION_ANALYSIS.md → "" (not a task)
- task-003-summary.md → "" (lowercase not supported)
- TASK-003B-4.5.md → "" (decimal not supported)
```

**Complexity:** O(1) - Regex matching

---

### 4.2 Relative Link Path Adjustment

**Algorithm:**
```
INPUT:
  - markdown_file (path)
  - depth_change (integer, default: 1)
OUTPUT: updated_file (with adjusted links)

1. Parse markdown file line by line
2. For each line:
   a. Detect link patterns:
      - Inline: [text](path)
      - Reference: [ref]: path
   b. Extract link path
   c. If path is relative (not http/https):
      - Calculate prefix: repeat "../" depth_change times
      - Prepend prefix to path
   d. Replace original link with updated link
3. Write updated content back to file
4. Validate updated links

EXAMPLE:
  Original: [docs](../docs/guide.md)
  Depth change: 1
  Updated: [docs](../../docs/guide.md)

EDGE CASES:
- Absolute URLs (http/https) → no change
- Already absolute paths (/path/to/file) → no change
- Anchor links (#section) → no change
- Images ![alt](path) → same logic as links
```

**Complexity:** O(n*m) where n = lines, m = links per line

---

### 4.3 File Naming Standardization

**Algorithm:**
```
INPUT:
  - original_filename (string)
  - task_id (string)
OUTPUT: standardized_filename (string)

1. Remove file extension
2. Remove task ID prefix
   - "TASK-003B-4-IMPLEMENTATION-SUMMARY" → "IMPLEMENTATION-SUMMARY"
3. Convert to lowercase
4. Replace underscores with hyphens
5. Apply naming rules (pattern matching):
   - *implementation* → "implementation-summary.md"
   - *completion* → "completion-summary.md"
   - *complexity* → "complexity-evaluation.md"
   - *design* → "design-summary.md"
   - *test* → "test-results.md"
   - *day-N* → preserve numbering
6. If no match, use normalized name

EDGE CASES:
- Multiple hyphens → collapse to single
- Special characters → remove or escape
- Unicode → preserve (UTF-8 support)
- Spaces → replace with hyphens
```

**Complexity:** O(1) - String operations

---

### 4.4 Idempotency Check

**Algorithm:**
```
INPUT: migration_state (current file system)
OUTPUT: boolean (already_migrated or not)

1. Check if task subfolders already exist:
   - Scan tasks/completed/ for TASK-XXX directories
2. For each task folder:
   - Check if main task file exists (TASK-XXX.md)
   - Check if related files exist
3. If task folder exists and contains files:
   - Mark as already migrated
   - Skip migration for this task
4. If task folder doesn't exist or is empty:
   - Mark as needs migration

VERIFICATION:
- Count task files in root (should be 0 after migration)
- Count task subfolders in tasks/completed/ (should match task count)
- Verify no duplicate files

IDEMPOTENCY GUARANTEE:
- Running script twice should result in:
  - First run: N files migrated
  - Second run: 0 files migrated, all skipped
```

**Complexity:** O(n) where n = number of tasks

---

## 5. Testing Strategy

### 5.1 Unit Tests (60% coverage target)

**Test Framework:** BATS (Bash Automated Testing System)

**Unit Test Files:**

```bash
tests/unit/
├── test_task_id_parser.bats          # 12 test cases
├── test_link_updater.bats            # 15 test cases
├── test_name_standardizer.bats       # 10 test cases
├── test_file_discovery.bats          # 8 test cases
├── test_backup_manager.bats          # 6 test cases
├── test_git_operations.bats          # 7 test cases
├── test_project_detection.bats       # 4 test cases
└── test_validator.bats               # 9 test cases

Total: 71 unit test cases
```

**Example Unit Test:**
```bash
# tests/unit/test_task_id_parser.bats

@test "extract_task_id: simple numeric" {
  result=$(extract_task_id "TASK-003-SUMMARY.md")
  [ "$result" = "TASK-003" ]
}

@test "extract_task_id: with letter suffix" {
  result=$(extract_task_id "TASK-003B-IMPLEMENTATION.md")
  [ "$result" = "TASK-003B" ]
}

@test "extract_task_id: with letter and number" {
  result=$(extract_task_id "TASK-003B-4-COMPLEXITY-ANALYSIS.md")
  [ "$result" = "TASK-003B-4" ]
}

@test "extract_task_id: analysis file returns empty" {
  result=$(extract_task_id "TASK_DUPLICATION_ANALYSIS.md")
  [ -z "$result" ]
}
```

---

### 5.2 Integration Tests (30% coverage target)

**Integration Test Files:**

```bash
tests/integration/
├── test_migration_flow.bats          # End-to-end migration
├── test_idempotency.bats            # Run twice, verify no changes
├── test_edge_cases.bats             # Spaces, unicode, conflicts
└── test_rollback.bats               # Backup and rollback scenarios

Total: 29 integration test cases
```

**Example Integration Test:**
```bash
# tests/integration/test_migration_flow.bats

setup() {
  # Create test repository
  export TEST_DIR=$(mktemp -d)
  cd "$TEST_DIR"
  git init

  # Create sample files
  mkdir -p tasks/completed
  echo "# Task 003" > tasks/completed/TASK-003.md
  echo "# Implementation" > TASK-003-IMPLEMENTATION-SUMMARY.md
  git add .
  git commit -m "Initial commit"
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "end-to-end migration success" {
  # Run migration
  run ./migrate-completed-tasks.sh --execute
  [ "$status" -eq 0 ]

  # Verify structure
  [ -d "tasks/completed/TASK-003" ]
  [ -f "tasks/completed/TASK-003/TASK-003.md" ]
  [ -f "tasks/completed/TASK-003/implementation-summary.md" ]

  # Verify root is clean
  [ ! -f "TASK-003-IMPLEMENTATION-SUMMARY.md" ]
}

@test "idempotency: second run makes no changes" {
  # First run
  ./migrate-completed-tasks.sh --execute

  # Second run
  run ./migrate-completed-tasks.sh --execute
  [ "$status" -eq 0 ]
  [[ "$output" =~ "already migrated" ]]
}
```

---

### 5.3 Edge Case Tests (10% coverage target)

**Edge Cases to Test:**

1. **Filenames with spaces**
   - Input: `TASK-003 IMPLEMENTATION SUMMARY.md`
   - Expected: Handled correctly or error message

2. **Unicode characters**
   - Input: `TASK-003-日本語-SUMMARY.md`
   - Expected: Preserve unicode in standardized name

3. **Conflicting filenames**
   - Scenario: Two files map to same standardized name
   - Expected: Append suffix (e.g., `-2.md`)

4. **Nested task folders**
   - Scenario: Task folder already contains subdirectories
   - Expected: Preserve structure or flatten

5. **Broken symlinks**
   - Scenario: Task file is symlink to missing file
   - Expected: Skip or error with clear message

6. **Very long filenames**
   - Input: `TASK-003-VERY-LONG-FILENAME-THAT-EXCEEDS-255-CHARACTERS...`
   - Expected: Truncate or error

7. **Concurrent execution**
   - Scenario: Run two instances simultaneously
   - Expected: Lock file prevents second instance

8. **Partial migration state**
   - Scenario: Previous migration was interrupted
   - Expected: Resume or rollback

9. **Git merge conflicts**
   - Scenario: Merge conflict in migrated files
   - Expected: Detect and abort with error

10. **Empty task folders**
    - Scenario: Task folder created but no files
    - Expected: Skip or create .gitkeep

**Example Edge Case Test:**
```bash
@test "edge case: filename with spaces" {
  echo "# Test" > "TASK-003 IMPLEMENTATION SUMMARY.md"

  run ./migrate-completed-tasks.sh --execute
  [ "$status" -eq 0 ]

  # Verify file moved correctly
  [ -f "tasks/completed/TASK-003/implementation-summary.md" ]
}
```

---

### 5.4 Test Coverage Plan

**Target Coverage:** 80%+

**Coverage Breakdown:**
- **lib/task_id_parser.sh**: 90% (critical path)
- **lib/link_updater.sh**: 85% (high complexity)
- **lib/name_standardizer.sh**: 85% (many edge cases)
- **lib/file_discovery.sh**: 80%
- **lib/backup_manager.sh**: 75%
- **lib/git_operations.sh**: 75%
- **lib/validator.sh**: 80%
- **lib/core.sh**: 70% (utility functions)

**Coverage Tool:**
```bash
# Use bashcov for coverage analysis
gem install bashcov

# Run tests with coverage
bashcov -- bats tests/unit/*.bats tests/integration/*.bats

# Generate HTML report
bashcov --html coverage/
```

---

## 6. Error Handling

### 6.1 Error Categories

**Category 1: Validation Errors (Exit Code 1)**
- Not a git repository
- Bash version < 4.0
- Missing required commands (git, find, sed)
- Lock file exists (concurrent execution)

**Category 2: Migration Errors (Exit Code 2)**
- Git mv failure
- File not found during migration
- Permission denied
- Disk space insufficient

**Category 3: Backup Errors (Exit Code 3)**
- Backup creation failed
- Backup corruption detected
- Rollback failure

**Category 4: Validation Errors (Exit Code 4)**
- Broken links after migration
- Files still in root after migration
- Empty task folders created

---

### 6.2 Error Handling Strategies

**Strategy 1: Fail Fast**
```bash
set -euo pipefail

# Exit immediately on:
# - Non-zero exit code (-e)
# - Undefined variables (-u)
# - Pipe failures (-o pipefail)
```

**Strategy 2: Graceful Degradation**
```bash
# Allow non-critical operations to fail
find docs/tasks -name "TASK-*.md" 2>/dev/null || true
```

**Strategy 3: Transactional Migration**
```bash
# Pseudo-code
begin_transaction()
  create_backup()
  migrate_files() || rollback_backup()
  validate_migration() || rollback_backup()
end_transaction()
```

**Strategy 4: Error Recovery**
```bash
handle_error() {
  local exit_code=$?
  local line_number=$1

  log ERROR "Error on line $line_number (exit code: $exit_code)"

  # Attempt recovery
  if [[ -f "$BACKUP_FILE" ]]; then
    log WARN "Attempting automatic rollback..."
    rollback_backup "$BACKUP_FILE"
  fi

  cleanup_on_exit
  exit "$exit_code"
}

trap 'handle_error $LINENO' ERR
```

---

### 6.3 Error Handling Flowchart

```
[Error Detected]
      ↓
[Determine Error Category]
      ↓
  ┌───┴───┐
  ↓       ↓
[Critical] [Non-Critical]
  ↓           ↓
[Log Error] [Log Warning]
  ↓           ↓
[Check Backup Exists]
  ↓
[Rollback if Available]
  ↓
[Cleanup Resources]
  ↓
[Exit with Code]
```

---

## 7. Dependencies

### 7.1 External Commands

**Required (Must Have):**
- `bash` (v4.0+) - Associative arrays support
- `git` (v2.0+) - For git mv and history preservation
- `find` - File discovery
- `grep` - Pattern matching
- `sed` - Text processing
- `awk` - Text processing
- `tar` - Backup compression

**Optional (Nice to Have):**
- `markdown-link-check` - Link validation
- `shellcheck` - Static analysis
- `bats` - Testing framework
- `bashcov` - Coverage analysis

---

### 7.2 Dependency Checking

```bash
# Check bash version
check_bash_version() {
  local version="${BASH_VERSINFO[0]}"
  if [[ $version -lt 4 ]]; then
    die "Bash 4.0+ required (current: $version)" 1
  fi
}

# Check required commands
check_required_commands() {
  local required_commands=(git find grep sed awk tar)
  local missing_commands=()

  for cmd in "${required_commands[@]}"; do
    if ! command -v "$cmd" &>/dev/null; then
      missing_commands+=("$cmd")
    fi
  done

  if [[ ${#missing_commands[@]} -gt 0 ]]; then
    die "Missing required commands: ${missing_commands[*]}" 1
  fi
}
```

---

### 7.3 Platform Compatibility

**Supported Platforms:**
- ✅ macOS (10.15+)
- ✅ Linux (Ubuntu 18.04+, Debian 10+, RHEL 8+)
- ⚠️ Windows (via Git Bash, WSL, or Cygwin)

**Platform-Specific Considerations:**

```bash
# Detect platform
detect_platform() {
  case "$(uname -s)" in
    Darwin*)  echo "macos" ;;
    Linux*)   echo "linux" ;;
    CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

# Platform-specific sed syntax
sed_in_place() {
  local file=$1
  shift
  local pattern="$*"

  if [[ "$(detect_platform)" == "macos" ]]; then
    sed -i '' "$pattern" "$file"  # macOS requires '' after -i
  else
    sed -i "$pattern" "$file"     # Linux doesn't
  fi
}
```

---

## 8. Risks and Mitigations

### Risk 1: Git History Loss

**Risk Level:** HIGH
**Impact:** Permanent loss of file history and blame information

**Mitigation:**
- ✅ **Always use `git mv` instead of regular `mv`**
- ✅ **Verify git status after each move**
- ✅ **Create backup before any file operations**
- ✅ **Test on sample repository first**

**Validation:**
```bash
# After migration, verify history preserved
git log --follow tasks/completed/TASK-003/TASK-003.md
# Should show full history from original location
```

---

### Risk 2: Broken Links

**Risk Level:** MEDIUM
**Impact:** Documentation becomes fragmented, references fail

**Mitigation:**
- ✅ **Comprehensive link detection** (inline + reference-style)
- ✅ **Accurate path adjustment** (depth-aware)
- ✅ **Post-migration link validation**
- ✅ **Dry-run mode to preview changes**

**Validation:**
```bash
# Use markdown-link-check if available
find tasks/completed -name "*.md" -exec markdown-link-check {} \;
```

---

### Risk 3: Data Loss

**Risk Level:** HIGH
**Impact:** Permanent loss of task files or related documents

**Mitigation:**
- ✅ **Mandatory backup before migration** (cannot skip by default)
- ✅ **Rollback capability** (restore from backup)
- ✅ **Dry-run mode** (preview without changes)
- ✅ **Interactive mode** (confirm each phase)

**Recovery Strategy:**
```bash
# If migration fails, rollback immediately
./migrate-completed-tasks.sh --rollback .migration-backups/backup-20251017-120000.tar.gz
```

---

### Risk 4: Concurrent Execution

**Risk Level:** MEDIUM
**Impact:** File corruption, duplicate migrations, inconsistent state

**Mitigation:**
- ✅ **Lock file mechanism** (.migration-lock)
- ✅ **Atomic file creation** (use `set -C` for lock)
- ✅ **Process ID tracking** (store PID in lock file)
- ✅ **Stale lock detection** (check if process still running)

**Implementation:**
```bash
create_lock_file() {
  if (set -C; echo $$ > "$LOCK_FILE") 2>/dev/null; then
    trap remove_lock_file EXIT
    return 0
  else
    local lock_pid=$(cat "$LOCK_FILE" 2>/dev/null)
    if ! kill -0 "$lock_pid" 2>/dev/null; then
      log WARN "Stale lock file detected, removing"
      rm -f "$LOCK_FILE"
      return 0
    fi
    die "Migration already in progress (PID: $lock_pid)" 1
  fi
}
```

---

### Risk 5: Partial Migration State

**Risk Level:** MEDIUM
**Impact:** Incomplete migration, files in inconsistent locations

**Mitigation:**
- ✅ **Atomic operations** (move all or none per task)
- ✅ **Transaction-like behavior** (rollback on failure)
- ✅ **Resume capability** (detect partial state, continue)
- ✅ **Idempotency** (safe to re-run)

**Detection:**
```bash
detect_partial_migration() {
  # Check if some tasks migrated, others not
  local migrated_count=$(find tasks/completed -mindepth 1 -maxdepth 1 -type d | wc -l)
  local root_files_count=$(find . -maxdepth 1 -name "TASK-*.md" | wc -l)

  if [[ $migrated_count -gt 0 && $root_files_count -gt 0 ]]; then
    log WARN "Partial migration detected"
    return 0
  fi
  return 1
}
```

---

### Risk 6: Performance Issues

**Risk Level:** LOW
**Impact:** Slow execution on large repositories

**Mitigation:**
- ✅ **Batch operations** (group files by task)
- ✅ **Parallel processing** (use `xargs -P` for large sets)
- ✅ **Progress indicators** (show % complete)
- ✅ **Optimize regex** (compile once, reuse)

**Performance Optimization:**
```bash
# Parallel git mv for large file sets
parallel_git_mv() {
  local files=("$@")

  printf '%s\n' "${files[@]}" | \
    xargs -P 4 -I {} bash -c 'git_move_file {}'
}
```

---

## 9. Estimated Effort Summary

### 9.1 Development Phase Breakdown

| Phase | Component | LOC | Hours | Dependencies |
|-------|-----------|-----|-------|--------------|
| A | CLI + Infrastructure | 200 | 3 | None |
| B | File Discovery | 235 | 2 | Phase A |
| C | Backup Management | 75 | 2 | Phase A |
| D | Git Operations | 70 | 2 | Phase A |
| E | Link Management | 90 | 2 | Phase A, D |
| F | Name Standardization | 85 | 1.5 | Phase A |
| G | Validation + Reporting | 95 | 2 | All phases |

**Total Development:** 850 LOC, 14.5 hours

---

### 9.2 Testing Phase Breakdown

| Test Type | Test Cases | Hours | Coverage Target |
|-----------|------------|-------|-----------------|
| Unit Tests | 71 | 4 | 60% |
| Integration Tests | 29 | 3 | 30% |
| Edge Case Tests | 10 | 2 | 10% |
| Manual QA | N/A | 2 | N/A |

**Total Testing:** 11 hours

---

### 9.3 Documentation and Deployment

| Activity | Hours |
|----------|-------|
| Technical Design Document | 3 (completed) |
| User Guide | 1 |
| API Documentation | 1 |
| Deployment Testing | 2 |
| Post-Deployment Monitoring | 1 |

**Total Documentation:** 8 hours

---

### 9.4 Grand Total

**Total Estimated Effort:**
- Development: 14.5 hours
- Testing: 11 hours
- Documentation: 8 hours
- **TOTAL: 33.5 hours (~4-5 working days)**

**With Contingency (25%):** 42 hours (~5-6 working days)

---

## 10. Success Criteria

### 10.1 Functional Success Criteria

- ✅ **All 54 task files migrated** from root to `tasks/completed/TASK-XXX/`
- ✅ **All 6 coverage files organized** in `coverage/reports/`
- ✅ **All analysis files archived** in `docs/archive/`
- ✅ **Zero files remaining in root** (except essential project files)
- ✅ **All relative links updated** and validated
- ✅ **Git history preserved** for all moved files
- ✅ **Idempotent execution** (safe to run multiple times)

---

### 10.2 Quality Success Criteria

- ✅ **80%+ test coverage** (unit + integration tests)
- ✅ **Zero broken links** after migration
- ✅ **Shellcheck clean** (no warnings or errors)
- ✅ **All edge cases handled** gracefully
- ✅ **Comprehensive error messages** for failures
- ✅ **Backup/rollback tested** and verified

---

### 10.3 Performance Success Criteria

- ✅ **Migration completes in <2 minutes** for ai-engineer (62 files)
- ✅ **Migration completes in <5 minutes** for MyDrive (200+ files)
- ✅ **Backup creation in <30 seconds**
- ✅ **Link validation in <1 minute**

---

### 10.4 Usability Success Criteria

- ✅ **Clear help message** with examples
- ✅ **Progress indicators** during execution
- ✅ **Dry-run mode** for safe preview
- ✅ **Interactive mode** for step-by-step confirmation
- ✅ **Comprehensive migration report** at completion

---

## 11. Deployment Plan

### 11.1 Pre-Deployment Checklist

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Edge case tests passing
- [ ] Shellcheck validation clean
- [ ] Backup/rollback tested
- [ ] Dry-run tested on both projects
- [ ] Documentation complete
- [ ] Code review completed

---

### 11.2 Deployment Steps

**Step 1: Deploy to ai-engineer (smaller scope)**
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/ai-engineer

# 1. Review current state
find . -maxdepth 1 -name "TASK-*.md" | wc -l  # Should show 54

# 2. Run dry-run
./migrate-completed-tasks.sh

# 3. Review preview, confirm no issues

# 4. Execute migration
./migrate-completed-tasks.sh --execute --interactive

# 5. Verify results
./migrate-completed-tasks.sh --validate-only

# 6. Commit changes
git add -A
git commit -m "feat: Reorganize completed task files into subfolders (TASK-016)"
git push
```

**Step 2: Deploy to MyDrive (larger scope)**
```bash
cd /Users/richardwoollcott/Projects/appmilla_github/DeCUK.Mobile.MyDrive

# Follow same steps as ai-engineer
# Expected to migrate 200+ files
```

---

### 11.3 Post-Deployment Validation

**Validation Checklist:**
- [ ] No task files in root directory
- [ ] All task subfolders have at least one file
- [ ] No broken links detected
- [ ] Git history preserved (verify with `git log --follow`)
- [ ] Coverage files in correct location
- [ ] Analysis files archived
- [ ] `.gitignore` updated
- [ ] Documentation updated

---

### 11.4 Rollback Plan

**If migration fails or issues detected:**
```bash
# Option 1: Git reset (if not yet pushed)
git reset --hard HEAD~1

# Option 2: Rollback using backup
./migrate-completed-tasks.sh --rollback .migration-backups/backup-20251017-120000.tar.gz

# Option 3: Manual rollback
git revert <commit-hash>
```

---

## 12. Appendix

### 12.1 File Structure After Migration

```
/Users/richardwoollcott/Projects/appmilla_github/ai-engineer/
├── migrate-completed-tasks.sh              # Main script
├── lib/
│   ├── core.sh                            # Core utilities
│   ├── project_detection.sh               # Project type detection
│   ├── file_discovery.sh                  # File finding
│   ├── task_id_parser.sh                  # Task ID extraction
│   ├── backup_manager.sh                  # Backup/rollback
│   ├── git_operations.sh                  # Git mv wrapper
│   ├── link_updater.sh                    # Link adjustment
│   ├── name_standardizer.sh               # Filename normalization
│   └── validator.sh                       # Post-migration validation
├── tests/
│   ├── unit/
│   │   ├── test_task_id_parser.bats
│   │   ├── test_link_updater.bats
│   │   ├── test_name_standardizer.bats
│   │   ├── test_file_discovery.bats
│   │   ├── test_backup_manager.bats
│   │   ├── test_git_operations.bats
│   │   ├── test_project_detection.bats
│   │   └── test_validator.bats
│   └── integration/
│       ├── test_migration_flow.bats
│       ├── test_idempotency.bats
│       ├── test_edge_cases.bats
│       └── test_rollback.bats
├── .migration-backups/
│   └── backup-20251017-120000.tar.gz
├── tasks/completed/
│   ├── TASK-002/
│   │   └── completion-report.md
│   ├── TASK-003A/
│   │   └── implementation-summary.md
│   ├── TASK-003B-4/
│   │   ├── complexity-analysis.md
│   │   ├── design-summary.md
│   │   ├── implementation-plan.md
│   │   └── implementation-summary.md
│   └── ... (52 more task folders)
├── coverage/
│   ├── .gitkeep
│   ├── .gitignore
│   └── reports/
│       ├── coverage.json
│       ├── task-003e-coverage.json
│       ├── task-006-coverage.json
│       └── ... (6 coverage files)
└── docs/
    └── archive/
        ├── task-duplication-analysis.md
        └── task-numbering-correction.md
```

---

### 12.2 Command Examples

**Basic Usage:**
```bash
# Preview migration (dry-run)
./migrate-completed-tasks.sh

# Execute migration with interactive confirmation
./migrate-completed-tasks.sh --execute --interactive

# Execute migration (auto-approve all)
./migrate-completed-tasks.sh --execute

# Validate existing structure
./migrate-completed-tasks.sh --validate-only

# Rollback to backup
./migrate-completed-tasks.sh --rollback .migration-backups/backup-20251017-120000.tar.gz
```

**Advanced Usage:**
```bash
# Force migration (skip safety checks)
./migrate-completed-tasks.sh --execute --force

# Skip backup (not recommended)
./migrate-completed-tasks.sh --execute --skip-backup

# Verbose output
./migrate-completed-tasks.sh --execute --verbose

# Quiet mode (errors only)
./migrate-completed-tasks.sh --execute --quiet
```

---

### 12.3 Troubleshooting Guide

**Issue 1: "Lock file exists" error**
```bash
# Check if migration is actually running
ps aux | grep migrate-completed-tasks.sh

# If no process found, remove stale lock
rm -f .migration-lock

# Retry migration
./migrate-completed-tasks.sh --execute
```

**Issue 2: "Git mv failed" error**
```bash
# Check git status
git status

# Ensure working tree is clean
git add -A
git commit -m "WIP: Before migration"

# Retry migration
./migrate-completed-tasks.sh --execute
```

**Issue 3: "Broken links detected" warning**
```bash
# Validate links manually
markdown-link-check tasks/completed/TASK-003/TASK-003.md

# Fix broken links manually
# Re-run validation
./migrate-completed-tasks.sh --validate-only
```

---

### 12.4 References

**Bash Best Practices:**
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/)
- [ShellCheck](https://www.shellcheck.net/)

**Testing:**
- [BATS Documentation](https://github.com/bats-core/bats-core)
- [bashcov Coverage Tool](https://github.com/infertux/bashcov)

**Git Operations:**
- [Git mv Documentation](https://git-scm.com/docs/git-mv)
- [Preserving Git History](https://stackoverflow.com/questions/2314652/is-it-possible-to-move-rename-files-in-git-and-maintain-their-history)

---

## 13. Conclusion

This technical design provides a comprehensive blueprint for implementing a production-ready bash script to migrate 62 files in the ai-engineer project and establish a maintainable task organization structure. The design emphasizes:

- **Safety**: Mandatory backups, rollback capability, git history preservation
- **Reliability**: Idempotent execution, comprehensive error handling, validation
- **Maintainability**: Modular architecture, extensive testing, clear documentation
- **Performance**: Efficient algorithms, parallel processing, progress indicators

**Next Steps:**
1. Review and approve this technical design
2. Begin Phase A implementation (CLI + Infrastructure)
3. Implement phases B-G sequentially with testing
4. Deploy to ai-engineer project first (smaller scope)
5. Deploy to MyDrive project after validation

**Estimated Timeline:** 5-6 working days with 25% contingency buffer

---

**Document Version:** 1.0
**Author:** AI Engineer System
**Date:** 2025-10-17
**Related Task:** TASK-016
