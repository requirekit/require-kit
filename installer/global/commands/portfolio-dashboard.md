# Portfolio Dashboard - Executive Project Overview

High-level portfolio visualization with executive metrics, business value tracking, and strategic project management insights.

## Usage
```bash
/portfolio-dashboard [options]
```

## Examples
```bash
# Executive overview dashboard
/portfolio-dashboard

# Business value focus
/portfolio-dashboard --business-value

# Resource allocation view
/portfolio-dashboard --resources

# Timeline and milestones
/portfolio-dashboard --timeline

# Risk assessment view
/portfolio-dashboard --risks

# External stakeholder view
/portfolio-dashboard --stakeholder

# Quarter planning view
/portfolio-dashboard --quarter Q1-2024
```

## Dashboard Formats

### Executive Overview (Default)
```
╔════════════════════════════════════════════════════════════════════════════════╗
║                        PORTFOLIO EXECUTIVE DASHBOARD                          ║
║                              Q1 2024 Progress                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝

📊 PORTFOLIO HEALTH SUMMARY
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Overall Progress: ████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░ 67% │
│ Business Value Delivered: $2.4M (Target: $3.5M by Q1 end)                     │
│ Timeline Status: ⚠️ 3 days behind (recoverable)                               │
│ Budget Utilization: 58% ($580K of $1M allocated)                              │
│ Quality Score: 9.1/10 (Excellent)                                             │
│ Team Satisfaction: 8.7/10 (High)                                              │
└─────────────────────────────────────────────────────────────────────────────────┘

🎯 STRATEGIC EPIC OVERVIEW
┌─────────────┬──────────────────────┬──────────┬─────────────┬─────────────┬──────────────┐
│ Epic ID     │ Initiative           │ Priority │ Progress    │ Business    │ Status       │
│             │                      │          │             │ Value       │              │
├─────────────┼──────────────────────┼──────────┼─────────────┼─────────────┼──────────────┤
│ EPIC-001    │ User Management      │ High     │ 78%         │ $1.2M       │ ✅ On Track  │
│             │ Complete user system │          │ (8/10 tasks)│ delivered   │              │
│             │ Target: Week 5       │          │             │             │              │
├─────────────┼──────────────────────┼──────────┼─────────────┼─────────────┼──────────────┤
│ EPIC-002    │ Payment Platform     │ Critical │ 34%         │ $0.8M       │ ⚠️ At Risk   │
│             │ Revenue generation   │          │ (3/8 tasks) │ projected   │ (3d behind)  │
│             │ Target: Week 8       │          │             │             │              │
├─────────────┼──────────────────────┼──────────┼─────────────┼─────────────┼──────────────┤
│ EPIC-003    │ Mobile Expansion     │ Medium   │ 15%         │ $0.4M       │ ✅ On Track  │
│             │ Market expansion     │          │ (1/8 tasks) │ projected   │ (planning)   │
│             │ Target: Week 10      │          │             │             │              │
└─────────────┴──────────────────────┴──────────┴─────────────┴─────────────┴──────────────┘

📈 KEY PERFORMANCE INDICATORS
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Q1 2024 METRICS                                   │
├─────────────────────┬─────────────────┬─────────────────┬─────────────────────┤
│ Delivery Velocity   │ Quality Metrics │ Resource Util   │ Business Impact     │
├─────────────────────┼─────────────────┼─────────────────┼─────────────────────┤
│ Epic Velocity:      │ Code Coverage:  │ Team Capacity:  │ Revenue Impact:     │
│ 1.2/month (↗️)      │ 88% avg (↗️)    │ 85% utilized    │ $2.4M delivered     │
│ Target: 1.5/month   │ Target: 85%     │ Target: 80%     │ Target: $3.5M       │
│                     │                 │                 │                     │
│ Feature Velocity:   │ Security Score: │ Overtime Hours: │ User Adoption:      │
│ 2.3/month (↗️)      │ 9.5/10 (↗️)     │ 12% avg        │ 15K new users       │
│ Target: 3.0/month   │ Target: 9.0     │ Target: <10%    │ Target: 20K         │
│                     │                 │                 │                     │
│ Task Completion:    │ Defect Rate:    │ External Deps:  │ Time to Market:     │
│ 2.1/week (→)        │ 0.3% (↗️)       │ 2 pending       │ 8 weeks avg        │
│ Target: 2.5/week    │ Target: <0.5%   │ Target: 0       │ Target: 6 weeks     │
└─────────────────────┴─────────────────┴─────────────────┴─────────────────────┘

🎯 QUARTERLY GOALS PROGRESS
Q1 2024 Objectives:
✅ User Management System: 78% → On track for Week 5 completion
⚠️ Payment Integration: 34% → At risk, need mitigation plan
⏳ Mobile Foundation: 15% → On track for planning milestone
✅ Quality Standards: 9.1/10 → Exceeding target
⚠️ Revenue Target: $2.4M/$3.5M → Need acceleration

🚨 EXECUTIVE ATTENTION REQUIRED
1. Payment Platform (EPIC-002): 3 days behind due to payment provider API delays
   Impact: $0.7M revenue at risk
   Recommendation: Escalate with payment provider, consider alternative

2. Resource Allocation: Mike Johnson overallocated (125% capacity)
   Impact: Potential burnout, delivery risk
   Recommendation: Redistribute 2 tasks to available team members

3. External Dependencies: 2 critical dependencies pending resolution
   Impact: Blocks 4 tasks, potential 1-week delay
   Recommendation: Daily check-ins with external teams

💡 STRATEGIC RECOMMENDATIONS
├── Accelerate Payment Platform: Add contractor resource for 4 weeks
├── Risk Mitigation: Develop backup plan for payment provider issues
├── Team Expansion: Consider hiring 1 additional frontend developer
└── Process Optimization: Implement daily standups for blocked items

🏆 ACHIEVEMENTS THIS QUARTER
✅ User Registration System delivered 2 days early
✅ Security audit passed with 9.8/10 score
✅ Team productivity increased 15% from Q4
✅ Zero critical security vulnerabilities
✅ Customer satisfaction: 4.8/5 stars
```

