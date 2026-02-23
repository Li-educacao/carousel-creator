---
paths: "**/*.py"
---

# Python Rules

## File Header

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module description."""
```

## Style

- snake_case for functions/variables, UPPERCASE for constants
- Function docstrings: narrative form (`"""Gera relatório formatado."""`)
- Type hints: use for complex data (CSVs, APIs, dicts); optional for simple scripts
- No classes for configuration — use simple dicts/lists in `config.py`

## Configuration Pattern

- Business constants: `config.py` (pricing tiers, keywords, mappings)
- Secrets: `.env` loaded via `python-dotenv` (`load_dotenv()`)
- Never hardcode API keys, tokens, or credentials

## CSV & Encoding (Bling-Specific)

- Bling CSVs use delimiter `;` and UTF-8 with double-encoding bug
- Always implement char-by-char double-encoding fix (detect `0xC0-0xDF` byte pairs)
- Comment: `# Bling double-encoding bug` near the fix
- Test with real data before batch processing

## Error Handling

- Catch specific exceptions first, then broad `Exception`
- Always `traceback.print_exc()` for debugging
- Return `False` on recoverable errors, `sys.exit(1)` for fatal
- Selenium: always `driver.quit()` in `finally` block

## Logging

- Simple `log(emoji, message)` pattern (no `logging` module)
- Step tracking: `log_step(step, total, message)` for multi-step processes
- Emoji indicators: checkmark for success, X for errors

## Async

- Entry point: `asyncio.run(main_async())`
- Windows compat: `asyncio.WindowsSelectorEventLoopPolicy()` if needed
- Use async only for Telegram/HTTP — batch DB operations are sync

## Selenium Patterns

- `WebDriverWait` with explicit `EC` conditions (never `time.sleep()` as primary wait)
- Vue.js forms: dispatch `input`, `change`, `blur` events after setting value
- File downloads: monitor `.crdownload` completion, filter by timestamp
- Always configure `ChromeOptions` with download directory preferences

## Script CLI Arguments

- Support `--dry-run` for preview mode
- Parse via `sys.argv` or `argparse` for complex scripts
- Print summary at end with totals (imported, skipped, errors)

## Imports

Standard library → third-party (one blank line between groups):
```python
import os
import sys

from dotenv import load_dotenv
from selenium import webdriver
```
