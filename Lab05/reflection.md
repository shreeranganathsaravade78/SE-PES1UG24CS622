# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the style issues, such as docstrings, snake_case names, long lines and the one-line `if` statement, because the tools state exactly what to change. The hardest were the mutable default argument (`tags=[]`) and the bare `except` in `oldest_available`. For both, I had to understand why the code was wrong, not just follow the message. The bare `except` was hiding the case where the query returns no row, so the real fix was to check for an empty result instead of catching everything. The global counter was also tricky, because removing it meant rewriting `shelter_status()` to count adopted pets from the database.

## 2. Did the static analysis tools report any false positives?

I did not see clear false positives. The Bandit B311 warning about `random` is Low severity and would not matter for a demo program, but adoption codes should not be guessable, so I treated it as a real issue and used `secrets`. A few Pylint messages, like the naming of the module-level counter, were more about style than about bugs. The tools also overlap: one problem, such as the bare `except`, was reported by Flake8 and Pylint, and one fix cleared both.

## 3. How could you integrate static analysis tools into a real development workflow?

I would run Flake8, Pylint and Bandit automatically on every commit with a pre-commit hook, and again in a CI pipeline (for example GitHub Actions) so a pull request fails if the Bandit scan finds issues or the Pylint score drops below a set threshold. I would also enable them in the editor so problems show up while writing code, not at the end.

## 4. What improvements did you see in the code after the fixes?

The Pylint score went from 3.95/10 to 10.00/10, Bandit went from 3 findings to none, and Flake8 went from 5 violations to none. The code is also safer: the SQL query can no longer be injected, and adoption codes are unpredictable. It is more robust: errors are logged instead of hidden, the tag list no longer leaks between pets, and `oldest_available()` returns `None` explicitly when no pet is left. It is also easier to read because of the docstrings, consistent names and shorter lines, and the program prints the same output as before.