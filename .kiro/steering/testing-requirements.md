# Testing Requirements

## CRITICAL: Test Before Claiming Success

**NEVER claim a fix is complete without running tests that prove it works.**

### Mandatory Testing Protocol

**ALWAYS execute these steps when making ANY code changes:**

1. **Before making changes**: Run tests to confirm the problem exists
2. **After making changes**: Run tests to prove the fix works
3. **Only then**: Claim the fix is complete

### Required Test Commands

#### Basic Syntax and Functionality Test
```bash
python test_syntax_and_basic_functionality.py
```
**Must pass before claiming any Python code changes work.**

#### Specific Component Tests

**PDF Manager Issues:**
```bash
python -c "from src.utils.pdf_mgr import PDFManager; pm = PDFManager(); print('PDF Manager OK')"
```

**Section Count Validation:**
```bash
python -c "
import sys; sys.path.append('src')
from utils.section_generators import SectionManager
sm = SectionManager()
sections = sm.identify_sections({'name': 'Test'})
print(f'Sections: {len(sections)} (should be 7)')
"
```

**Icon Path Testing:**
```bash
python -c "
from pathlib import Path
icons_dir = Path('src/resources/icons')
print(f'Icons exist: {icons_dir.exists()}')
print(f'SVG count: {len(list(icons_dir.glob(\"*.svg\")))}')
"
```

### Testing Rules

1. **NO EXCEPTIONS**: Every code change must be tested
2. **SHOW RESULTS**: Always display test output as proof
3. **TEST FIRST**: Confirm the problem before fixing
4. **TEST AFTER**: Prove the fix works before claiming success
5. **FAIL FAST**: If tests fail, stop and fix before continuing

### Accountability Commands

Use these phrases to enforce testing:
- "Test this first"
- "Prove it works" 
- "Show me the test results"
- "Run the tests before claiming success"

### Integration with Version Management

Testing and version management work together:
1. Run tests to confirm problem
2. Make code changes
3. **Increment version** (`python src/utils/version.py`)
4. Run tests to prove fix works
5. Only then claim success

**If tests fail after version increment, increment again after fixing.**