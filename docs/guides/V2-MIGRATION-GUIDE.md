# Migration Guide: v1.x → v2.0 Enterprise Edition

## 📋 Overview

Agentecflow v2.0 introduces enterprise-grade project management capabilities while maintaining full backward compatibility with v1.x workflows. This guide helps you migrate to the enhanced enterprise features.

## 🔄 What's New in v2.0

### Enterprise Features Added
- **Epic → Feature → Task Hierarchy**: Three-tier project structure
- **PM Tool Integration**: Jira, Linear, GitHub Projects, Azure DevOps
- **Portfolio Management**: Executive dashboards and business metrics
- **Progress Rollup**: Automatic progress calculation across hierarchy
- **Agentecflow Stages**: Complete Stage 1-4 implementation
- **Enhanced Quality Gates**: Comprehensive validation workflows

### Enhanced Templates
- **TypeScript API**: NestJS with Result patterns
- **Full Stack**: React + Python with shared types
- **Updated Stacks**: All templates enhanced with enterprise capabilities

## 🚀 Migration Strategies

### Option 1: Fresh Start (Recommended for New Projects)
```bash
# Install v2.0
curl -sSL https://raw.githubusercontent.com/appmilla/agentic-flow/main/installer/scripts/install.sh | bash

# Initialize with enterprise template
agentecflow init typescript-api  # or your preferred stack
```

### Option 2: In-Place Migration (Existing Projects)
```bash
# Backup existing project
cp -r .claude .claude.v1.backup

# Reinitialize with v2.0 capabilities
agentecflow init --upgrade

# Migrate existing tasks to hierarchy
/migrate-tasks-to-v2
```

### Option 3: Gradual Migration (Mixed Mode)
Continue using v1.x commands while gradually adopting v2.0 features:
```bash
# Keep using existing commands
/gather-requirements
/task-create "My Task"

# Add enterprise structure gradually
/epic-create "Strategic Initiative"
/feature-create "Feature Name" epic:EPIC-001
```

## 📊 Command Migration Map

### v1.x → v2.0 Command Evolution

| v1.x Command | v2.0 Enhanced Command | Notes |
|--------------|----------------------|-------|
| `/task-create` | `/task-create` + hierarchy | Now supports epic/feature linking |
| `/task-implement` | `/task-work` | Unified implementation + testing |
| `/task-test` | Part of `/task-work` | Automatic quality gates |
| `/task-complete` | `/task-complete` | Now includes progress rollup |
| `/execute-tests` | Part of `/task-work` | Integrated into workflow |
| `/update-state` | Automatic | Progress updates automatically |

### New Enterprise Commands
```bash
# Epic Management
/epic-create "Strategic Initiative"
/epic-status EPIC-001
/epic-sync EPIC-001

# Feature Management
/feature-create "User Feature" epic:EPIC-001
/feature-status FEAT-001
/feature-generate-tasks FEAT-001

# Visualization
/hierarchy-view --mode=detailed
/portfolio-dashboard --stakeholder=executive
```

## 🔧 Project Structure Changes

### v1.x Structure
```
.claude/
docs/
  requirements/
  bdd/
  adr/
src/
tests/
```

### v2.0 Enhanced Structure
```
.claude/              # Enhanced configuration
docs/                 # All documentation
  requirements/
  bdd/
  adr/
  state/
tasks/                # Task management
  backlog/
  in_progress/
  in_review/
  blocked/
  completed/
epics/                # Epic management
  active/
  archived/
features/             # Feature management
  active/
  archived/
portfolio/            # Portfolio metrics
  metrics/
  reports/
src/                  # Source code (unchanged)
tests/                # Tests (unchanged)
```

## 📝 Configuration Migration

### Update .claude/settings.json
```json
{
  "version": "2.0.0",
  "enterprise": {
    "hierarchy_enabled": true,
    "pm_tool_integration": true,
    "portfolio_tracking": true
  },
  "pm_tools": {
    "jira": {
      "url": "https://company.atlassian.net",
      "project_key": "PROJ"
    },
    "linear": {
      "team_id": "company-team"
    }
  },
  "quality_gates": {
    "coverage_threshold": 80,
    "review_required": true
  }
}
```

## 🎯 Migration Steps by Use Case

### For Individual Developers
1. **Update Installation**
   ```bash
   curl -sSL https://raw.githubusercontent.com/appmilla/agentic-flow/main/installer/scripts/install.sh | bash
   ```

2. **Continue Current Workflow**
   - All v1.x commands still work
   - Quality gates are enhanced but compatible
   - `/task-work` replaces `/task-implement` + `/task-test`

3. **Gradual Adoption**
   ```bash
   # Start grouping related tasks
   /epic-create "My Project Goals"
   /feature-create "Core Feature" epic:EPIC-001
   /task-create "Implementation" feature:FEAT-001
   ```

### For Small Teams
1. **Team Migration Meeting**
   - Review enterprise features
   - Plan epic/feature structure
   - Assign PM tool admin

2. **Project Restructuring**
   ```bash
   # Create strategic epics
   /epic-create "User Management" stakeholders:[pm@team.com]
   /epic-create "Core Features" stakeholders:[lead@team.com]

   # Migrate existing work
   /feature-create "Authentication" epic:EPIC-001
   /task-create "Login System" feature:FEAT-001
   ```

3. **Workflow Training**
   - `/task-work` unified workflow
   - Hierarchy visualization
   - Progress tracking

