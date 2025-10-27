# Claude Code Software Engineering Lifecycle System

## Project Context

This is an AI-powered software engineering lifecycle system that uses EARS notation for requirements, BDD/Gherkin for test specifications, and markdown-driven state tracking. The system is technology-agnostic with stack-specific plugins.

## Core Principles

1. **Requirements First**: Every feature starts with EARS-notated requirements
2. **Test-Driven**: BDD scenarios generated from requirements drive implementation
3. **Quality Gates**: Automated testing and verification before completion
4. **State Tracking**: Transparent progress monitoring through markdown
5. **Technology Agnostic**: Core methodology works across all stacks

## System Philosophy

- Start simple, iterate toward complexity
- Markdown-driven for human and AI readability
- Verification through actual test execution
- Lightweight Architecture Decision Records
- Comprehensive changelogs for traceability

## Workflow Overview

1. **Gather Requirements**: Interactive Q&A sessions
2. **Formalize with EARS**: Convert to structured notation
3. **Generate BDD**: Create testable scenarios
4. **Implement**: Build with tests
5. **Verify**: Execute tests and quality gates
6. **Track**: Update state and changelog

## Technology Stack Detection

The system will detect your project's technology stack and apply appropriate testing strategies:
- React/TypeScript → Playwright + Vitest
- Python API → pytest + pytest-bdd
- Mobile → Platform-specific testing
- Infrastructure → Terraform testing

## Getting Started

Run `/gather-requirements` to begin a new feature development cycle.
