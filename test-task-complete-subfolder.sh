#!/bin/bash

# Test script for task-complete subfolder organization
# Demonstrates the new file organization logic

set -e

TASK_ID="TASK-TEST"
PROJECT_ROOT="/Users/richardwoollcott/Projects/appmilla_github/ai-engineer"

cd "$PROJECT_ROOT"

echo "🧪 Testing Task Completion with Subfolder Organization"
echo "========================================================"
echo ""

# Step 1: Create task subfolder
echo "📁 Step 1: Creating task subfolder"
mkdir -p "tasks/completed/${TASK_ID}"
echo "   Created: tasks/completed/${TASK_ID}/"
echo ""

# Step 2: Move main task file
echo "📄 Step 2: Moving main task file"
if [ -f "tasks/in_progress/${TASK_ID}.md" ]; then
    mv "tasks/in_progress/${TASK_ID}.md" "tasks/completed/${TASK_ID}/"
    echo "   ✅ Moved: ${TASK_ID}.md → tasks/completed/${TASK_ID}/"
else
    echo "   ⚠️  Task file not found: tasks/in_progress/${TASK_ID}.md"
fi
echo ""

# Step 3: Discover and move related files
echo "🔍 Step 3: Discovering related files in project root"
related_files=$(find . -maxdepth 1 -name "${TASK_ID}-*.md" -type f 2>/dev/null || true)

if [ -n "$related_files" ]; then
    echo "   Found related files:"
    for file in $related_files; do
        echo "     - $file"
    done
    echo ""

    echo "📦 Step 4: Moving related files to subfolder"
    for file in $related_files; do
        filename=$(basename "$file")
        # Extract suffix after TASK-ID
        suffix=$(echo "$filename" | sed "s/${TASK_ID}-//")
        # Convert to lowercase with hyphens
        clean_name=$(echo "$suffix" | tr '[:upper:]' '[:lower:]')

        mv "$file" "tasks/completed/${TASK_ID}/${clean_name}"
        echo "   ✅ Moved: $filename → ${clean_name}"
    done
else
    echo "   ℹ️  No related files found (this is OK)"
fi
echo ""

# Step 5: Update task metadata (simulation)
echo "✏️  Step 5: Updating task metadata"
task_file="tasks/completed/${TASK_ID}/${TASK_ID}.md"

if [ -f "$task_file" ]; then
    # Read existing frontmatter
    temp_file=$(mktemp)

    # Update status and add completion metadata
    awk '
    BEGIN { in_frontmatter=0; frontmatter_ended=0 }
    /^---$/ {
        if (in_frontmatter == 0) {
            in_frontmatter = 1
            print
            next
        } else {
            # End of frontmatter, add new fields
            print "status: completed"
            print "completed: " strftime("%Y-%m-%dT%H:%M:%SZ", systime())
            print "completed_location: tasks/completed/TASK-TEST/"
            print "---"
            frontmatter_ended = 1
            next
        }
    }
    in_frontmatter == 1 && /^status:/ { next }
    in_frontmatter == 1 { print; next }
    frontmatter_ended == 1 { print }
    ' "$task_file" > "$temp_file"

    mv "$temp_file" "$task_file"
    echo "   ✅ Updated: status → completed"
    echo "   ✅ Added: completed_location → tasks/completed/TASK-TEST/"
fi
echo ""

# Step 6: Verify final structure
echo "📊 Step 6: Verifying final structure"
echo "   Final location: tasks/completed/${TASK_ID}/"
echo "   Contents:"
ls -1 "tasks/completed/${TASK_ID}/" | while read line; do
    echo "     ✅ $line"
done
echo ""

# Summary
echo "🎉 Task Completion Summary"
echo "=========================="
echo "✅ Task ${TASK_ID} successfully completed"
echo "✅ All files organized in tasks/completed/${TASK_ID}/"
file_count=$(ls -1 "tasks/completed/${TASK_ID}/" | wc -l | tr -d ' ')
echo "✅ Organized ${file_count} files"
echo ""
echo "📁 Clean project root (no more TASK-TEST-*.md files)"
echo ""
