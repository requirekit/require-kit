# Figma MCP Server Setup Guide

## Overview

The Figma MCP (Model Context Protocol) server enables Claude Code to directly extract design specifications, images, and design tokens from Figma files. This integration is essential for the UX design specialist sub-agents to implement pixel-perfect components from Figma designs.

**Official Resources:**
- [Figma MCP Announcement](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)

---

## Prerequisites

- Claude Code installed and configured
- Figma account with access to design files
- Node.js 18+ installed (for MCP server)
- npm or yarn package manager

---

## Installation Steps

### 1. Install Figma MCP Server

The Figma MCP server is typically installed globally or as part of your project:

```bash
# Global installation (recommended)
npm install -g @figma/mcp-server

# Or via Claude Code MCP registry
# Claude Code will prompt you to install when first accessing Figma tools
```

### 2. Get Figma Personal Access Token

1. Go to [Figma Account Settings](https://www.figma.com/settings)
2. Navigate to **Personal Access Tokens** section
3. Click **Generate new token**
4. Give it a descriptive name (e.g., "Claude Code MCP Integration")
5. Set appropriate scopes:
   - ✅ File content - Read only
   - ✅ Design system - Read only (if using design tokens)
   - ✅ Dev resources - Read only
6. Copy the token immediately (it won't be shown again)

### 3. Configure MCP Server in Claude Code

Add the Figma MCP configuration to your Claude Code settings:

**Location:** `~/.claude/config.json` or project-specific `.claude/config.json`

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": [
        "@figma/mcp-server"
      ],
      "env": {
        "FIGMA_ACCESS_TOKEN": "YOUR_FIGMA_TOKEN_HERE"
      }
    }
  }
}
```

**Security Note:** For production use, consider storing the token in a secure environment variable rather than directly in the config file:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": [
        "@figma/mcp-server"
      ],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_TOKEN}"
      }
    }
  }
}
```

Then set the environment variable:
```bash
# Add to ~/.bashrc or ~/.zshrc
export FIGMA_TOKEN="your_figma_token_here"
```

### 4. Verify Installation

Test the MCP connection in Claude Code:

```bash
# In Claude Code, try listing available MCP tools
@mcp list

# You should see Figma tools like:
# - figma-dev-mode:get_code
# - figma-dev-mode:get_image
# - figma-dev-mode:get_variable_defs
```

Or verify manually:

```bash
# Test with a Figma file URL
@figma-dev-mode:get_metadata --fileKey="YOUR_FILE_KEY"
```

---

## Available MCP Tools

### 1. `figma-dev-mode:get_code`

Extract code snippets and component specifications from Figma nodes.

**Usage:**
```bash
figma-dev-mode:get_code \
  --nodeId="2:3" \
  --fileKey="abc123xyz" \
  --clientFrameworks="react"
```

**Parameters:**
- `nodeId` (required): Node ID in format "X:Y" (convert from URL format)
- `fileKey` (required): File key from Figma URL
- `clientFrameworks` (optional): Target framework (react, vue, html, etc.)

**Returns:**
- Component structure
- Styling specifications (CSS/Tailwind)
- Dimensions and layout
- Text content
- Interactive properties

### 2. `figma-dev-mode:get_image`

Get a rendered image/screenshot of a Figma node.

**Usage:**
```bash
figma-dev-mode:get_image \
  --nodeId="2:3" \
  --fileKey="abc123xyz" \
  --format="png" \
  --scale=2
```

**Parameters:**
- `nodeId` (required): Node ID in "X:Y" format
- `fileKey` (required): File key from Figma URL
- `format` (optional): png, jpg, svg (default: png)
- `scale` (optional): 1-4 for resolution (default: 2)

**Returns:**
- Base64 encoded image
- Image URL (temporary)
- Dimensions

### 3. `figma-dev-mode:get_variable_defs`

Extract design tokens and variables from Figma files.

**Usage:**
```bash
figma-dev-mode:get_variable_defs \
  --nodeId="2:3" \
  --fileKey="abc123xyz"
```

**Returns:**
- Color tokens
- Typography tokens
- Spacing tokens
- Effect tokens (shadows, etc.)
- Variable references

### 4. `figma-dev-mode:get_metadata`

Get file and node metadata.

**Usage:**
```bash
figma-dev-mode:get_metadata \
  --fileKey="abc123xyz"
```

**Returns:**
- File name
- Last modified date
- Version information
- Component library info

---

## Critical: Node ID Conversion

**IMPORTANT:** Figma URLs use hyphens in node IDs, but the API requires colons.

### URL Format → API Format

| Figma URL | API Parameter |
|-----------|---------------|
| `node-id=2-2` | `nodeId: "2:2"` |
| `node-id=15-24` | `nodeId: "15:24"` |
| `node-id=123-456` | `nodeId: "123:456"` |

### Conversion Examples

