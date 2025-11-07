---
id: TASK-DOCS-004
title: Set up GitHub Actions workflow for MkDocs deployment to GitHub Pages
status: completed
created: 2025-11-06T00:00:00Z
updated: 2025-11-06T12:00:00Z
priority: high
tags: [documentation, github-actions, github-pages, ci-cd]
epic: null
feature: null
requirements: []
dependencies: ["TASK-DOCS-002", "TASK-DOCS-003"]
complexity_evaluation:
  score: 5
  level: "medium"
  review_mode: "QUICK_OPTIONAL"
  factor_scores:
    - factor: "file_complexity"
      score: 2
      max_score: 3
      justification: "Single workflow file + some testing"
    - factor: "pattern_familiarity"
      score: 1
      max_score: 2
      justification: "GitHub Actions is well-documented"
    - factor: "risk_level"
      score: 1
      max_score: 3
      justification: "Medium risk - deployment automation"
    - factor: "dependencies"
      score: 1
      max_score: 2
      justification: "Depends on mkdocs.yml being correct"
---

# Task: Set up GitHub Actions Workflow for MkDocs Deployment to GitHub Pages

## Context

After TASK-DOCS-002 (MkDocs config) and TASK-DOCS-003 (landing pages), we have:
- Working mkdocs.yml configuration
- Complete documentation site that builds locally
- All landing pages and navigation in place

Now we need to automate deployment to GitHub Pages using GitHub Actions.

**Approach**: Use modern GitHub Pages deployment (actions/deploy-pages@v4) for automated deployment to RequireKit documentation site.

## Objective

Create a GitHub Actions workflow that automatically builds and deploys the MkDocs site to GitHub Pages whenever documentation changes are pushed to the main branch.

## Requirements

### Workflow File Creation
- [ ] Create `.github/workflows/docs.yml`
- [ ] Use modern GitHub Pages deployment action
- [ ] Configure proper permissions
- [ ] Set up Python environment
- [ ] Install MkDocs Material

### Trigger Configuration
- [ ] Trigger on push to main branch
- [ ] Only when docs/, mkdocs.yml, or workflow file changes
- [ ] Support manual workflow dispatch (for testing)
- [ ] Don't trigger on pull requests (optional: add preview later)

### Build Steps
- [ ] Checkout repository
- [ ] Set up Python 3.12 (or latest stable)
- [ ] Install MkDocs Material via pip
- [ ] Run `mkdocs build --strict` (fail on warnings)
- [ ] Upload build artifact

### Deployment Steps
- [ ] Configure GitHub Pages
- [ ] Upload pages artifact
- [ ] Deploy to GitHub Pages
- [ ] Use proper permissions (pages: write, id-token: write)

### Error Handling
- [ ] Fail workflow on build errors
- [ ] Fail workflow on warnings (--strict flag)
- [ ] Provide clear error messages
- [ ] Don't deploy if build fails

### Optimization
- [ ] Cache pip dependencies for faster builds
- [ ] Only trigger when relevant files change
- [ ] Skip deploy on fork PRs (security)

## Acceptance Criteria

### Workflow File ✅
- [ ] `.github/workflows/docs.yml` created
- [ ] Valid YAML syntax
- [ ] Uses modern GitHub Pages actions (not gh-pages branch)
- [ ] Well-commented for maintainability

### Permissions ✅
- [ ] `contents: read` for checkout
- [ ] `pages: write` for deployment
- [ ] `id-token: write` for authentication
- [ ] No unnecessary permissions

### Trigger Configuration ✅
- [ ] Triggers on push to main branch
- [ ] Only when docs/ changes
- [ ] Only when mkdocs.yml changes
- [ ] Only when workflow file changes
- [ ] Supports workflow_dispatch for manual runs

### Build Process ✅
- [ ] Python 3.12 (or latest) set up
- [ ] MkDocs Material installed
- [ ] `mkdocs build --strict` runs
- [ ] Build artifacts uploaded
- [ ] Pip cache configured (faster builds)

### Deployment Process ✅
- [ ] GitHub Pages configured
- [ ] Artifact uploaded to Pages
- [ ] Deployment succeeds
- [ ] Site accessible at GitHub Pages URL

### Testing ✅
- [ ] Workflow runs successfully on push
- [ ] Site deploys to GitHub Pages
- [ ] No broken links in deployed site
- [ ] Search works on deployed site
- [ ] Navigation works on deployed site

## Implementation Plan

### Phase 1: Workflow File Structure
1. Create `.github/workflows/` directory
2. Create `docs.yml` workflow file
3. Add name and trigger configuration
4. Add permissions block

### Phase 2: Build Job Configuration
1. Define job to run on ubuntu-latest
2. Add checkout step
3. Add Python setup step
4. Add MkDocs Material installation
5. Add build step with --strict flag

### Phase 3: Deployment Job Configuration
1. Add Pages setup step
2. Add artifact upload step
3. Add deployment step
4. Configure dependencies between jobs

### Phase 4: Optimization
1. Add pip cache for faster builds
2. Configure path filters for triggers
3. Add workflow_dispatch for manual runs
4. Add comments for maintainability