### Business Value Dashboard
```bash
/portfolio-dashboard --business-value

💰 BUSINESS VALUE DASHBOARD

📊 Revenue Impact Tracking
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BUSINESS VALUE DELIVERY                              │
└─────────────────────────────────────────────────────────────────────────────────┘

💵 Value by Epic
EPIC-001: User Management System
├── Target Value: $1.5M (user acquisition & retention)
├── Delivered Value: $1.2M (80% of target)
├── ROI: 240% (development cost: $500K)
└── Payback Period: 4.2 months

EPIC-002: Payment Platform
├── Target Value: $2.0M (direct revenue processing)
├── Projected Value: $0.8M (based on 34% completion)
├── ROI: 160% (development cost: $750K)
└── Payback Period: 6.8 months (projected)

EPIC-003: Mobile Expansion
├── Target Value: $1.0M (market expansion)
├── Projected Value: $0.4M (based on 15% completion)
├── ROI: 133% (development cost: $400K)
└── Payback Period: 8.5 months (projected)

📈 Value Realization Timeline
Month 1: $0.2M (User registration revenue)
Month 2: $0.6M (Authentication platform value)
Month 3: $1.2M (Complete user management value)
Month 4: $1.8M (Payment processing begins)
Month 5: $2.4M (Current total delivered)
Month 6: $3.2M (Projected with payment completion)

🎯 Business Metrics Dashboard
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ User Metrics    │ Revenue Metrics │ Cost Metrics    │ Quality Metrics │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ New Users:      │ Monthly Revenue:│ Dev Cost:       │ User Satisfaction│
│ 15,000          │ $485K           │ $580K total     │ 4.8/5 stars     │
│ Target: 20,000  │ Target: $650K   │ Budget: $1M     │ Target: 4.5      │
│                 │                 │                 │                 │
│ User Retention: │ Revenue Growth: │ Cost Per User:  │ System Uptime:  │
│ 87%             │ 32% MoM         │ $38.67          │ 99.95%          │
│ Target: 85%     │ Target: 25%     │ Target: <$40    │ Target: 99.9%   │
│                 │                 │                 │                 │
│ Conversion Rate:│ ARPU:           │ Support Cost:   │ Performance:    │
│ 12.3%           │ $32.33          │ $0.85/user      │ <200ms avg      │
│ Target: 15%     │ Target: $35     │ Target: <$1     │ Target: <300ms  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

💡 Value Optimization Opportunities
1. Accelerate payment completion: +$0.5M additional Q1 revenue
2. Optimize user onboarding: +2% conversion rate improvement
3. Reduce support costs: Automated help system (-$0.20/user)
4. Mobile early access: +$0.2M additional revenue opportunity
```

