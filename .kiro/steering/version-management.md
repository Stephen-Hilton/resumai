# Version Management Instructions

## CRITICAL: Auto-Increment Version on Every Change

**ALWAYS execute this when making ANY code changes:**

### Get new version
From the project root, run the command below to return the new version number to stdout:
```bash
python src/version.py
```

This also updates pyproject.toml with the new version number.