### For Enterprise Teams
1. **PM Tool Integration Setup**
   ```bash
   # Configure Jira integration
   agentecflow config jira --url=https://company.atlassian.net --project=PROJ

   # Test integration
   /epic-create "MVP Development" export:jira
   ```

2. **Portfolio Structure Design**
   ```bash
   # Strategic epic creation
   /epic-create "Q4 Objectives" business_value:10 effort_estimate:55
   /epic-create "Technical Debt" business_value:3 effort_estimate:21

   # Feature planning
   /feature-create "User Onboarding" epic:EPIC-001
   /feature-create "Performance Optimization" epic:EPIC-002
   ```

3. **Stakeholder Dashboard Setup**
   ```bash
   # Executive reporting
   /portfolio-dashboard --stakeholder=executive --schedule=weekly

   # Development metrics
   /hierarchy-view --mode=timeline --export=pdf
   ```

## 🧪 Testing Migration

### Validate v1.x Compatibility
```bash
# Test existing commands still work
/gather-requirements test-feature
/formalize-ears requirements.md
/generate-bdd REQ-001

# Verify quality gates
/task-work TASK-001 --mode=standard
```

### Test New Enterprise Features
```bash
# Test hierarchy creation
/epic-create "Test Epic"
/feature-create "Test Feature" epic:EPIC-001
/task-create "Test Task" feature:FEAT-001

# Test visualization
/hierarchy-view
/portfolio-dashboard --stakeholder=development
```

### Validate PM Tool Integration
```bash
# Test external sync
/epic-sync EPIC-001
/feature-sync FEAT-001
/task-sync TASK-001

# Verify external tool updates
```

## 🔍 Common Migration Issues

### Issue: "Command not found"
**Cause**: Old installation conflicts with new version
**Solution**:
```bash
# Clean installation
rm -rf ~/.agentecflow
curl -sSL https://install-script-url | bash
source ~/.bashrc
```

### Issue: "Invalid epic reference"
**Cause**: Tasks created without epic/feature hierarchy
**Solution**:
```bash
# Create missing hierarchy
/epic-create "Legacy Work"
/feature-create "Existing Tasks" epic:EPIC-001

# Link existing tasks
/task-update TASK-001 feature:FEAT-001
```

### Issue: "PM tool sync failed"
**Cause**: Missing or incorrect PM tool configuration
**Solution**:
```bash
# Reconfigure PM tools
agentecflow config jira --reset
agentecflow config jira --url=correct-url --project=PROJ

# Test connection
/epic-create "Test Epic" export:jira
```

### Issue: "Quality gates too strict"
**Cause**: v2.0 has enhanced quality standards
**Solution**:
```bash
# Temporarily adjust thresholds
/task-work TASK-001 --coverage-threshold=70

# Or update project configuration
agentecflow config quality-gates --coverage=75
```

## 📈 Benefits After Migration

### Enhanced Productivity
- **70% fewer commands**: Unified `/task-work` workflow
- **Automatic quality gates**: No manual test execution
- **Progress visibility**: Real-time hierarchy updates
- **PM tool sync**: Automatic stakeholder updates

### Better Project Management
- **Strategic alignment**: Epic-level planning
- **Feature tracking**: Clear development phases
- **Resource planning**: Capacity and timeline visibility
- **Risk management**: Early bottleneck identification

### Improved Quality
- **Comprehensive testing**: TDD/BDD/Standard modes
- **Coverage enforcement**: Automatic quality validation
- **Review workflows**: Built-in approval processes
- **Documentation**: Self-documenting hierarchy

## 🎯 Migration Timeline

### Week 1: Planning
- [ ] Review enterprise features
- [ ] Plan epic/feature structure
- [ ] Configure PM tool integration
- [ ] Team training on new commands

### Week 2: Implementation
- [ ] Install v2.0 on development machines
- [ ] Migrate high-priority projects
- [ ] Test PM tool synchronization
- [ ] Validate quality gate configuration

### Week 3: Adoption
- [ ] Team starts using `/task-work` workflow
- [ ] Regular hierarchy review meetings
- [ ] Portfolio dashboard monitoring
- [ ] Stakeholder feedback collection

### Week 4: Optimization
- [ ] Fine-tune quality gate thresholds
- [ ] Optimize PM tool sync frequency
- [ ] Establish governance processes
- [ ] Document team-specific workflows

## 🚀 Next Steps After Migration

1. **Master the Unified Workflow**
   ```bash
   /task-work TASK-XXX --mode=tdd
   ```

2. **Establish Epic Planning Rhythm**
   - Weekly epic status reviews
   - Monthly portfolio dashboard reviews
   - Quarterly strategic planning

3. **Optimize PM Tool Integration**
   - Configure notification preferences
   - Establish sync schedules
   - Train stakeholders on dashboard access

4. **Leverage Analytics**
   - Track velocity improvements
   - Monitor quality metrics
   - Identify process bottlenecks

## 📚 Additional Resources

- [Enterprise Features Guide](ENTERPRISE-FEATURES-GUIDE.md)
- [Command Usage Guide v2.0](COMMAND_USAGE_GUIDE.md)
- [Quick Reference v2.0](QUICK_REFERENCE.md)
- [PM Tool Integration Setup](../setup/PM_TOOL_SETUP.md)

## 💬 Support

For migration assistance:
1. Check troubleshooting sections in guides
2. Review examples in [Command Usage Guide](COMMAND_USAGE_GUIDE.md)
3. Test with sample projects before migrating production work

---

*This migration guide ensures a smooth transition to Agentecflow v2.0 enterprise capabilities while maintaining productivity throughout the upgrade process.*