**Example 1:**
```
URL: https://figma.com/design/abc123?node-id=2-2
           ↓
API: figma-dev-mode:get_code --nodeId="2:2" --fileKey="abc123"
```

**Example 2:**
```
URL: https://figma.com/file/xyz789/Project?node-id=15-24
           ↓
API: figma-dev-mode:get_image --nodeId="15:24" --fileKey="xyz789"
```

### Conversion Function (JavaScript)

```javascript
function convertNodeId(url) {
  const match = url.match(/node-id=(\d+)-(\d+)/);
  if (match) {
    return `${match[1]}:${match[2]}`;
  }
  return null;
}

// Usage
const url = "https://figma.com/design/abc?node-id=2-2";
const nodeId = convertNodeId(url); // Returns "2:2"
```

### Conversion Function (Python)

```python
import re

def convert_node_id(url: str) -> str | None:
    """Convert Figma URL node-id format to API format."""
    match = re.search(r'node-id=(\d+)-(\d+)', url)
    if match:
        return f"{match.group(1)}:{match.group(2)}"
    return None

# Usage
url = "https://figma.com/design/abc?node-id=2-2"
node_id = convert_node_id(url)  # Returns "2:2"
```

---

## Common Usage Patterns

### Pattern 1: Extract React Component

```bash
# 1. Get component code
figma-dev-mode:get_code \
  --nodeId="2:3" \
  --fileKey="abc123" \
  --clientFrameworks="react"

# 2. Get component screenshot for reference
figma-dev-mode:get_image \
  --nodeId="2:3" \
  --fileKey="abc123" \
  --scale=2

# 3. Get design tokens
figma-dev-mode:get_variable_defs \
  --nodeId="2:3" \
  --fileKey="abc123"
```

### Pattern 2: Visual Regression Test Setup

```bash
# Extract high-resolution reference image
figma-dev-mode:get_image \
  --nodeId="2:3" \
  --fileKey="abc123" \
  --format="png" \
  --scale=3

# Save for Playwright comparison
# tests/visual-regression/baseline/component-name.png
```

### Pattern 3: Design Token Extraction

```bash
# Get all design variables
figma-dev-mode:get_variable_defs \
  --fileKey="abc123"

# Export to design system
# → Convert to CSS custom properties
# → Generate Tailwind config
# → Create design token JSON
```

---

## Integration with AI Engineer Workflow

### In Requirements Phase

```bash
/gather-requirements
# Include Figma URL in requirements:
# "Implement login form from https://figma.com/design/abc?node-id=2-2"
```

### In EARS Formalization

```markdown
# REQ-001: Login Form UI

When a user views the login page, the system shall display a login form matching the Figma design at:
- File Key: abc123xyz
- Node ID: 2:2 (https://figma.com/design/abc123xyz?node-id=2-2)
```

### In Task Implementation

```bash
/task-work TASK-002

# System automatically:
# 1. Detects Figma reference
# 2. Converts node-id=2-2 to nodeId="2:2"
# 3. Extracts design data via MCP
# 4. Routes to appropriate tech stack specialist
# 5. Implements component with pixel-perfect fidelity
# 6. Creates visual regression tests
```

---

## Troubleshooting

### Issue: "Figma MCP server not found"

**Solution:**
```bash
# Reinstall the MCP server
npm install -g @figma/mcp-server

# Verify installation
which @figma/mcp-server

# Restart Claude Code
```

### Issue: "Authentication failed"

