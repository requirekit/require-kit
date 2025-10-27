# MCP Zeplin - Reference and Utilities

Reference guide for Zeplin MCP server tools, setup, and troubleshooting.

## Overview

The Zeplin MCP server provides 6 tools for extracting design data from Zeplin projects:
1. `zeplin:get_project` - Get project metadata
2. `zeplin:get_screen` - Get screen designs
3. `zeplin:get_component` - Get reusable components
4. `zeplin:get_styleguide` - Get design system tokens
5. `zeplin:get_colors` - Get color palette
6. `zeplin:get_text_styles` - Get typography specifications

## Installation

### Install Zeplin MCP Server
```bash
npm install -g @zeplin/mcp-server
```

### Configure Access Token

1. **Generate Token**:
   - Go to https://app.zeplin.io/profile/developer
   - Click "Generate new token"
   - Copy the token (starts with `zplnt_`)

2. **Add to Environment**:
   ```bash
   # In .env file
   ZEPLIN_ACCESS_TOKEN=zplnt_your_token_here
   ```

3. **Verify Setup**:
   ```bash
   /mcp-zeplin verify
   ```

## Commands

### /mcp-zeplin verify
Verify Zeplin MCP setup and connection.

```bash
/mcp-zeplin verify
```

**Output**:
```
✅ ZEPLIN MCP SETUP VERIFIED

MCP Server: @zeplin/mcp-server
Version: 1.0.0
Status: Connected

Available Tools:
✅ zeplin:get_project
✅ zeplin:get_screen
✅ zeplin:get_component
✅ zeplin:get_styleguide
✅ zeplin:get_colors
✅ zeplin:get_text_styles

Authentication: Valid
Token: zplnt_***************abc (masked)
```

### /mcp-zeplin test-connection
Test connection to Zeplin API.

```bash
/mcp-zeplin test-connection [--project-id PROJECT_ID]
```

**Output**:
```
✅ ZEPLIN CONNECTION TEST SUCCESSFUL

Test: Get project metadata
Project ID: abc123
Project Name: MyApp Mobile
Platform: iOS
Response Time: 234ms

Connection: Stable
Rate Limit: 100 requests/hour remaining
```

## MCP Tools Reference

### 1. zeplin:get_project

Extract project metadata including platform, name, and styleguide overview.

