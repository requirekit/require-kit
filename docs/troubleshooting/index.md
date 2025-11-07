# Troubleshooting

Common issues and solutions for RequireKit.

## Installation Issues

### Commands Not Found

**Problem**: `/gather-requirements` command not recognized

**Solutions**:
1. Verify PATH includes `~/.agentecflow/bin`
2. Reload shell: `exec $SHELL`
3. Re-run installer with `--repair` flag

See [Installation Guide](../getting-started/installation.md#troubleshooting) for details.

### Marker File Missing

**Problem**: Integration with taskwright not detected

**Solution**:
```bash
# Check for marker files
ls ~/.agentecflow/*.marker

# Re-run installer if missing
cd /path/to/require-kit
./installer/scripts/install.sh --repair
```

## Runtime Issues

### Requirements Not Generating

**Problem**: `/formalize-ears` not creating requirement files

**Solutions**:
1. Check draft file exists in `docs/requirements/draft/`
2. Verify draft has sufficient content
3. Review agent output for errors

### BDD Generation Fails

**Problem**: `/generate-bdd` not creating scenarios

**Solutions**:
1. Ensure requirements exist (REQ-*.md files)
2. Check requirements are properly formatted
3. Verify EARS patterns are correct

## Integration Issues

### taskwright Not Detected

**Problem**: Integration features not available

**Solution**:
```bash
# Verify both marker files exist
ls ~/.agentecflow/*.marker

# Should show: require-kit.marker + taskwright.marker
```

See the [Integration Guide](../INTEGRATION-GUIDE.md#troubleshooting) for detailed troubleshooting.

## Common Questions

See the [FAQ](../faq.md) for frequently asked questions.

## Getting Help

1. Check the [FAQ](../faq.md)
2. Review [Integration Guide](../INTEGRATION-GUIDE.md)
3. Open an issue on [GitHub](https://github.com/yourusername/require-kit/issues)

## Troubleshooting Files

For specific issues, see:
- `docs/troubleshooting/zeplin-maui-icon-issues.md` - Zeplin MCP issues

---

**Still stuck?** Open an issue on [GitHub](https://github.com/yourusername/require-kit/issues) with:
- Description of the problem
- Steps to reproduce
- Error messages
- Your environment (OS, Claude version)
