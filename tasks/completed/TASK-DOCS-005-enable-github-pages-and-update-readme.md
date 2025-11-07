---
id: TASK-DOCS-005
title: Enable GitHub Pages and update README with documentation link
status: backlog
created: 2025-11-06T00:00:00Z
updated: 2025-11-06T00:00:00Z
priority: medium
tags: [documentation, github-pages, readme]
epic: null
feature: null
requirements: []
dependencies: ["TASK-DOCS-004"]
complexity_evaluation:
  score: 2
  level: "simple"
  review_mode: "AUTO_PROCEED"
  factor_scores:
    - factor: "file_complexity"
      score: 1
      max_score: 3
      justification: "Simple README update"
    - factor: "pattern_familiarity"
      score: 0
      max_score: 2
      justification: "Standard configuration task"
    - factor: "risk_level"
      score: 0
      max_score: 3
      justification: "Zero risk - configuration only"
    - factor: "dependencies"
      score: 1
      max_score: 2
      justification: "Requires GitHub Actions workflow working"
---

# Task: Enable GitHub Pages and Update README with Documentation Link

## Context

After TASK-DOCS-004 (GitHub Actions workflow), we have:
- Automated MkDocs build and deployment workflow
- Site artifacts being generated
- Deployment action configured

Now we need to:
1. Enable GitHub Pages in repository settings (if not auto-enabled)
2. Verify the site is accessible
3. Update README to link to the documentation site
4. (Optional) Decide on custom domain

## Objective

Finalize GitHub Pages setup and make the documentation discoverable by adding prominent links in the README.

## Requirements

### GitHub Pages Configuration
- [ ] Navigate to repository Settings → Pages
- [ ] Verify "GitHub Actions" is selected as source
- [ ] Verify site is being deployed
- [ ] Verify site URL is accessible: https://requirekit.github.io/require-kit/
- [ ] Check for any deployment errors

### Site Verification
- [ ] Visit deployed site URL
- [ ] Test homepage loads correctly
- [ ] Test navigation works (all links)
- [ ] Test search functionality
- [ ] Test on mobile device (responsive)
- [ ] Check for console errors
- [ ] Verify all pages load (no 404s)

### README Updates
- [ ] Add "Documentation" section near top of README
- [ ] Add direct link to documentation site
- [ ] Add link in "Quick Start" section
- [ ] (Optional) Add documentation badge
- [ ] Keep existing documentation links for now (no breaking changes)

### Custom Domain Decision (Optional)
- [ ] Decide if using custom domain (docs.requirekit.dev or similar)
- [ ] If yes: Configure DNS CNAME record
- [ ] If yes: Add custom domain in GitHub Pages settings
- [ ] If yes: Wait for SSL certificate provisioning
- [ ] If no: Use GitHub Pages default URL

### Documentation Site Health Check
- [ ] All navigation links work
- [ ] Search indexes all pages
- [ ] Code blocks have syntax highlighting
- [ ] Images load (if any)
- [ ] External links work
- [ ] No broken internal links
- [ ] Responsive on mobile/tablet/desktop

## Acceptance Criteria

### GitHub Pages Enabled ✅
- [ ] GitHub Pages configured in repository settings
- [ ] Source set to "GitHub Actions"
- [ ] Site deployed successfully
- [ ] URL accessible: https://requirekit.github.io/require-kit/

### Site Verification ✅
- [ ] Homepage loads correctly
- [ ] All navigation works
- [ ] Search works
- [ ] Mobile responsive
- [ ] No console errors
- [ ] All pages accessible (no 404s)

### README Updated ✅
- [ ] "Documentation" section added
- [ ] Clear link to docs site
- [ ] Link appears early in README (before or after features)
- [ ] Quickstart section mentions docs
- [ ] Existing doc links preserved (backward compatibility)

### Custom Domain (If Applicable) ✅
- [ ] DNS CNAME configured (if using custom domain)
- [ ] Custom domain added in GitHub settings
- [ ] SSL certificate issued
- [ ] HTTPS redirect works
- [ ] Both www and non-www work (if applicable)

