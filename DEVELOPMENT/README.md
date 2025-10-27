# Development Documentation

This directory contains internal development documentation, change logs, and archived materials that are primarily for maintainers and contributors rather than end users.

## Structure

```
DEVELOPMENT/
├── archive/           # Old documentation and notes
├── changelog/         # Change logs and update notes
└── README.md         # This file
```

## Contents

### `/archive`
Contains historical documentation, old implementation notes, and superseded designs that we want to keep for reference but shouldn't be part of the main documentation.

### `/changelog`
Contains detailed change logs for significant updates and refactoring work, including:
- Implementation changes
- Architecture updates
- Breaking changes
- Migration guides for internal changes

## For End Users

If you're looking for user-facing documentation, please see:
- `/docs` - Main documentation directory
- `/docs/guides` - User guides and tutorials
- `/installer/README.md` - Installation instructions
- `/README.md` - Project overview

## For Contributors

When making significant changes:
1. Document the changes in a markdown file in `/changelog`
2. Use the format: `YYYY-MM-description.md`
3. Move old/superseded documentation to `/archive`
4. Keep user-facing docs in `/docs` clean and current