### Resource Allocation Dashboard
```bash
/portfolio-dashboard --resources

👥 RESOURCE ALLOCATION DASHBOARD

📊 Team Capacity & Utilization
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            TEAM RESOURCE OVERVIEW                              │
└─────────────────────────────────────────────────────────────────────────────────┘

👨‍💻 Development Team (5 members)
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Team Member     │ Capacity    │ Allocation  │ Active Tasks│ Efficiency  │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Mike Johnson    │ 40h/week    │ 125% ⚠️     │ 3 tasks     │ 92%         │
│ (Tech Lead)     │             │ 50h actual │ (overloaded)│             │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Sarah Chen      │ 40h/week    │ 95%         │ 2 tasks     │ 88%         │
│ (Senior Dev)    │             │ 38h actual │ (optimal)   │             │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Lisa Park       │ 40h/week    │ 80%         │ 2 tasks     │ 85%         │
│ (Frontend)      │             │ 32h actual │ (available) │             │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Alex Rodriguez  │ 40h/week    │ 75%         │ 1 task      │ 90%         │
│ (QA Engineer)   │             │ 30h actual │ (available) │             │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ Emma Wilson     │ 32h/week    │ 90%         │ 2 tasks     │ 93%         │
│ (Part-time)     │             │ 29h actual │ (optimal)   │             │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

🎯 Resource Distribution by Epic
EPIC-001 (User Management): 45% team capacity
├── Mike Johnson: 30% (critical path tasks)
├── Sarah Chen: 25% (authentication work)
└── Lisa Park: 20% (UI components)

EPIC-002 (Payment System): 35% team capacity
├── Mike Johnson: 40% (payment integration)
├── Alex Rodriguez: 30% (testing)
└── Emma Wilson: 25% (API work)

EPIC-003 (Mobile Platform): 20% team capacity
├── Sarah Chen: 15% (architecture)
└── Lisa Park: 35% (mobile UI)

⚠️ Resource Constraints & Bottlenecks
1. Mike Johnson: 125% allocated (critical bottleneck)
   Impact: Delays across EPIC-001 and EPIC-002
   Recommendation: Redistribute TASK-020 and TASK-013

2. Frontend capacity: Lisa available for additional 8h/week
   Opportunity: Accelerate mobile UI work or take on payment UI

3. QA capacity: Alex available for additional 10h/week
   Opportunity: Increase test coverage or automate testing

💰 Resource Cost Analysis
Total Team Cost: $68K/month
├── Development: $55K (81%)
├── QA & Testing: $8K (12%)
└── Management: $5K (7%)

Cost per Epic:
├── EPIC-001: $30.6K (45% of capacity)
├── EPIC-002: $23.8K (35% of capacity)
└── EPIC-003: $13.6K (20% of capacity)

Cost per Feature Delivered: $11.3K average
Cost per Task Completed: $2.6K average
ROI on Team Investment: 285% (excellent)

📊 Skill Matrix & Coverage
┌─────────────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Skill Area      │ Mike    │ Sarah   │ Lisa    │ Alex    │ Emma    │
├─────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ Backend API     │ ★★★★★   │ ★★★★    │ ★★      │ ★★      │ ★★★     │
│ Frontend UI     │ ★★      │ ★★★     │ ★★★★★   │ ★★      │ ★★★     │
│ Database        │ ★★★★    │ ★★★     │ ★       │ ★★      │ ★★★     │
│ Testing         │ ★★★     │ ★★★     │ ★★      │ ★★★★★   │ ★★      │
│ Mobile          │ ★★      │ ★★★★    │ ★★★★    │ ★★      │ ★★      │
│ DevOps          │ ★★★★    │ ★★      │ ★       │ ★★★     │ ★       │
│ Security        │ ★★★★    │ ★★★     │ ★★      │ ★★★★    │ ★★      │
└─────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘

🔍 Skill Gap Analysis
Strengths: Backend development, Testing, Security
Gaps: Advanced mobile development, DevOps automation
Recommendation: Training investment or contractor for mobile expertise

💡 Resource Optimization Recommendations
1. Redistribute 2 tasks from Mike to Lisa and Alex (immediate)
2. Cross-train Sarah and Emma on mobile development (2-week investment)
3. Consider contractor for DevOps automation (4-week engagement)
4. Implement pair programming for knowledge transfer (ongoing)
```