## Implementation Plan

### Phase 1: GitHub Pages Configuration
1. Go to repository settings → Pages
2. Under "Build and deployment"
3. Verify "Source" is set to "GitHub Actions"
4. If not set, select "GitHub Actions"
5. Note the site URL (usually auto-populated)

### Phase 2: Wait for Deployment
1. Wait for GitHub Actions workflow to complete
2. Check Actions tab for deployment status
3. Green checkmark = successful deployment
4. Note any errors if deployment fails

### Phase 3: Site Verification
1. Visit https://requirekit.github.io/require-kit/
2. Click through all navigation items
3. Test search (search for "EARS", "BDD", "requirements", etc.)
4. Open browser console, check for errors
5. Test on mobile (Chrome DevTools responsive mode)
6. Verify all pages load correctly

### Phase 4: README Updates
1. Open README.md
2. Add "Documentation" section after "What You Get"
3. Add link to docs site
4. Update "Quick Start" to mention docs
5. Optionally add documentation badge
6. Commit changes

### Phase 5: Custom Domain (Optional)
1. Decide: Yes or No to custom domain
2. If NO: Skip to Phase 6
3. If YES:
   - Add CNAME record in DNS: `docs.taskwright.dev → taskwright-dev.github.io`
   - In GitHub Pages settings, add custom domain: `docs.taskwright.dev`
   - Check "Enforce HTTPS" (after DNS propagates)
   - Wait for SSL certificate (5-10 minutes)
   - Test both http://docs.taskwright.dev and https://docs.taskwright.dev
   - Update README to use custom domain URL

### Phase 6: Final Verification
1. Test all links in README
2. Verify docs link works
3. Verify site loads quickly (<2 seconds)
4. Check for any final issues
5. Mark task complete

## README Updates

### Add Documentation Section

Add this section after "What You Get" in README.md:

```markdown
## Documentation

📚 **[View Full Documentation](https://requirekit.github.io/require-kit/)**

Comprehensive guides for requirements management:
- [Quickstart Guide](https://requirekit.github.io/require-kit/getting-started/)
- [EARS Notation](https://requirekit.github.io/require-kit/concepts/ears-notation/)
- [BDD/Gherkin Generation](https://requirekit.github.io/require-kit/concepts/bdd-generation/)
- [Epic/Feature Hierarchy](https://requirekit.github.io/require-kit/concepts/hierarchy/)
- [Guides](https://requirekit.github.io/require-kit/guides/)
- [Integration](https://requirekit.github.io/require-kit/integration/)
- [Troubleshooting](https://requirekit.github.io/require-kit/troubleshooting/)
```

### Update Quick Start Section

Add reference in "5-Minute Quickstart":

```markdown
## 5-Minute Quickstart

**📚 Full documentation: https://requirekit.github.io/require-kit/**

### Option 1: Quick Install (Recommended)
...
```

### Optional: Add Documentation Badge

At the top with other badges:

```markdown
![docs](https://img.shields.io/badge/docs-mkdocs-blue)
```

Or clickable badge:

```markdown
[![documentation](https://img.shields.io/badge/docs-online-blue)](https://requirekit.github.io/require-kit/)
```

## Success Criteria

### Deliverables
- [ ] GitHub Pages enabled and site deployed
- [ ] Site accessible at public URL
- [ ] README updated with documentation link
- [ ] All site functionality verified

### Quality Metrics
- [ ] Site loads in <2 seconds
- [ ] Zero broken links on deployed site
- [ ] Zero console errors
- [ ] Search works correctly
- [ ] Mobile responsive (tested on 3+ screen sizes)

### User Experience
- [ ] Clear path from README to docs
- [ ] Docs link prominent in README (top 3 sections)
- [ ] Site navigation intuitive
- [ ] Search returns relevant results
- [ ] Professional appearance

## Notes

### GitHub Pages URL Structure

**Default GitHub Pages URL**:
- Format: `https://<username>.github.io/<repository>/`
- For RequireKit: `https://requirekit.github.io/require-kit/`
- Note the trailing slash (optional but recommended)

