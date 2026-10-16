# Static Code Analysis — Issues and Fixes

## Project
- **Repository:** L5_16_pet_shelter
- **Python file:** `pet_shelter.py`
- **Tools:** Pylint, Bandit, Flake8
- **Note:** Line numbers refer to the original file, before any fixes.

## Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL injection (B608) | Security — Medium | 10 | The INSERT query was built with `%` string formatting, so a name like `O'Brien` breaks it and crafted input could inject SQL. | Replaced with a parameterized query: `VALUES (?, ?, ?, 0)` with the values passed as a tuple. |
| Mutable default argument (W0102) | Bug | 9 | `tags=[]` is created once and shared across calls, so tags from earlier pets leak into later ones. | Changed the default to `None` and create a new list inside the function. |
| Weak random generator (B311) | Security — Low | 22 | `random.randint()` is predictable, which is unsuitable for adoption codes. | Replaced with `secrets.randbelow(9000) + 1000`. |
| Silent exception handling (B110) | Security / Quality | 36 | `except Exception: pass` in `clearUnadopted` swallowed every error silently. | Catch only `sqlite3.Error` and log it with `logging.error`. |
| Bare except (E722, W0702) | Bug | 29 | The bare `except` in `oldestAvailable` hid all errors; it only existed to handle an empty result. | Removed the try/except and check whether the query returned a row: `row[0] if row else None`. |
| Global statement (W0603) | Design | 16 | A global `adoption_count` made state hidden and hard to manage. | Removed the global and compute the status by counting adopted pets in the database. |
| Naming convention (C0103) | Style | 6, 9, 21, 25, 33, 40 | camelCase function names and a lowercase module-level constant. | Renamed functions to snake_case and removed the counter variable. |
| Missing docstrings (C0114, C0116) | Style | 1, 9, 15, 21, 25, 33, 40, 45 | The module and all functions had no docstrings. | Added a module docstring and a one-line docstring to every function. |
| Long lines (E501, C0301) | Style | 5, 10, 27 | Lines exceeded Flake8's 79-character and Pylint's 100-character limits. | Wrapped the SQL strings and calls across multiple lines. |
| Multiple statements on one line (E701, C0321) | Style | 41 | `if ...: return` on a single line. | Split into a conditional expression: `return "active" if adopted > 0 else "quiet"`. |
| Missing final newline (W292, C0304, W293) | Style | End of file | The file did not end with a newline, and an extra indented blank line was added while fixing it. | Ended the file with exactly one newline and no trailing whitespace. |
| Unguarded entry point | Design | End of file | `main()` ran on import. | Wrapped the call in `if __name__ == "__main__":`. |

## Fix Verification

| Tool | Before | After |
|---|---|---|
| Pylint | 3.95/10 | < 9.71/10> |
| Bandit | 3 findings (1 Medium, 2 Low) | < No issues identified> |
| Flake8 | 5 violations | < 0 violations> |

## Commits
- Fix Bandit security issues: <hash>
- Fix Pylint issues: 61988ee
- Fix Flake8 formatting issues and guard entry point: <hash>