## Risk Assessment Dashboard

### Risk Overview
```bash
/portfolio-dashboard --risks

🚨 PORTFOLIO RISK ASSESSMENT

📊 Risk Heat Map
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               RISK MATRIX                                      │
│                    HIGH IMPACT                                                  │
│                ╔═══════════════╦═══════════════╗                               │
│    HIGH PROB   ║ 🔴 CRITICAL   ║ 🔴 CRITICAL   ║                               │
│                ║ Resource      ║ Payment API   ║                               │
│                ║ Bottleneck    ║ Dependency    ║                               │
│                ╠═══════════════╬═══════════════╣                               │
│    LOW PROB    ║ 🟡 MEDIUM     ║ 🟠 HIGH       ║                               │
│                ║ Team Turnover ║ Security      ║                               │
│                ║               ║ Vulnerability ║                               │
│                ╚═══════════════╩═══════════════╝                               │
│                    LOW IMPACT       HIGH IMPACT                                │
└─────────────────────────────────────────────────────────────────────────────────┘

🔴 CRITICAL RISKS (Immediate Action Required)

Risk #1: Payment Provider API Dependency
├── Impact: 🔴 High ($0.7M revenue at risk)
├── Probability: 🔴 High (ongoing delays)
├── Epic Affected: EPIC-002 (Payment System)
├── Timeline Impact: +2 weeks delay
├── Mitigation Status: 🟡 In Progress
└── Next Review: Tomorrow 9:00 AM

Mitigation Plan:
├── Primary: Daily escalation calls with payment provider
├── Secondary: Implement mock API for development continuation
└── Tertiary: Evaluate alternative payment providers (2-week lead time)

Risk #2: Resource Bottleneck (Mike Johnson)
├── Impact: 🔴 High (blocks 2 epics)
├── Probability: 🔴 High (125% utilization)
├── Epics Affected: EPIC-001, EPIC-002
├── Timeline Impact: +1 week delay
├── Mitigation Status: 🟢 Ready to Execute
└── Action Date: This week

Mitigation Plan:
├── Immediate: Redistribute 2 tasks to Lisa and Alex
├── Short-term: Hire contractor for 4 weeks
└── Long-term: Promote Sarah to co-tech lead

🟠 HIGH RISKS (Monitor Closely)

Risk #3: Security Vulnerability Discovery
├── Impact: 🔴 High (potential security breach)
├── Probability: 🟡 Medium (10% chance)
├── Epic Affected: All epics
├── Timeline Impact: +3 weeks if discovered
├── Mitigation Status: 🟢 Proactive
└── Next Review: Weekly security scans

Risk #4: Mobile Platform Technology Shift
├── Impact: 🟠 Medium (rework required)
├── Probability: 🟡 Medium (React Native updates)
├── Epic Affected: EPIC-003
├── Timeline Impact: +2 weeks
├── Mitigation Status: 🟢 Monitoring
└── Technology Review: Monthly

🟡 MEDIUM RISKS (Planned Monitoring)

Risk #5: Team Member Departure
├── Impact: 🟠 Medium (knowledge loss)
├── Probability: 🟢 Low (high satisfaction)
├── Timeline Impact: +4 weeks for replacement
├── Mitigation: Cross-training and documentation
└── Review Frequency: Quarterly

Risk #6: External Integration Changes
├── Impact: 🟡 Low (minor rework)
├── Probability: 🟡 Medium (vendor updates)
├── Timeline Impact: +1 week
├── Mitigation: Versioned API contracts
└── Review Frequency: Monthly

📊 Risk Trend Analysis
Month 1: 3 risks identified, 1 resolved
Month 2: 5 risks identified, 2 resolved, 1 escalated
Month 3: 6 risks identified, 3 resolved, 2 active
Trend: Risk identification improving, resolution rate stable

💡 Risk Management Recommendations
1. Implement daily risk standup for critical risks
2. Establish alternative vendor relationships (payment, hosting)
3. Increase team cross-training to reduce single points of failure
4. Create emergency response playbook for critical issues
5. Monthly risk review with stakeholders
```

This portfolio dashboard provides executive-level insights while maintaining full integration with the **Epic → Feature → Task hierarchy** and **Agentecflow workflow tracking**.