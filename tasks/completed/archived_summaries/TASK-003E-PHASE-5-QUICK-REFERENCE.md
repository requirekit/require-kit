# TASK-003E Phase 5 Quick Reference Card

**Status**: READY FOR IMPLEMENTATION
**Estimated Effort**: 5 days (37 hours)
**Priority**: HIGH (7 tests failing, 7 edge cases missing)

---

## TL;DR

- **What**: Fix 7 test failures + implement 7 missing edge cases
- **Why**: Achieve production-ready quality (90% test coverage, 100% edge case coverage)
- **When**: 5 days (Days 1-5 detailed in checklist)
- **Who**: Assign to developer familiar with Python testing

---

## Current Status

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Tests Passing | 569/576 | 580+/580+ | 7 failures |
| Edge Cases | 11/18 | 18/18 | 7 missing |
| Coverage | 69% | ≥90% | +21% |

---

## Day-by-Day Plan

### Day 1: Fix Test Failures (7 hours)
- Path resolver tests (9 failures) - macOS symlink issue
- File operation tests (2 failures) - parent dir creation
- Stub tests (3 failures) - update expectations

### Day 2: Error Handling (8 hours)
- File write failure graceful degradation
- Configuration flag conflict detection
- Corrupted metrics file skipping
- User-friendly error messages

### Day 3: Boundary & State (6 hours)
- Empty plan section display ("Not specified")
- Modification complexity warnings
- Q&A question limits (max 20)

### Day 4: Edge Case Tests (8 hours)
- Create `tests/edge_cases/` directory
- Write 18 new tests (error, boundary, config, state)

### Day 5: Documentation (8 hours)
- Update README with error patterns
- Create troubleshooting guide
- Update CLAUDE.md with examples

---

## Top 3 Priority Fixes

### 1. Path Resolver Tests (9 failures)
**File**: `tests/unit/test_path_resolver.py`
**Fix**: Use `Path.resolve()` to handle macOS symlinks
```python
expected = Path(tmp_path).resolve()  # Add .resolve()
actual = result.resolve()
assert actual == expected
```

### 2. File Write Failure Handling
**File**: `installer/global/commands/lib/review_modes.py`
**Fix**: Graceful degradation in `_move_task_to_backlog()`
```python
try:
    FileOperations.atomic_write(backlog_path, updated_content)
except OSError as e:
    logger.error(f"Failed to move task file: {e}")
    print(f"\n⚠️ Warning: Could not move task file (saved in place)")
    # Continue - don't fail task
```

### 3. Configuration Flag Conflicts
**File**: `installer/global/commands/lib/review_router.py` (or new `flag_validator.py`)
**Fix**: Validate conflicting flags
```python
def validate_user_flags(user_flags: Dict[str, bool]) -> None:
    if user_flags.get("skip_review") and user_flags.get("force_review"):
        raise ValueError(
            "Conflicting flags: --skip-review and --force-review "
            "cannot be used together"
        )
```

---

## Edge Cases Summary

### Error Handling (4/5 ✅, 1/5 ❌)
- ✅ Plan generation failure → Fail-safe score=10
- ✅ Complexity calculation error → Fail-safe score=10
- ✅ User interrupt (Ctrl+C) → Clean exit
- ✅ Invalid user input → Re-prompt (max 3 attempts)
- ❌ **File write failure** → **MISSING** (Priority Fix)

### Boundary Conditions (3/5 ✅, 2/5 ❌)
- ✅ Task with 0 files → Minimum score=1
- ✅ Task with 50+ files → Capped at score=10
- ✅ Task with no dependencies → Score=0
- ✅ Task with 10+ dependencies → Future factor
- ❌ **Empty plan sections** → **MISSING** (Shows "None")

### Configuration (2/4 ✅, 2/4 ❌)
- ✅ Invalid threshold values → Use defaults
- ❌ **Conflicting flags** → **MISSING** (No validation)
- ✅ Missing settings.json → Use defaults
- ❌ **Corrupted metrics file** → **MISSING** (May crash)