### Phase 5: Testing
1. Commit and push workflow file
2. Make a test change to docs/
3. Verify workflow runs
4. Verify site deploys
5. Test deployed site functionality

### Phase 6: Documentation
1. Update README with docs link
2. Add badge for build status (optional)
3. Document workflow in this task

## Workflow File Structure

```yaml
name: Deploy Documentation

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - '.github/workflows/docs.yml'
  workflow_dispatch:  # Allow manual runs

# Permissions for GitHub Pages deployment
permissions:
  contents: read
  pages: write
  id-token: write

# Ensure only one deployment at a time
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'  # Cache pip dependencies

      - name: Install MkDocs Material
        run: pip install mkdocs-material

      - name: Build documentation
        run: mkdocs build --strict  # Fail on warnings

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'site'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## Success Criteria

### Deliverables
- [ ] `.github/workflows/docs.yml` created
- [ ] Workflow runs successfully on push to main
- [ ] Site deployed to GitHub Pages
- [ ] GitHub Pages URL accessible

### Quality Metrics
- [ ] Workflow completes in <3 minutes
- [ ] Build step uses --strict flag (no warnings)
- [ ] Deployment succeeds on first try
- [ ] No unnecessary permissions granted
- [ ] Pip cache reduces build time by 30%+

### Production Ready
- [ ] Site accessible at https://requirekit.github.io/require-kit/
- [ ] All pages load correctly
- [ ] Navigation works
- [ ] Search works
- [ ] Mobile responsive
- [ ] No console errors

## Notes

### Why Modern Approach (Not gh-pages Branch)

**ChatGPT Suggestion (Outdated)**:
- Uses `peaceiris/actions-gh-pages@v3`
- Creates/pushes to gh-pages branch
- Requires GH_PAGES token management
- More complex state management

**Modern Approach (Recommended)**:
- Uses `actions/deploy-pages@v4`
- No branch creation needed
- Uses GitHub's built-in OIDC authentication
- Simpler, more secure
- GitHub's official recommendation as of 2024

### GitHub Pages Settings

After workflow is set up, configure in GitHub:
1. Go to Settings → Pages
2. Under "Build and deployment"
3. Select "GitHub Actions" (not "Deploy from a branch")
4. Source: "GitHub Actions"

The first workflow run will configure this automatically.

### Workflow Dispatch

The `workflow_dispatch` trigger allows manual runs:
1. Go to Actions tab
2. Select "Deploy Documentation"
3. Click "Run workflow"
4. Choose branch (usually main)
5. Click "Run workflow"

Useful for:
- Testing workflow changes
- Force rebuild after config changes
- Redeploying without code changes

### Path Filters

Only trigger when relevant files change:
```yaml
paths:
  - 'docs/**'           # Any doc file
  - 'mkdocs.yml'        # Config changes
  - '.github/workflows/docs.yml'  # Workflow changes
```

This prevents unnecessary builds when code changes but docs don't.

### Pip Cache

The `cache: 'pip'` option in `setup-python` action:
- Caches pip dependencies between runs
- Reduces build time from ~60s to ~10s
- Invalidates cache when requirements change
- No manual cache key management needed

### Concurrency Group

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

- Ensures only one deployment at a time
- Prevents race conditions
- Doesn't cancel in-progress deployments (queue them)

### Security Considerations

1. **Fork PRs**: Workflow won't deploy from fork PRs (good for security)
2. **Permissions**: Minimal permissions (contents: read, pages: write)
3. **OIDC**: Uses GitHub's OIDC tokens (no secrets needed)
4. **Strict Build**: `--strict` flag catches potential issues

### Troubleshooting

**If workflow fails**:
1. Check workflow logs in Actions tab
2. Look for build errors (mkdocs build --strict)
3. Verify mkdocs.yml is valid
4. Check path filters (did relevant files change?)

**If deployment succeeds but site doesn't work**:
1. Check GitHub Pages settings (should be "GitHub Actions")
2. Verify site URL: https://requirekit.github.io/require-kit/
3. Check browser console for errors
4. Test site locally with `mkdocs serve`

**If Pages settings not showing**:
1. Workflow must run at least once
2. Wait 1-2 minutes after first run
3. Refresh GitHub settings page

### Reusability for Taskwright

This workflow was copied from Taskwright:
1. Workflow structure is identical
2. No changes needed (paths are the same)
3. GitHub Pages URL is different: https://requirekit.github.io/require-kit/

Completely reusable across repositories!

## Timeline Estimate

**Estimated Duration**: 1-2 hours

### Breakdown:
- Workflow file creation: 30 minutes
- Testing and debugging: 30 minutes
- GitHub Pages configuration: 15 minutes
- Verification and documentation: 30 minutes

## Related Documents

- `.github/workflows/` directory (to be created)
- `mkdocs.yml` (from TASK-DOCS-002)
- GitHub Actions documentation
- GitHub Pages documentation

## Next Steps After Completion

After this task completes:
1. Move to TASK-DOCS-005: Enable GitHub Pages (if not auto-enabled)
2. Verify deployed site works correctly
3. Update README with documentation link
4. (Optional) Consider custom domain setup (separate task)