**Usage**:
```typescript
const projectResponse = await mcp__zeplin__get_project({
  projectId: "abc123"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID

**Response**:
```typescript
interface ProjectResponse {
  id: string;
  name: string;
  description: string;
  platform: "ios" | "android" | "web" | "macos";
  thumbnail: string;
  numberOfScreens: number;
  numberOfComponents: number;
  styleguide: {
    colors: number;
    textStyles: number;
    spacing: number;
  };
  updatedAt: string;
}
```

**Example Response**:
```json
{
  "id": "abc123",
  "name": "MyApp Mobile",
  "description": "Mobile app design system",
  "platform": "ios",
  "thumbnail": "https://...",
  "numberOfScreens": 24,
  "numberOfComponents": 18,
  "styleguide": {
    "colors": 12,
    "textStyles": 8,
    "spacing": 6
  },
  "updatedAt": "2025-10-09T12:00:00Z"
}
```

### 2. zeplin:get_screen

Extract screen design including layers, image, and metadata.

**Usage**:
```typescript
const screenResponse = await mcp__zeplin__get_screen({
  projectId: "abc123",
  screenId: "def456"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID
- `screenId` (required): Zeplin screen ID

**Response**:
```typescript
interface ScreenResponse {
  id: string;
  name: string;
  description: string;
  image: {
    url: string;
    width: number;
    height: number;
    format: "png" | "jpg";
  };
  layers: Array<{
    id: string;
    name: string;
    type: string;
    properties: object;
  }>;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}
```

**Example Response**:
```json
{
  "id": "def456",
  "name": "Login Screen",
  "description": "User authentication screen",
  "image": {
    "url": "https://...",
    "width": 375,
    "height": 812,
    "format": "png"
  },
  "layers": [
    {
      "id": "layer1",
      "name": "Email Input",
      "type": "input",
      "properties": { ... }
    }
  ],
  "tags": ["authentication", "login"],
  "createdAt": "2025-10-01T10:00:00Z",
  "updatedAt": "2025-10-09T12:00:00Z"
}
```

### 3. zeplin:get_component

Extract reusable component design.

**Usage**:
```typescript
const componentResponse = await mcp__zeplin__get_component({
  projectId: "abc123",
  componentId: "ghi789"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID
- `componentId` (required): Zeplin component ID

**Response**:
```typescript
interface ComponentResponse {
  id: string;
  name: string;
  description: string;
  image: {
    url: string;
    width: number;
    height: number;
  };
  properties: Record<string, any>;
  variants: Array<{
    name: string;
    properties: object;
  }>;
  usageCount: number;
}
```

**Example Response**:
```json
{
  "id": "ghi789",
  "name": "Primary Button",
  "description": "Main action button component",
  "image": {
    "url": "https://...",
    "width": 320,
    "height": 48
  },
  "properties": {
    "backgroundColor": "#3B82F6",
    "textColor": "#FFFFFF",
    "borderRadius": 8
  },
  "variants": [
    {
      "name": "Default",
      "properties": { ... }
    },
    {
      "name": "Disabled",
      "properties": { ... }
    }
  ],
  "usageCount": 15
}
```

### 4. zeplin:get_styleguide

Extract complete design system including colors, typography, and spacing.

**Usage**:
```typescript
const styleguideResponse = await mcp__zeplin__get_styleguide({
  projectId: "abc123"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID

**Response**:
```typescript
interface StyleguideResponse {
  colors: Array<{
    id: string;
    name: string;
    value: string;  // Hex color
    usage: string;
  }>;
  textStyles: Array<{
    id: string;
    name: string;
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
    lineHeight: number;
    letterSpacing: number;
    color: string;
  }>;
  spacing: Array<{
    id: string;
    name: string;
    value: number;  // Pixels
  }>;
}
```

**Example Response**:
```json
{
  "colors": [
    {
      "id": "color1",
      "name": "Primary",
      "value": "#3B82F6",
      "usage": "Primary actions and highlights"
    },
    {
      "id": "color2",
      "name": "Text Primary",
      "value": "#1F2937",
      "usage": "Primary text content"
    }
  ],
  "textStyles": [
    {
      "id": "text1",
      "name": "Heading 1",
      "fontFamily": "Inter",
      "fontSize": 32,
      "fontWeight": 700,
      "lineHeight": 40,
      "letterSpacing": -0.5,
      "color": "#1F2937"
    }
  ],
  "spacing": [
    {
      "id": "space1",
      "name": "Small",
      "value": 8
    },
    {
      "id": "space2",
      "name": "Medium",
      "value": 16
    }
  ]
}
```

### 5. zeplin:get_colors

Extract color palette from project styleguide.

**Usage**:
```typescript
const colorsResponse = await mcp__zeplin__get_colors({
  projectId: "abc123"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID

**Response**:
```typescript
interface ColorsResponse {
  colors: Array<{
    id: string;
    name: string;
    value: string;  // Hex format (#RRGGBB)
    rgba: {
      r: number;  // 0-255
      g: number;  // 0-255
      b: number;  // 0-255
      a: number;  // 0-1
    };
    usage: string;
  }>;
}
```

**Example Response**:
```json
{
  "colors": [
    {
      "id": "color1",
      "name": "Primary Blue",
      "value": "#3B82F6",
      "rgba": {
        "r": 59,
        "g": 130,
        "b": 246,
        "a": 1.0
      },
      "usage": "Primary actions, links"
    },
    {
      "id": "color2",
      "name": "Gray 50",
      "value": "#F9FAFB",
      "rgba": {
        "r": 249,
        "g": 250,
        "b": 251,
        "a": 1.0
      },
      "usage": "Background, surfaces"
    }
  ]
}
```

### 6. zeplin:get_text_styles

Extract typography specifications from project styleguide.

**Usage**:
```typescript
const textStylesResponse = await mcp__zeplin__get_text_styles({
  projectId: "abc123"
});
```

**Parameters**:
- `projectId` (required): Zeplin project ID

**Response**:
```typescript
interface TextStylesResponse {
  textStyles: Array<{
    id: string;
    name: string;
    fontFamily: string;
    fontSize: number;      // Pixels
    fontWeight: number;    // 100-900
    fontStyle: "normal" | "italic";
    lineHeight: number;    // Pixels
    letterSpacing: number; // Pixels
    textAlign: "left" | "center" | "right" | "justify";
    color: string;         // Hex format
  }>;
}
```

**Example Response**:
```json
{
  "textStyles": [
    {
      "id": "text1",
      "name": "Heading 1",
      "fontFamily": "Inter",
      "fontSize": 32,
      "fontWeight": 700,
      "fontStyle": "normal",
      "lineHeight": 40,
      "letterSpacing": -0.5,
      "textAlign": "left",
      "color": "#1F2937"
    },
    {
      "id": "text2",
      "name": "Body Regular",
      "fontFamily": "Inter",
      "fontSize": 16,
      "fontWeight": 400,
      "fontStyle": "normal",
      "lineHeight": 24,
      "letterSpacing": 0,
      "textAlign": "left",
      "color": "#374151"
    }
  ]
}
```

## URL to ID Extraction

### Extract IDs from Zeplin URLs

**URL Formats**:
```
Project: https://app.zeplin.io/project/abc123
Screen: https://app.zeplin.io/project/abc123/screen/def456
Component: https://app.zeplin.io/project/abc123/component/ghi789
```

**Extraction Function**:
```typescript
function extractZeplinIds(url: string): {
  projectId: string | null;
  screenId: string | null;
  componentId: string | null;
} {
  const projectMatch = url.match(/project\/([a-zA-Z0-9]+)/);
  const screenMatch = url.match(/screen\/([a-zA-Z0-9]+)/);
  const componentMatch = url.match(/component\/([a-zA-Z0-9]+)/);

  return {
    projectId: projectMatch ? projectMatch[1] : null,
    screenId: screenMatch ? screenMatch[1] : null,
    componentId: componentMatch ? componentMatch[1] : null
  };
}
```

**Examples**:
```typescript
extractZeplinIds("https://app.zeplin.io/project/abc123")
// => { projectId: "abc123", screenId: null, componentId: null }

extractZeplinIds("https://app.zeplin.io/project/abc123/screen/def456")
// => { projectId: "abc123", screenId: "def456", componentId: null }

extractZeplinIds("https://app.zeplin.io/project/abc123/component/ghi789")
// => { projectId: "abc123", screenId: null, componentId: "ghi789" }
```

## Icon Format Handling

### Icon Code Formats from Zeplin

Zeplin MCP typically returns icon codes in HTML entity format:

**Common Format**:
```
&#xe5d2; (lowercase hex digits)
```

**Expected Icon Properties** in MCP responses:
```json
{
  "id": "icon-element-123",
  "type": "icon",
  "properties": {
    "icon": "&#xe5d2;",
    "fontFamily": "MaterialIcons",
    "size": 24,
    "color": "#FFFFFF"
  }
}
```

### Icon Conversion

The `/zeplin-to-maui` workflow automatically converts icon codes to XAML format:

**Input** (from Zeplin MCP):
```
&#xe5d2;
```

**Output** (for XAML):
```xml
<FontImageSource Glyph="&#xE5D2;" />
```

**Key Conversion**: Lowercase hex → Uppercase hex (XAML requirement)

### Icon Font Families

**Material Design Icons** (most common):
- Unicode range: U+E000 to U+F8FF
- Font family: "MaterialIcons"
- Download: [Material Design Icons](https://fonts.google.com/icons)

**Font Awesome** (alternative):
- Unicode range: U+F000 to U+F8FF
- Font family: "FontAwesome"
- Requires different conversion logic

### Troubleshooting Icon Issues

If icons don't render correctly after generation:

1. **Verify icon code format in Zeplin**:
   ```bash
   # Check MCP response
   /mcp-zeplin test-connection --project-id abc123
   ```

2. **Check icon conversion log**:
   ```
   Icon Conversion Summary:
     ✅ Successful: 7
     ❌ Failed: 0
   ```

3. **Validate Material Design Icons font setup**:
   - Font file: `Resources/Fonts/MaterialIcons-Regular.ttf`
   - MauiProgram.cs: `fonts.AddFont("MaterialIcons-Regular.ttf", "MaterialIcons")`
   - App.xaml: `<FontFamily x:Key="IconsFontFamily">MaterialIcons</FontFamily>`

**Common Issues**:
- Icons as Chinese characters → Incorrect hex case (fixed by converter)
- Icons not visible → Missing font file
- Wrong icon displayed → Incorrect icon code in Zeplin

**Solutions**: See [Icon Troubleshooting Guide](../../docs/troubleshooting/zeplin-maui-icon-issues.md)

## Troubleshooting

### Authentication Errors

**Problem**: `401 Unauthorized` or `Invalid access token`

**Solution**:
```bash
1. Generate new token: https://app.zeplin.io/profile/developer
2. Verify token format: zplnt_[32-character-string]
3. Update .env: ZEPLIN_ACCESS_TOKEN=zplnt_your_token
4. Restart application to reload environment
```

### Rate Limiting

**Problem**: `429 Too Many Requests`

**Solution**:
```bash
# Zeplin rate limits:
- 100 requests per hour per token (default)
- 1000 requests per hour (pro accounts)

# Wait for rate limit reset or:
1. Use caching to reduce duplicate requests
2. Implement exponential backoff retry logic
3. Upgrade to pro account for higher limits
```

### Invalid Project/Screen/Component ID

**Problem**: `404 Not Found` or `Invalid ID`

**Solution**:
```bash
1. Verify ID format:
   - Project: alphanumeric string
   - Screen: alphanumeric string
   - Component: alphanumeric string

2. Check URL in Zeplin:
   - Open design in Zeplin
   - Copy URL from browser
   - Extract IDs using pattern matching

3. Verify permissions:
   - Token must have read access to project
   - Project must be shared with token owner
```

### Network Errors

**Problem**: `ECONNREFUSED`, `ETIMEDOUT`, or `Network error`

**Solution**:
```bash
1. Check internet connection
2. Verify MCP server is running
3. Check firewall settings
4. Try with verbose logging:
   /mcp-zeplin verify --verbose
```

### MCP Server Not Found

**Problem**: `MCP server not available` or `Command not found`

**Solution**:
```bash
# Install Zeplin MCP server
npm install -g @zeplin/mcp-server

# Verify installation
npm list -g @zeplin/mcp-server

# If still not found, check PATH
echo $PATH

# Reinstall if needed
npm uninstall -g @zeplin/mcp-server
npm install -g @zeplin/mcp-server
```

## Quick Reference Cheat Sheet

### Common Operations

```bash
# Verify setup
/mcp-zeplin verify

# Test connection
/mcp-zeplin test-connection --project-id abc123

# Extract design
/zeplin-to-maui https://app.zeplin.io/project/abc123/screen/def456

# Force refresh
/zeplin-to-maui <url> --force-refresh
```

### Environment Variables

```bash
# Required
ZEPLIN_ACCESS_TOKEN=zplnt_your_token_here

# Optional
ZEPLIN_PROJECT_ID=abc123  # Default project
ZEPLIN_CACHE_TTL=3600     # Cache time-to-live (seconds)
```

### Token Scopes

Required scopes for Zeplin Personal Access Token:
- ✅ `read` - Read project data (required)
- ❌ `write` - Write project data (not needed)
- ❌ `delete` - Delete project data (not needed)

### Rate Limits

| Account Type | Requests/Hour | Burst Limit |
|--------------|---------------|-------------|
| Free | 100 | 10 |
| Pro | 1000 | 50 |
| Enterprise | Custom | Custom |

### Response Times

| Operation | Expected Time | Timeout |
|-----------|---------------|---------|
| get_project | <500ms | 5s |
| get_screen | <1s | 10s |
| get_component | <1s | 10s |
| get_styleguide | <2s | 15s |
| get_colors | <500ms | 5s |
| get_text_styles | <500ms | 5s |

## Best Practices

### 1. Caching
Cache MCP responses to reduce API calls:
- Cache duration: 1 hour (3600 seconds)
- Cache key: `zeplin:{projectId}:{screenId}:{timestamp}`
- Invalidate on `--force-refresh`

### 2. Error Handling
Implement retry logic with exponential backoff:
- Max attempts: 3
- Initial delay: 1 second
- Backoff multiplier: 2x (1s, 2s, 4s)

### 3. Logging
Enable verbose logging for debugging:
```bash
/zeplin-to-maui <url> --verbose
```

### 4. Token Security
- Never commit tokens to version control
- Use environment variables (.env file)
- Rotate tokens regularly (every 90 days)
- Use minimal required scopes

### 5. Performance
- Parallel API calls where possible
- Use project-level styleguide for multiple screens
- Cache color and text style definitions
- Implement request deduplication

## Related Commands

- `/zeplin-to-maui` - Generate MAUI components from Zeplin
- `/task-work TASK-XXX` - Integrate with task workflow

## External Documentation

- [Zeplin MCP Server](https://mcp.so/server/mcp-server/zeplin)
- [Zeplin MCP Setup Guide](https://support.zeplin.io/en/articles/11559086-zeplin-mcp-server)
- [Zeplin API Documentation](https://docs.zeplin.dev/reference)

---

**Last Updated**: 2025-10-09
**Version**: 1.0.0