**Custom Domain URL** (if used):
- Format: `https://docs.requirekit.dev/` or similar
- Cleaner, more professional
- Requires DNS configuration

### Custom Domain Setup (Detailed)

If you decide to use a custom domain:

**1. DNS Configuration**:
```
Type: CNAME
Name: docs
Value: requirekit.github.io
TTL: 3600 (or auto)
```

**2. GitHub Pages Settings**:
- Go to Settings → Pages
- Under "Custom domain", enter: `docs.requirekit.dev` (or your chosen domain)
- Click "Save"
- Wait for DNS check (green checkmark)

**3. SSL Certificate**:
- GitHub automatically provisions SSL
- Takes 5-10 minutes after DNS propagates
- Once ready, check "Enforce HTTPS"

**4. Verification**:
- Test: `http://docs.requirekit.dev` → redirects to https
- Test: `https://docs.requirekit.dev` → site loads
- Test: old URL still works (GitHub redirects)

### Custom Domain Pros/Cons

**Pros**:
- Professional URL (`docs.requirekit.dev` vs `requirekit.github.io/require-kit/`)
- Easier to remember
- Better SEO
- Can migrate to different host later without breaking links

**Cons**:
- Requires domain ownership
- Requires DNS configuration (~5 minutes)
- Adds complexity (one more thing to manage)

**Recommendation**: Start with GitHub Pages default, upgrade to custom domain later if needed. No code changes required—just update README.

### Testing Checklist

Before marking complete:
- [ ] Visit homepage
- [ ] Click "Getting Started" → loads
- [ ] Click "Core Concepts" → loads
- [ ] Click a guide link → loads correct guide
- [ ] Search for "quality" → returns relevant results
- [ ] Open page in mobile (DevTools responsive mode)
- [ ] Check browser console → no errors
- [ ] Check all images load (if any)
- [ ] Click external links (GitHub, RequireKit) → open correctly

### Troubleshooting

**Site returns 404**:
- Check GitHub Actions workflow completed successfully
- Check GitHub Pages is enabled (Settings → Pages)
- Wait 1-2 minutes after deployment
- Clear browser cache

**Site loads but search doesn't work**:
- Search indexes are generated during build
- Check `site/search/search_index.json` exists
- Rebuild site (`mkdocs build --strict`)

**Custom domain shows "DNS not configured"**:
- DNS changes take 5-60 minutes to propagate
- Check DNS with: `dig docs.requirekit.dev` (should show CNAME)
- Wait and try again

**HTTPS not available**:
- SSL certificate takes 5-10 minutes after DNS propagates
- Check GitHub Pages settings for SSL status
- Don't force HTTPS until certificate ready

### Reusability for Taskwright

This process was copied from Taskwright:
1. Enable GitHub Pages (Settings → Pages → GitHub Actions)
2. Site URL: `https://requirekit.github.io/require-kit/`
3. Update RequireKit README with docs link
4. (Optional) Custom domain: `docs.requirekit.dev`

Process is identical, just different URLs and content.

## Timeline Estimate

**Estimated Duration**: 30-60 minutes

### Breakdown:
- GitHub Pages configuration: 5 minutes
- Wait for deployment: 2-5 minutes
- Site verification: 10 minutes
- README updates: 10 minutes
- Custom domain (if used): 15-30 minutes
- Final verification: 10 minutes

## Related Documents

- `README.md` (to be updated)
- GitHub Pages settings (web UI)
- Deployed documentation site

## Next Steps After Completion

After this task completes:
1. Documentation site is live and discoverable
2. Users can access comprehensive guides
3. README directs users to full documentation
4. (Optional) Create TASK-DOCS-006: Add custom domain (if desired later)
5. (Optional) Create TASK-DOCS-007: Add version badge automation
6. Monitor documentation for user feedback and improvements

## Success Markers

✅ Documentation site live
✅ README updated
✅ Users can discover docs easily
✅ Site performs well (fast, responsive)
✅ Ready to announce documentation availability