### Concurrency & State (1/4 ✅, 3/4 ❌)
- ✅ Multiple modifications (v1→v4) → Version history
- ❌ **Modification increases complexity** → **MISSING** (No warning)
- ❌ **Long Q&A session (10+ questions)** → **MISSING** (No limit)
- ❌ Timeout during file write → **MISSING** (Hard to handle)

---

## Test File Organization

```
tests/
├── edge_cases/              # NEW (Day 4)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_error_handling.py       # 5 tests
│   ├── test_boundary_conditions.py  # 5 tests
│   ├── test_configuration_edge.py   # 4 tests
│   └── test_concurrency_state.py    # 4 tests
├── unit/                    # Existing
├── integration/             # Existing
└── e2e/                    # Existing
```

---

## Files to Modify

### Core Implementation
1. `installer/global/commands/lib/review_modes.py`
   - File write failure handling
   - Empty plan section display
   - Modification complexity warnings

2. `installer/global/commands/lib/review_router.py` (or new `flag_validator.py`)
   - Configuration flag validation

3. `installer/global/commands/lib/metrics_storage.py`
   - Corrupted metrics file skipping

4. `installer/global/commands/lib/qa_manager.py`
   - Q&A question limit

5. `installer/global/commands/lib/error_messages.py` (NEW)
   - User-friendly error formatters

### Tests to Fix
1. `tests/unit/test_path_resolver.py` (9 tests)
2. `tests/unit/test_full_review.py` (4 tests)
3. `tests/unit/test_json_serializer.py` (1 test)
4. `tests/unit/test_metrics_storage.py` (1 test)

### Tests to Create
1. `tests/edge_cases/test_error_handling.py` (5 tests)
2. `tests/edge_cases/test_boundary_conditions.py` (5 tests)
3. `tests/edge_cases/test_configuration_edge.py` (4 tests)
4. `tests/edge_cases/test_concurrency_state.py` (4 tests)

### Documentation to Update
1. `installer/global/commands/lib/README.md`
2. `docs/TROUBLESHOOTING.md` (NEW)
3. `CLAUDE.md`

---

## Testing Commands

### Run All Tests
```bash
pytest tests/ -v --cov=installer --cov-report=term --cov-report=json
```

### Run Only Edge Case Tests
```bash
pytest tests/edge_cases/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_path_resolver.py -v
```

### Check Coverage
```bash
pytest tests/ --cov=installer --cov-report=html
open htmlcov/index.html
```

---

## Success Criteria Checklist

### Tests
- [ ] All 7 test failures fixed (569 → 580+ passing)
- [ ] 18 new edge case tests implemented and passing
- [ ] Unit test coverage ≥ 90% (currently 69%)
- [ ] Integration test coverage ≥ 80%

### Edge Cases
- [ ] 5/5 error handling edge cases implemented
- [ ] 5/5 boundary condition edge cases implemented
- [ ] 4/4 configuration edge cases implemented
- [ ] 4/4 concurrency/state edge cases implemented

### Code Quality
- [ ] All modules < 10 cyclomatic complexity
- [ ] All user-facing errors have friendly messages
- [ ] All file operations remain atomic
- [ ] All user inputs remain validated

### Documentation
- [ ] Error handling patterns documented
- [ ] Troubleshooting guide created
- [ ] Edge case examples in CLAUDE.md
- [ ] API docs updated

---

## Common Pitfalls to Avoid

1. **Don't break existing tests** while fixing failures
   - Run full test suite after each fix
   - Commit incrementally

2. **Don't over-engineer edge case handlers**
   - Keep solutions simple
   - Follow existing patterns

3. **Don't skip test coverage**
   - Write tests for all edge cases
   - Aim for ≥90% unit coverage

4. **Don't forget cross-platform testing**
   - Test on macOS and Linux
   - Use Path.resolve() for symlinks

5. **Don't leave TODO comments**
   - Implement all edge cases in Phase 5
   - Document any deferred items

---

## Useful Code Snippets

### Error Message Formatter Template
```python
def format_file_error(error: OSError, context: str) -> str:
    """Format file operation error with context."""
    if error.errno == 30:  # Read-only file system
        return (
            f"Cannot write to {context}: File system is read-only.\n"
            f"Solution: Check disk permissions or free up space."
        )
    else:
        return (
            f"Cannot write to {context}: {error}\n"
            f"Solution: Check file permissions and try again."
        )
```