**Solution:**
1. Verify token is valid at [Figma Account Settings](https://www.figma.com/settings)
2. Check token has correct scopes (File content, Design system, Dev resources)
3. Ensure token is correctly set in config:
   ```bash
   echo $FIGMA_TOKEN  # Should output your token
   ```
4. Try regenerating the token if expired

### Issue: "Node not found"

**Solution:**
1. Verify node ID conversion:
   ```
   URL: node-id=2-2 → API: "2:2"
   ```
2. Check node exists in Figma file:
   - Open file in Figma
   - Select the node
   - Verify the ID in the URL matches
3. Ensure you have access to the file

### Issue: "Invalid file key"

**Solution:**
1. Extract file key from URL correctly:
   ```
   https://figma.com/design/[FILE_KEY]/Name?node-id=X-Y
                            ^^^^^^^^^^
   ```
2. Ensure file is accessible with your token:
   ```bash
   figma-dev-mode:get_metadata --fileKey="YOUR_FILE_KEY"
   ```

### Issue: "Rate limit exceeded"

**Solution:**
1. Figma API has rate limits (typically 100 requests/minute)
2. Add delay between requests in batch operations
3. Cache design data when possible
4. Consider upgrading Figma plan for higher limits

### Issue: "MCP connection timeout"

**Solution:**
```bash
# Check network connectivity
ping figma.com

# Verify MCP server is running
ps aux | grep figma

# Restart Claude Code and try again
```

---

## Best Practices

### 1. Design Token Management

**Extract once, reuse everywhere:**
```bash
# Extract design tokens at project start
figma-dev-mode:get_variable_defs --fileKey="abc123"

# Save to version control
# src/design-tokens/figma-tokens.json

# Generate code from tokens
# → tailwind.config.js
# → src/styles/variables.css
# → src/theme/index.ts
```

### 2. Caching Design Data

**Cache design extractions to avoid rate limits:**
```bash
# Create cache directory
mkdir -p .figma-cache

# Save extracted data
figma-dev-mode:get_code --nodeId="2:3" > .figma-cache/node-2-3.json

# Use cached data when available
# Only re-extract when design changes
```

### 3. Version Control

**Include Figma file version in commits:**
```bash
# Document design version in component
/**
 * LoginForm Component
 *
 * Figma: https://figma.com/design/abc123?node-id=2-2
 * Version: 2024-10-07 (v1.2.3)
 * Last synced: 2024-10-07
 */
```

### 4. Visual Regression Testing

**Always create visual tests for Figma implementations:**
```typescript
// tests/components/LoginForm.visual.spec.ts
test('matches Figma design', async ({ page }) => {
  await page.goto('/login');
  await expect(page.locator('[data-testid=login-form]'))
    .toHaveScreenshot('login-form.png', {
      threshold: 0.01 // 99% similarity required
    });
});
```

### 5. Design Drift Detection

**Set up automated checks for design changes:**
```bash
# Weekly cron job to check design versions
figma-dev-mode:get_metadata --fileKey="abc123" | \
  jq '.version' | \
  diff - .figma-cache/last-version.txt

# Alert if design has changed
# Trigger re-implementation if needed
```

---

## Security Considerations

### Token Storage

**Never commit tokens to version control:**

```gitignore
# .gitignore
.claude/config.json
.env
.figma-token
```

**Use environment variables:**
```bash
# .env (not committed)
FIGMA_TOKEN=your_token_here

# Load in config
export $(cat .env | xargs)
```

### Access Control

1. Use minimal token scopes (read-only)
2. Rotate tokens regularly (every 90 days)
3. Revoke unused tokens immediately
4. Use team-level tokens for shared projects

### Audit Logging

```bash
# Log all Figma API calls
figma-dev-mode:* 2>&1 | tee -a .figma-audit.log

# Review monthly for unauthorized access
```

---

## Advanced Configuration

### Custom MCP Server Settings

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_TOKEN}",
        "FIGMA_CACHE_DIR": ".figma-cache",
        "FIGMA_LOG_LEVEL": "info"
      },
      "timeout": 30000,
      "retries": 3
    }
  }
}
```

### Multiple Figma Accounts

```json
{
  "mcpServers": {
    "figma-personal": {
      "command": "npx",
      "args": ["@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_PERSONAL_TOKEN}"
      }
    },
    "figma-work": {
      "command": "npx",
      "args": ["@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_WORK_TOKEN}"
      }
    }
  }
}
```

---

## Testing Your Setup

### Quick Test Script

```bash
#!/bin/bash
# test-figma-mcp.sh

echo "Testing Figma MCP Setup..."

# 1. Check environment
echo "1. Checking environment..."
if [ -z "$FIGMA_TOKEN" ]; then
  echo "❌ FIGMA_TOKEN not set"
  exit 1
fi
echo "✅ FIGMA_TOKEN configured"

# 2. Test metadata endpoint
echo "2. Testing metadata API..."
figma-dev-mode:get_metadata --fileKey="YOUR_TEST_FILE_KEY"
if [ $? -eq 0 ]; then
  echo "✅ Metadata API working"
else
  echo "❌ Metadata API failed"
  exit 1
fi

# 3. Test code extraction
echo "3. Testing code extraction..."
figma-dev-mode:get_code \
  --nodeId="2:3" \
  --fileKey="YOUR_TEST_FILE_KEY" \
  --clientFrameworks="react"
if [ $? -eq 0 ]; then
  echo "✅ Code extraction working"
else
  echo "❌ Code extraction failed"
  exit 1
fi

echo ""
echo "🎉 All tests passed! Figma MCP is configured correctly."
```

---

## Next Steps

1. ✅ Install and configure Figma MCP server
2. ✅ Test with a sample Figma file
3. ✅ Set up Zeplin MCP (see [zeplin-mcp-setup.md](./zeplin-mcp-setup.md))
4. 📋 Review [ux-design-subagent-recommendations.md](../research/ux-design-subagent-recommendations.md)
5. 🚀 Start implementing UX design specialists

---

## Support & Resources

- **Figma Community**: [Figma Community Forum](https://forum.figma.com/)
- **MCP Documentation**: [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- **Claude Code**: [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- **Issue Tracking**: Report issues in your project repository

---

**Last Updated:** 2025-10-07
**Version:** 1.0.0
**Status:** ✅ Production Ready
