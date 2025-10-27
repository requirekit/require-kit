# Zeplin MCP Server Setup Guide

## Overview

The Zeplin MCP (Model Context Protocol) server enables Claude Code to extract design specifications, style guides, and component libraries from Zeplin projects. This integration complements the Figma MCP server and provides an alternative design system integration for the UX design specialist sub-agents.

**Official Resources:**
- [Zeplin MCP Server](https://mcp.so/server/mcp-server/zeplin)
- [Zeplin MCP Setup Guide](https://support.zeplin.io/en/articles/11559086-zeplin-mcp-server)

---

## Prerequisites

- Claude Code installed and configured
- Zeplin account with access to projects
- Node.js 18+ installed (for MCP server)
- npm or yarn package manager
- Zeplin Personal Access Token (see setup below)

---

## Installation Steps

### 1. Install Zeplin MCP Server

Install the Zeplin MCP server via npm:

```bash
# Global installation (recommended)
npm install -g @zeplin/mcp-server

# Or install locally in your project
npm install --save-dev @zeplin/mcp-server
```

**Alternative Installation via MCP Registry:**
```bash
# Claude Code can auto-install from MCP registry
# Will be prompted when first accessing Zeplin tools
```

### 2. Get Zeplin Personal Access Token

1. Log in to [Zeplin](https://app.zeplin.io/)
2. Go to **Settings** → **Developer** (or visit [app.zeplin.io/profile/developer](https://app.zeplin.io/profile/developer))
3. Click **Personal Access Tokens**
4. Click **Create new token**
5. Configure token settings:
   - **Name**: "Claude Code MCP Integration"
   - **Scopes** (select appropriate access):
     - ✅ Read projects
     - ✅ Read styleguides
     - ✅ Read components
     - ✅ Read screens
     - ✅ Read colors
     - ✅ Read text styles
     - ✅ Read spacing tokens
   - **Expiration**: Set according to security policy (90 days recommended)
6. Click **Create token**
7. **Copy the token immediately** (it won't be shown again)

### 3. Configure MCP Server in Claude Code

Add the Zeplin MCP configuration to your Claude Code settings:

**Location:** `~/.claude/config.json` or project-specific `.claude/config.json`

```json
{
  "mcpServers": {
    "zeplin": {
      "command": "npx",
      "args": [
        "@zeplin/mcp-server"
      ],
      "env": {
        "ZEPLIN_ACCESS_TOKEN": "YOUR_ZEPLIN_TOKEN_HERE"
      }
    }
  }
}
```

**Security Note:** For production use, store the token in an environment variable:

```json
{
  "mcpServers": {
    "zeplin": {
      "command": "npx",
      "args": [
        "@zeplin/mcp-server"
      ],
      "env": {
        "ZEPLIN_ACCESS_TOKEN": "${ZEPLIN_TOKEN}"
      }
    }
  }
}
```

Set the environment variable:
```bash
# Add to ~/.bashrc or ~/.zshrc
export ZEPLIN_TOKEN="your_zeplin_token_here"
```

### 4. Configure Both Figma and Zeplin (Recommended)

For projects using both design systems:

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_TOKEN}"
      }
    },
    "zeplin": {
      "command": "npx",
      "args": ["@zeplin/mcp-server"],
      "env": {
        "ZEPLIN_ACCESS_TOKEN": "${ZEPLIN_TOKEN}"
      }
    }
  }
}
```

### 5. Verify Installation

Test the MCP connection in Claude Code:

```bash
# List available MCP tools
@mcp list

# You should see Zeplin tools like:
# - zeplin:get_project
# - zeplin:get_screen
# - zeplin:get_component
# - zeplin:get_styleguide
# - zeplin:get_colors
# - zeplin:get_text_styles
```

Or test manually:

```bash
# List your Zeplin projects
@zeplin:list_projects
```

---

## Available MCP Tools

### 1. `zeplin:list_projects`

List all Zeplin projects you have access to.

**Usage:**
```bash
zeplin:list_projects
```

**Returns:**
- Project IDs
- Project names
- Project descriptions
- Team information
- Platform (iOS, Android, Web, macOS)

### 2. `zeplin:get_project`

Get detailed information about a specific project.

**Usage:**
```bash
zeplin:get_project --projectId="PROJECT_ID"
```

**Parameters:**
- `projectId` (required): Zeplin project ID

**Returns:**
- Project metadata
- Number of screens
- Number of components
- Styleguide reference
- Team members
- Platform configuration

### 3. `zeplin:get_screen`

Get screen details including layout, components, and specifications.

**Usage:**
```bash
zeplin:get_screen \
  --projectId="PROJECT_ID" \
  --screenId="SCREEN_ID"
```

**Parameters:**
- `projectId` (required): Zeplin project ID
- `screenId` (required): Screen ID

**Returns:**
- Screen name and description
- Dimensions
- Component list
- Layer structure
- Annotations and notes
- Image URL (high-resolution)
- Design specifications

### 4. `zeplin:get_component`

Get component specifications and variants.

**Usage:**
```bash
zeplin:get_component \
  --projectId="PROJECT_ID" \
  --componentId="COMPONENT_ID"
```

**Parameters:**
- `projectId` (required): Zeplin project ID
- `componentId` (required): Component ID

**Returns:**
- Component name
- Description
- Variants
- Properties
- Dimensions
- Design specifications
- Code snippets (if configured)

### 5. `zeplin:get_styleguide`

Get the complete styleguide including colors, text styles, and spacing.

**Usage:**
```bash
zeplin:get_styleguide --projectId="PROJECT_ID"
```

**Returns:**
- All color tokens
- Text style definitions
- Spacing tokens
- Component library
- Design system variables

### 6. `zeplin:get_colors`

Get color palette from styleguide.

**Usage:**
```bash
zeplin:get_colors --projectId="PROJECT_ID"
```

**Returns:**
```json
{
  "colors": [
    {
      "name": "Primary Blue",
      "hex": "#007AFF",
      "rgb": "0, 122, 255",
      "hsl": "211, 100%, 50%"
    },
    {
      "name": "Text Primary",
      "hex": "#1C1C1E",
      "rgb": "28, 28, 30",
      "hsl": "240, 3%, 11%"
    }
  ]
}
```

### 7. `zeplin:get_text_styles`

Get typography specifications from styleguide.

**Usage:**
```bash
zeplin:get_text_styles --projectId="PROJECT_ID"
```

**Returns:**
```json
{
  "textStyles": [
    {
      "name": "Heading 1",
      "fontFamily": "Inter",
      "fontSize": 32,
      "fontWeight": 700,
      "lineHeight": 40,
      "letterSpacing": -0.5,
      "color": "#1C1C1E"
    },
    {
      "name": "Body",
      "fontFamily": "Inter",
      "fontSize": 16,
      "fontWeight": 400,
      "lineHeight": 24,
      "letterSpacing": 0,
      "color": "#3C3C43"
    }
  ]
}
```

### 8. `zeplin:get_spacing`

Get spacing tokens from styleguide.

**Usage:**
```bash
zeplin:get_spacing --projectId="PROJECT_ID"
```

**Returns:**
```json
{
  "spacing": [
    { "name": "xs", "value": "4px" },
    { "name": "sm", "value": "8px" },
    { "name": "md", "value": "16px" },
    { "name": "lg", "value": "24px" },
    { "name": "xl", "value": "32px" }
  ]
}
```

---

## Zeplin URL Structure

### Project URLs
```
https://app.zeplin.io/project/{PROJECT_ID}
```

### Screen URLs
```
https://app.zeplin.io/project/{PROJECT_ID}/screen/{SCREEN_ID}
```

### Component URLs
```
https://app.zeplin.io/project/{PROJECT_ID}/component/{COMPONENT_ID}
```

### Extracting IDs from URLs

**JavaScript:**
```javascript
function extractZeplinIds(url) {
  const projectMatch = url.match(/project\/([a-zA-Z0-9]+)/);
  const screenMatch = url.match(/screen\/([a-zA-Z0-9]+)/);
  const componentMatch = url.match(/component\/([a-zA-Z0-9]+)/);

  return {
    projectId: projectMatch ? projectMatch[1] : null,
    screenId: screenMatch ? screenMatch[1] : null,
    componentId: componentMatch ? componentMatch[1] : null
  };
}

// Usage
const url = "https://app.zeplin.io/project/abc123/screen/def456";
const ids = extractZeplinIds(url);
// { projectId: "abc123", screenId: "def456", componentId: null }
```

**Python:**
```python
import re
from typing import Optional, Dict

def extract_zeplin_ids(url: str) -> Dict[str, Optional[str]]:
    """Extract project, screen, and component IDs from Zeplin URL."""
    project_match = re.search(r'project/([a-zA-Z0-9]+)', url)
    screen_match = re.search(r'screen/([a-zA-Z0-9]+)', url)
    component_match = re.search(r'component/([a-zA-Z0-9]+)', url)

    return {
        'project_id': project_match.group(1) if project_match else None,
        'screen_id': screen_match.group(1) if screen_match else None,
        'component_id': component_match.group(1) if component_match else None
    }

# Usage
url = "https://app.zeplin.io/project/abc123/screen/def456"
ids = extract_zeplin_ids(url)
# {'project_id': 'abc123', 'screen_id': 'def456', 'component_id': None}
```

---

## Common Usage Patterns

### Pattern 1: Extract Complete Screen Design

```bash
# 1. Get project info
zeplin:get_project --projectId="abc123"

# 2. Get screen details
zeplin:get_screen \
  --projectId="abc123" \
  --screenId="def456"

# 3. Get styleguide for design tokens
zeplin:get_styleguide --projectId="abc123"

# 4. Get all colors
zeplin:get_colors --projectId="abc123"

# 5. Get all text styles
zeplin:get_text_styles --projectId="abc123"
```

### Pattern 2: Component Library Extraction

```bash
# 1. List all components in project
zeplin:get_project --projectId="abc123"

# 2. Get specific component details
zeplin:get_component \
  --projectId="abc123" \
  --componentId="comp789"

# 3. Get component variants
zeplin:get_component \
  --projectId="abc123" \
  --componentId="comp789" \
  --includeVariants=true
```

### Pattern 3: Design System Export

```bash
# Export complete design system
# 1. Colors
zeplin:get_colors --projectId="abc123" > design-tokens/colors.json

# 2. Typography
zeplin:get_text_styles --projectId="abc123" > design-tokens/typography.json

# 3. Spacing
zeplin:get_spacing --projectId="abc123" > design-tokens/spacing.json

# 4. Complete styleguide
zeplin:get_styleguide --projectId="abc123" > design-tokens/styleguide.json
```

---

## Integration with AI Engineer Workflow

### In Requirements Phase

```bash
/gather-requirements
# Include Zeplin URL in requirements:
# "Implement dashboard screen from https://app.zeplin.io/project/abc123/screen/def456"
```

### In EARS Formalization

```markdown
# REQ-002: Dashboard Screen UI

When a user views the dashboard, the system shall display the layout matching the Zeplin screen at:
- Project ID: abc123
- Screen ID: def456
- URL: https://app.zeplin.io/project/abc123/screen/def456
```

### In Task Implementation

```bash
/task-work TASK-003

# System automatically:
# 1. Detects Zeplin reference
# 2. Extracts project and screen IDs
# 3. Fetches design data via MCP
# 4. Routes to design-system-orchestrator
# 5. Coordinates with appropriate tech stack specialist
# 6. Implements screen with pixel-perfect fidelity
# 7. Creates visual regression tests
```

---

## Design System Orchestrator Integration

The `design-system-orchestrator` agent detects and routes between Figma and Zeplin:

```markdown
## Detection Logic (from design-system-orchestrator.md)

1. Check for Figma URL patterns:
   - figma.com/design/*
   - figma.com/file/*

2. Check for Zeplin URL patterns:
   - app.zeplin.io/project/*
   - zeplin.io/project/*

3. Check project configuration:
   - .claude/settings.json → designSystem.primary
   - Project has FIGMA_TOKEN or ZEPLIN_TOKEN set

4. Route to appropriate specialist:
   - Figma detected → figma-design-specialist
   - Zeplin detected → zeplin-design-specialist
   - Both available → Ask user preference
```

---

## Troubleshooting

### Issue: "Zeplin MCP server not found"

**Solution:**
```bash
# Reinstall the MCP server
npm install -g @zeplin/mcp-server

# Verify installation
which @zeplin/mcp-server
npx @zeplin/mcp-server --version

# Restart Claude Code
```

### Issue: "Authentication failed"

**Solution:**
1. Verify token is valid at [Zeplin Developer Settings](https://app.zeplin.io/profile/developer)
2. Check token scopes include necessary permissions
3. Ensure token hasn't expired
4. Test token manually:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.zeplin.dev/v1/projects
   ```
5. Regenerate token if needed

### Issue: "Project not found"

**Solution:**
1. Verify you have access to the project in Zeplin web app
2. Check project ID is correct:
   ```bash
   zeplin:list_projects  # Get list of accessible projects
   ```
3. Ensure token has "Read projects" scope
4. Verify team membership if project is team-owned

### Issue: "Screen/Component not found"

**Solution:**
1. Get valid screen/component IDs:
   ```bash
   zeplin:get_project --projectId="abc123"
   # Lists all screens and components
   ```
2. Verify ID extraction from URL is correct
3. Check if screen/component was archived or deleted

### Issue: "Rate limit exceeded"

**Solution:**
1. Zeplin API rate limits:
   - Free: 100 requests/hour
   - Paid: 1000 requests/hour
2. Implement request caching
3. Add delays between batch operations
4. Upgrade Zeplin plan if needed

---

## N8N Integration (Optional)

Zeplin can also be integrated via N8N for more complex workflows:

### Setup N8N for Zeplin

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["@n8n/mcp-server"],
      "env": {
        "N8N_API_KEY": "${N8N_API_KEY}",
        "N8N_INSTANCE_URL": "${N8N_INSTANCE_URL}"
      }
    }
  }
}
```

### N8N Workflow Example

Create an N8N workflow for advanced Zeplin operations:
1. Trigger on Zeplin webhook (design updates)
2. Fetch updated design data
3. Generate code from design
4. Create pull request with changes
5. Notify team via Slack

---

## Best Practices

### 1. Design Token Management

**Extract and version control design tokens:**
```bash
# Extract tokens at project initialization
zeplin:get_styleguide --projectId="abc123" > src/design-tokens/zeplin.json

# Generate code from tokens
npm run generate-tokens

# Outputs:
# → src/styles/colors.css
# → src/styles/typography.css
# → src/theme/tokens.ts
# → tailwind.config.js (extended)
```

### 2. Component Library Sync

**Keep component library in sync:**
```bash
#!/bin/bash
# scripts/sync-zeplin-components.sh

PROJECT_ID="abc123"

# Get all components
zeplin:get_project --projectId="$PROJECT_ID" | \
  jq -r '.components[].id' | \
  while read -r component_id; do
    echo "Syncing component: $component_id"
    zeplin:get_component \
      --projectId="$PROJECT_ID" \
      --componentId="$component_id" \
      > "components/zeplin-specs/${component_id}.json"
  done
```

### 3. Design Version Control

**Track design versions:**
```markdown
/**
 * DashboardScreen Component
 *
 * Zeplin: https://app.zeplin.io/project/abc123/screen/def456
 * Last synced: 2024-10-07
 * Version: 1.3.0
 * Changes: Updated color tokens, new spacing
 */
```

### 4. Automated Design Sync

**Set up automated sync checks:**
```yaml
# .github/workflows/design-sync.yml
name: Check Design Sync

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am

jobs:
  check-design:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Zeplin for updates
        run: |
          npm run check-design-updates
          # Compares current design specs with Zeplin
          # Creates issue if designs have changed
```

### 5. Multi-Platform Support

**Extract platform-specific designs:**
```bash
# iOS-specific
zeplin:get_project --projectId="ios-project-id"

# Android-specific
zeplin:get_project --projectId="android-project-id"

# Web-specific
zeplin:get_project --projectId="web-project-id"

# Combine into unified design system
npm run merge-platform-tokens
```

---

## Security Considerations

### Token Storage

**Never commit tokens to version control:**

```gitignore
# .gitignore
.claude/config.json
.env
.zeplin-token
zeplin-credentials.json
```

**Use environment variables:**
```bash
# .env (not committed)
ZEPLIN_TOKEN=your_token_here
FIGMA_TOKEN=your_figma_token_here

# Load in shell
export $(cat .env | xargs)
```

### Token Scopes

**Use minimal required scopes:**
- ✅ Read projects (required)
- ✅ Read styleguides (required)
- ✅ Read components (required)
- ✅ Read screens (required)
- ❌ Write access (not needed for design extraction)
- ❌ Admin access (not needed)

### Token Rotation

```bash
# Rotate tokens quarterly
# 1. Generate new token in Zeplin
# 2. Update environment variables
# 3. Test with new token
# 4. Revoke old token
# 5. Update team documentation
```

---

## Advanced Configuration

### Custom MCP Server Settings

```json
{
  "mcpServers": {
    "zeplin": {
      "command": "npx",
      "args": ["@zeplin/mcp-server"],
      "env": {
        "ZEPLIN_ACCESS_TOKEN": "${ZEPLIN_TOKEN}",
        "ZEPLIN_CACHE_DIR": ".zeplin-cache",
        "ZEPLIN_LOG_LEVEL": "info",
        "ZEPLIN_REQUEST_TIMEOUT": "30000"
      },
      "timeout": 30000,
      "retries": 3,
      "rateLimit": {
        "requests": 100,
        "period": 3600
      }
    }
  }
}
```

### Caching Configuration

```bash
# Enable aggressive caching for design data
export ZEPLIN_CACHE_DIR=".zeplin-cache"
export ZEPLIN_CACHE_TTL="86400"  # 24 hours

# Cache structure
.zeplin-cache/
├── projects/
│   └── abc123.json
├── screens/
│   └── def456.json
├── components/
│   └── comp789.json
└── styleguides/
    └── abc123.json
```

---

## Testing Your Setup

### Quick Test Script

```bash
#!/bin/bash
# test-zeplin-mcp.sh

echo "Testing Zeplin MCP Setup..."

# 1. Check environment
echo "1. Checking environment..."
if [ -z "$ZEPLIN_TOKEN" ]; then
  echo "❌ ZEPLIN_TOKEN not set"
  exit 1
fi
echo "✅ ZEPLIN_TOKEN configured"

# 2. Test list projects
echo "2. Testing list projects..."
zeplin:list_projects
if [ $? -eq 0 ]; then
  echo "✅ List projects working"
else
  echo "❌ List projects failed"
  exit 1
fi

# 3. Test get project (use your project ID)
echo "3. Testing get project..."
PROJECT_ID="YOUR_PROJECT_ID"
zeplin:get_project --projectId="$PROJECT_ID"
if [ $? -eq 0 ]; then
  echo "✅ Get project working"
else
  echo "❌ Get project failed"
  exit 1
fi

# 4. Test get styleguide
echo "4. Testing get styleguide..."
zeplin:get_styleguide --projectId="$PROJECT_ID"
if [ $? -eq 0 ]; then
  echo "✅ Get styleguide working"
else
  echo "❌ Get styleguide failed"
  exit 1
fi

echo ""
echo "🎉 All tests passed! Zeplin MCP is configured correctly."
```

---

## Comparison: Figma vs Zeplin

| Feature | Figma MCP | Zeplin MCP |
|---------|-----------|------------|
| **Design Extraction** | Node-based | Screen/Component-based |
| **Design Tokens** | Variables API | Styleguide API |
| **Code Generation** | Dev Mode snippets | Code snippets (if configured) |
| **Platform Support** | All platforms | iOS, Android, Web, macOS |
| **Component Library** | Components + Variants | Components + Variants |
| **Collaboration** | Real-time | Developer handoff focus |
| **Best For** | Design → Code in single tool | Separate design and handoff |

---

## Next Steps

1. ✅ Install and configure Zeplin MCP server
2. ✅ Test with a sample Zeplin project
3. ✅ Extract design tokens to version control
4. 📋 Review [ux-design-subagent-recommendations.md](../research/ux-design-subagent-recommendations.md)
5. 🔧 Configure design-system-orchestrator
6. 🚀 Start implementing UX design specialists

---

## Support & Resources

- **Zeplin Support**: [support.zeplin.io](https://support.zeplin.io/)
- **Zeplin API Docs**: [docs.zeplin.dev](https://docs.zeplin.dev/)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **Claude Code**: [docs.anthropic.com/claude](https://docs.anthropic.com/claude/docs)
- **Community**: [Zeplin Community Forum](https://community.zeplin.io/)

---

**Last Updated:** 2025-10-07
**Version:** 1.0.0
**Status:** ✅ Production Ready