### Graceful Degradation Template
```python
try:
    # Critical operation
    perform_operation()
except SpecificError as e:
    # Log error
    logger.error(f"Operation failed: {e}")
    # Show user-friendly message
    print(f"\n⚠️ Warning: Operation failed (continuing...)")
    # Continue workflow - don't fail
```

### Input Validation Template
```python
invalid_attempts = 0
max_attempts = 3

while True:
    user_input = input("Your choice: ").strip().lower()

    if user_input in valid_choices:
        return user_input

    invalid_attempts += 1
    print(f"\n❌ Invalid choice: '{user_input}'")
    print(f"Please enter {', '.join(valid_choices)}")

    if invalid_attempts >= max_attempts:
        print(f"⚠️ {invalid_attempts} invalid attempts. Please review options.")
```

---

## Key Contacts & Resources

### Code Review Documents
- **Detailed Review**: `/TASK-003E-PHASE-5-EDGE-CASE-REVIEW.md`
- **Implementation Checklist**: `/TASK-003E-PHASE-5-IMPLEMENTATION-CHECKLIST.md`
- **Executive Summary**: `/TASK-003E-PHASE-5-EXECUTIVE-SUMMARY.md`
- **Quick Reference**: `/TASK-003E-PHASE-5-QUICK-REFERENCE.md` (this document)

### Related Tasks
- **TASK-003E**: Comprehensive Testing & Documentation (parent)
- **TASK-003D**: Configuration & Metrics (parallel)
- **TASK-003C**: Integration task-work workflow (dependency)

### Useful Links
- **pytest Documentation**: https://docs.pytest.org/
- **Python Error Handling Best Practices**: https://realpython.com/python-exceptions/
- **Code Coverage with pytest**: https://pytest-cov.readthedocs.io/

---

## Questions & Support

### FAQ

**Q: Which edge cases are highest priority?**
A: File write failure handling, configuration flag conflicts, and path resolver test fixes.

**Q: Can I defer any edge cases?**
A: Timeout handling (concurrency edge case) can be deferred - it's OS-level and already mitigated by atomic writes.

**Q: How do I handle platform-specific tests?**
A: Use `Path.resolve()` to resolve symlinks, mock platform-specific behavior, test on both macOS and Linux.

**Q: What if I discover new edge cases?**
A: Document them in a backlog task, don't block Phase 5 completion.

**Q: How do I know when I'm done?**
A: All checkboxes in Success Criteria are checked, all tests passing, coverage ≥ 90%.

### Getting Help

If you encounter issues:
1. Review detailed analysis in main review document
2. Check implementation checklist for specific guidance
3. Run test suite to identify regressions
4. Consult troubleshooting guide (to be created Day 5)

---

## Timeline & Milestones

### Day 1 Milestone
- ✅ All 7 test failures fixed
- ✅ Tests passing: 580+/580+
- ✅ CI/CD pipeline green

### Day 3 Milestone (Mid-Point)
- ✅ All critical edge cases implemented
- ✅ Error handling complete
- ✅ Boundary & state edge cases complete

### Day 5 Milestone (Completion)
- ✅ 18 edge case tests passing
- ✅ Coverage ≥ 90% unit, ≥ 80% integration
- ✅ Documentation updated
- ✅ Production-ready

---

## Final Checklist

Before marking Phase 5 complete:

- [ ] All 7 test failures fixed
- [ ] 7 missing edge cases implemented
- [ ] 18 new edge case tests written and passing
- [ ] Coverage targets met (≥90% unit, ≥80% integration)
- [ ] All modules < 10 cyclomatic complexity
- [ ] Error messages are user-friendly
- [ ] Documentation updated (README, troubleshooting, CLAUDE.md)
- [ ] Code reviewed by peer
- [ ] Commits are clean and descriptive
- [ ] CHANGELOG.md updated with Phase 5 improvements

---

**Created**: 2025-10-10
**Last Updated**: 2025-10-10
**Version**: 1.0
**Status**: READY FOR IMPLEMENTATION

**Print this card and keep it at your desk during Phase 5 implementation!**
