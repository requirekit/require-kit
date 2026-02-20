# Hierarchy Commands

Commands for visualizing and navigating requirement hierarchies.

## /hierarchy-view

View complete epic/feature/requirement hierarchy with pattern-aware tree rendering.

**Usage:**
```bash
/hierarchy-view EPIC-XXX
/hierarchy-view EPIC-XXX [--pattern <type>] [--graphiti-status]
```

**Examples:**
```bash
/hierarchy-view EPIC-001
/hierarchy-view EPIC-001 --pattern standard
/hierarchy-view EPIC-001 --pattern direct
/hierarchy-view EPIC-001 --graphiti-status
```

**Options:**

| Flag | Description |
|---|---|
| `--pattern <type>` | Filter hierarchy display by organisation pattern: `standard`, `direct`, or `mixed` |
| `--graphiti-status` | Show Graphiti sync status for each node in the hierarchy |

### Pattern-Aware Tree Rendering

The command automatically detects and renders each epic's organisation pattern. The pattern label is shown next to the epic name, and the tree structure adapts accordingly.

**Standard Pattern Output (Epic → Feature → Task):**
```
EPIC-001: E-Commerce Platform          [pattern: standard]
├── FEAT-001: Product Catalog
│   ├── REQ-001: Product search functionality
│   ├── REQ-002: Product filtering
│   └── BDD-001: Product browsing scenarios
├── FEAT-002: Shopping Cart
│   ├── REQ-003: Add items to cart
│   └── BDD-002: Shopping cart scenarios
└── FEAT-003: Checkout Process
    ├── REQ-004: Payment processing
    └── BDD-003: Checkout scenarios
```

**Direct Pattern Output (Epic → Task):**
```
EPIC-002: Configuration Refactor       [pattern: direct]
├── TASK-001: Extract config from hardcoded values
├── TASK-002: Add environment variable support
├── TASK-003: Add config validation on startup
├── REQ-001: The system shall load configuration from environment variables
└── BDD-001: Configuration loading scenarios
```

**Mixed Pattern Output (Epic → Feature + Task):**
```
EPIC-003: API Integration Layer        [pattern: mixed]
├── FEAT-001: REST Client
│   ├── TASK-001: HTTP client wrapper
│   ├── TASK-002: Retry logic
│   └── TASK-003: Response parsing
└── [Direct Tasks]
    ├── TASK-004: API key management
    └── TASK-005: Rate limiting setup
```

### Graphiti Health Display

When viewing workflow status, the command includes a Graphiti knowledge graph health indicator showing:

- Connection status (connected / standalone mode)
- Episodes synced per entity type
- Last sync timestamp
- Group ID (`{project}__requirements`)

Use `--graphiti-status` to annotate each node in the tree with its Graphiti sync state.

[See detailed documentation →](../guides/command_usage_guide.md#hierarchy-view)

For complete command documentation, see the [Command Usage Guide](../guides/command_usage_guide.md).

For a full explanation of organisation patterns, see [Epic/Feature Hierarchy](../core-concepts/hierarchy.md).
